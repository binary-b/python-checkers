# import gui items
import pygame
from pygame.locals import *

import globals as gl
import View
import Button

class MainMenu (View.View):
    def __init__ (self):
        self.bg = pygame.image.load ('./img/background.jpg')
        self.btns = [
                Button.Button (gl.screen_res[0]//2, 350, 'btn1.jpg', lambda:print ('press')),
                Button.Button (gl.screen_res[0]//2, 550, 'btn2.jpg', gl.quit)
                ]

    def update (self):
        pass

    def draw (self):
        gl.screen.blit (self.bg, (0, 0))
        for btn in self.btns:
            btn.draw ()

    def event (self, ev):
        for btn in self.btns:
            btn.event (ev)
