import os, sys, json, shutil
settings = json.load(open("./mcppt_settings.json", 'r'))["deploy.py"]

# print (settings)

for i in os.listdir(settings["plugin-build-out-path"]):
# # Copy Plugin:
    shutil.copy(
        os.path.join(settings["plugin-build-out-path"], i),
        settings["rainmeter-plugin-path"]
    )


for i in os.listdir(settings["py-ext-build-out-path"]):
# # Copy Plugin:
    if i.endswith(".dll"):
        shutil.copy(
            os.path.join(settings["py-ext-build-out-path"], i),
            os.path.join(settings["rainmeter-root-path"], i.removesuffix(".dll")+".pyd")
        )
    else:
        shutil.copy(
        os.path.join(settings["py-ext-build-out-path"], i),
        settings["rainmeter-root-path"]
    )


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

recursive_overwrite(settings["plugin-loader-scripts-path"], settings["rainmeter-root-path"])
recursive_overwrite(settings["rainmeter-skin-src-path"], settings["rainmeter-skin-dest-path"])


# input("Press Enter to close...")