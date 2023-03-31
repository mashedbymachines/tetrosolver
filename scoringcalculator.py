
class ScoringCalculator():

    def __init__(self):
        self.scoring = 0

    def updateSore(self, newClearedLines):

        pass

class IngoScoringCalculator(ScoringCalculator):

    def __init__(self):
        super().__init__()
        self.__lastLineClear = 0

    def updateSore(self, newClearedLines):

        for l in range(newClearedLines):
            self.scoring += (10 * (l + 1)) + (10 * self.__lastLineClear)

        if newClearedLines == 4:
            self.scoring += 250

        self.__lastLineClear = newClearedLines
