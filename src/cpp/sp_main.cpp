/*

	Original Copyright:
	Copyright (C) 2013 Johannes Blume

	This program is free software; you can redistribute it and/or
	modify it under the terms of the GNU General Public License
	as published by the Free Software Foundation; either version 2
	of the License, or (at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program; if not, write to the Free Software
	Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
*/
// #include "ManageSP.h"
#include <filesystem>

#include <Windows.h>
#include <RainmeterAPI.h>

#include "PyRainmeter.h"
#include "ManagePython.h"
#include "utils.h"

#include "sp_main.h"


using namespace std;
using namespace std::filesystem;


Measure::Measure() {
	measureIdObject = NULL;
	getStringResult = NULL;
	mainThreadState = NULL;
	lastRm = NULL;
}

PLUGIN_EXPORT void Initialize(void** data, void* rm)
{
	bool should_save = false;
	if (!pyInfo.plugin_initialized){
		InitializePython(true);
		should_save = true;
	}

	Measure *measure = new Measure;
	measure->mainThreadState = mainThreadState;
	*data = measure;

	if (should_save) {
		PyEval_SaveThread();
	}

	pyInfo.measures_loaded++;
}


PLUGIN_EXPORT void Reload(void* data, void* rm, double* maxValue)
{
	Measure *measure = (Measure*) data;
	PyObject *rainmeterObject = NULL;
	measure->lastRm = NULL;
	// PyEval_RestoreThread(mainThreadState);
	PyEval_RestoreThread(measure->mainThreadState);

	if (pyInfo.global_rm == NULL) {
		RmLog(LOG_DEBUG, L"INIT LOADER");
		PyController_Init(rm);
		rainmeterObject = pyInfo.global_rm;
	} else {
		rainmeterObject = CreateRainmeterObject(rm);
		pyInfo.global_rm = rainmeterObject;
	}

	if (measure->measureIdObject == NULL)	{
		if (rainmeterObject == NULL){
			rainmeterObject = CreateRainmeterObject(rm);
		}

		PyObject *resultObj = PyObject_CallMethod(pyInfo.loader, "loadMeasure", "O", rainmeterObject);
		// PyObject *resultObj = PyObject_CallMethod(pyInfo.loader, "loadMeasure", "OOO", classPathObj, scriptPathObj, className);

		if (resultObj != NULL)
		{
			measure->measureIdObject = resultObj;
		}
		else
		{
			PyErr_Print();
			PyErr_Clear();
		}
	}

	if (measure->measureIdObject != NULL)
	{
		if (rainmeterObject == NULL){
			rainmeterObject = CreateRainmeterObject(rm);
		}
		// PyObject *resultObj = PyObject_CallMethod(measure->measureObject, "Reload", "Od", rainmeterObject, maxValue);
		PyObject *resultObj = PyObject_CallMethod(pyInfo.loader, "callReload", "OOd", measure->measureIdObject, rainmeterObject, maxValue);
		if (resultObj != NULL)
		{
			Py_DECREF(resultObj);
		}
		else
		{
			PyErr_Clear();
		}

	}
	if (rainmeterObject != NULL){
		Py_DECREF(rainmeterObject);
	}

	PyEval_SaveThread();
}

PLUGIN_EXPORT double Update(void* data)
{
	Measure *measure = (Measure*) data;
	if (measure->measureIdObject == NULL)
	{
		return -1.0;
	}

	// PyEval_RestoreThread(mainThreadState);
	PyEval_RestoreThread(measure->mainThreadState);
	// PyObject *resultObj = PyObject_CallMethod(measure->measureObject, "Update", NULL);
	PyObject *resultObj = PyObject_CallMethod(pyInfo.loader, "callUpdate", "O", measure->measureIdObject);
	double result = 0.0;
	if (resultObj != NULL) 
	{
		result = PyFloat_Check(resultObj) ? PyFloat_AsDouble(resultObj) : 0.0;
		Py_DECREF(resultObj);
	}
	else
	{
		PyErr_Clear();
	}
	PyEval_SaveThread();
	return result;
}

