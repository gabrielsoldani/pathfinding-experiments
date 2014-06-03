pathfinding-experiments
=======================

This is a tool to help beginners understand pathfinding algorithms and its challenges in a 2D square tile-based video game, like Pac-Man and most Pokémon games.

It currently implements [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search), and  displays graphically every iteration of the algorithm.

It is written in [Python 2.7.x](https://www.python.org/) and uses [Processing.py](https://github.com/jdf/processing.py).

How to run
----------

On Windows, download Processing.py to the **processing-py** directory and run **start.bat**.

Alternatively, run **app.py** using Processing.py.

Commands
--------

Left Click sets the start and end positions. Click once to set the start position, then again to set the end position and start the algorithm.

Right Click toggles walls. Right click a ground tile to make it a wall tile and vice versa.
