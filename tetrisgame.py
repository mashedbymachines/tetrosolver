from gametype import GameType
from outputmanager import IngoAppOutputManager, LumptyOutputManager, JstrisOutputManager
from piecepicker import GameColorPiecePicker
from scoringcalculator import IngoScoringCalculator


class TetrisGame():

    def __init__(self, gameType=None):
        self.__gameType = gameType
        self.outputManager = None
        self.piecePicker = None
        self.scoringCalculator = None

        if gameType != None:
            if gameType == GameType.INGO:
                self.outputManager = IngoAppOutputManager()
                self.scoringCalculator = IngoScoringCalculator()
            elif gameType == GameType.LUMPTY:
                self.outputManager = LumptyOutputManager()
            elif gameType == GameType.JSTRIS:
                self.outputManager = JstrisOutputManager()
            self.piecePicker = GameColorPiecePicker(gameType)
