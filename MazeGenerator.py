WIDTH = 10
HEIGHT = 10
WALLCHAR = '#'
CORRCHAR = ' '

def generateFullRow(length, character):
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
    l.append(character)
    #room for corridors
    for i in range(length):
        l.append(character)
    #righ wall
    l.append(character)

    return ''.join(l)

str = generateFullRow(WIDTH, WALLCHAR)
print(str)
