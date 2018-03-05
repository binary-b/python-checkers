# import gui items
import pygame
from pygame.locals import *

import View
import globals as gl

class Button (View.View):
    def __init__ (self, pos, img, fnc):
        self.fnc = fnc
        self.img = pygame.image.load ('./img/btn/' + img)
        self.rect = self.img.get_rect ()
        self.rect.move_ip (pos[0], pos[1])

        self.active = False

    def update (self):
        pass

    def draw (self):
        rect = self.rect
        if self.active:
            rect = rect.move (7, 0)
        gl.screen.blit (self.img, rect)

    def event (self, ev):
        if ev.type == MOUSEMOTION:
            if self.rect.collidepoint (ev.pos):
                self.active = True
            else:
                self.active = False
        elif ev.type == MOUSEBUTTONUP:
            if self.rect.collidepoint (ev.pos):
                self.fnc ()
