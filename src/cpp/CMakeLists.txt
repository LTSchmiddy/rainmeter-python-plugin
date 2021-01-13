target_sources(${TARGET_NAME}
    PUBLIC
    "./main.h"
    "./main.cpp"
    "./PyRainmeter.h"
    "./PyRainmeter.cpp"
    "./ManagePython.h"
    "./ManagePython.cpp"
    "./utils.h"
    "./utils.cpp"
)

target_sources(${TARGET_NAME_SP}
    PUBLIC
    "./sp_main.h"
    "./sp_main.cpp"
    "./utils.h"
    "./utils.cpp"
    "./PyRainmeter.h"
    "./PyRainmeter.cpp"
    "./ManagePython.h"
    "./ManagePython.cpp"
)

add_subdirectory("./RmPype")