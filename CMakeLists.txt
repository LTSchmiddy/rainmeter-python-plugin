cmake_minimum_required(VERSION 3.0.0)
project(RmPythonExtensions VERSION 0.1.0)

cmake_policy(SET CMP0076 NEW)
set (CMAKE_CXX_STANDARD 17)
set (_SILENCE_CXX17_CODECVT_HEADER_DEPRECATION_WARNING 1)

set(TARGET_NAME PyPluginE)
set(TARGET_NAME_SP PyPlugin)

set(Boost_USE_STATIC_LIBS ON) 
set(Boost_USE_MULTITHREADED ON)  
set(Boost_USE_STATIC_RUNTIME OFF) 

set(Python_USE_STATIC_LIBS ON)

include_directories(${RAINMETER_API_ROOT})
include_directories(${LOCAL_TRIPLET_INCLUDE_DIR}/python3.9)

# If you're using Boost:
find_package(Boost 1.45.0 REQUIRED) 
find_package(Python COMPONENTS Interpreter Development REQUIRED)
find_package(ZLIB REQUIRED)
# if(Boost_FOUND)

add_library(${TARGET_NAME} SHARED)
add_library(${TARGET_NAME_SP} SHARED)

# Prevents spam from debug linking for Python
set_target_properties(${TARGET_NAME} PROPERTIES LINK_FLAGS "/ignore:4099")
set_target_properties(${TARGET_NAME_SP} PROPERTIES LINK_FLAGS "/ignore:4099")

message(STATUS ${Python_LIBRARIES})

target_link_libraries(${TARGET_NAME} ${Boost_LIBRARIES})
target_link_libraries(${TARGET_NAME} ${Python_LIBRARIES})
target_link_libraries(${TARGET_NAME} ZLIB::ZLIB)
target_link_libraries(${TARGET_NAME} ${RAINMETER_API_LIB})

target_link_libraries(${TARGET_NAME_SP} ${Boost_LIBRARIES})
target_link_libraries(${TARGET_NAME_SP} ${Python_LIBRARIES})
target_link_libraries(${TARGET_NAME_SP} ZLIB::ZLIB)
target_link_libraries(${TARGET_NAME_SP} ${RAINMETER_API_LIB})


add_subdirectory("./src/cpp")

set_target_properties(${TARGET_NAME}
    PROPERTIES
    ARCHIVE_OUTPUT_DIRECTORY "./arc/"
    LIBRARY_OUTPUT_DIRECTORY "./lib/"
    RUNTIME_OUTPUT_DIRECTORY "./bin/"
)

set_target_properties(${TARGET_NAME_SP}
    PROPERTIES
    ARCHIVE_OUTPUT_DIRECTORY "./arc/"
    LIBRARY_OUTPUT_DIRECTORY "./lib/"
    RUNTIME_OUTPUT_DIRECTORY "./bin/"
)
target_compile_definitions(${TARGET_NAME_SP} PUBLIC SP_MODE=1)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
