import random as rnd
from enum import Enum

rnd.seed()


class TileType(Enum):
    UNDEFINED = 0
    PATH = 1
    WALL = 2
    PLAYER = 3
    MONSTER = 4


PATHWIDTH = 2
WIDTH = 10
HEIGHT = 10
WALLCHAR = '#'
TILECHAR = ' '
PLAYERCHAR = '@'
MONSTERCHAR = 'M'
DENSITY = 0.4
STARTLIFE = 10
STARTMONSTERLIFE = 4
NUMMONSTERS = 3

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

    # left wall
    l.append(TileType.WALL)

    # inner columns
    for i in range(width - 1):
        draw = rnd.random()
        nextchar = TileType.WALL if draw < density else TileType.PATH
        l.append(TileType.PATH)
        l.append(nextchar)

    # ensure wall as the rightmost character
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

    # left wall
    l.append(TileType.WALL)

    # rinner columns
    for i in range(length):
        draw = rnd.random()
        nextchar = TileType.WALL if draw < density else TileType.PATH
        l.append(nextchar)
        l.append(TileType.WALL)

    # rightmost wall is already ensured

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
    # First row is full
    maze = [GenerateFullWallRow(width)]

    # Generate inner rows
    for i in range(height - 1):
        maze.append(GenerateRowOdd(width, density))
        maze.append(GenerateRowEven(width, density))

    # Add Last Row
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
        elif tile == TileType.MONSTER:
            l.append(MONSTERCHAR)
            l.append(' ' * (multiplier - 1))
        else:
            l.append(WALLCHAR * multiplier)
        i += 1

    l.append('\n')
    return ''.join(l)

#####################################################
#               VARIOUS MAZE FUNCTIONS              #
#  TODO: maaybe make a maze class sooner or later   #
#####################################################


def GetMazeWidth(maze):
    '''
    Returns the total number of columns of the maze,
    outer walls included
    '''
    return len(maze)


def GetMazeHeight(maze):
    '''
    Returns the total number of rows of the maze,
    outer walls included
    '''
    return len(maze[0])


def IsCoordinateInBound(maze, x, y):
    '''
    Returns true if the coordinates are in the maze,
    outer walls included
    '''
    totalRows = GetMazeWidth(maze)
    totalCols = GetMazeHeight(maze)

    return (0 <= x
            and x <= totalCols - 1
            and 0 <= y
            and y <= totalRows - 1)


def GenerateInternalCoordinate(maze):
    '''
    Generates random coordinates in the internal of
    the maze (outer walls excluded)
    '''
    totalRows = GetMazeWidth(maze)
    totalCols = GetMazeHeight(maze)
    genX = rnd.randint(1, totalCols - 2)
    genY = rnd.randint(1, totalRows - 2)
    return genX, genY

    #####################################################
    #               DEFINING ENTITIES                   #
    #####################################################


class Entity():
    # assigning a default TileType
    typ = TileType.UNDEFINED

    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY

    def __str__(self):
        return f"Entity - x:{self.posX} y:{self.posY}"

    def MoveTo(self, maze, destX, destY):
        '''
        Moves the entity in a precise coordinate in the passed maze.
        Returns
        -------
        destTile : TileType
          the type of the tile in which the entity tried to move.
        '''

        # Check if destination tile is valid
        if not IsCoordinateInBound(maze, destX, destY):
            print("Invalid movement!")
            destTile = maze[self.posY][self.posX]
            return destTile

        destTile = maze[destY][destX]
        if destTile == TileType.PATH:
            # Move the entity only if the next tile is free
            # Free the current tile
            maze[self.posY][self.posX] = TileType.PATH
            # update position
            self.posX = destX
            self.posY = destY
            # update the new tile
            maze[self.posY][self.posX] = self.typ
        return destTile

    def MoveRel(self, maze, movX, movY):
        '''
        Moves the entity in the passed maze horizontally and vertically
        of the given amount of tiles.
        Returns
        -------
        destTile : TileType
          the type of the tile in which the entity tried to move.
        '''
        destX = self.posX + movX
        destY = self.posY + movY

        # Check if the movement is safe is done in the
        # MoveTo function!

        destTile = self.MoveTo(maze, destX, destY)
        return destTile, destX, destY


