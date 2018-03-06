import copy

import globals as gl

from Board import *

class Computer (Board):
    def makeMove (self, board):
        backup = self.backup ()
        while not self._applyMove ():
            self.move = []
            self.move.append (self._randomMove ())
            self.move.append (self._randomMove ())
            print ('\n')
        self.restore (backup)
