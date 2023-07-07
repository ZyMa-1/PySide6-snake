# PySide6-snake

[![Python Version](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/release/python-310/)
[![Licence MIT](https://img.shields.io/badge/License-MIT-purple.svg)](/LICENCE)  
Snake game in PySide6, was kinda bored idk

Building with Nuitka (1.6.6) command:

```bash
nuitka --onefile --follow-imports --quiet --disable-console --plugin-enable=pyside6 --output-filename=snake_game.exe .\main.py
```

![screnshot](/screenshot.png)