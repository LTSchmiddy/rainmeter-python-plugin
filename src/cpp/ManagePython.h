#ifndef __MANAGE_PYTHON__
#define __MANAGE_PYTHON__

#include <filesystem>
#include <string>

#include "main.h"

#define PYTHON_HOME "PythonHome"
#define PYTHON_LOADER "python_loader.py"

struct PythonInfo {
    bool plugin_initialized = false;
    unsigned measures_loaded = 0;

    PyObject* controller = NULL;
    PyObject* global_rm;
};

extern PythonInfo pyInfo;
extern PyThreadState *mainThreadState;

void InitializePython();

void PyController_Init(void* rm);

void AddDirToPath(LPCWSTR dir);
PyObject* LoadObjectFromScript(LPCWSTR scriptPath, char* fileName, LPCWSTR className);
void LoadMeasureScript(LPCWSTR scriptPath, char* fileName, LPCWSTR className, Measure* measure);

#endif