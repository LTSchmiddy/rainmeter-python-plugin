#ifndef __MANAGE_PYTHON__
#define __MANAGE_PYTHON__

#include <filesystem>
#include <string>

// #include "main.h"

#define PYTHON_HOME "PythonHome"

#ifndef SP_MODE

    #define PYTHON_LOADER "measure_host.py"
    #define PY_HOST_CLASS L"MeasureHost"

#else

    #define PYTHON_LOADER "sp_host.py"
    #define PY_HOST_CLASS L"SpHost"

#endif


struct PythonInfo {
    bool plugin_initialized = false;
    unsigned measures_loaded = 0;

    std::filesystem::path exec_path;
    std::filesystem::path console_exec_path;

    PyObject* loader = NULL;
    PyObject* global_rm;
};

extern PythonInfo pyInfo;
extern PyThreadState *mainThreadState;

void InitializePython(bool spMode);
void InitializePython();


void PyController_Init(void* rm);

void AddDirToPath(LPCWSTR dir);
PyObject* LoadObjectFromScript(LPCWSTR scriptPath, char* fileName, LPCWSTR className);
// void LoadMeasureScript(LPCWSTR scriptPath, char* fileName, LPCWSTR className, Measure* measure);

#endif