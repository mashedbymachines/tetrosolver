import random

import piece
from field import Field, FieldConfig


class TetroConfig():

    def __init__(self):
        self.log = False
        self.fieldConfig = FieldConfig()
        random.seed(None)


class TetroSolver():

    def __init__(self, game, solverConfig):
        self.__field = Field(solverConfig.fieldConfig)
        self.__game = game
        self.__config = solverConfig

    def getGameScore(self):
        if self.__game.scoringCalculator is not None:
            return self.__game.scoringCalculator.scoring
        else:
            return self.__field.rowsCleared

    def check(self):
        res = True
        currentPiece = self.__game.piecePicker.getNewPiece()
        if currentPiece is not None:
            res = self.__addToBestPosition(currentPiece)
        return res

    def getField(self):
        return self.__field

    def __addToBestPosition(self, thePiece):

        bestField = None
        bestScore = 999999999
        bestRotation = 0
        bestPosition = 0
        bestColumnHeights = []


        for rotation in range(4):
            if rotation > 0 and thePiece.pieceType == piece.PieceType.O_SHAPE:
                # No need to check rotated O
                break
            if rotation > 1 and \
                    (thePiece.pieceType == piece.PieceType.I_SHAPE or
                     thePiece.pieceType == piece.PieceType.S_SHAPE or
                     thePiece.pieceType == piece.PieceType.Z_SHAPE):
                # No need to check more than 2 rotations for I, S, Z
                break
            thePiece.setRotation(rotation)
            for position in range(self.__field.WIDTH - thePiece.getWidth() + 1):
                score, field, height, clearedLines, columnHeights = self.__field.tryAddPiece(thePiece, position)
                if score < bestScore:
                    bestScore = score
                    bestRotation = rotation
                    bestPosition = position
                    bestField = field
                    bestHeight = height
                    bestClearedLines = clearedLines
                    bestColumnHeights = columnHeights

        if bestField == None:
            if self.__config.log:
                print("Found no place to add piece")
            return False

        if self.__config.log:
            print(f"Move piece to position {bestPosition} with rotation {bestRotation}")

        self.__field.validatePieceAdd(bestField, thePiece, bestRotation, bestHeight, bestClearedLines, bestColumnHeights)

        if bestHeight > Field.LOSE_HEIGHT:
            if self.__config.log:
                print(f"Height was too high({bestHeight}), game lost")
            return False

        if self.__game.outputManager is not None:
            self.__game.outputManager.output(bestRotation, bestPosition)

        if self.__game.scoringCalculator is not None:
            self.__game.scoringCalculator.updateSore(bestClearedLines)

        return True

