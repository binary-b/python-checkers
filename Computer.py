import copy

import globals as gl

from Board import Board

class Computer (Board):
    def __init__ (self, board):
        self.board = board.board
        self.player = board.player

    def makeMove (self, board):
        backup = self.backup ()
        while not self._applyMove ():
            self.move = []
            self.move.append (self._randomMove ())
            self.move.append (self._randomMove ())
            print ('\n')
        self.restore (backup)

        return self.move
