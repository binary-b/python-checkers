# import gui items
import pygame
from pygame.locals import *

import globals as gl
import View

# PLAYER = 1
# COMPUTER = 2
# PLAYER_KING = 3
# COMPUTER_KING = 4

FIELD =     1 << 0      # null if empty
PLAYER =    1 << 1      # id of player
KING =      1 << 2      # if 0 than an ordinary man


class Board (View.View):
    board = [
            [0,3,0,3,0,3,0,3],
            [3,0,3,0,3,0,3,0],
            [0,3,0,3,0,3,0,3],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [1,0,1,0,1,0,1,0],
            [0,1,0,1,0,1,0,1],
            [1,0,1,0,1,0,1,0]
            ]

    def __init__ (self):
        self.board_img = pygame.image.load ('./img/board.png')
        self.man_w_img = pygame.image.load ('./img/white_man.png')
        self.man_r_img = pygame.image.load ('./img/red_man.png')
        self.king_w_img = pygame.image.load ('./img/white_king.png')
        self.king_r_img = pygame.image.load ('./img/red_king.png')
        self.rect_trans = pygame.image.load ('./img/rect_transparent.png')

        self.font = pygame.font.Font ('./fonts/AnonymousPro-Regular.ttf', 70)

        self.move = []
        self.rect = Rect (0,0,720,720)

        self.player = False

    def applyMove (self):
        self.backup ()

        if self._applyMove ():
            self.player = not self.player
            print ('correct move')
        else:
            self.restore ()
            print ('incorrect move')

        self.move = []

    def _applyMove (self):
        for pos_1, pos_2 in zip (self.move, self.move[1:]):
            field_1 = self.board [pos_1[0]][pos_1[1]]
            field_2 = self.board [pos_2[0]][pos_2[1]]
            print (pos_1, pos_2)
            print ('player: ', self.player)

            # validating the move

            # checking starting position
            if not (field_1 & FIELD and not (self.player ^ bool (field_1 & PLAYER))):
                return False

            # checking end position
            if field_2 & FIELD:
                return False

            # checking if move on single diagonal
            if not (pos_1[0] + pos_1[1] == pos_2[0] + pos_2[1]
                    or pos_1[0] - pos_1[1] == pos_2[0] - pos_2[1]):
                return False


            # if man being moved
            if not field_1 & KING:
                # check if distance == 1
                if abs (pos_1[0] - pos_2[0]) != 1:
                    return False

            self.board [pos_1[0]][pos_1[1]] = 0
            self.board [pos_2[0]][pos_2[1]] = field_1

        return True

    def cancelMove (self):
        self.move = []

    def update (self):
        pass

    def draw (self):
        gl.screen.blit (self.board_img, (0, 0))
        for x in range (8):
            for y in range (8):
                el = self.board[y][x]
                if el & FIELD:
                    if el & PLAYER:
                        gl.screen.blit (self.man_w_img, (x*90, y*90))
                    else:
                        gl.screen.blit (self.man_r_img, (x*90, y*90))

        for id, pos in enumerate (self.move):
            pos = (pos[1]*90, pos[0]*90)
            gl.screen.blit (self.rect_trans, pos)
            text = self.font.render (str (id+1), True, (0,0,0))

            text_rect = text.get_rect ()
            pos = (pos[0] + (90 - text_rect.width)/2,
                    pos[1] + (90 - text_rect.height)/2)
            gl.screen.blit (text, pos)

    def event (self, ev):
        if ev.type == MOUSEBUTTONUP:
            if self.rect.collidepoint (ev.pos):
                pos = (ev.pos[1] // 90, ev.pos[0] // 90)
                self.move.append (pos)

    def backup (self):
        self.board_bk = self.board[:]

    def restore (self):
        self.board = self.board_bk
