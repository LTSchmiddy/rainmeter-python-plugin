#include "RmPypeMain.h"
#include "RmPypeModule.h"
// #include "RmPypeObject.h"

PyMODINIT_FUNC PyInit_rm_pype(void)
{
    return PyModule_Create(&RmPypeModule);
}