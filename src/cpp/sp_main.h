#ifndef __SP_MAIN__
#define __SP_MAIN__

#include <Python.h>

struct Measure
{
	Measure();

    // bool uses_gstate = false;
	// PyGILState_STATE gstate;
    PyThreadState *mainThreadState;
    PyObject* measureIdObject;
	wchar_t* getStringResult;
    void* lastRm;
};

#endif