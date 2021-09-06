LOOKUP_KEY = "deploy.py"
MODE = ['debug', 'release'][0]

settings_filepath = "./mct_user_settings.json"

import os, sys, json, shutil
mcppt_file = json.load(open(settings_filepath, 'r'))


if LOOKUP_KEY not in mcppt_file:
    mcppt_file[LOOKUP_KEY] = {
        "debug": {
            "plugin-build-out-path": "./build-Debug/bin/",
            "plugin-loader-scripts-path": "./src/py/",
            "rainmeter-plugin-path": "./Rainmeter-Testing/Plugins/",
            "rainmeter-root-path": "./Rainmeter-Testing",
            "python-home-bundle-path": "./assets/PythonHome",
            "python-home-bundle-dest": "./Rainmeter-Testing/PythonHome",
            "rainmeter-skin-src-path": "./src/rainmeter",
            "rainmeter-skin-dest-path": "./Rainmeter-Testing/Skins"
        },
        "release": {
            "plugin-build-out-path": "./build-Release/bin/",
            "plugin-loader-scripts-path": "./src/py/",
            "rainmeter-plugin-path": "./bin/Plugins/",
            "rainmeter-root-path": "./bin",
            "python-home-bundle-path": "./assets/PythonHome",
            "python-home-bundle-dest": "./bin/PythonHome",
            "rainmeter-skin-src-path": "./src/rainmeter",
            "rainmeter-skin-dest-path": "./bin/Skins"
        }
    }
        
    json.dump(mcppt_file, open(settings_filepath, 'w'), indent=4)
        

settings = mcppt_file[LOOKUP_KEY][MODE]

def recursive_overwrite(src, dest, ignore=None):
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                recursive_overwrite(os.path.join(src, f), 
                                    os.path.join(dest, f), 
                                    ignore)
    else:
        shutil.copyfile(src, dest)

print("Copying compiled plugins... ", end="")
recursive_overwrite(settings["plugin-build-out-path"], settings["rainmeter-plugin-path"])
print("Done.")

print("Copying loader .py scripts... ", end="")
recursive_overwrite(settings["plugin-loader-scripts-path"], settings["rainmeter-root-path"])
print("Done.")

print("Copying CPython embedded interpreter bundle... ", end="")
recursive_overwrite(settings["python-home-bundle-path"], settings["python-home-bundle-dest"])
print("Done.")

print("Copying testing skins for Rainmeter... ", end="")
recursive_overwrite(settings["rainmeter-skin-src-path"], settings["rainmeter-skin-dest-path"])
print("Done.")

print("Operation completed.")


# input("Press Enter to close...")