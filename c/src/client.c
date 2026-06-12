#include "robolytics/client.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdarg.h>
#include <time.h>
#include <curl/curl.h>

#define DEFAULT_BASE_URL "https://chaveta.beaglabs.com"
#define INGEST_PATH "/api/v1/ingest"
#define TOKEN_PATH "/api/auth/oauth2/token"

struct RobolyticsClient {
    char *base_url;
    char *client_id;
    char *client_secret;
    char *access_token;
};

struct curl_buffer {
    char *data;
    size_t size;
};

static size_t write_cb(void *contents, size_t size, size_t nmemb, void *userp) {
    size_t realsize = size * nmemb;
    struct curl_buffer *buf = (struct curl_buffer *)userp;
    char *ptr = realloc(buf->data, buf->size + realsize + 1);
    if (!ptr) return 0;
    buf->data = ptr;
    memcpy(&(buf->data[buf->size]), contents, realsize);
    buf->size += realsize;
    buf->data[buf->size] = 0;
    return realsize;
}

RobolyticsClient *robolytics_client_create(
    const char *base_url,
    const char *client_id,
    const char *client_secret)
{
    RobolyticsClient *c = calloc(1, sizeof(RobolyticsClient));
    c->base_url = strdup(base_url ? base_url : DEFAULT_BASE_URL);
    c->client_id = strdup(client_id ? client_id : "");
    c->client_secret = strdup(client_secret ? client_secret : "");
    return c;
}

void robolytics_client_destroy(RobolyticsClient *client) {
    if (!client) return;
    free(client->base_url);
    free(client->client_id);
    free(client->client_secret);
    free(client->access_token);
    free(client);
}

static int fetch_token(RobolyticsClient *client) {
    if (client->access_token) return 0;
    if (!client->client_id[0] || !client->client_secret[0]) return -1;

    CURL *curl = curl_easy_init();
    if (!curl) return -1;

    char url[1024];
    snprintf(url, sizeof(url), "%s%s", client->base_url, TOKEN_PATH);

    char body[512];
    snprintf(body, sizeof(body),
        "grant_type=client_credentials&client_id=%s&client_secret=%s",
        client->client_id, client->client_secret);

    struct curl_buffer buf = {0};
    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, body);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_cb);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &buf);

    CURLcode res = curl_easy_perform(curl);
    curl_easy_cleanup(curl);

    if (res != CURLE_OK || !buf.data) return -1;

    /* Parse JSON: {"access_token":"..."} */
    char *start = strstr(buf.data, "\"access_token\"");
    if (!start) { free(buf.data); return -1; }
    start = strchr(start + 14, '"');
    if (!start) { free(buf.data); return -1; }
    char *end = strchr(start + 1, '"');
    if (!end) { free(buf.data); return -1; }
    *end = '\0';
    client->access_token = strdup(start + 1);
    free(buf.data);
    return 0;
}

static int do_ingest(RobolyticsClient *client, const char *json_body) {
    if (fetch_token(client) != 0) return -1;

    CURL *curl = curl_easy_init();
    if (!curl) return -1;

    char url[1024];
    snprintf(url, sizeof(url), "%s%s", client->base_url, INGEST_PATH);

    char auth[1024];
    snprintf(auth, sizeof(auth), "Authorization: Bearer %s", client->access_token);

    struct curl_slist *headers = NULL;
    headers = curl_slist_append(headers, auth);
    headers = curl_slist_append(headers, "Content-Type: application/json");

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, json_body);

    CURLcode res = curl_easy_perform(curl);
    long http_code = 0;
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &http_code);
    curl_easy_cleanup(curl);
    curl_slist_free_all(headers);

    return (res == CURLE_OK && http_code >= 200 && http_code < 300) ? 0 : -1;
}

static void json_printf(char *buf, size_t *pos, size_t size, const char *fmt, ...) {
    va_list ap;
    va_start(ap, fmt);
    int n = vsnprintf(buf + *pos, size - *pos, fmt, ap);
    va_end(ap);
    if (n > 0) *pos += (size_t)n;
}

static char *build_event_json(
    const char *event_type,
    const char *scenario_id,
    const char *extra_json)
{
    char buf[8192];
    size_t pos = 0;
    long long ts = (long long)time(NULL) * 1000000000LL;

    json_printf(buf, &pos, sizeof(buf),
        "{"
        "\"eventId\":\"ev_%lld\","
        "\"timestampNs\":%lld,"
        "\"source\":\"c-sdk\","
        "\"sourceVersion\":\"1.0.0\","
        "\"%s\":{"
        "\"scenarioId\":\"%s\"",
        ts, ts, event_type, scenario_id);

    if (extra_json && extra_json[0]) {
        json_printf(buf, &pos, sizeof(buf), ",%s", extra_json);
    }

    json_printf(buf, &pos, sizeof(buf), "}}");
    return strdup(buf);
}

int robolytics_scenario_started(
    RobolyticsClient *client,
    const char *scenario_id,
    const char *domain,
    const char *software_version)
{
    char extra[512];
    snprintf(extra, sizeof(extra),
        "\"domain\":\"%s\",\"softwareVersion\":\"%s\"",
        domain ? domain : "", software_version ? software_version : "");
    char *json = build_event_json("scenarioStarted", scenario_id, extra);
    int ret = do_ingest(client, json);
    free(json);
    return ret;
}

int robolytics_mission_completed(
    RobolyticsClient *client,
    const char *scenario_id,
    int status,
    size_t n_metrics,
    const char **metric_keys,
    const double *metric_values)
{
    char extra[4096] = {0};
    size_t pos = 0;
    json_printf(extra, &pos, sizeof(extra), "\"status\":%d,\"metrics\":{", status);
    for (size_t i = 0; i < n_metrics; i++) {
        if (i > 0) json_printf(extra, &pos, sizeof(extra), ",");
        json_printf(extra, &pos, sizeof(extra), "\"%s\":%g", metric_keys[i], metric_values[i]);
    }
    json_printf(extra, &pos, sizeof(extra), "}");
    char *json = build_event_json("missionCompleted", scenario_id, extra);
    int ret = do_ingest(client, json);
    free(json);
    return ret;
}

int robolytics_obstacle_encountered(
    RobolyticsClient *client,
    const char *scenario_id,
    const char *obstacle_class,
    bool collision,
    double relative_speed)
{
    char extra[512];
    snprintf(extra, sizeof(extra),
        "\"obstacleClass\":\"%s\",\"collision\":%s,\"relativeSpeed\":%g",
        obstacle_class ? obstacle_class : "",
        collision ? "true" : "false",
        relative_speed);
    char *json = build_event_json("obstacleEncountered", scenario_id, extra);
    int ret = do_ingest(client, json);
    free(json);
    return ret;
}

int robolytics_object_identified(
    RobolyticsClient *client,
    const char *scenario_id,
    const char *class_name,
    double confidence)
{
    char extra[512];
    snprintf(extra, sizeof(extra),
        "\"className\":\"%s\",\"confidence\":%g",
        class_name ? class_name : "", confidence);
    char *json = build_event_json("objectIdentified", scenario_id, extra);
    int ret = do_ingest(client, json);
    free(json);
    return ret;
}
