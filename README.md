# Game of Life
python implementation of Conway's Game of Life. Tested on python 3.6

![alt text](https://github.com/Brinon/game_of_life/blob/master/demos/long_thing_demo.gif)

The game consist in a matrix of cells that can be either activate or inactive. Each step cells update by the following rules:

* For a cell that is *active*:
  - Each cell with one or no active neighbors becomes inactive, as if by solitude.
  - Each cell with four or more active neighbors becomes inactive, as if by overpopulation.
  - Each cell with two or three active neighbors survives active.
* For a cell that is *inactive*
  - Each cell with active three neighbors becomes active.

Usage:
```
pythonw app.py
pythonw app.py -f /path/to/file.json # initiallices from a previously saved state 
```

# Controls
You can toggle the state of a cell clicking on it.

* `space`: step
* `a`: toggle autoplay
* `s`: save the current state of the cells to a json file
* `r`: restart the game, deactivating all the cells
* `q`: quit

# Requirements
* pygame
* numpy

# Cool demos

## Oscillators
![alt text](https://github.com/Brinon/game_of_life/blob/master/demos/oscillators_demo.gif)

## Long thing
![alt text](https://github.com/Brinon/game_of_life/blob/master/demos/long_thing_demo.gif)