PLUGIN_EXPORT LPCWSTR GetString(void* data)
{
	Measure *measure = (Measure*) data;
	if (measure->measureIdObject == NULL)
	{
		return measure->getStringResult;
	}

	// PyEval_RestoreThread(mainThreadState);
	PyEval_RestoreThread(measure->mainThreadState);
	// PyObject *resultObj = PyObject_CallMethod(measure->measureObject, "GetString", NULL);
	PyObject *resultObj = PyObject_CallMethod(pyInfo.loader, "callGetString", "O", measure->measureIdObject);
	if (measure->getStringResult != NULL)
	{
		PyMem_Free(measure->getStringResult);
		measure->getStringResult = NULL;
	}
	if (resultObj != NULL)
	{
		if (resultObj != Py_None)
		{
			PyObject *strObj = PyObject_Str(resultObj);
			measure->getStringResult = PyUnicode_AsWideCharString(strObj, NULL);
			Py_DECREF(strObj);
		}
		Py_DECREF(resultObj);
	}
	else
	{
		PyErr_Clear();
	}
	PyEval_SaveThread();
	return measure->getStringResult;
}


PLUGIN_EXPORT void ExecuteBang(void* data, LPCWSTR args)
{
	Measure *measure = (Measure*) data;
	if (measure->measureIdObject == NULL)
	{
		return;
	}

	PyEval_RestoreThread(measure->mainThreadState);
	PyObject *argsObj = PyUnicode_FromWideChar(args, -1);
	PyObject *resultObj = PyObject_CallMethod(pyInfo.loader, "callExecuteBang", "OO", measure->measureIdObject, argsObj);
	if (resultObj != NULL)
	{
		Py_DECREF(resultObj);
	}
	else
	{
		PyErr_Clear();
	}
	Py_DECREF(argsObj);
	PyEval_SaveThread();
}

PLUGIN_EXPORT void Finalize(void* data)
{
	Measure *measure = (Measure*) data;
	PyEval_RestoreThread(measure->mainThreadState);
	if (measure->measureIdObject != NULL)
	{
		PyObject *resultObj = PyObject_CallMethod(pyInfo.loader, "callFinalize", "O", measure->measureIdObject);
		if (resultObj != NULL)
		{
			Py_DECREF(resultObj);
		}
		else
		{
			PyErr_Clear();
		}

		if (measure->getStringResult != NULL)
		{
			PyMem_Free(measure->getStringResult);
		}
		Py_DECREF(measure->measureIdObject);
	}
	delete measure;
	pyInfo.measures_loaded--;
	if (pyInfo.measures_loaded == 0) {
		Py_DECREF(pyInfo.global_rm);
		pyInfo.global_rm = NULL;

		// Terminating the Python subprocess:
		PyObject *resultObj = PyObject_CallMethod(pyInfo.loader, "terminate", NULL);
		if (resultObj != NULL)
		{
			Py_DECREF(resultObj);
		}
		
		else {
			PyErr_Print();
			PyErr_Clear();
		}
	}

	PyEval_SaveThread();
	//Py_Finalize(); // Testing this without killing the interpreter to reset its status
}

// Rainmeter plugins can call custom functions to get special values from a measure.
// We can use allow call custom methods on Python measures.

PLUGIN_EXPORT LPCWSTR Func(void* data, const int argc, const WCHAR* argv[]) {
	// return nullptr;
	Measure* measure = (Measure*) data;
	if (argc < 0) { 
		RmLog(measure->lastRm, LOG_ERROR, L"No Python method specified.");
		return L"ERR"; 
	}

	if (measure->measureIdObject == NULL) { return nullptr; }

	PyEval_RestoreThread(measure->mainThreadState);

	PyObject* funcNameObj = PyUnicode_FromWideChar(argv[0], -1);
	PyObject* argsObj = PyTuple_New(argc - 1);

	for (int i = 1; i < argc; i++) {
		PyObject* arg = PyUnicode_FromWideChar(argv[i], -1);
		PyTuple_SetItem(argsObj, i - 1, arg);
	}

	PyObject* resultObj = PyObject_CallMethod(pyInfo.loader, "callFunc", "OOO", measure->measureIdObject, funcNameObj, argsObj);

	Py_DECREF(funcNameObj);
	Py_DECREF(argsObj);

	if (resultObj == NULL)
	{
		PyErr_Print();
		PyErr_Clear();
		PyEval_SaveThread();
		return nullptr;

	} else if (resultObj == Py_None) {
		Py_DECREF(resultObj);
		PyEval_SaveThread();
		return nullptr;
	}

	static wchar_t* retVal;
	if (retVal != NULL) {
		PyMem_Free(retVal);
	}

	retVal = PyUnicode_AsWideCharString(resultObj, NULL);
	Py_DECREF(resultObj);
	
	PyEval_SaveThread();
	// return L"WORKING";
	return retVal;

}