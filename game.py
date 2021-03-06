import pygame, sys
import math
import numpy as np
from collections import defaultdict
import xml.etree.ElementTree as ET

from pygame.locals import *

from tilemap import tilemap, Map
#initialise the pygame module
pygame.init()

#create a new drawing surface, width=300, height=300

map = Map("assets/mymap.tmx", tilemap)
WIDTH, HEIGHT = SCREENSIZE = np.array((640,480))
DISPLAYSURF = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption('My cool game')
DRAW = 25
pygame.time.set_timer(DRAW, 333)

scroll = [200, 100]

running = True
#loop (repeat) forever
while running:
    #get all the user events
    for event in pygame.event.get():
        #if the user wants to quit
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == KEYUP:
            pass
        elif event.type == MOUSEBUTTONDOWN:
            pass
        elif event.type == DRAW:
            map.draw(DISPLAYSURF, scroll)
            pygame.display.update()
            DISPLAYSURF.fill((0,0,0))

    pressed = pygame.key.get_pressed()
    if pressed[K_LEFT] == 1:
        scroll[0]+=10
    elif pressed[K_RIGHT] == 1:
        scroll[0]-=10


    #update the display

pygame.quit()
sys.exit()
