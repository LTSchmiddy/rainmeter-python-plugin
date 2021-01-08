cd PythonHome
python.exe get-pip.py
python.exe -m pip install pywin32 win10toast ptvsd
echo from win10toast import ToastNotifier; toaster = ToastNotifier(); toaster.show_toast("RmPythonPlugin", "Pip Installed", duration=10) | python.exe
cd ../