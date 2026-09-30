#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

__version__ = "0.1.1" # should shange with behavioral (or major code) changes

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib # potential fallback for older Python versions (?)
    except ImportError: # nothings going your way today, is it? lmfao
        sys.exit("error: Python 3.11+ is required, or install 'tomli' for older versions")

def getTrackedPath():
    """Returns the platforms' path to tracked.toml"""
    home = Path.home()

    if sys.platform == "win32":
        # windows ew, why tf you gotta be so bloody difficult
        appData = Path(os.environ.get("APPDATA", home / "AppData/Roaming"))
        return appData / "mitoconfig" / "tracked.toml"
    else:
        # linux yayyyyyy, mac is alright too (if you're rich) though
        xdgConfig = Path(os.environ.get("XDG_CONFIG_HOME", home / ".config"))
        return xdgConfig / "mitoconfig" / "tracked.toml"

def loadTracked():
    """Parses the .toml file and returns us a dictionary"""
    path = getTrackedPath()

    if not path.exists():
        return {}
    try:
        with open(path, "rb") as f:
            return tomllib.load(f)
    except Exception as e:
        print(f"error: failed to parse TOML file at {path}\n{e}")
        sys.exit(1)

def main():
    # snatch those args into sum we can fw
    caller = Path(sys.argv[0]).name # it's not john p, dw
    rawArgs = sys.argv[1:]

    if caller == "config":
        if not rawArgs: # vro wtf did you expect to happen
            printHelp()
            return
        args = ["edit"] + rawArgs
    else:
        args = rawArgs

    # son😭
    if "--help" in args or "-h" in args or "help" in args:
        print()
        printHelp()
        return
    elif not args:
        print("error: no command specified, fella ion work standalone\n")
        printHelp()
        return

    command = args[0]
    commandArgs = args[1:]

    if command == "edit":
        editConfig(commandArgs)
    elif command == "tracked":
        doTracked(commandArgs)
    elif command == "backup":
        doBackup(commandArgs)
    elif command == "vial":
        vialUp(commandArgs)
    elif command == "spore":
        doSpore(commandArgs)
    else:
        print(f"unknown command: {command}\n")
        printHelp()

def printHelp():
    GREEN = "\033[32m"
    CYAN = "\033[36m"
    BOLD = "\033[1m"
    RED = "\033[31m"
    RST = "\033[0m" # clear formatting
    EDITOR = os.environ.get('VISUAL') or os.environ.get('EDITOR') or 'nano'

    print(f"{GREEN}Mitoconfig{RST} is a {BOLD}WIP{RST} configuration management tool designed to make editing, backing up and reproducing/sharing configurations much easier.\n")

    print(f"{BOLD}Usage{GREEN}:{RST}\n")
    print(f"  mitoconfig {GREEN}<command>{RST} [arguments]/[flags]\n")
    print(f"  config {GREEN}<TARGET>{RST}         Simple but fast and useful shortcut for 'mitoconfig edit'\n")

    print(f"{BOLD}Mitoconfig Commands{GREEN}:\n")
    print(f"  {GREEN}tracked{RST}                View or edit your tracked file, containing all tracked config/data items")
    print(f"  {GREEN}edit{RST} <NAME>            Open a tracked shortcut (files edit with {EDITOR}, directories run cd and ls)")
    print(f"  {GREEN}backup{RST} <TARGETS>       Create a fast and temporary backup of a tracked target                    {BOLD}{RED}[WIP]{RST}")
    print(f"  {GREEN}vial{RST} <TARGETS> [PATH]  Seal targeted tracked items into a portable {CYAN}.mito{RST} file                    {BOLD}{RED}[WIP]{RST}")
    print(f"  {GREEN}spore{RST} <PATH/URL>       Deploy a {CYAN}.mito{RST} vial, reconstructing its files onto your system            {BOLD}{RED}[WIP]{RST}\n")

    print(f"{BOLD}Backup Subcommands{GREEN}:\n")
    print(f"  {GREEN}backup restore{RST} <TARGS>  Replace active configs/data items with their backup variants             {BOLD}{RED}[WIP]{RST}")
    print(f"  {GREEN}backup kill{RST} <TARGETS>   Permanently delete specific target backups                               {BOLD}{RED}[WIP]{RST}")
    print(f"  {GREEN}backup clear{RST}            Wipe all backups to free up disk space                                   {BOLD}{RED}[WIP]{RST}\n")

    print(f"{BOLD}Flags{GREEN}:\n")
    print(f"  {GREEN}-h, --help{RST}             Display this help message")
    print(f"  {GREEN}-a, --all{RST}              Target all tracked config and data files (careful: storage can go brrr)")
    print(f"  {GREEN}-c, --configs{RST}          Target all tracked configuration files and directories")
    print(f"  {GREEN}-d, --data{RST}             Target all tracked data directories (e.g. browsers)")
    print(f"  {GREEN}-y, --yes{RST}              Auto-confirm all warnings during spore deployment or vial creation\n")

