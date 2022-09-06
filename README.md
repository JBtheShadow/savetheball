This game was made during a Lua Development + Love2D tutorial and later ported
to Python + PyGame by me. As such there most likely are things that are not very
Pythonic but in the end this is more of a learning experience for me than anything else.

The game itself consists of moving a circle with your mouse cursor and avoiding enemy
shapes for as long as you can. See how high of a score you can achieve.

If you have Python 3.9 (unsure if other versions will work) you can run:
```
python3 "src\main.py"
```

Command to build the exe:
```
pyinstaller "src\main.py" --onefile --name savetheball --windowed
```
