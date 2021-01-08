#include <string>
#include <filesystem>

#define PYTHON_HOME "PythonHome"

std::string to_string(std::wstring wstr);
std::wstring to_wstring(std::string str);

std::string get_rm_path_string();
std::filesystem::path get_rm_path();
std::filesystem::path get_rm_dir_path();
std::filesystem::path get_python_interpreter_home();
std::filesystem::path get_python_interpreter_exec();
std::filesystem::path get_python_interpreter_wexec();
std::filesystem::path get_python_loader_home();