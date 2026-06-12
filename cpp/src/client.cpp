#include <robolytics/client.hpp>

#include <curl/curl.h>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <stdexcept>
#include <sstream>

namespace robolytics {

struct curl_buffer {
    std::string data;
};

static size_t write_cb(void *contents, size_t size, size_t nmemb, void *userp) {
    auto *buf = static_cast<curl_buffer*>(userp);
    size_t realsize = size * nmemb;
    buf->data.append(static_cast<char*>(contents), realsize);
    return realsize;
}

struct Client::Impl {
    std::string base_url;
    std::string client_id;
    std::string client_secret;
    std::string access_token;
    CURL *curl = nullptr;

    Impl(std::string id, std::string secret, std::string url)
        : base_url(std::move(url)),
          client_id(std::move(id)),
          client_secret(std::move(secret)) {
        curl = curl_easy_init();
        if (!curl) throw std::runtime_error("Failed to initialize libcurl");
    }

    ~Impl() {
        if (curl) curl_easy_cleanup(curl);
    }
};

Client::Client(std::string client_id, std::string client_secret, std::string base_url)
    : pimpl(std::make_unique<Impl>(std::move(client_id), std::move(client_secret), std::move(base_url))) {}

Client::~Client() = default;

Client::Client(Client&&) noexcept = default;
Client& Client::operator=(Client&&) noexcept = default;

void Client::set_base_url(std::string url) {
    pimpl->base_url = std::move(url);
}

std::string Client::fetch_token() {
    if (!pimpl->access_token.empty()) return pimpl->access_token;
    if (pimpl->client_id.empty() || pimpl->client_secret.empty())
        throw std::runtime_error("No credentials provided");

    std::string url = pimpl->base_url + "/api/auth/oauth2/token";
    std::string postfields =
        "grant_type=client_credentials&client_id=" + pimpl->client_id +
        "&client_secret=" + pimpl->client_secret;

    curl_buffer buf;
    curl_easy_setopt(pimpl->curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(pimpl->curl, CURLOPT_POSTFIELDS, postfields.c_str());
    curl_easy_setopt(pimpl->curl, CURLOPT_WRITEFUNCTION, write_cb);
    curl_easy_setopt(pimpl->curl, CURLOPT_WRITEDATA, &buf);

    CURLcode res = curl_easy_perform(pimpl->curl);
    if (res != CURLE_OK)
        throw std::runtime_error("Token fetch failed: " + std::string(curl_easy_strerror(res)));

    // Parse {"access_token":"..."}
    auto pos = buf.data.find("\"access_token\"");
    if (pos == std::string::npos) throw std::runtime_error("No access_token in response");
    pos = buf.data.find('"', pos + 15);
    if (pos == std::string::npos) throw std::runtime_error("Malformed token response");
    auto end = buf.data.find('"', pos + 1);
    if (end == std::string::npos) throw std::runtime_error("Malformed token response");

    pimpl->access_token = buf.data.substr(pos + 1, end - pos - 1);
    return pimpl->access_token;
}

bool Client::do_ingest(std::string_view json_body) {
    try {
        auto token = fetch_token();
    } catch (...) {
        return false;
    }

    std::string url = pimpl->base_url + "/api/v1/ingest";
    std::string auth = "Authorization: Bearer " + pimpl->access_token;

    struct curl_slist *headers = nullptr;
    headers = curl_slist_append(headers, auth.c_str());
    headers = curl_slist_append(headers, "Content-Type: application/json");

    curl_buffer buf;
    curl_easy_setopt(pimpl->curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(pimpl->curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(pimpl->curl, CURLOPT_POSTFIELDS, json_body.data());
    curl_easy_setopt(pimpl->curl, CURLOPT_POSTFIELDSIZE, (long)json_body.size());
    curl_easy_setopt(pimpl->curl, CURLOPT_WRITEFUNCTION, write_cb);
    curl_easy_setopt(pimpl->curl, CURLOPT_WRITEDATA, &buf);

    CURLcode res = curl_easy_perform(pimpl->curl);
    curl_slist_free_all(headers);

    if (res != CURLE_OK) return false;

    long http_code = 0;
    curl_easy_getinfo(pimpl->curl, CURLINFO_RESPONSE_CODE, &http_code);
    return http_code >= 200 && http_code < 300;
}

// ---- Event builders ----

static std::string ts_ns() {
    return std::to_string(static_cast<long long>(std::time(nullptr)) * 1000000000LL);
}

static std::string event_id() {
    auto ns = static_cast<unsigned long long>(std::time(nullptr)) * 1000000000ULL;
    return "ev_" + std::to_string(ns);
}

static std::string json_escape(std::string_view s) {
    std::string out;
    out.reserve(s.size() + 4);
    for (char c : s) {
        if (c == '"') out += "\\\"";
        else if (c == '\\') out += "\\\\";
        else out += c;
    }
    return out;
}

static std::string build_json(std::string_view event_type, std::string_view extra) {
    std::ostringstream os;
    os << "{"
       << "\"eventId\":\"" << event_id() << "\","
       << "\"timestampNs\":" << ts_ns() << ","
       << "\"source\":\"cpp-sdk\","
       << "\"sourceVersion\":\"1.0.0\","
       << "\"" << event_type << "\":{"
       << extra
       << "}}";
    return os.str();
}

bool Client::scenario_started(
    std::string_view scenario_id,
    std::string_view domain,
    std::string_view software_version,
    std::string_view scenario_name,
    std::string_view seed)
{
    std::ostringstream extra;
    extra << "\"scenarioId\":\"" << json_escape(scenario_id) << "\"";
    if (!domain.empty()) extra << ",\"domain\":\"" << json_escape(domain) << "\"";
    if (!software_version.empty()) extra << ",\"softwareVersion\":\"" << json_escape(software_version) << "\"";
    if (!scenario_name.empty()) extra << ",\"scenarioName\":\"" << json_escape(scenario_name) << "\"";
    if (!seed.empty()) extra << ",\"seed\":\"" << json_escape(seed) << "\"";
    return do_ingest(build_json("scenarioStarted", extra.str()));
}

bool Client::mission_completed(
    std::string_view scenario_id,
    MissionStatus status,
    const Metrics& metrics,
    std::string_view mission_id,
    std::string_view software_version)
{
    std::ostringstream extra;
    extra << "\"scenarioId\":\"" << json_escape(scenario_id) << "\"";
    extra << ",\"status\":" << static_cast<int>(status);
    if (!mission_id.empty()) extra << ",\"missionId\":\"" << json_escape(mission_id) << "\"";
    if (!software_version.empty()) extra << ",\"softwareVersion\":\"" << json_escape(software_version) << "\"";

    extra << ",\"metrics\":{";
    for (size_t i = 0; i < metrics.size(); ++i) {
        if (i > 0) extra << ",";
        extra << "\"" << json_escape(metrics[i].first) << "\":" << metrics[i].second;
    }
    extra << "}";

    return do_ingest(build_json("missionCompleted", extra.str()));
}

bool Client::obstacle_encountered(
    std::string_view scenario_id,
    std::string_view obstacle_class,
    bool collision,
    double relative_speed,
    std::string_view mission_id,
    unsigned int step)
{
    std::ostringstream extra;
    extra << "\"scenarioId\":\"" << json_escape(scenario_id) << "\"";
    extra << ",\"obstacleClass\":\"" << json_escape(obstacle_class) << "\"";
    extra << ",\"collision\":" << (collision ? "true" : "false");
    extra << ",\"relativeSpeed\":" << relative_speed;
    if (!mission_id.empty()) extra << ",\"missionId\":\"" << json_escape(mission_id) << "\"";
    extra << ",\"step\":" << step;
    return do_ingest(build_json("obstacleEncountered", extra.str()));
}

bool Client::object_identified(
    std::string_view scenario_id,
    std::string_view class_name,
    double confidence,
    std::string_view mission_id)
{
    std::ostringstream extra;
    extra << "\"scenarioId\":\"" << json_escape(scenario_id) << "\"";
    extra << ",\"className\":\"" << json_escape(class_name) << "\"";
    extra << ",\"confidence\":" << confidence;
    if (!mission_id.empty()) extra << ",\"missionId\":\"" << json_escape(mission_id) << "\"";
    return do_ingest(build_json("objectIdentified", extra.str()));
}

} // namespace robolytics