class Player(Entity):
    typ = TileType.PLAYER

    def __init__(self, posX, posY, life):
        super().__init__(posX, posY)
        self.life = life

    def __str__(self):
        return f"{self.typ} - x:{self.posX} y:{self.posY} - LP:{self.life}"

    def GetsHit(self):
        self.life -= 1


class Monster(Entity):
    typ = TileType.MONSTER

    def __init__(self, posX, posY, life):
        super().__init__(posX, posY)
        self.life = life

    def __str__(self):
        return f"{self.typ} - x:{self.posX} y:{self.posY} - LP:{self.life}"

    def GetsHit(self):
        self.life -= 1


#####################################################
#                    INITIALIZING                   #
#####################################################
def InitializeGame(width, height, density, startingLP, numMonsters, monsterStartLP):
    # Generate maze map
    maze = GenerateMaze(width, height, density)

    # Get valid initial coordinates for player by repeated tries.
    (startX, startY) = GetFreeCoordinates(maze)

    # Valid starting coordinates found, initialize player
    # and update map
    player = Player(startX, startY, startingLP)
    maze[startY][startX] = TileType.PLAYER

    # Generate Monsters
    monsters = []

    for i in range(numMonsters):
        (startX, startY) = GetFreeCoordinates(maze)
        monster = Monster(startX, startY, monsterStartLP)
        maze[startY][startX] = TileType.MONSTER
        monsters.append(monster)

    return (maze, player, monsters)


def GetFreeCoordinates(maze):
    # Emulating a do-while loop
    while True:
        startX, startY = GenerateInternalCoordinate(maze)

        if maze[startY][startX] == TileType.PATH:
            break

    return startX, startY

#####################################################
#              COMMAND MANAGEMENT                   #
#####################################################


def Execute(command, maze, player, monsters):
    # move up
    if command == "w":
        destTile, destX, destY = player.MoveRel(maze, 0, -1)
    # move left
    elif command == "a":
        destTile, destX, destY = player.MoveRel(maze, -1, 0)
    # move down
    elif command == "s":
        destTile, destX, destY = player.MoveRel(maze, 0, 1)
    # move right
    elif command == "d":
        destTile, destX, destY = player.MoveRel(maze, 1, 0)
    else:
        print("unknown command!")
        return

    if destTile == TileType.MONSTER:
        print("Oh, a monster!")
        for monster in monsters:
            if monster.posX == destX and monster.posY == destY:
                monster.GetsHit()
                KillMonsterIfNeeded(monsters, monster, maze)


def KillMonsterIfNeeded(monsters, monster, maze):
    if monster.life <= 0:
        print("You killed a monster!")
        monsters.remove(monster)
        print(f"There are {len(monsters)} monsters remaining!")
        maze[monster.posY][monster.posX] = TileType.PATH


#####################################################
#                    MAIN SECTION                   #
#####################################################
def main():
    print("Welcome to this simple maze!")
    print("Type the commands w-a-s-d to move your character")
    print("Type \"exit\" to terminate the execution.")
    print("Initializing game...")

    maze, player, monsters = InitializeGame(
        WIDTH, HEIGHT, DENSITY, STARTLIFE, NUMMONSTERS, STARTMONSTERLIFE)
    render = RenderMaze(maze)
    print(render)

    while True:
        command = input("What to do?")
        if command == "exit":
            break

        Execute(command, maze, player, monsters)
        print(RenderMaze(maze))

        if player.life <= 0:
            print("Player is dead! Game Over!")
            break

        if len(monsters) <= 0:
            print("All monsters are dead! You Win!")
            break


if __name__ == "__main__":
    main()
