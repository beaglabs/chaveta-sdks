cmake_minimum_required(VERSION 3.16)
project(robolytics VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(CURL REQUIRED)

add_library(robolytics
    src/client.cpp
)

target_include_directories(robolytics
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
)

target_link_libraries(robolytics PUBLIC CURL::libcurl)

install(TARGETS robolytics
    EXPORT robolyticsTargets
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)

install(DIRECTORY include/robolytics DESTINATION include)
install(EXPORT robolyticsTargets DESTINATION lib/cmake/robolytics)
