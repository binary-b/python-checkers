# import gui items
import pygame
from pygame.locals import *

import globals as gl
import View
import Board
import Button

class Game (View.View):
    def __init__ (self):
        self.board = Board.Board ()
        self.btns = [
                Button.Button ((730,gl.screen_res[1] -450), 'btn_new_game.png', self.newGame),
                Button.Button ((730,gl.screen_res[1] -375), 'btn_apply_move.png', self.board.applyMove),
                Button.Button ((730,gl.screen_res[1] -300), 'btn_cancel_move.png', self.board.cancelMove),
                Button.Button ((730,gl.screen_res[1] -225), 'btn_help.png', lambda:print ('press')),
                Button.Button ((730,gl.screen_res[1] -150), 'btn_credits.png', lambda:print ('press')),
                Button.Button ((730,gl.screen_res[1] -75), 'btn_quit.png', gl.quit)
                ]

    def update (self):
        pass

    def newGame (self):
        print ('starting new game')

    def draw (self):
        gl.screen.fill (Color (70, 41, 10))
        self.board.draw ()
        for btn in self.btns:
            btn.draw ()

    def event (self, ev):
        for btn in self.btns:
            btn.event (ev)
        self.board.event (ev)
