import random as rnd
from enum import Enum

rnd.seed()


class TileType(Enum):
    UNDEFINED = 0
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
    #assigning a default TileType
    typ = TileType.UNDEFINED

    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY
    
    def __str__(self):
        return f"Entity - x:{self.posX} y:{self.posY}"
    
    def MoveUp(self, maze):
        '''
        Moves the entity up in the passed maze.
        Returns the type of the tile in which the entity tried to move.
        '''
        destTile = maze[self.posY - 1][self.posX]
        if destTile == TileType.PATH:
            #Move the entity only if the next tile is free
            #Free the current tile
            maze[self.posY][self.posX] = TileType.PATH
            #update position
            self.posY -= 1
            #update the new tile
            maze[self.posY][self.posX] = self.typ
        return maze, destTile
            

class Player(Entity):
    typ = TileType.PLAYER
    def __init__(self, posX, posY, life):
        super().__init__(posX, posY)
        self.life = life

    def __str__(self):
        return f"{self.typ} - x:{self.posX} y:{self.posY} - LP:{self.life}"


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

        if maze[startY][startX] == TileType.PATH:
            break 

    #Valid starting coordinates found, initialize player
    #and update map
    player = Player(startX, startY, startingLP)
    maze[startY][startX] = TileType.PLAYER

    return (maze, player)

#####################################################
#              COMMAND MANAGEMENT                   #
#####################################################
def Execute(command, maze, player):
    #move up
    if command == "w":
        maze, destTile = player.MoveUp(maze)
        render = RenderMaze(maze)
        print(render)
    #move left
    elif command == "a":
        print("moving left...")
    #move down
    elif command == "s":
        print("moving down...")
    #move right
    elif command == "d":
        print("moving right...")
    else:
        print("unknown command!")

    return maze, player


#####################################################
#                    MAIN SECTION                   #
#####################################################
def main():
    print("Welcome to this simple maze!")
    print("Type the commands w-a-s-d to move your character")
    print("Type \"exit\" to terminate the execution.")
    print("Initializing game...")

    maze , player = InitializeGame(WIDTH, HEIGHT, DENSITY, STARTLIFE)
    render = RenderMaze(maze)
    print(render)

    while True:
        command = input("What to do?")
        if command == "exit":
            break
        maze, player = Execute(command, maze, player)


if __name__== "__main__":
    main()