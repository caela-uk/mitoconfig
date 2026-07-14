#!/usr/bin/env python3
import sys
import os


def main():
    # snatch those args into sum we can fw frfr
    args = sys.argv[1:]

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
    RST = "\033[0m" # clear formatting
    EDITOR = os.environ.get('VISUAL') or os.environ.get('EDITOR') or 'nano'

    print(f"{GREEN}Mitoconfig{RST} is a {BOLD}WIP{RST} configuration management tool designed to make editing, backing up and reproducing/sharing configurations much easier.\n")

    print(f"{BOLD}Usage{GREEN}:{RST}\n")
    print(f"  mitoconfig {GREEN}<command>{RST} [arguments]/[flags]\n")
    print(f"  config {GREEN}<TARGET>{RST}      \\  Simple but fast and useful shortcut for 'mitoconfig edit'\n")

    print(f"{BOLD}Mitoconfig Commands{GREEN}:\n")
    print(f"  {GREEN}tracked{RST}                View or edit your tracked file, containing all tracked config/data items")
    print(f"  {GREEN}edit{RST} <NAME>            Open a tracked shortcut (files edit with {EDITOR}, directories run cd and ls)")
    print(f"  {GREEN}backup{RST} <TARGETS>       Create a fast and temporary backup of a tracked target")
    print(f"  {GREEN}vial{RST} <TARGETS> [PATH]  Seal targeted tracked items into a portable {CYAN}.mito{RST} file")
    print(f"  {GREEN}spore{RST} <PATH/URL>       Deploy a {CYAN}.mito{RST} vial, reconstructing its files onto your system\n")

    print(f"{BOLD}Backup Subcommands{GREEN}:\n")
    print(f"  {GREEN}backup restore{RST} <TARGS>  Replace active configs/data items with their backup variants")
    print(f"  {GREEN}backup kill{RST} <TARGETS>   Permanently delete specific target backups")
    print(f"  {GREEN}backup clear{RST}            Wipe all backups to free up disk space\n")

    print(f"{BOLD}Flags{GREEN}:\n")
    print(f"  {GREEN}-h, --help{RST}             Display this help message")
    print(f"  {GREEN}-a, --all{RST}              Target all tracked config and data files (careful: storage can go brrr)")
    print(f"  {GREEN}-c, --configs{RST}          Target all tracked configuration files and directories")
    print(f"  {GREEN}-d, --data{RST}             Target all tracked data directories (e.g. browsers)")
    print(f"  {GREEN}-y, --yes{RST}              Auto-confirm all warnings during spore deployment or vial creation\n")


def edit_config(args):
    # basically a quick shortcut to edit a file, so ion have to type something like 'micro ~/.config/hypr/hyprland.lua'- in a bit ima alias 'mitoconfig edit' to 'config' with a link or sum
    # when the user opens a shortcut where the path is a directory, just run cd and ls (make sure ls runs with their actual shell so alias' could work)
    if not args:
        print("error: please provide a shortcut name or create a shortcut in [TRACKED FILE PATH]") # future me make ts point to the right place and be OS specific
        return
    
    name = args[0]
    print(f"opening config shortcut: {name}")


def do_tracked(args):
    # edit the tracked file
    print("open tracked file in default editor")


def do_backup(args):
    # quick backup, might even do data to .cache or something because it's not made to last indefinitely and should be cleared every now and then
    if not args:
        print("error: please specify a target")
        return

    # what are we backing up
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