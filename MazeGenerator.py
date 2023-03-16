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

def GenerateFullWallRow(width):
    """
    Generate a line full walls.

    Parameters
    ----------
    width : int
        width of the labyrinth in which the wall then fits

    Returns
    -------
    line : List<TileType>
        a list of TileTypes full of wall blocks of the appropriate length for a
        labyrinth of the given width
    """

    assert width > 0, "Width value must be > 0" 
    return [TileType.WALL] * (width * 2 + 1)


def GenerateRowOdd(width, density):
    """
    Generate a line of the maze, (odd lines),
    which have paths in all odd spots and possibly
    walls in even spots.
    Chance of having walls is determined by the density parameter.

    Parameters
    ----------
    width : int
        width of the maze row
    density : float
        density of the walls. Must be between 0 and 1.

    Returns
    -------
    line : List<TileType>
        a list of TileTypes describind an odd row of the labyrinth
    """

    assert width > 0, "Width value must be > 0" 
    assert 0 <= density and density <= 1, "Invalid density parameter" 

    # if I remember correctly, appending with + is not a great idea
    # better create a list and then join it into a string
    l = []

    #left wall
    l.append(TileType.WALL)
    
    #inner columns
    for i in range(width - 1):
        draw = rnd.random()
        nextchar = TileType.WALL if draw < density else TileType.PATH
        l.append(TileType.PATH)
        l.append(nextchar)

    #ensure wall as the rightmost character
    l.append(TileType.PATH)
    l.append(TileType.WALL)

    return l

def GenerateRowEven(length, density):
    """
    Generate a line of the maze, (even)
    Which has walls in all even spots and possibly
    walls in the even spots.
    Chance of having walls is determined by the density parameter.

    Parameters
    ----------
    width : int
        width of the maze row
    density : float
        density of the walls. Must be between 0 and 1.

    Returns
    -------
    line : List<TileType>
        a list of TileTypes describind an even row of the labyrinth
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
    """
    Generates a maze.

    Parameters
    ----------
    width : int
        width of the maze
    height : int
        height of the maze
    density : float
        density of the walls. Must be between 0 and 1.

    Returns
    -------
    maze : List<List<TileType>>
        matrix of TileTypes describing the labyrinth
    """
    #First row is full
    maze = [GenerateFullWallRow(width)]

    #Generate inner rows
    for i in range(height - 1):
        maze.append(GenerateRowOdd(width, density))
        maze.append(GenerateRowEven(width, density))

    #Add Last Row
    maze.append(GenerateRowOdd(width, density))
    maze.append(GenerateFullWallRow(width))

    return maze

def RenderMaze(maze):
    """
    Converts a matrix describing a maze into a string
    """
    mazeStr = []
    for line in maze:
        mazeStr.append(RenderMazeLine(line))
    return ''.join(mazeStr)

def RenderMazeLine(line):
    """
    Converts a list describing a maze row into a string, ended by a newline.
    """
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