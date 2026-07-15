#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

__version__ = "0.1.0"

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib # potential fallback for older Python versions (?)
    except ImportError: # nothings going your way today, is it? lmfao
        sys.exit("error: Python 3.11+ is required, or install 'tomli' for older versions")


def get_tracked_path():
    # returns the platforms path to tracked.toml
    home = Path.home()

    if sys.platform == "win32":
        # windows ew, why tf you gotta be so bloody difficult
        appdata = Path(os.environ.get("APPDATA", home / "AppData/Roaming"))
        return appdata / "mitoconfig" / "tracked.toml"
    else:
        # linux yayyyyyy, mac is alright too though
        xdg_config = Path(os.environ.get("XDG_CONFIG_HOME", home / ".config"))
        return xdg_config / "mitoconfig" / "tracked.toml"


def load_tracked():
    # parses the .toml file and returns us a dictionary
    path = get_tracked_path()

    if not path.exists():
        # gis an empty dict if the file isn't created yet so mitoconfig don't crash
        return {}
    try:
        with open(path, "rb") as f:
            return tomllib.load(f)
    except Exception as e:
        print(f"error: failed to parse TOML file at {path}\n{e}")
        sys.exit(1)


def main():
    # snatch those args into sum we can fw frfr

    caller = Path(sys.argv[0]).name # it's not john p, dw
    raw_args = sys.argv[1:]

    # support for the config shortcut
    if caller == "config":
        if not raw_args: # vro wtf did you expect to happen
            print_help()
            return
        args = ["edit"] + raw_args
    else:
        args = raw_args

    # son😭
    if "--help" in args or "-h" in args or "help" in args:
        print()
        print_help()
        return
    elif not args:
        print("error: no command specified, fella ion work standalone\n")
        print_help()
        return

    command = args[0]
    command_args = args[1:]

    if command == "edit":
        edit_config(command_args)
    elif command == "tracked":
        do_tracked(command_args)
    elif command == "backup":
        do_backup(command_args)
    elif command == "vial":
        vial_up(command_args)
    elif command == "spore":
        do_spore(command_args)
    else:
        print(f"unknown command: {command}\n")
        print_help()


def print_help():
    # prints this big help message - in future I should add a link to documentation

    # tuff colours
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


def edit_config(args):
    # edit a file or open a dir by an alias or name

    tracked_path = get_tracked_path()

    if not args:
        print(f"error: please provide a shortcut name or create a shortcut in {tracked_path}")
        return

    name = args[0]
    data = load_tracked()

    # name or alias, that IS the question
    target_properties = None
    target_key = None

    if name in data:
        target_key = name
        target_properties = data[name]
    else:
        for key, prop in data.items():
            if prop.get("alias") == name:
                target_key = key
                target_properties = prop
                break

    if not target_properties:
        print(f"error: target '{name}' not found in tracked.toml")
        return

    raw_path = target_properties.get("path")
    if not raw_path:
        print(f"error: target '{target_key}' has no path specified in tracked.toml")
        return

    # bro can we normalize tildas for /home/user
    real_path = Path(raw_path).expanduser()

    if not real_path.exists():
        print(f"error: path '{real_path}' does not exist on your machine")
        return

    editor = os.environ.get('VISUAL') or os.environ.get('EDITOR') or 'nano'

    # if the item is a directory then we have to run cd and ls on the shells behalf
    if real_path.is_dir():
        shell = os.environ.get('SHELL', 'sh')
        print(f"dir: \033[32m{raw_path}\n")
        try:
            subprocess.run([shell, "-c", "ls"], cwd=real_path)
            # hello shell
            subprocess.run([shell], cwd=real_path)
        except Exception as e:
            print(f"error: could not open shell: {e}")
 
    # finally, a regular text file
    else:
        try:
            # open editor of choice
            subprocess.run([editor, str(real_path)], check=True)
            # i hope people use post_edit, it's super useful
            post_edit = target_properties.get("post_edit")
            if post_edit:
                subprocess.run(post_edit, shell=True)
        except Exception as e:
            print(f"error: failed to edit file: {e}")


def do_tracked(args):
    # edit the tracked file
    path = get_tracked_path()

    # newbies have it easy, haters gonna hate vro
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        # create an example if they don't have one just yet
        default_template = """# Mitoconfig Tracked File TOML Example
# Some example use cases (change these):

[hyprland]
alias = "hypr"
path = "~/.config/hypr/hyprland.lua"
type = "config" # simple config file that should not contain sensitive data


[cpupower] # sets CPU clock speeds, something unique to each processor
path = "/etc/default/cpupower-service.conf"
type = "config"
post_edit = "sudo systemctl restart cpupower"
this_machine_only = true
# ^^ the above tagging means there is no housefire when moved to another machine, just for an example


[firedog] # example browser
path = "~/.config/mozzarella/firedog/"
type = "data"
# ^^ set to data, because a browser contains sensitive data you wouldn't always want to copy, is also very storage heavy with caches and everything


[fish]
path = "~/.config/fish/config.fish"
type = "config"
post_edit = "fish" # the commmand "fish" here would reload fish after editing config


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
# - You can wrap a 'post_edit' script to run directly after exiting your editor, this is useful for reloading services or shells, just for example.
#
# - If 'this_machine_only' is equal to 'true' on an item, when putting your configurations into a vial it would ALWAYS exclude that specific item.
#   Useful for machine-specific tweaks (like setting your CPU frequency) that would definitely screw with other computers if copied over.
#
"""
        path.write_text(default_template)
        # happy now? :D
        # *damn newbies*

    editor = os.environ.get('VISUAL') or os.environ.get('EDITOR') or 'nano'

    try:
        subprocess.run([editor, str(path)], check=True)
    except Exception as e:
        print(f"error: failed to open editor: {e}")


def do_backup(args):
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

    # if you're not clearing, killing or restoring then you're clearly just backing up shi like a good boy
    if action in ["--all", "-a"]:
        print("back up all tracked items")
    elif action in ["--configs", "-c"]:
        print("back up all tracked config files/directories")
    elif action in ["--data", "-d"]:
        print("back up all tracked data files/directories")
    else:
        print(f'''back up target: "{action}"''')


def vial_up(args):
    # put all of your configs, data, or both into a vial (.mito file) to be opened elsewhere with spore- zip based unless there's sum faster
    # in future make a full TUI and guide for vial creation (like adding packages and scripts with the planned mitosys) and sharing
    if not args:
        print("error: please specify what to vial up")
        return

    # argument 0 is what we're gonna put in the vial
    target = args[0]
    
    # argument 1 is WHERE the vial file goes
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


def do_spore(args):
    # open up a vial .mito file and replace your configs out with the ones in there + ofc your tracked file, possibly not full overwrite everywhere though maybe a merge (?)
    if not args:
        print("error: please provide a path or URL to a .mito file.")
        return

    # did they use the --yes flag?
    force_yes = "--yes" in args or "-y" in args

    # look past the --yes flag for the path
    source_path = "nothing"
    for item in args:
        if item not in ["--yes", "-y"]:
            source_path = item
            break

    print(f'''spore from vial: "{source_path}" (would skip warnings: {force_yes})''')


if __name__ == "__main__":
    main()