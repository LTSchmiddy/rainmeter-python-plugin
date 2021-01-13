#include <Python.h>
#include <Windows.h>
#define RM_PYPE_BUFFER_SIZE 2048
#define RM_PYPE_TIMEOUT 1000

typedef struct RmPypeObject {
	PyObject_HEAD
	
	char* name;
	HANDLE handle;

	DWORD mode = PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT;
	DWORD timeout = RM_PYPE_TIMEOUT;

	RmPypeObject() {
		name = NULL;
	}
} RmPypeObject;

PyObject* CreateRmPypeObject();