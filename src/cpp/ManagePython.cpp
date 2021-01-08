#include <Windows.h>
#include <Python.h>
#include <RainmeterAPI.h>

#include "PyRainmeter.h"
#include "utils.h"
#include "main.h"

#include "ManagePython.h"

using namespace std;
using namespace std::filesystem;


PythonInfo pyInfo;
PyThreadState *mainThreadState = NULL;

void InitializePython() {
	path interpHome = get_python_interpreter_home();
    wstring debugDefaultHome = to_wstring(interpHome.u8string());
	string defaultHome = interpHome.u8string();
	RmLog(LOG_DEBUG, debugDefaultHome.c_str());

	const char* homePathShort = defaultHome.c_str();
	size_t len = defaultHome.length() - 1;

	wstring homePath = Py_DecodeLocale(homePathShort, &len);
	// Uses the default Python Installation:
	Py_SetPythonHome(homePath.c_str());

	// path searchPathLib = get_python_interpreter_home();
	// searchPathLib.append("python.zip");
	// path searchPathDLLs = get_python_interpreter_home();
	// searchPathDLLs.append("DLLs");

	// path rm_dir_path = get_rm_dir_path();

	// wstring pySearchPath = 
	// 	wstring(Py_GetPath()) + L";" +
	// 	to_wstring(interpHome.u8string()) + L";" + 
	// 	to_wstring(searchPathLib.u8string()) + L";" + 
	// 	to_wstring(searchPathDLLs.u8string())+ L";" + 
	// 	to_wstring(rm_dir_path.u8string());

	// Py_SetPath(pySearchPath.c_str());
	// RmLog(LOG_DEBUG, Py_GetPath());
	Py_Initialize();
	mainThreadState = PyThreadState_Get();

	wstring loader_path = to_wstring(get_python_loader_home().u8string());
	RmLog(LOG_DEBUG, loader_path.c_str());
	pyInfo.loader = LoadObjectFromScript(loader_path.c_str(), PYTHON_LOADER, PY_HOST_CLASS);

    pyInfo.plugin_initialized = true;
}

void PyController_Init(void* rm){

	pyInfo.global_rm = CreateRainmeterObject(rm);
	pyInfo.exec_path = get_python_interpreter_exec();

	PyObject *resultObj = PyObject_CallMethod(pyInfo.loader, "setup", "Os", pyInfo.global_rm, pyInfo.exec_path.u8string().c_str());
	if (resultObj != NULL)
	{
		Py_DECREF(resultObj);
	}
	else
	{
		PyErr_Print();
		PyErr_Clear();
	}
}

void AddDirToPath(LPCWSTR dir)
{
	PyObject *pathObj = PySys_GetObject("path");
	PyObject *scriptDirObj = PyUnicode_FromWideChar(dir, -1);
	if (!PySequence_Contains(pathObj, scriptDirObj))
	{
		PyList_Append(pathObj, scriptDirObj);
	}
	Py_DECREF(scriptDirObj);
}


PyObject* LoadObjectFromScript(LPCWSTR scriptPath, char* fileName, LPCWSTR className)
{
	try 
	{
		FILE* f = _Py_wfopen(scriptPath, L"r");
		if (f == NULL)
		{
			throw L"Error opening Python script";
		}

		PyObject *globals = PyModule_GetDict(PyImport_AddModule("__main__"));
		PyObject *result = PyRun_FileEx(f, fileName, Py_file_input, globals, globals, 1);
		if (result == NULL)
		{
			PyErr_Print();
			throw L"Error loading Python script";
		}

		Py_DECREF(result);
		PyObject *classNameObj = PyUnicode_FromWideChar(className, -1);
		PyObject *classObj = PyDict_GetItem(globals, classNameObj);
		Py_DECREF(classNameObj);
		if (classObj == NULL)
		{
			throw L"Python class not found";
		}

		PyObject* retVal = PyObject_CallObject(classObj, NULL);
		if (retVal == NULL)
		{
			throw L"Error instantiating Python class";
		}
		return retVal;
	}
	catch (wchar_t *error) {
		RmLog(LOG_ERROR, (LPCWSTR)error);
		return NULL;
	}
}




/* Old. Will be implementing a new measure-loading system in the interpreter itself:
void LoadMeasureScript(LPCWSTR scriptPath, char* fileName, LPCWSTR className, Measure* measure)
{
	try 
	{
		FILE* f = _Py_wfopen(scriptPath, L"r");
		if (f == NULL)
		{
			throw L"Error opening Python script";
		}

		PyObject *globals = PyModule_GetDict(PyImport_AddModule("__main__"));
		PyObject *result = PyRun_FileEx(f, fileName, Py_file_input, globals, globals, 1);
		if (result == NULL)
		{
			throw L"Error loading Python script";
		}

		Py_DECREF(result);
		PyObject *classNameObj = PyUnicode_FromWideChar(className, -1);
		PyObject *classObj = PyDict_GetItem(globals, classNameObj);
		Py_DECREF(classNameObj);
		if (classObj == NULL)
		{
			throw L"Python class not found";
		}

		PyObject *measureObj = PyObject_CallObject(classObj, NULL);
		if (measureObj == NULL)
		{
			throw L"Error instantiating Python class";
		}

		measure->measureObject = measureObj;
		measure->getStringResult = NULL;
	}
	catch (wchar_t *error)
	{
		measure->measureObject = NULL;
		measure->getStringResult = error;
	}
}
*/