def editConfig(args):
    """Edit a file or open a dir by an alias or name"""
    trackedPath = getTrackedPath()

    if not args:
        print(f"error: please provide a shortcut name or create a shortcut in {trackedPath}")
        return

    name = args[0]
    data = loadTracked()

    # name or alias, that IS the question
    targetProperties = None
    targetKey = None

    if name in data:
        targetKey = name
        targetProperties = data[name]
    else:
        for key, prop in data.items():
            if prop.get("alias") == name:
                targetKey = key
                targetProperties = prop
                break

    if not targetProperties:
        print(f"error: target '{name}' not found in tracked.toml")
        return

    rawPath = targetProperties.get("path")
    if not rawPath:
        print(f"error: target '{targetKey}' has no path specified in tracked.toml")
        return

    realPath = Path(rawPath).expanduser() # tildas work now

    if not realPath.exists():
        print(f"error: path '{realPath}' does not exist on your machine")
        return

    editor = os.environ.get('VISUAL') or os.environ.get('EDITOR') or 'nano'

    # if the item is a directory then we have to run cd and ls on the shells behalf
    if realPath.is_dir():
        shell = os.environ.get('SHELL', 'sh')
        print(f"dir: \033[32m{rawPath}\n")
        try:
            subprocess.run([shell, "-c", "ls"], cwd=realPath)
            subprocess.run([shell], cwd=realPath)
        except Exception as e:
            print(f"error: could not open shell: {e}")

    else:
        try:
            # open editor of choice
            subprocess.run([editor, str(realPath)], check=True)
            postEdit = targetProperties.get("postEdit")
            if postEdit:
                subprocess.run(postEdit, shell=True)
        except Exception as e:
            print(f"error: failed to edit file: {e}")

def doTracked(args):
    path = getTrackedPath()

    # newbies have it easy, haters gonna hate vro
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        defaultTemplate = """# Mitoconfig Tracked File TOML Example
# Some example use cases (change these):

[hyprland]
alias = "hypr"
path = "~/.config/hypr/hyprland.lua"
type = "config" # simple config file that should not contain sensitive data

[cpupower] # sets CPU clock speeds, something unique to each processor
path = "/etc/default/cpupower-service.conf"
type = "config"
postEdit = "sudo systemctl restart cpupower"
thisMachineOnly = true
# ^^ the above tagging means there is no housefire when moved to another machine, just for an example

[firedog] # example browser
path = "~/.config/mozzarella/firedog/"
type = "data"
# ^^ set to data, because a browser contains sensitive data you wouldn't always want to copy, is also very storage heavy with caches and everything

[fish]
path = "~/.config/fish/config.fish"
type = "config"
postEdit = "exec fish" # the commmand "exec fish" here would reload fish after editing config

[obs-studio]
alias = "obs"
path = "~/.config/obs-studio/"
type = "data" # could contain stream keys you wouldn't want to share, so mark it off as data for safety

# Please Note:
#
# - You MUST specify whether a tracked item is config or data, this is necessary for security and saving storage space during the creation of backups/vials
#
# - An alias is an alternative name for an item, so for example with the default configuration: 'config hyprland' and 'config hypr' would both edit the same file.
#
# - You can wrap a 'postEdit' script to run directly after exiting your editor, this is useful for reloading services or shells, just for example.
#
# - If 'thisMachineOnly' is equal to 'true' on an item, when putting your configurations into a vial it would ALWAYS exclude that specific item.
#   Useful for machine-specific tweaks (like setting your CPU frequency) that would definitely screw with other computers if copied over.
"""
        path.write_text(defaultTemplate)
        # happy now? :D
        # *damn newbies*

    editor = os.environ.get('VISUAL') or os.environ.get('EDITOR') or 'nano'
    try:
        subprocess.run([editor, str(path)], check=True)
    except Exception as e:
        print(f"error: failed to open editor: {e}")

