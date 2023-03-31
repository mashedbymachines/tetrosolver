import time

import pyautogui


class OutputManager():

    def __init__(self):
        pass

    def getReadyForInput(self):
        pass

    def rotate(self):
        pass

    def moveToMaxLeft(self):
        pass

    def moveRight(self):
        pass

    def throwDown(self):
        pass

    def output(self, rotation, position):
        # rotate piece
        # move piece to max left by long swipe
        # Move piece step by step to right position
        # Send piece down
        # Reset

        self.getReadyForInput()

        for r in range(rotation):
            self.rotate()

        self.moveToMaxLeft()

        for p in range(position):
            self.moveRight()

        self.throwDown()


class PrintOutputManager(OutputManager):

    def __init__(self):
        super().__init__()

    def getReadyForInput(self):
        pass

    def rotate(self):
        print("Outpt: Rotate")

    def moveToMaxLeft(self):
        print("Output: Move to max left")

    def moveRight(self):
        print("Output: Move right")

    def throwDown(self):
        print("Output: Throw down")

class IngoAppOutputManager(OutputManager):

    def __init__(self):
        super().__init__()

    def getReadyForInput(self):
        pass

    def rotate(self):
        assert False, "Not implemented"

    def moveToMaxLeft(self):
        assert False, "Not implemented"

    def moveRight(self):
        assert False, "Not implemented"

    def throwDown(self):
        assert False, "Not implemented"


class LumptyOutputManager(OutputManager):

    def __init__(self):
        super().__init__()

    def getReadyForInput(self):
        time.sleep(0.7)

    def rotate(self):
        pyautogui.press('up')

    def moveToMaxLeft(self):
        pyautogui.press('left', presses=4)

    def moveRight(self):
        pyautogui.press('right')

    def throwDown(self):
        pyautogui.keyDown('down')
        time.sleep(0.06)
        pyautogui.keyUp('down')


class JstrisOutputManager(OutputManager):

    def __init__(self):
        super().__init__()

    def getReadyForInput(self):
        pass

    def rotate(self):
        pyautogui.press('up')

    def moveToMaxLeft(self):
        pyautogui.press('left', presses=5)

    def moveRight(self):
        pyautogui.press('right')

    def throwDown(self):
        pyautogui.press('space')