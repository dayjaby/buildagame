import pygame, sys
import math
import numpy as np
from collections import defaultdict

from pygame.locals import *

from tilemap import tilemap, TilemapEditor
#initialise the pygame module
pygame.init()

#create a new drawing surface, width=300, height=300
LAYERS = 2
MAPWIDTH, MAPHEIGHT = MAPSIZE = (20,20)
WIDTH, HEIGHT = SCREENSIZE = np.array((1200,800))
DISPLAYSURF = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption('My cool game')

te = TilemapEditor(tilemap, (200,800))
scroll = [200, 0]
a = np.array([[32, -32], [16, 16]])
ainv = np.linalg.inv(a)
positions = np.dot(a, np.indices(MAPSIZE).reshape((2, MAPWIDTH * MAPHEIGHT))).reshape((2, MAPWIDTH, MAPHEIGHT))

current_map = np.zeros((LAYERS,MAPWIDTH,MAPHEIGHT), dtype=np.int32)
for layer in range(LAYERS):
    current_map[layer,:,:] = tilemap.layer_default_tile[layer]
te.current_layer = 1
te.current_tile = 142

def draw_tile(layer, x, y, tile=None):
    if tile is None:
        tile = current_map[layer, x, y]
    DISPLAYSURF.blit(tilemap.image,
        dest=positions[:,x,y] + scroll - tilemap.get_offset(tile),
        area=tilemap.get_rect(tile))

def get_mouse_tile(pos = None):
    if pos is None:
        pos = pygame.mouse.get_pos()
    return np.dot(ainv, np.array(pos) - scroll).astype(int)


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
            elif event.key == K_l:
                if te.current_layer == 0:
                    te.current_layer = 1
                elif te.current_layer == 1:
                    te.current_layer = 0
            elif event.key == K_0:
                te.current_tile = tilemap.layer_default_tile[te.current_layer]
            elif event.key == K_DOWN:
                te.current_tile += 10
            elif event.key == K_UP:
                te.current_tile -= 10
        elif event.type == KEYUP:
            pass
        elif event.type == MOUSEBUTTONDOWN:
            pass
        elif event.type == MOUSEBUTTONUP:
            if te.get_rect().collidepoint(event.pos):
                te.set_current_tile_under_pos(event.pos)
            else:
                x,y = get_mouse_tile(event.pos)
                if x >= 0 and x < MAPWIDTH and y >= 0 and y < MAPHEIGHT:
                    current_map[te.current_layer,x,y] = te.current_tile
        else:
            pass

    pressed = pygame.key.get_pressed()
    if pressed[K_LEFT] == 1:
        scroll[0]+=10
    elif pressed[K_RIGHT] == 1:
        scroll[0]-=10

    mx,my = get_mouse_tile()
    for layer in range(0,LAYERS):
        for x in range(MAPWIDTH):
            for y in range(MAPHEIGHT):
                if te is not None and x == mx and y == my and layer == te.current_layer:
                    draw_tile(layer, x, y, te.current_tile)
                else:
                    draw_tile(layer, x, y)

    te.draw(DISPLAYSURF)
    #update the display
    pygame.display.update()
    DISPLAYSURF.fill((0,0,0))

pygame.quit()
sys.exit()
