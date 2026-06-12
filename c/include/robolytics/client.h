/*
 * robolytics — C client SDK for the Chaveta RobotOps Analytics platform.
 *
 * Generated from buf.build/beaglabs/robolytics.
 *
 * Usage:
 *   #include "robolytics/client.h"
 *
 *   RobolyticsClient *client = robolytics_client_create(
 *       "https://chaveta.beaglabs.com",
 *       getenv("CHAVETA_CLIENT_ID"),
 *       getenv("CHAVETA_CLIENT_SECRET")
 *   );
 *
 *   robolytics_scenario_started(client, "warehouse-nav-v2", "warehouse", "3.2.1");
 *   robolytics_mission_completed(client, "warehouse-nav-v2",
 *       MISSION_STATUS_SUCCESS, 3,
 *       (const char*[]){"collision_rate", "route_completion_pct", "shelves_inspected"},
 *       (double[]){0.0, 100.0, 412.0});
 *   robolytics_client_destroy(client);
 */

#ifndef ROBOLYTICS_CLIENT_H
#define ROBOLYTICS_CLIENT_H

#include <stddef.h>
#include <stdbool.h>

#define MISSION_STATUS_UNSPECIFIED  0
#define MISSION_STATUS_SUCCESS      1
#define MISSION_STATUS_FAILURE      2
#define MISSION_STATUS_TIMEOUT      3
#define MISSION_STATUS_INTERVENTION 4

typedef struct RobolyticsClient RobolyticsClient;

/* Create a new client. base_url can be NULL to use default. */
RobolyticsClient *robolytics_client_create(
    const char *base_url,
    const char *client_id,
    const char *client_secret);

/* Destroy the client. */
void robolytics_client_destroy(RobolyticsClient *client);

/* Send a ScenarioStarted event. */
int robolytics_scenario_started(
    RobolyticsClient *client,
    const char *scenario_id,
    const char *domain,
    const char *software_version);

/* Send a MissionCompleted event with n_metrics key/value pairs. */
int robolytics_mission_completed(
    RobolyticsClient *client,
    const char *scenario_id,
    int status,
    size_t n_metrics,
    const char **metric_keys,
    const double *metric_values);

/* Send an ObstacleEncountered event. */
int robolytics_obstacle_encountered(
    RobolyticsClient *client,
    const char *scenario_id,
    const char *obstacle_class,
    bool collision,
    double relative_speed);

/* Send an ObjectIdentified event. */
int robolytics_object_identified(
    RobolyticsClient *client,
    const char *scenario_id,
    const char *class_name,
    double confidence);

#endif /* ROBOLYTICS_CLIENT_H */
