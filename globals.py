import os
import sys

view = None
screen = None
screen_res = (1080, 720)

def setView (a):
    global view
    view = a
def quit ():
    global view
    view = None

def openWithSystemDefault ( filename ):
    if sys.platform.startswith ('linux'):
        os.system ('xpdf ' + filename + ' &')
    elif sys.platform.startswith ('win32'):
        os.system ('start' + filename)
    elif sys.platform.startswith ('darwin'):
        os.system ('open' + filename)
