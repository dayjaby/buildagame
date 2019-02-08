    #import the pygame module, and the
#sys module for exiting the window we create
import pygame, sys
import math
import numpy as np
from collections import defaultdict

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

class Tile:
    def __init__(self, size, offset):
        self.size = np.array(size)
        self.offset = offset
        self.disabled = False


class Tilemap:
    def __init__(self, image, tile_count, tile_size, tile_offset):
        self.image = pygame.image.load("tilemap.png")
        self.tile_count = tile_count
        self.tile_size = np.array(tile_size)
        self.tiles = defaultdict(lambda: Tile(tile_size, tile_offset))

    def add_special_tile(self, tile, size, offset):
        for x in range(size[0]):
            for y in range(size[1]):
                dtile = self.get_x(tile) + x + (self.get_y(tile) + y) * self.tile_count[0]
                print(dtile)
                self.tiles[dtile].disabled = True

        self.tiles[tile] = Tile(self.tile_size * size, offset)

    def get_offset(self, tile):
        return self.tiles[tile].offset

    def get_x(self, tile):
        return tile%self.tile_count[0]

    def get_y(self, tile):
        return tile/self.tile_count[0]

    def get_rect(self, tile):
        size = self.tiles[tile].size
        return Rect(
            self.get_x(tile)*self.tile_size[0],
            self.get_y(tile)*self.tile_size[1],
            size[0], size[1])

tilemap = Tilemap(pygame.image.load("tilemap.png"), (10,17), (64,64), (32,32))
tilemap.add_special_tile(137, (4,3), (96,112))
tilemap.add_special_tile(134, (3,3), (96,132))
scroll = [200, 0]

a = np.array([[32, -32], [16, 16]])
ainv = np.linalg.inv(a)
positions = np.dot(a, np.indices(MAPSIZE).reshape((2, MAPWIDTH * MAPHEIGHT))).reshape((2, MAPWIDTH, MAPHEIGHT))

current_map = np.zeros((LAYERS,MAPWIDTH,MAPHEIGHT))
current_map[1,:,:] = 9
current_layer = 1

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
            pass
        elif event.type == KEYUP:
            pass
        elif event.type == MOUSEBUTTONDOWN:
            pass
        elif event.type == MOUSEBUTTONUP:
            x,y = (np.dot(ainv, np.array(event.pos) - scroll)).astype(int)
            if x >= 0 and x < MAPWIDTH and y >= 0 and y < MAPHEIGHT:
                current_map[current_layer,x,y] = 134
        else:
            pass

    pressed = pygame.key.get_pressed()
    if pressed[K_LEFT] == 1:
        scroll[0]+=10
    elif pressed[K_RIGHT] == 1:
        scroll[0]-=10
    for layer in range(0,LAYERS):
        for x in range(MAPWIDTH):
            for y in range(MAPHEIGHT):
                #pos = np.dot(a, np.array([[x], [y]]))
                tile = current_map[layer, x, y]
                DISPLAYSURF.blit(tilemap.image,
                    dest=positions[:,x,y] + scroll - tilemap.get_offset(tile),
                    area=tilemap.get_rect(tile))

    #update the display
    pygame.display.update()
    DISPLAYSURF.fill((0,0,0))

pygame.quit()
sys.exit()
