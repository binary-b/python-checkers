# import gui items
import pygame
from pygame.locals import *

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

    if not gl.view:
        break

    gl.view.update ()
    gl.screen.fill (Color (0,0,0))
    gl.view.draw ()

    pygame.display.flip ()
