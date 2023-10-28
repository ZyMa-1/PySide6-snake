# PySide6-snake

[![Python Version](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/release/python-310/)
[![Licence MIT](https://img.shields.io/badge/License-MIT-purple.svg)](/LICENCE)  
Snake game using PySide6 library.

![screnshot](/screenshot.png)

---

# Flow of the game
- Game ready to start
- Any button pressed
- Game starts
- Every tick snake moves, input between ticks changes direction
- Game over
- Waiting for some time, and starting over again

# Game controls
- Arrow keys

# Building the project into executable
Building with Nuitka (1.6.6) command:

```bash
nuitka --onefile --follow-imports --quiet --disable-console --plugin-enable=pyside6 --output-filename=snake_game.exe .\main.py
```
