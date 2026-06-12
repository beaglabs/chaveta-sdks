#pragma once

#include <string>
#include <vector>
#include <string_view>
#include <utility>
#include <memory>
#include <optional>

namespace robolytics {

enum class MissionStatus {
    UNSPECIFIED = 0,
    SUCCESS = 1,
    FAILURE = 2,
    TIMEOUT = 3,
    INTERVENTION = 4,
};

using Metrics = std::vector<std::pair<std::string, double>>;

class Client {
public:
    Client(std::string client_id, std::string client_secret,
           std::string base_url = "https://chaveta.beaglabs.com");

    ~Client();

    // Non-copyable, movable
    Client(const Client&) = delete;
    Client& operator=(const Client&) = delete;
    Client(Client&&) noexcept;
    Client& operator=(Client&&) noexcept;

    // Configuration
    void set_base_url(std::string url);

    // Event methods — return true on success
    bool scenario_started(
        std::string_view scenario_id,
        std::string_view domain = "",
        std::string_view software_version = "",
        std::string_view scenario_name = "",
        std::string_view seed = "");

    bool mission_completed(
        std::string_view scenario_id,
        MissionStatus status = MissionStatus::SUCCESS,
        const Metrics& metrics = {},
        std::string_view mission_id = "",
        std::string_view software_version = "");

    bool obstacle_encountered(
        std::string_view scenario_id,
        std::string_view obstacle_class,
        bool collision = false,
        double relative_speed = 0.0,
        std::string_view mission_id = "",
        unsigned int step = 0);

    bool object_identified(
        std::string_view scenario_id,
        std::string_view class_name,
        double confidence = 0.0,
        std::string_view mission_id = "");

private:
    class Impl;
    std::unique_ptr<Impl> pimpl;

    std::string fetch_token();
    bool do_ingest(std::string_view json_body);
};

} // namespace robolytics
