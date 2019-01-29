#import the pygame module, and the
#sys module for exiting the window we create
import pygame, sys
import math
import numpy as np

#import some useful constants
# see http://www.raspberry-pi-geek.com/Archive/2014/05/Pygame-modules-for-interactive-programs
from pygame.locals import *
from pygame import Rect

#initialise the pygame module
pygame.init()

#create a new drawing surface, width=300, height=300
LAYERS = 2
MAPWIDTH, MAPHEIGHT = MAPSIZE = (20,20)
WIDTH, HEIGHT = SCREENSIZE = (1200,800)
DISPLAYSURF = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption('My cool game')

tilemap = pygame.image.load("tilemap.png")
scrollx, scrolly = (200, 0)

def transform(pos):
    px, py = pos
    y = (2*py - px - 2*scrolly+scrollx-32)/64.0
    x = (py - 16*y - scrolly-32)/16.0
    return int(x),int(y)

tiles = np.zeros((LAYERS,MAPWIDTH,MAPHEIGHT))
holding = [False]*300
tiles[1,:,:] = 9
current_layer = 1

#loop (repeat) forever
while True:
    #get all the user events
    for event in pygame.event.get():
        #if the user wants to quit
        if event.type == QUIT:
            #end the game and close the window
            print("quit")
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            holding[event.key] = True
        elif event.type == KEYUP:
            holding[event.key] = False
        elif event.type == MOUSEBUTTONUP:
            x,y = transform(event.pos)
            tiles[current_layer,x,y] = 50
        else:
            pass
    
    if holding[K_LEFT] == 1:
        scrollx+=5
    elif holding[K_RIGHT] == 1:
        scrollx-=5
    for layer in range(0,LAYERS):
        for x in range(MAPWIDTH):
            for y in range(MAPHEIGHT):
                DISPLAYSURF.blit(tilemap, 
                    dest=(32*x-32*y+scrollx,16*x+16*y+scrolly), 
                    area=Rect((tiles[layer,x,y]%10)*64,(tiles[layer,x,y]/10)*64,64,64))

    #update the display      
    pygame.display.update()
    DISPLAYSURF.fill((0,0,0))

