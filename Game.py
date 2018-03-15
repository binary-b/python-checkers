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
                Button.Button ((730,gl.screen_res[1] -225), 'btn_help.png', lambda:gl.openWithSystemDefault ('docs/help.pdf')),
                Button.Button ((730,gl.screen_res[1] -150), 'btn_credits.png', lambda:gl.openWithSystemDefault ('docs/credits.pdf')),
                Button.Button ((730,gl.screen_res[1] -75), 'btn_quit.png', gl.quit)
                ]

        self.status = [
                pygame.image.load ('img/status_in_progress.png'),
                pygame.image.load ('img/status_lost.png'),
                pygame.image.load ('img/status_won.png')
                ]

    def update (self):
        self.board.update ()

    def newGame (self):
        print ('starting new game')
        self.board.reset ()

    def draw (self):
        gl.screen.fill (Color (70, 41, 10))
        self.board.draw ()
        for btn in self.btns:
            btn.draw ()

        pos = (730, 10)
        if not self.board.ended:
            gl.screen.blit (self.status[0], pos)
        else:
            gl.screen.blit (self.status[1+self.board.player], pos)

    def event (self, ev):
        for btn in self.btns:
            btn.event (ev)
        self.board.event (ev)
