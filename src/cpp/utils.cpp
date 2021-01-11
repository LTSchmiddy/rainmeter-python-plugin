#include <codecvt>
#include <locale>

#include <Windows.h>
#include <Python.h>
#include <RainmeterAPI.h>

#include "ManagePython.h"
#include "utils.h"

#define _SILENCE_CXX17_CODECVT_HEADER_DEPRECATION_WARNING 1
using namespace std;
using namespace std::filesystem;

using convert_t = std::codecvt_utf8<wchar_t>;
wstring_convert<convert_t, wchar_t> strconverter;


string to_string(std::wstring wstr) {
    return strconverter.to_bytes(wstr);
}

wstring to_wstring(std::string str) {
    return strconverter.from_bytes(str);
}


// path to Rainmeter.exe
string get_rm_path_string() {
    TCHAR execPath[MAX_PATH];

    if( !GetModuleFileNameA( NULL, execPath, MAX_PATH ) )
    {
        return "";
    }

    return execPath;
}

path get_rm_path() {
    return ((path)get_rm_path_string());
}


path get_rm_dir_path() {
    return ((path)get_rm_path_string()).remove_filename();
}

path get_python_interpreter_home() {
    path rmPath = get_rm_dir_path();

    rmPath.append(PYTHON_HOME);
    return rmPath;
}

path get_python_interpreter_exec() {
    path rmPath = get_python_interpreter_home();

    rmPath.append("python.exe");
    return rmPath;
}

path get_python_interpreter_wexec() {
    path rmPath = get_python_interpreter_home();

    rmPath.append("pythonw.exe");
    return rmPath;
}

path get_python_loader_home() {
    path rmPath = get_rm_dir_path();

    rmPath.append(PYTHON_LOADER);
    return rmPath;
}