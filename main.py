# import gui items
import pygame
from pygame.locals import *

import datetime

import globals as gl
import Game

pygame.font.init ()

gl.view = Game.Game ()
gl.screen = pygame.display.set_mode (gl.screen_res)

while True:
    for ev in pygame.event.get ():
        if not gl.view:
            break
        if ev.type == QUIT:
            gl.quit ()
            break
        else:
            gl.view.event (ev)

        if ev.type == KEYDOWN:
            if ev.key == K_F3:
                pygame.image.save (gl.screen, 'screenshoots/' + datetime.datetime.now ().strftime ('%Y_%m_%d_%H_%M_%S') + '.png')

    if not gl.view:
        break

    gl.screen.fill (Color (0,0,0))
    gl.view.draw ()
    gl.view.update ()

    pygame.display.flip ()
