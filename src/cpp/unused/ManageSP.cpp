#include <filesystem>
#include <stdio.h>
#include <tchar.h>

#include "ManageSP.h"
#include "utils.h"

using namespace std;
using namespace std::filesystem;

SpInfo spInfo;

void StartPyProcess() {
    ZeroMemory( &spInfo.si, sizeof(spInfo.si) );
    spInfo.si.cb = sizeof(spInfo.si);
    ZeroMemory( &spInfo.pi, sizeof(spInfo.pi) );

    

    LPSTR interp_path = (char*)get_python_interpreter_exec().u8string().c_str();
    // LPSTR interp_path = get_python_interpreter_exec().u8string().c_str();

    if( !CreateProcessA(NULL,   // No module name (use command line)
        "PythonHome\\python.exe sp_host.py",        // Command line
        NULL,           // Process handle not inheritable
        NULL,           // Thread handle not inheritable
        FALSE,          // Set handle inheritance to FALSE
        0,              // No creation flags
        NULL,           // Use parent's environment block
        NULL,           // Use parent's starting directory 
        &spInfo.si,            // Pointer to STARTUPINFO structure
        &spInfo.pi )           // Pointer to PROCESS_INFORMATION structure
    ) 
    {
        printf( "CreateProcess failed (%d).\n", GetLastError() );
        return;
    }
}

void EndPyProcess() {
    TerminateProcess(
        spInfo.pi.hProcess,
        0
    );
}
