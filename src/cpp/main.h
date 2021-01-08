#ifndef __MAIN__
#define __MAIN__

#include <Python.h>


struct Measure
{
	Measure();

    // bool uses_gstate = false;
	// PyGILState_STATE gstate;
    PyThreadState *mainThreadState;
    PyObject* measureObject;
	wchar_t* getStringResult;
    void* lastRm;
};

#endif