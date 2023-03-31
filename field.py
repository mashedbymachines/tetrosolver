from cell import CLEARED_CELL
from piece import Piece


class FieldConfig():

    def __init__(self):
        self.log = False
        self.HOLE_FACTOR = 0
        self.HEIGHT_FACTOR = 0
        self.HEIGHT_FACTOR_HIGH = 0
        self.HEIGHT_FACTOR_HIGH_LIMIT = 0
        self.FLAT_FACTOR = 0
        self.LINE_FACTOR = 0

class Field():
    HEIGHT = 22
    WIDTH = 10
    LOSE_HEIGHT = HEIGHT - 4

    def __init__(self, fieldConfig):
        self.field = [[CLEARED_CELL for j in range(Field.WIDTH)] for i in range(Field.HEIGHT)]
        self.currentHeight = 0
        self.lastPieceAdded = None
        self.rowsCleared = 0
        self.config = fieldConfig
        self.__columnHeights = [0] * Field.WIDTH

    def __checkLines(self, real, startHeight):
        clearedLines = 0
        self.__lastLinesSolved = 0
        filledRows = []
        # Find the filled in rows

        for y in range(startHeight, Field.HEIGHT):
            filledRow = True
            for cell in self.field[y]:
                if cell == CLEARED_CELL:
                    filledRow = False
                    break
            if filledRow:
                filledRows.append(y)

        # Remove filed in lines, from top
        for filledRow in filledRows:
            self.__lastLinesSolved += 1
            clearedLines += 1
            del self.field[filledRow]
            self.field.insert(0, [CLEARED_CELL] * Field.WIDTH)

        return clearedLines

    def __checkCollision(self, thePiece, position, depth):

        for cell in thePiece.cells:
            x = cell[0]
            y = cell[1]
            if depth + y >= Field.HEIGHT:
                return True
            if position + x >= Field.WIDTH:
                continue
            if self.field[depth + y][position + x] != CLEARED_CELL:
                return True
        return False


    def __addPieceInternal(self, real, thePiece, position):
        modifiedColumns = [False] * Field.WIDTH

        # Find  depth before collision, start checking from first possible height
        startHeight = max(0, (Field.HEIGHT - 1 - self.currentHeight - Piece.HEIGHT))
        for depth in range(startHeight, Field.HEIGHT):
            if self.__checkCollision(thePiece, position, depth):
                lastDepth = depth - 1
                break

        # Fill the spot by the piece
        for cell in thePiece.cells:
            y = cell[1]
            x = cell[0]
            self.field[lastDepth + y][position + x] = thePiece.pieceType
            modifiedColumns[position + x] = True

        # Clear filled lines
        clearedLines = self.__checkLines(real, Field.HEIGHT - (thePiece.getHeight() + self.currentHeight))
        if clearedLines > 0:
            modifiedColumns = [True] * Field.WIDTH

        return modifiedColumns, clearedLines

    def tryAddPiece(self, thePiece, position):
        # Try to add piece here and calculate score of field
        self.__originalField = [row[:] for row in self.field]
        modifiedColumns, clearedLines = self.__addPieceInternal(False, thePiece, position)
        score, maxHeight, columnHeights = self.__calculateScore(modifiedColumns)
        newField = self.field
        self.field = self.__originalField
        return score, newField, maxHeight, clearedLines, columnHeights

    def validatePieceAdd(self, field, thePiece, bestRotation, height, clearedLines, columnHeights):
        self.field = field
        thePiece.setRotation(bestRotation)
        self.lastPieceAdded = thePiece
        self.currentHeight = height
        self.rowsCleared += clearedLines
        self.__columnHeights = columnHeights

    def __calculateScore(self, modifiedColumns, real=False):
        # Lowest amount of empty cells under filled cell
        # Lowest height in general
        # Lowest difference between low and high point
        score = 0
        maxHeight, bumpiness, columnHeights = self.__getBumpiness(modifiedColumns)
        score += bumpiness * self.config.FLAT_FACTOR

        holes = self.__getNumberOfHoles(maxHeight)
        score += holes * self.config.HOLE_FACTOR
        #maxHeight = self.__getTotalHeight()

        if self.config.HEIGHT_FACTOR_HIGH_LIMIT > 0 and maxHeight > self.config.HEIGHT_FACTOR_HIGH_LIMIT:
            score += maxHeight * self.config.HEIGHT_FACTOR_HIGH
        else:
            score += maxHeight * self.config.HEIGHT_FACTOR

        # Always avoid moves that loses at all costs
        if maxHeight == Field.LOSE_HEIGHT:
            score += 10000
        elif maxHeight > Field.LOSE_HEIGHT:
            score += 50000

        lines = self.__lastLinesSolved
        score -= lines * self.config.LINE_FACTOR

        return score, maxHeight, columnHeights

    def __getNumberOfHoles(self, maxHeight):
        holes = 0
        startHeight = Field.HEIGHT - maxHeight
        #Check columns from max height to last row,
        # count holes under filled cells

        for x in range(Field.WIDTH):
            startCounting = False
            for y in range(startHeight, Field.HEIGHT - 1):
                if self.field[y][x] != CLEARED_CELL:
                    startCounting = True
                elif startCounting:
                    holes += 1

        return holes

    def __getBumpiness(self, modifiedColumns):
        columnHeights = self.__calculateColumnHeights(modifiedColumns)
        bumpiness = 0
        for i, h in enumerate(columnHeights):
            if i == 0:
                continue
            bumpiness += abs(columnHeights[i-1] - h)

        maxHeight = max(columnHeights)
        return maxHeight, bumpiness, columnHeights


    def __calculateColumnHeights(self, modifiedColumns):
        columnHeights = self.__columnHeights[:]
        for x in range(Field.WIDTH):

            #Skip unmodified columns
            if not modifiedColumns[x]:
                continue

            for y in range(Field.HEIGHT):

                if self.field[y][x] != CLEARED_CELL:
                    columnHeights[x] = Field.HEIGHT - y
                    break
        return columnHeights
