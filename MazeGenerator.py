import random as rnd
from enum import Enum

rnd.seed()


class TileType(Enum):
    PATH = 1
    WALL = 2
    PLAYER = 3

PATHWIDTH = 2
WIDTH = 10
HEIGHT = 10
WALLCHAR = '#'
TILECHAR = ' '
PLAYERCHAR = '@'
DENSITY = 0.4
STARTLIFE = 10

#####################################################
#                LABYRINTH GENERATION               #
#####################################################
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
        elif tile == TileType.PLAYER:
            l.append(PLAYERCHAR)
            l.append(' ' * (multiplier - 1))
        else:
            l.append(WALLCHAR * multiplier)
        i += 1
    
    l.append('\n')
    return ''.join(l)


#####################################################
#               DEFINING ENTITIES                   #
#####################################################
class Entity():
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY
    
    def __str__(self):
        return f"Entity - x:{self.posX} y:{self.posY}"

class Player(Entity):
    char = '@'
    def __init__(self, posX, posY, life):
        super().__init__(posX, posY)
        self.life = life

    def __str__(self):
        return f"Player[{self.char}] - x:{self.posX} y:{self.posY} - LP:{self.life}"


#####################################################
#                    INITIALIZING                   #
#####################################################
def InitializeGame(width, height, density, startingLP):
    #Generate maze map
    maze = GenerateMaze(width, height, density)

    #Get valid initial coordinates for player by repeated tries.
    #Emulating a do-while loop
    while True:
        startX = rnd.randint(1, 2 * width - 1)
        startY = rnd.randint(1, 2 * height - 1)

        if maze[startX][startY] == TileType.PATH:
            break 

    #Valid starting coordinates found, initialize player
    #and update map
    player = Player(startX, startY, startingLP)
    maze[startX][startY] = TileType.PLAYER

    return (maze, player)


#####################################################
#                    MAIN SECTION                   #
#####################################################
def main():
    maze , player = InitializeGame(WIDTH, HEIGHT, DENSITY, STARTLIFE)
    render = RenderMaze(maze)
    print(render)


if __name__== "__main__":
    main()