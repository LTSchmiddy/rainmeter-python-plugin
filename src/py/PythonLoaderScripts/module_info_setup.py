import os, sys, subprocess, pathlib, time, traceback



try:
    from PythonLoaderUtils.module_info import ModuleInfo
    ModuleInfo.interp_path = sys.executable
    
    minfo_path = sys.argv[1]
    print(f"-> Setting up dependencies for {minfo_path}...\n")
    time.sleep(2)

    minfo = ModuleInfo.load_module_info(minfo_path)
    minfo.setup_dependencies()

    print(f"\n-> Setup completed. Exiting...")
    time.sleep(2)
    
except Exception as e:
    traceback.print_exception(type(e), e, e.__traceback__)
    input("Press Enter to close...")
