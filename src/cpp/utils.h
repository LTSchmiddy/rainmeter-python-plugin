#include <string>
#include <filesystem>

#define PYTHON_HOME "PythonHome"

std::string to_string(std::wstring wstr);
std::wstring to_wstring(std::string str);

std::string get_exec_path();
std::filesystem::path get_python_loader_home();
std::filesystem::path get_python_interpreter_home();