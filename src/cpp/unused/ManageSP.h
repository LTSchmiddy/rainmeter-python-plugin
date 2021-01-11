#ifndef __MANAGE_SP__
#define __MANAGE_SP__


#include <Windows.h>
#define SP_HOST "sp_host.py"

struct SpInfo{
    STARTUPINFO si;
    PROCESS_INFORMATION pi;
    unsigned int measureCount;
};
extern SpInfo spInfo;

void StartPyProcess();
void EndPyProcess();

#endif