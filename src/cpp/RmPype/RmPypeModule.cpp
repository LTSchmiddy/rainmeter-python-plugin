#include "RmPypeModule.h"

#include "RmPypeObject.h"
#include <Windows.h>
#include "structmember.h"

static PyObject *RmPypeModule_SpawnPipe(PyObject* self) {
    return CreateRmPypeObject();
}

static PyMethodDef RmPypeModule_methods[] = {
    {"spawn_pipe", (PyCFunction)RmPypeModule_SpawnPipe, METH_NOARGS, ""},
    {NULL}   /* sentinel */
};

// static PyMemberDef RmPypeModule_members[] = {
// 	// {"LOG_ERROR", T_INT, offsetof(RainmeterObject, logError), READONLY, ""},
// 	{"RmPype", T_STRING, offsetof(RmPypeObject, name), READONLY, ""},
// 	{NULL}
// };

struct PyModuleDef RmPypeModule = {
    PyModuleDef_HEAD_INIT,
    "rm_pype",
    NULL,
    -1,
    RmPypeModule_methods
};