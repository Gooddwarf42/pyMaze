import random as rnd

rnd.seed()

WIDTH = 10
HEIGHT = 10
WALLCHAR = '#'
CORRCHAR = ' '
TILECHAR = ' '
DENSITY = 0.4

def generateFullRow(length, wallcharacter):
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

    # if I remember correctly, appending with + is not a great idea
    # better create a list and then join it into a string
    l = []

    #left wall
    l.append(wallcharacter)
    #room for corridors
    for i in range(length):
        #tile space
        l.append(wallcharacter)
        l.append(wallcharacter)
        #wall space
        l.append(wallcharacter)
    #right wall
    #l.append(wallcharacter)

    #append neLine
    l.append('\n')

    return ''.join(l)

def generateRowTiles(length, wallchar, tilechar, corrchar, density):
    """
    Generate a line of the maze,
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
    l.append(wallchar)
    #room for corridors
    for i in range(length -1):
        l.append(tilechar)
        l.append(tilechar)
        
        draw = rnd.random()
        nextchar = wallchar if draw < density else corrchar
        l.append(nextchar)

    #ensure wall as the rightmost character
    l.append(tilechar)
    l.append(tilechar)
    l.append(wallchar)

    #append neLine
    l.append('\n')

    return ''.join(l)

def generateRowWalls(length, wallchar, corrchar, density):
    """
    Generate a line of the maze,
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
    l.append(wallchar)
    #room for corridors
    for i in range(length):      
        draw = rnd.random()
        nextchar = wallchar if draw < density else corrchar
        l.append(nextchar)
        l.append(nextchar)

        l.append(wallchar)
    #right wall
    #l.append(wallcharacter)

    #append neLine
    l.append('\n')

    return ''.join(l)


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
