[![GitHub](https://img.shields.io/badge/mitoconifg-label?style=for-the-badge&logo=github&logoColor=white&label=github&color=blue)](https://github.com/caela-uk/mitoconfig/)
[![MIT License](https://img.shields.io/badge/MIT-label?style=for-the-badge&logoColor=white&label=licence&color=green)](https://github.com/caela-uk/mitoconfig/blob/main/LICENCE.md)
![Work in Progress](https://img.shields.io/badge/Work_in_Progress-label?style=for-the-badge&logo=linux&logoColor=white&color=red)


**Mitoconfig** is a **work-in-progress**, open-source configuration management tool designed to make editing, backing up and reproducing/sharing configurations much easier.
> and faster!

This is a small hobby project named after the biological process of **mitosis**. It is something that I have found myself needing time and time again whilst moving between systems and Linux distributions, or just generally working on configs *(oh my, shortcuts and backups are **soooo** necessary on the daily)*

<details>
<summary><h3>Mitoconfig Feature Roadmap</h3></summary>

## Roadmap
### Core
- [x] Basic argument handling and help page
- [x] Read tracked items from TOML
- [x] Edit any config file with shortcuts
- [ ] Working backup and restoration system
- [ ] Vial/Spore functionality and .mito archive format
- [ ] Set up compilation and building with nuitka (?)
- [ ] Publish to the AUR

### Future (?)
- [ ] Releases for more repositories and platforms
- [ ] Mitosys module for reproducing package installations and more across (Linux/UNIX) systems (?)
- [ ] Services for automatic backups and (?) cross-system syncing
</details>

## Documentation/Help
Documentation will be coming at **some point**, probably via a GitHub Wiki. It will likely be needed for some people editing the tracked file, *even though it's already got some pretty intuitive notes in it.*

<details>
<summary><h3>Cheatsheet</h3></summary>

```yaml
Usage:
  mitoconfig <command> [arguments]/[flags]
  config <TARGET>          Simple but fast and useful shortcut for 'mitoconfig edit'

Mitoconfig Commands:
  tracked                  View or edit your tracked file, containing all tracked config/data items
  edit <NAME>              Open a tracked shortcut (files edit with your default editor, directories run cd and ls)
  backup <TARGETS>         Create a fast and temporary backup of a tracked target                 [WIP]
  vial <TARGETS> [PATH]    Seal targeted tracked items into a portable .mito file                 [WIP]
  spore <PATH/URL>         Deploy a .mito vial, reconstructing its files onto your system         [WIP]

Backup Subcommands:
  backup restore <TARGS>   Replace active configs/data items with their backup variants           [WIP]
  backup kill <TARGETS>    Permanently delete specific target backups                             [WIP]
  backup clear             Wipe all backups to free up disk space                                 [WIP]

Flags:
  -h, --help               Display this help message
  -a, --all                Target all tracked config and data files (careful; storage can go brrr)
  -c, --configs            Target all tracked configuration files and directories
  -d, --data               Target all tracked data directories (e.g. browsers)
  -y, --yes                Auto-confirm all warnings during spore deployment or vial creation
```
> Note that you can only run the commands `mitoconfig` and `config` if you have installed mitoconfig, which is *currently* a manual task requiring a functioning brain, a download/clone, perseverance and a couple symlinks.
</details>

## Contributions
In its current state, Mitoconfig is certainly not ready for actual usage and therefore bug reports via GitHub Issues will only be accepted for incorrect argument processing. However, please feel free to suggest features or open pull requests.

In future it would also be great if this project could be ported to more places than just my current AUR scope.

## Installation
What? I didn't even think of that yet. Let me get back to you.

> [!IMPORTANT]
> This project is **entirely WIP**! During this phase, it is **guaranteed** that things will **NOT** work as expected.