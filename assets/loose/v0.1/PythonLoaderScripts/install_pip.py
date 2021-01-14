import os, sys, subprocess, pathlib, time

import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    # sys.stderr = open("pip_err.log", "w")
    if is_admin():
        # print(f"CWD: {os.getcwd()}")
        run_install()
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)



def run_install():
    print("PyPlugin[E] needs to install Pip. Please wait...\n")
    time.sleep(2)

    subprocess.run([
        sys.executable,
        str(pathlib.Path(os.path.dirname(sys.executable)).joinpath("get-pip.py"))
    ])

    print("\nInstalling PyPlugin[E] dependencies...\n")
    time.sleep(3)
    
    subprocess.run([
        sys.executable,
        "-m",
        "pip",
        "install",
        "pywin32",
        "virtualenv",
        "ansicolors",
        "win10toast", 
        "ptvsd"
    ])
    print("\nDone! Rainmeter will restart.")
    subprocess.Popen([sys.argv[1]])
    input("Press Enter to close...")
    
if __name__ == '__main__':
    main()