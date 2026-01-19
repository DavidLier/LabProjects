#pragma once

#include <string>
#include <chrono>

struct ScheduledSignal {
public:
    std::string signal;
    std::chrono::steady_clock::time_point scheduledTime;

    ScheduledSignal(const std::string& signal, std::chrono::steady_clock::time_point time): signal(signal), scheduledTime(time) {}

    bool operator<(const ScheduledSignal& other) const {
        return scheduledTime > other.scheduledTime;
    }
};