def doBackup(args):
    # quick backup, might even do data to .cache or something because it's not made to last indefinitely and should be cleared every now and then

    if not args:
        print("error: please specify a target")
        return

    action = args[0]
    if action in ["clear", "--clear", "-C"]:
        print("clear all backups")
        return

    if action in ["restore", "--restore", "-r"]:
        # we're tryna restore, so lets make sure restore isn't the path
        target = args[1] if len(args) > 1 else "nothing"

        if target in ["--all", "-a"]:
            print("restore backup for all tracked items")
        elif target in ["--configs", "-c"]:
            print("restore backup for all tracked config files/directories")
        elif target in ["--data", "-d"]:
            print("restore backup for all tracked data files/directories")
        else:
            print(f'''restore backup for: "{target}"''')
        return

    if action in ["kill", "--kill", "-k"]:
        # we gotta grab a target
        target = args[1] if len(args) > 1 else "nothing"

        if target in ["--all", "-a"]:
            print("delete backup for all tracked items")
        elif target in ["--configs", "-c"]:
            print("delete backup for all tracked config files/directories")
        elif target in ["--data", "-d"]:
            print("delete backup for all tracked data files/directories")
        else:
            print(f'''delete backup for: "{target}"''')
        return

    # if you're not clearing, killing or restoring then you're clearly just backing up shi like a good boy (edit: why the fuck did i type that)
    if action in ["--all", "-a"]:
        print("back up all tracked items")
    elif action in ["--configs", "-c"]:
        print("back up all tracked config files/directories")
    elif action in ["--data", "-d"]:
        print("back up all tracked data files/directories")
    else:
        print(f'''back up target: "{action}"''')

def vialUp(args):
    # put all of your configs, data, or both into a vial (.mito file) to be opened elsewhere with spore- depends on 7zip for efficient de/compression
    # in future make a full TUI and template/docs for vial creation (like adding packages and scripts with the planned mitosys) and sharing
    if not args:
        print("error: please specify what to vial up")
        return

    target = args[0]

    destination = args[1] if len(args) > 1 else "./"

    if target in ["--all", "-a"]:
        print(f"vial up all tracked items into a .mito file at: {destination}")
    elif target in ["--configs", "-c"]:
        print(f"vial up all tracked config files/directories into a .mito file at: {destination}")
    elif target in ["--data", "-d"]:
        print(f"vial up all tracked data files/directories into a .mito file at: {destination}")
    else:
        print(f'''vial up "{target}" into a .mito file at: {destination}''')
    # currently would lack the ability to name the .mito file and would not show the .mito files path, just the parent folder

def doSpore(args):
    """Open up a vial .mito file and replace your configs out with the ones in there + ofc your tracked file, possibly not full overwrite everywhere though maybe a merge (?)"""
    if not args:
        print("error: please provide a path or URL to a .mito file.")
        return

    forceYes = "--yes" in args or "-y" in args

    # look past the --yes flag for the path
    sourcePath = "nothing"
    for item in args:
        if item not in ["--yes", "-y"]:
            sourcePath = item
            break

    print(f'''spore from vial: "{sourcePath}" (would skip warnings: {forceYes})''')

if __name__ == "__main__":
    main()
