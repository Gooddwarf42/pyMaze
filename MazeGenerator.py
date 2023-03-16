import random as rnd
from enum import Enum

rnd.seed()


class TileType(Enum):
    PATH = 1
    WALL = 2

PATHWIDTH = 2
WIDTH = 10
HEIGHT = 10
WALLCHAR = '#'
TILECHAR = ' '
DENSITY = 0.4

def generateFullWallRow(length):
    """
    Generate a line full of the selected characters,
    allowing for a number of corridors passed as parameter.

    Parameters
    ----------
    length : int
        length of the row of characters to generate
    character : char
        character to fill the line with

    Returns
    -------
    line : str
        the full row
    """

    assert length > 0, "Length value must be > 0" 
    return [TileType.WALL] * (length * 2 + 1)


def generateRowTiles(length, density):
    """
    Generate a line of the maze, (odd lines)
    allowing for a number of corridors passed as parameter.
    Probability of a given tile to be a wall is given by the
    density parameter

    Parameters
    ----------
    length : int
        length of the maze row
    wallchar : char
        character used for walls

    Returns
    -------
    line : str
        the row of the maze
    """

    assert length > 0, "Length value must be > 0" 
    assert 0 <= density and density <= 1, "Invalid density parameter" 

    # if I remember correctly, appending with + is not a great idea
    # better create a list and then join it into a string
    l = []

    #left wall
    l.append(TileType.WALL)
    
    #inner columns
    for i in range(length - 1):
        draw = rnd.random()
        nextchar = TileType.WALL if draw < density else TileType.PATH
        l.append(TileType.PATH)
        l.append(nextchar)

    #ensure wall as the rightmost character
    l.append(TileType.PATH)
    l.append(TileType.WALL)

    return l

def generateRowWalls(length, density):
    """
    Generate a line of the maze, (even)
    allowing for a number of corridors passed as parameter.
    Probability of a given tile to be a wall is given by the
    density parameter

    Parameters
    ----------
    length : int
        length of the maze row
    wallchar : char
        character used for walls

    Returns
    -------
    line : str
        the row of the maze
    """

    assert length > 0, "Length value must be > 0" 
    assert 0 <= density and density <= 1, "Invalid density parameter" 

    l = []

    #left wall
    l.append(TileType.WALL)

    #rinner columns
    for i in range(length):      
        draw = rnd.random()
        nextchar = TileType.WALL if draw < density else TileType.PATH
        l.append(nextchar)
        l.append(TileType.WALL)
    
    #rightmost wall is already ensured

    return l

def GenerateMaze(width, height, density):
    #First row is full
    maze = [generateFullWallRow(width)]

    #Generate inner rows
    for i in range(height - 1):
        maze.append(generateRowTiles(width, density))
        maze.append(generateRowWalls(width, density))

    #Add Last Row
    maze.append(generateRowTiles(width, density))
    maze.append(generateFullWallRow(width))

    return maze

def RenderMaze(maze):
    mazeStr = []
    for line in maze:
        mazeStr.append(RenderMazeLine(line))
    return ''.join(mazeStr)

def RenderMazeLine(line):
    l = []
    # mimicking index
    i = 0
    for tile in line:
        multiplier = 2 if i % 2 == 1 else 1
        if tile == TileType.PATH:
            l.append(TILECHAR * multiplier) 
        else:
            l.append(WALLCHAR * multiplier)
        i += 1
    
    l.append('\n')
    return ''.join(l)

maze = GenerateMaze(WIDTH, HEIGHT, DENSITY)
render = RenderMaze(maze)
print(render)


"""
maze = []
str = generateFullRow(WIDTH, WALLCHAR)
maze.append(str)
for i in range(HEIGHT - 1):
    str = generateRowTiles(WIDTH, WALLCHAR, TILECHAR, CORRCHAR, DENSITY)
    maze.append(str)
    str = generateRowWalls(WIDTH, WALLCHAR, CORRCHAR, DENSITY)
    maze.append(str)

#last row
str = generateRowTiles(WIDTH, WALLCHAR, TILECHAR, CORRCHAR, DENSITY)
maze.append(str)
str = generateFullRow(WIDTH, WALLCHAR)
maze.append(str)


mazeStr = ''.join(maze)
print(mazeStr)
"""