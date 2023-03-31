import random

import pyautogui

import piece
from gametype import GameType


class PiecePicker():
    
    def __init__(self, gameType):
        self._gameType = gameType

    def getNewPiece(self):
        assert False, "Not Implemented"


class GameColorPiecePicker(PiecePicker):

    def __init__(self, gameType):
        super().__init__(gameType)
        self.__readyForNext = True
        self.__gameType = gameType
        pyautogui.alert(text='Move mouse to where tetris pieces will appear and press Enter', title='Welcome',
                        button='OK')
        tetrisorigin = pyautogui.position()
        self.__origin = tetrisorigin

    def getNewPiece(self):
        currentPiece = None
        currentColor = pyautogui.pixel(self.__origin.x, self.__origin.y)
        #print(f"Color at origin: {currentColor}")
        if self.__readyForNext:
            if piece.isValidPieceColor(currentColor, self.__gameType):
                currentPiece = piece.createPieceFromColor(currentColor, self.__gameType)
                print(f"Detected piece: {currentPiece}")
                #self.__readyForNext = False
        else:
            #Wait for background again
            currentColor = pyautogui.pixel(self.__origin.x, self.__origin.y)
            if not piece.isValidPieceColor(currentColor, self.__gameType):
                self.__readyForNext = True

        return currentPiece

class InputPiecePicker(PiecePicker):
    
    def __init__(self, gameType=GameType.INGO):
        super().__init__(gameType)

    def getNewPiece(self):
        print("Add new piece by letter:")
        try:
            inputList = list(input())
            if len (inputList) > 0:
                currentPiece = piece.createPieceFromLetter(inputList[0], self._gameType)
                print(f"Selected piece: {currentPiece}")

                return currentPiece
            else:
                return None
        except ValueError:
            return None

class AutoPiecePicker(PiecePicker):

    def __init__(self, gameType=GameType.INGO):
        super().__init__(gameType)

    def getNewPiece(self):
        randomType = random.randint(0, 6)
        currentPiece = piece.createPieceFromType(randomType, self._gameType)
        return currentPiece


class SequentialPiecePicker(PiecePicker):

    def __init__(self, gameType=GameType.INGO):
        super().__init__(gameType)
        self.__nextPiece = 0

    def getNewPiece(self):
        currentPiece = piece.createPieceFromType( self.__nextPiece, self._gameType)
        if self.__nextPiece == 6:
            self.__nextPiece = 0
        else:
            self.__nextPiece += 1

        return currentPiece
