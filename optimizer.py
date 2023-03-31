import random
import threading
import time
from multiprocessing import Process, Queue
from copy import deepcopy

import pyautogui

from field import Field
from piecepicker import AutoPiecePicker
from scoringcalculator import IngoScoringCalculator
from tetrisgame import TetrisGame, GameType
from tetrosolver import TetroSolver, TetroConfig

from pycallgraph2 import PyCallGraph
from pycallgraph2.output import GraphvizOutput

__exit = False

def testPerformanceMethod(solver):
    global __exit
    with PyCallGraph(output=GraphvizOutput()):
        while True:
            if __exit:
                break
            if not solver.check():
                break
    print(f"Finished perf test with score {solver.getField().rowsCleared}")

OPTIMIZE_LINES = False
def testThread(solver, results, id):
    global __exit
    global OPTIMIZE_LINES
    while True:
        if __exit:
            break
        if not solver.check():
            break
    if OPTIMIZE_LINES:
        print(f"Finished thread {id} with lines {solver.getField().rowsCleared}")
        results.put(solver.getField().rowsCleared)
    else:
        print(f"Finished thread {id} with score {solver.getGameScore()}")
        results.put(solver.getGameScore())




def optimizerThread():
    global __exit

    geneticLoop = 0

    outputManager = None
    game = TetrisGame()
    game.piecePicker = AutoPiecePicker()
    game.scoringCalculator = IngoScoringCalculator()


    solverConfig = TetroConfig()
    solverConfig.log = False
    solverConfig.fieldConfig.log = False

    solverConfig.fieldConfig.FLAT_FACTOR = 1.1720148713567564
    solverConfig.fieldConfig.HOLE_FACTOR = 5.312056910769751
    solverConfig.fieldConfig.HEIGHT_FACTOR = 0.1765673301273726
    solverConfig.fieldConfig.LINE_FACTOR = 1.4106621037891096
    #solverConfig.fieldConfig.HEIGHT_FACTOR_HIGH_LIMIT = (2 * Field.HEIGHT) / 3
    #solverConfig.fieldConfig.HEIGHT_FACTOR_HIGH = solverConfig.fieldConfig.HEIGHT_FACTOR * 2

    #Best avg lines 1093
    #solverConfig.fieldConfig.FLAT_FACTOR = 1.1720148713567564
    #solverConfig.fieldConfig.HOLE_FACTOR = 5.312056910769751
    #solverConfig.fieldConfig.HEIGHT_FACTOR = 0.1765673301273726
    #solverConfig.fieldConfig.LINE_FACTOR = 1.4106621037891096

    # Best max lines 9170
    #solverConfig.fieldConfig.FLAT_FACTOR = 1.1455756043684062
    #solverConfig.fieldConfig.HOLE_FACTOR = 5.3469699973650835
    #solverConfig.fieldConfig.HEIGHT_FACTOR = 0.20679723132559638
    #solverConfig.fieldConfig.LINE_FACTOR = 1.3793801183194825

    #Best avg score 25441
    #solverConfig.fieldConfig.FLAT_FACTOR = 1.1228687283916032
    #solverConfig.fieldConfig.HOLE_FACTOR = 5.193397373397724
    #solverConfig.fieldConfig.HEIGHT_FACTOR = 0.16380901479600363
    #solverConfig.fieldConfig.LINE_FACTOR = 1.2577257145153835

    # Best max score 150550
    #solverConfig.fieldConfig.FLAT_FACTOR =2577257145153835 1.2175710894063936
    #solverConfig.fieldConfig.HOLE_FACTOR = 5.461644433377028
    #solverConfig.fieldConfig.HEIGHT_FACTOR = 0.1799023338588184
    #solverConfig.fieldConfig.LINE_FACTOR = 1.4093925078956993

    bestScore = 1036
    bestMaxScore = 0

    bestConfig = deepcopy(solverConfig)
    bestEverConfig = deepcopy(solverConfig)

    CHANGE_SPEED = 5
    ITERATIONS = 25
    PERFORMANCE_TEST = False
    MUTATE_MEAN = True
    while not __exit:
        if PERFORMANCE_TEST:
            solver = TetroSolver(game,  solverConfig)
            testPerformanceMethod(solver)
            __exit = True
        else:
            geneticLoop += 1
            threadList = [None] * ITERATIONS
            resultsList = [None] * ITERATIONS
            testResults = [0] * ITERATIONS

            timeStart = time.time()
            for i in range(ITERATIONS):
                solver = TetroSolver(game, solverConfig)
                results = Queue()
                resultsList[i] = results
                runThread = Process(target=testThread, args=(solver, results, i))
                runThread.start()
                threadList[i] = runThread
            for i in range(ITERATIONS):
                threadList[i].join()
                testResults[i] = resultsList[i].get()

            timeEnd = time.time()
            totalScore = sum(testResults)
            maxScore = max(testResults)
            meanScore = totalScore / ITERATIONS
            print(f"[{geneticLoop}] Finished {ITERATIONS} iterations in {str(round((timeEnd - timeStart), 4))} s, mean score was: {meanScore}, MAX score was: {maxScore}")
            if meanScore > bestScore:
                bestScore = meanScore
                bestConfig = deepcopy(solverConfig)
                print(f"New best config found!")
                print(f"Flat factor: {bestConfig.fieldConfig.FLAT_FACTOR}")
                print(f"Hole factor: {bestConfig.fieldConfig.HOLE_FACTOR}")
                print(f"Height factor: {bestConfig.fieldConfig.HEIGHT_FACTOR}")
                print(f"Line factor: {bestConfig.fieldConfig.LINE_FACTOR}")
            if maxScore > bestMaxScore:
                bestMaxScore = maxScore
                bestEverConfig = deepcopy(solverConfig)
                print(f"New best MAX config found!")
                print(f"Flat factor: {bestEverConfig.fieldConfig.FLAT_FACTOR}")
                print(f"Hole factor: {bestEverConfig.fieldConfig.HOLE_FACTOR}")
                print(f"Height factor: {bestEverConfig.fieldConfig.HEIGHT_FACTOR}")
                print(f"Line factor: {bestEverConfig.fieldConfig.LINE_FACTOR}")

            # Mutate best config
            if MUTATE_MEAN:
                solverConfig = deepcopy(bestConfig)
            else:
                solverConfig = deepcopy(bestEverConfig)

            rnd = random.randint(-CHANGE_SPEED, CHANGE_SPEED) / 100
            solverConfig.fieldConfig.FLAT_FACTOR = max(solverConfig.fieldConfig.FLAT_FACTOR * (1 + rnd), 0.0)
            rnd = random.randint(-CHANGE_SPEED, CHANGE_SPEED) / 100
            solverConfig.fieldConfig.HOLE_FACTOR = max(solverConfig.fieldConfig.HOLE_FACTOR * (1 + rnd), 0.0)
            rnd = random.randint(-CHANGE_SPEED, CHANGE_SPEED) / 100
            solverConfig.fieldConfig.HEIGHT_FACTOR = max(solverConfig.fieldConfig.HEIGHT_FACTOR * (1 + rnd),
                                                         0.0)
            rnd = random.randint(-CHANGE_SPEED, CHANGE_SPEED) / 100
            solverConfig.fieldConfig.LINE_FACTOR = max(solverConfig.fieldConfig.LINE_FACTOR * (1 + rnd), 0.0)

    if not PERFORMANCE_TEST:
        print(f"Best config after {geneticLoop} rounds with score {bestScore}")
        print(f"Flat factor: {bestConfig.fieldConfig.FLAT_FACTOR}")
        print(f"Hole factor: {bestConfig.fieldConfig.HOLE_FACTOR}")
        print(f"Height factor: {bestConfig.fieldConfig.HEIGHT_FACTOR}")
        print(f"Line factor: {bestConfig.fieldConfig.LINE_FACTOR}")
        print(f"Best MAX config after {geneticLoop} rounds with MAX score {bestMaxScore}")
        print(f"Flat factor: {bestEverConfig.fieldConfig.FLAT_FACTOR}")
        print(f"Hole factor: {bestEverConfig.fieldConfig.HOLE_FACTOR}")
        print(f"Height factor: {bestEverConfig.fieldConfig.HEIGHT_FACTOR}")
        print(f"Line factor: {bestEverConfig.fieldConfig.LINE_FACTOR}")

if __name__ == "__main__":

    runThread = threading.Thread(target=optimizerThread)
    runThread.start()

    pyautogui.alert(text=f"Click here to quit", title='Prompt',
                    button='Exit')
    __exit = True
    runThread.join()



