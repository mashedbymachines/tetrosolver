import threading
import time

import pyautogui

from piecepicker import AutoPiecePicker, SequentialPiecePicker
from tetrisgame import TetrisGame, GameType
from tetrosolver import TetroSolver, TetroConfig

from pycallgraph2 import PyCallGraph
from pycallgraph2.output import GraphvizOutput

__exit = False

PROFILING = False
if PROFILING:
    PERFORMANCE_PIECES = 1000
else:
    PERFORMANCE_PIECES = 10000
COMPARE_TIME = 4.273208379745483
# First time: 12.4905264377594

def testPerformanceMethod(solver):
    global __exit
    global PROFILING
    pieces = 0
    startTime = time.time()
    percentageCheck = PERFORMANCE_PIECES / 20

    if PROFILING:
        with PyCallGraph(output=GraphvizOutput()):
            while True:
                if pieces % percentageCheck == 0:
                    print(f"{100 * (pieces / PERFORMANCE_PIECES)} %")
                if __exit:
                    break
                if pieces >= PERFORMANCE_PIECES:
                    break
                if not solver.check():
                    break
                pieces += 1
    else:
        while True:
            if pieces % percentageCheck == 0:
                print(f"{100 * (pieces / PERFORMANCE_PIECES)} %")
            if __exit:
                break
            if pieces >= PERFORMANCE_PIECES:
                break
            if not solver.check():
                break

            pieces += 1

    endTime = time.time()
    print(f"Finished performance test with pieces: {PERFORMANCE_PIECES}")
    print(f"Rows cleared: {solver.getGameScore()}")
    print(f"Time: {endTime - startTime}")
    print(f"Compare time: {COMPARE_TIME}")

def performanceThread():
    global __exit

    game = TetrisGame()
    game.piecePicker = SequentialPiecePicker()

    solverConfig = TetroConfig()
    solverConfig.log = False
    solverConfig.fieldConfig.log = False
    solverConfig.fieldConfig.FLAT_FACTOR = 1.1228687283916032
    solverConfig.fieldConfig.HOLE_FACTOR = 5.193397373397724
    solverConfig.fieldConfig.HEIGHT_FACTOR = 0.16380901479600363
    solverConfig.fieldConfig.LINE_FACTOR = 1.2577257145153835

    solver = TetroSolver(game, solverConfig)
    testPerformanceMethod(solver)

if __name__ == "__main__":

    runThread = threading.Thread(target=performanceThread)
    runThread.start()

    if PROFILING:
        pyautogui.alert(text=f"Click here to quit profiling", title='Performance test',
                        button='Exit')
        __exit = True

    runThread.join()



