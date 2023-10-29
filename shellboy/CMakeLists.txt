cmake_minimum_required (VERSION 3.0)
project(shellboy C)

set(CMAKE_C_COMPILER ${CMAKE_CURRENT_LIST_DIR}/lib/gbdk/bin/lcc)
set(CMAKE_SHARED_LIBRARY_LINK_C_FLAGS "") # Fix for -rdynamic not handled by lcc

FILE(GLOB_RECURSE Sources ./src/*.c)

add_executable(${CMAKE_PROJECT_NAME} ${Sources})
set_target_properties(
    ${CMAKE_PROJECT_NAME}
    PROPERTIES
        OUTPUT_NAME ${CMAKE_PROJECT_NAME}
        SUFFIX ".gb"
)