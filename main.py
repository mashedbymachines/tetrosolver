import threading
import time
import pyautogui

import gametype
from fieldpainter import FieldPainter
from outputmanager import PrintOutputManager
from piecepicker import InputPiecePicker, AutoPiecePicker
from scoringcalculator import IngoScoringCalculator
from tetrisgame import TetrisGame
from tetrosolver import TetroSolver, TetroConfig

__exit = False
__timeToDraw = False

SLOWNESS = 0.00

def colorPicker():
    global __exit
    while not __exit:
        currentPos = pyautogui.position()
        currentColor = pyautogui.pixel(currentPos.x, currentPos.y)
        print(f"Color at mouse: {currentColor}")
        time.sleep(0.5)


def tetroSolver(solver):
    global __timeToDraw
    global __exit
    while not __exit:
        if not solver.check():
            __exit = True
        __timeToDraw = True
        time.sleep(SLOWNESS)

if __name__ == "__main__":
    mode = pyautogui.confirm(text='Tetrosolver', title='Select mode', buttons=['REAL', 'MANUAL', 'AUTO'])

    tetrisorigin = None
    outputManager = None
    replay = True
    gameType = gametype.GameType.INGO
    game = None
    if mode == "REAL":
        selectedGame = pyautogui.confirm(text='Tetrosolver', title='Select game', buttons=['INGO', 'LUMPTY', 'JSTRIS'])
        if selectedGame == "INGO":
            gameType = gametype.GameType.INGO
        elif selectedGame == "JSTRIS":
            gameType = gametype.GameType.JSTRIS
        else:
            gameType = gametype.GameType.LUMPTY
        game = TetrisGame(gameType)
    else:
        game = TetrisGame()
        if mode == "MANUAL":
            game.piecePicker = InputPiecePicker()
            game.outputManager = PrintOutputManager()
        else:
            SLOWNESS = 0.1
            game.piecePicker = AutoPiecePicker()
            game.scoringCalculator = IngoScoringCalculator()

    fieldPainter = FieldPainter(gameType)

    while replay:
        solverConfig = TetroConfig()
        #solverConfig.log = True
        #solverConfig.fieldConfig.log = True
        solverConfig.fieldConfig.FLAT_FACTOR = 1.1720148713567564
        solverConfig.fieldConfig.HOLE_FACTOR = 5.312056910769751
        solverConfig.fieldConfig.HEIGHT_FACTOR = 0.1765673301273726
        solverConfig.fieldConfig.LINE_FACTOR = 1.4106621037891096
        #solverConfig.fieldConfig.HEIGHT_FACTOR_HIGH_LIMIT = (2 * Field.HEIGHT) / 3
        #solverConfig.fieldConfig.HEIGHT_FACTOR_HIGH = solverConfig.fieldConfig.HEIGHT_FACTOR * 2
        solver = TetroSolver(game, solverConfig)

        runThread = threading.Thread(target=tetroSolver, args=[solver])
        #runThread = threading.Thread(target=colorPicker)
        runThread.start()

        while (not __exit) or __timeToDraw:
            if __timeToDraw:
                __timeToDraw = False
                fieldPainter.paintField(solver.getField(), solver.getGameScore())


        __exit = True
        runThread.join()

        retry = pyautogui.confirm(text=f"Game over: score was {solver.getField().rowsCleared}", title='Finished', buttons=['RERUN', 'EXIT'])
        if retry == "EXIT":
            replay = False
        else:
            __exit = False



