# import gui items
import pygame
from pygame.locals import *

import random
import copy

import globals as gl
import View

FIELD =     1 << 0      # null if empty
PLAYER =    1 << 1      # id of player
KING =      1 << 2      # if 0 than an ordinary man


class Board (View.View):
    board_start = [
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

        self.board = copy.deepcopy (self.board_start)

    def reset (self):
        self.board = copy.deepcopy (self.board_start)
        self.move = []
        self.player = False

    def applyMove (self):
        backup = self.backup ()

        if self._applyMove ():
            self.player = not self.player
            print ('correct move')
            self.draw ()
        else:
            self.restore (backup)
            print ('incorrect move')

        self.move = []

    def _randomMove (self):
        x = random.randrange (64)

        return (x // 8, x % 8)

    def _applyMove (self):
        # check number of moves
        capturing = False
        if len (self.move) < 2:
            return False
        if len (self.move) > 2:
            capturing = True

        # print ('possible captures:', self._forceCapture ())
        if not capturing and self._forceCapture ():
            capturing = True

        for pos_1, pos_2 in zip (self.move, self.move[1:]):
            if not self._validateSingleMove (pos_1, pos_2, capturing):
                return False
            else:
                self._applySingleMove (pos_1, pos_2)

        if capturing and self._capturesByPiece (self.move [-1]):
            # print ('forced capture!')
            return False

        self._upgradeToKings ()

        return True

    def _applySingleMove (self, pos_1, pos_2):
        field_1 = self.board [pos_1[0]][pos_1[1]]

        dy = 1
        dx = 1
        if pos_1[0] > pos_2[0]:
            dy = -1
        if pos_1[1] > pos_2[1]:
            dx = -1
        
        self.board [pos_2[0]][pos_2[1]] = field_1

        # clear all in between
        y = pos_1 [0]
        x = pos_1 [1]
        while (y,x) != pos_2:
            self.board [y][x] = 0
            y += dy
            x += dx

    def _validateSingleMove (self, pos_1, pos_2, capturing):
        field_1 = self.board [pos_1[0]][pos_1[1]]
        field_2 = self.board [pos_2[0]][pos_2[1]]

        # print ('pos_1:', pos_1, 'pos_2:', pos_2)

        # checking starting position
        if not (field_1 & FIELD and not (self.player ^ bool (field_1 & PLAYER))):
            # print ('invalid start position')
            return False

        # checking end position
        if field_2 & FIELD:
            # print ('invalid end position')
            return False

        # checking if move on single diagonal
        if not (pos_1[0] + pos_1[1] == pos_2[0] + pos_2[1]
                or pos_1[0] - pos_1[1] == pos_2[0] - pos_2[1]):
            # print ('not on diagonal')
            return False

        # if man is moving
        if not field_1 & KING:
            d_y = pos_1[0] - pos_2[0]
            if abs (d_y) == 1:
                if capturing:
                    # print ('man: forced capturing')
                    return False

                # check direction
                if self.player:
                    if d_y != -1:
                        # print ('man: wrong direction')
                        return False
                else:
                    if d_y != 1:
                        # print ('man: wrong direction')
                        return False
            elif abs (d_y) == 2:
                # check if an opponent piece is in between
                y_a = (pos_1[0] + pos_2[0]) // 2
                x_a = (pos_1[1] + pos_2[1]) // 2
                field_a = self.board [y_a][x_a]
                if not (field_a & FIELD and ((field_a & PLAYER) >> 1 != self.player)):
                    # print ('no opponent in between')
                    return False
            else:
                # print ('invalid distance traveled')
                return False
        # if king is moving
        else:
            # count pieces in between
            pieces = 0
            dy = 1
            dx = 1
            if pos_1[0] > pos_2[0]:
                dy = -1
            if pos_1[1] > pos_2[1]:
                dx = -1

            y = pos_1[0] + dy
            x = pos_1[1] + dx
            while (y, x) != pos_2:
                field = self.board[y][x]
                if field & FIELD:
                    # check if its opponent
                    if (field & PLAYER)>>1 == self.player:
                        # print ('can\'t jump over own pieces', (y,x))
                        return False
                    else:
                        pieces += 1
                y += dy
                x += dx

            if pieces > 1:
                # print ('jumping over too many pieces')
                return False
            if capturing:
                if pieces != 1:
                    ##  print ('invalid capture (king)')
                    return False
            else:
                if not pieces in (0, 1):
                    # print ('invalid regular move (king)')
                    return False

        return True

    # returns True if a capture is possible,
    # False otherwise
    def _forceCapture (self):
        for y in range (8):
            for x in range (8):
                field = self.board [y][x]
                if (field & PLAYER) >> 1 == self.player:
                    if self._capturesByPiece ((y,x)):
                        return True

        return False

    def _capturesByPiece (self, pos):
        captures = []

        field = self.board [pos[0]][pos[1]]
        if field & FIELD:
            #king
            if field & KING:
                sum_xy = pos[0] + pos[1]
                diff_xy = pos[0] - pos[1]

                # y + x
                if sum_xy < 7:
                    y, x = sum_xy, 0
                else:
                    y, x = 7, sum_xy - 7
                while self._isOnBoard ((y,x)):
                    if self._validateSingleMove (pos, (y, x), True):
                        captures.append (((pos), (y,x)))
                    y -= 1
                    x += 1

                # y + x
                if diff_xy > 0:
                    y, x = diff_xy, 0
                else:
                    y, x = 0, -diff_xy
                while self._isOnBoard ((y,x)):
                    if self._validateSingleMove (pos, (y, x), True):
                        captures.append (((pos), (y,x)))
                    y += 1
                    x += 1

            #man
            else:
                # for d_pos in itertools.permutations ((-2, 2), 2):
                for d_pos in ((2, 2), (2, -2), (-2, 2), (-2, -2)):
                    pos_2 = (pos[0] + d_pos[0], pos[1] + d_pos[1])
                    if not self._isOnBoard (pos_2):
                        continue

                    # print ('testing: ', pos, pos_2)
                    if self._validateSingleMove (pos, pos_2, True):
                        # print ('here: ', pos, pos_2)
                        captures.append ((pos, pos_2))

        return captures

    def _upgradeToKings (self):
        for i in range (8):
            field_1 = self.board [0][i]
            field_2 = self.board [7][i]
            if field_1 & FIELD and (field_1 & PLAYER)>>1 == 0:
                self.board [0][i] = field_1 | KING
            if field_2 & FIELD and (field_2 & PLAYER)>>1 == 1:
                self.board [7][i] = field_2 | KING

    def _isOnBoard (self, pos):
        for i in pos:
            if i < 0 or i > 7:
                return False

        return True

    def cancelMove (self):
        self.move = []

    def update (self):
        if self.player == 1:
            computer = Computer (self)
            self.move = computer.getMove ()
            self._applyMove ()
            self.player = not self.player

            self.move = []

    def draw (self):
        gl.screen.blit (self.board_img, (0, 0))
        for x in range (8):
            for y in range (8):
                el = self.board[y][x]
                if el & FIELD:
                    if el & KING:
                        if el & PLAYER:
                            gl.screen.blit (self.king_w_img, (x*90, y*90))
                        else:
                            gl.screen.blit (self.king_r_img, (x*90, y*90))
                    else:
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
        return copy.deepcopy (self.board)

    def restore (self, backup):
        self.board = backup


class Computer (Board):
    def __init__ (self, board):
        self.parent = board
        self.board = board.board
        self.player = board.player
        self.move = []

    def getMove (self):
        moves = self._possibleMoves ()
        print ('possible moves (computer):', moves)

        if moves:
            return random.choice (moves)
        else:
            return []

    def _possibleMoves (self):
        moves = []
        moves += self._capturesOnBoard ()
        if not moves:
            moves += self._regularMovesOnBoard ()

        return moves

    def _capturesOnBoard (self):
        captures = []

        for y in range (8):
            for x in range (8):
                field = self.board [y][x]
                if (field & PLAYER) >> 1 == self.player:
                    captures += self._capturesByPiece ((y,x))

        return captures

    def _regularMovesOnBoard (self):
        moves = []

        for y in range (8):
            for x in range (8):
                field = self.board [y][x]
                if (field & PLAYER) >> 1 == self.player:
                    moves += self._regularMoveByPiece ((y,x))

        return moves

    def _regularMoveByPiece (self, pos):
        captures = []

        field = self.board [pos[0]][pos[1]]
        if field & FIELD:
            #king
            if field & KING:
                pass
                # sum_xy = pos[0] + pos[1]
                # diff_xy = pos[0] - pos[1]

                # # y + x
                # if sum_xy < 7:
                    # y, x = sum_xy, 0
                # else:
                    # y, x = 7, sum_xy - 7
                # while self._isOnBoard ((y,x)):
                    # if self._validateSingleMove (pos, (y, x), True):
                        # captures.append (((pos), (y,x)))
                    # y -= 1
                    # x += 1

                # # y + x
                # if diff_xy > 0:
                    # y, x = diff_xy, 0
                # else:
                    # y, x = 0, -diff_xy
                # while self._isOnBoard ((y,x)):
                    # if self._validateSingleMove (pos, (y, x), True):
                        # captures.append (((pos), (y,x)))
                    # y += 1
                    # x += 1

            #man
            else:
                for d_pos in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
                    pos_2 = (pos[0] + d_pos[0], pos[1] + d_pos[1])
                    if not self._isOnBoard (pos_2):
                        continue

                    # print ('testing: ', pos, pos_2)
                    if self._validateSingleMove (pos, pos_2, False):
                        # print ('here: ', pos, pos_2)
                        captures.append ((pos, pos_2))

        return captures
