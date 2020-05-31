<p align="center">
  <img width="320" height="270" src="https://i.imgur.com/z4Pv3vE.png">
</p>

##### A Minecraft: Bedrock server software written in Python

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](LICENSE)
[![Build Status](https://ci.nukkitx.com/job/NukkitX/job/Nukkit/job/master/badge/icon)](https://ci.nukkitx.com/job/NukkitX/job/Nukkit/job/master/)
![Tests](https://img.shields.io/jenkins/t/https/ci.nukkitx.com/job/NukkitX/job/Nukkit/job/master.svg)
[![Discord](https://img.shields.io/discord/393465748535640064.svg)](https://discord.gg/UTMZTaB)

Introduction
-------------

PocketFurnace is a clean server software for Minecraft: Bedrock Edition.
It has a few key advantages over other server software:

* Written in Python, unique, fast and easy development.
* Having a friendly structure, now the project is in beta phase, we will add plugins support in a future.

PocketFurnace is **under improvement** yet, we welcome contributions. 


Planned features
-------------
- Python plugins support
- Implement basic AI for mobs
- Create default vanilla generators and more vanilla-like worlds
- Add others software implementations
- LevelDB writing/saving for worlds


Running
-------------
It's easy, just make sure you've got virtualenv (preferrably installed via pip, may also be installed via source or Linux repository) and Python 3.5, then just run the following
```sh
$ pip install virtualenv  # Optional, but highly, highly recommended
$ virtualenv -p /usr/bin/python .venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
$ python main.py
$ deactivate
```

Plugin API
-------------
Information about plugins will be added in a future

Docker
-------------
Docker support will be added too.

Contributing
------------
Please read the [CONTRIBUTING](.github/CONTRIBUTING.md) guide before submitting any issue. Issues with insufficient information or in the wrong format will be closed and will not be reviewed.
If you wanna be part of PocketFurnace development send us a DM on Twitter


License
-----------
We're licensed under the GNU GPLv3, here's your copy:
 
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
	
	
Logo by [@Josewowgame2888](https://github.com/Josewowgame2888) - *All rights reserved, copy and reuse of the logo is forbidden*
