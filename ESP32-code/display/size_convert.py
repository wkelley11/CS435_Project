# Python script to modify the display size of a given line of text.
# Input: a string, the factor by which to expand the text.

# An expansion factor of 2 would double the size of the text (4 times as many pixels occupied).
# An expansion factor of 0.5 would halve the size of the text (4 times fewer pixels occupied).

import main, ssd1306

# Returns True if structure is a matrix, False otherwise
def isMatrix(structure):
        try:
            matrixSize = len(structure[0])
            matrixBool = True
        except TypeError:
            matrixBool = False
        return matrixBool

# Input: a matrix of bytes, the expansion factor
# The function will display to screen a matrix of bytes as expanded by the factor,
# where each value in the matrix is a single pixel.
def createNewMatrix(bytes, factor):

    # Get output matrix dimensions
    numMatrixRows = len(bytes) * factor
    numMatrixCols = len(bytes) * factor

    # initialize the output matrix: set all values to 0
    matrix = [[0 for i in range(numMatrixRows)] for j in range(numMatrixCols)]

    # either bytes is multiple bits, or it's not.
    if(isMatrix(bytes)):
        # For every array in bytes
        for array in bytes:
            # iterate over each bit in original byte array
            for i in range(len(bytes)):
                currentBitVal = bytes[i] # get the currently-considered-bit's value (0 or 1)
                for row in range(factor):
                    for col in range(factor):
                        matrix[(i * factor) + row][col] = currentBitVal

    else: # same code, just without looping over multiple arrays (only one)
        # iterate over each bit in original byte array
        for i in range(len(bytes)):
            currentBitVal = bytes[i] # get the currently considered bit's value (0 or 1)
            for row in range(factor):
                for col in range(factor):
                    matrix[(i * factor) + row][col] = currentBitVal

    return matrix



# Input:
# - the matrix, which is the newly expanded 'bytes' matrix
# - x coordinate of top left pixel
# - y coordinate of top right pixel
def matrixToScreen(oled, matrix, x, y):
    # Iterate through the matrix, printing its contents to screen
    for x_row in range(len(matrix)): # iterate over all the matrix's rows

        for y_column in range(len(matrix[0])): # iterate over each val in the row
            pixVal = matrix[x_row][y_column] # 1 or 0
            oled.pixel(x, y, pixVal)    # display corresponding pixel value (1 or 0)
            oled.show()                 # show
            # print("x: " + str(x) + "\n")
            # print("y: " + str(y) + "\n")
            # print("value: " + str(pixVal) + "\n")
            y += 1     # increment y position

        x += 1         # increment x position

# Input:
# - an array (or matrix) bytes
# - the factor by which to expand the size of the message
# - the x and y coordinates of the top left pixel where to display on oled
# Displays the message to screen, as expanded in size by factor.
def convertText(oled, bytes, factor, x, y):
    matrix = createNewMatrix(bytes, factor) # get the newly sized matrix
    matrixToScreen(oled, matrix, x, y)      # display it to the oled
