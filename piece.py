from enum import IntEnum

from Pieces import INGOpieces, JSTRISpieces, LUMPTYpieces
from gametype import GameType


class PieceType(IntEnum):
    I_SHAPE = 0
    L_SHAPE = 1
    J_SHAPE = 2
    O_SHAPE = 3
    S_SHAPE = 4
    Z_SHAPE = 5
    T_SHAPE = 6


pieceColorMap = {GameType.INGO: INGOpieces.pieceColors,
                 GameType.JSTRIS: JSTRISpieces.pieceColors,
                 GameType.LUMPTY: LUMPTYpieces.pieceColors}

filledCellsMap = {GameType.INGO:
                      {PieceType.I_SHAPE: INGOpieces.filledCellsI,
                       PieceType.L_SHAPE: INGOpieces.filledCellsL,
                       PieceType.J_SHAPE: INGOpieces.filledCellsJ,
                       PieceType.O_SHAPE: INGOpieces.filledCellsO,
                       PieceType.S_SHAPE: INGOpieces.filledCellsS,
                       PieceType.Z_SHAPE: INGOpieces.filledCellsZ,
                       PieceType.T_SHAPE: INGOpieces.filledCellsT},
                  GameType.JSTRIS:
                      {PieceType.I_SHAPE: JSTRISpieces.filledCellsI,
                       PieceType.L_SHAPE: JSTRISpieces.filledCellsL,
                       PieceType.J_SHAPE: JSTRISpieces.filledCellsJ,
                       PieceType.O_SHAPE: JSTRISpieces.filledCellsO,
                       PieceType.S_SHAPE: JSTRISpieces.filledCellsS,
                       PieceType.Z_SHAPE: JSTRISpieces.filledCellsZ,
                       PieceType.T_SHAPE: JSTRISpieces.filledCellsT},
                  GameType.LUMPTY:
                      {PieceType.I_SHAPE: LUMPTYpieces.filledCellsI,
                       PieceType.L_SHAPE: LUMPTYpieces.filledCellsL,
                       PieceType.J_SHAPE: LUMPTYpieces.filledCellsJ,
                       PieceType.O_SHAPE: LUMPTYpieces.filledCellsO,
                       PieceType.S_SHAPE: LUMPTYpieces.filledCellsS,
                       PieceType.Z_SHAPE: LUMPTYpieces.filledCellsZ,
                       PieceType.T_SHAPE: LUMPTYpieces.filledCellsT}
                  }

pieceStrings = ["I", "L", "J", "O", "S", "Z", "T"]


def getColorForCell(theCell, gameType):
    color = pieceColorMap[gameType][theCell]
    return color


def isValidPieceColor(rgb, gameType):
    return rgb in pieceColorMap[gameType]


def createPieceFromColor(rgb, gameType):
    if isValidPieceColor(rgb, gameType):
        pieceType = pieceColorMap[gameType].index(rgb)
        return Piece(pieceType, gameType)
    else:
        return None


def createPieceFromType(type, gameType):
    if 0 <= type <= 6:
        return Piece(type, gameType)
    else:
        return None


def createPieceFromLetter(letter, gameType):
    if letter in pieceStrings:
        type = pieceStrings.index(letter)
        return Piece(type, gameType)
    else:
        return None


class Piece:
    WIDTH = 4
    HEIGHT = 4

    def __init__(self, type, gameType):
        assert 0 <= type <= 6, "Invalid piece type"
        self.gameType = gameType
        self.pieceType = type
        self.color = pieceColorMap[self.gameType][type]
        self.setRotation(0)

    def __str__(self):
        if self.pieceType is None:
            return "INVALID"
        else:
            return pieceStrings[self.pieceType]

    def setRotation(self, rotation):
        assert rotation < 4
        self.rotation = rotation
        self.cells = filledCellsMap[self.gameType][self.pieceType][self.rotation]

    #TODO fix for games with other rotations
    def getWidth(self):
        if self.pieceType == PieceType.O_SHAPE:
            return 2
        elif self.pieceType == PieceType.L_SHAPE or \
                self.pieceType == PieceType.J_SHAPE or \
                self.pieceType == PieceType.S_SHAPE or \
                self.pieceType == PieceType.Z_SHAPE or \
                self.pieceType == PieceType.T_SHAPE:
            if self.rotation == 0 or self.rotation == 2:
                return 3
            else:
                return 2
        elif self.pieceType == PieceType.I_SHAPE:
            if self.rotation == 0 or self.rotation == 2:
                return 4
            else:
                return 1

    # TODO fix for games with other rotations
    def getHeight(self):
        if self.pieceType == PieceType.O_SHAPE:
            return 2
        elif self.pieceType == PieceType.L_SHAPE or \
                self.pieceType == PieceType.J_SHAPE or \
                self.pieceType == PieceType.S_SHAPE or \
                self.pieceType == PieceType.Z_SHAPE or \
                self.pieceType == PieceType.T_SHAPE:
            if self.rotation == 0 or self.rotation == 2:
                return 2
            else:
                return 3
        elif self.pieceType == PieceType.I_SHAPE:
            if self.rotation == 0 or self.rotation == 2:
                return 1
            else:
                return 4


