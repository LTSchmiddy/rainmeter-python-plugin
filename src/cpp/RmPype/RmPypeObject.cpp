#include <string>
#include "RmPypeObject.h"

#include "structmember.h"



using namespace std;



static PyObject* RmPype_CreatePipe(RmPypeObject* self, PyObject* args) {
	PyArg_ParseTuple(args, "s", &self->name);

	self->handle = CreateNamedPipeA(
		self->name,
		PIPE_ACCESS_DUPLEX,
		PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT, 
		PIPE_UNLIMITED_INSTANCES, 
		RM_PYPE_BUFFER_SIZE, 
		RM_PYPE_BUFFER_SIZE, 
		RM_PYPE_TIMEOUT,
		NULL
	);

	// Gotta return something for Python:
	Py_RETURN_NONE;
}

static PyObject* RmPype_ConnectPipe(RmPypeObject* self, PyObject* args) {
	PyArg_ParseTuple(args, "s", &self->name);

	self->handle = CreateFile(
		self->name,
        GENERIC_READ | GENERIC_WRITE,
        FILE_SHARE_READ | FILE_SHARE_WRITE,
        NULL,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL,
        NULL
	);

	SetNamedPipeHandleState(
		self->handle,
		&self->mode,
		NULL,
		&self->timeout
	);

	Py_RETURN_NONE;
}

static PyObject* RmPype_ClosePipe(RmPypeObject* self, PyObject* args) {
	CloseHandle(self->handle);
	PyMem_Free(self->name);

	// Py_INCREF(Py_None); return Py_None;
	Py_RETURN_NONE;
}

static PyObject* RmPype_ReadMessage(RmPypeObject* self, PyObject* args) {
	char buf[RM_PYPE_BUFFER_SIZE];

	DWORD byteCount = 0;

	bool success = ReadFile(
		self->handle,
		&buf,
		RM_PYPE_BUFFER_SIZE,
		&byteCount,
		NULL
	);

	if (success) {
		return PyUnicode_FromString(buf);
	}
	else {
		Py_RETURN_NONE;
	}
}

static PyObject* RmPype_WriteMessage(RmPypeObject* self, PyObject* args) {
	// char buf[RM_PYPE_BUFFER_SIZE];
	char* buf;
	PyArg_ParseTuple(args, "s", &buf);

	DWORD byteCount = 0;
	bool success = WriteFile(
		self->handle,
		&buf,
		(DWORD)strlen(buf),
		&byteCount,
		NULL
	);

	PyMem_Free(buf);

	if (success) {
		Py_RETURN_TRUE;
	}
	else {
		Py_RETURN_FALSE;
	}
}


static PyMethodDef RmPype_methods[] = {
	// {"RmGetMeasureName", (PyCFunction)Rainmeter_RmGetMeasureName, METH_NOARGS, ""},
	// {"RmGetSkinName", (PyCFunction)Rainmeter_RmGetSkinName, METH_NOARGS, ""},
	{NULL}
};

static PyMemberDef RmPype_members[] = {
	// {"LOG_ERROR", T_INT, offsetof(RainmeterObject, logError), READONLY, ""},
	{"name", T_STRING, offsetof(RmPypeObject, name), READONLY, ""},
	{NULL}
};

static PyTypeObject rmPypeType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"Rainmeter",               /* tp_name */
	sizeof(RmPypeObject),   /* tp_basicsize */
	0,                         /* tp_itemsize */
	0,                         /* tp_dealloc */
	0,                         /* tp_print */
	0,                         /* tp_getattr */
	0,                         /* tp_setattr */
	0,                         /* tp_reserved */
	0,                         /* tp_repr */
	0,                         /* tp_as_number */
	0,                         /* tp_as_sequence */
	0,                         /* tp_as_mapping */
	0,                         /* tp_hash  */
	0,                         /* tp_call */
	0,                         /* tp_str */
	0,                         /* tp_getattro */
	0,                         /* tp_setattro */
	0,                         /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,        /* tp_flags */
	"Wrapper for Win32 API named pipes, used for communicating with sub-interpreters.",       /* tp_doc */
	0,                         /* tp_traverse */
	0,                         /* tp_clear */
	0,                         /* tp_richcompare */
	0,                         /* tp_weaklistoffset */
	0,                         /* tp_iter */
	0,                         /* tp_iternext */
	RmPype_methods,         /* tp_methods */
	RmPype_members,         /* tp_members */
	0,                         /* tp_getset */
	0,                         /* tp_base */
	0,                         /* tp_dict */
	0,                         /* tp_descr_get */
	0,                         /* tp_descr_set */
	0,                         /* tp_dictoffset */
	0,                         /* tp_init */
	0,                         /* tp_alloc */
	0,                         /* tp_new */
};

PyObject* CreateRmPypeObject()
{
	if (!(rmPypeType.tp_flags & Py_TPFLAGS_READY))
	{
		rmPypeType.tp_new = PyType_GenericNew;
		PyType_Ready(&rmPypeType);
	}
	PyObject *obj = PyObject_CallObject((PyObject*) &rmPypeType, NULL);
	return (PyObject*) obj;
}