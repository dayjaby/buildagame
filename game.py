import pygame, sys
import math
import numpy as np
from collections import defaultdict

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
        self.layer = 0


class Tilemap:
    def __init__(self, image, tile_count, tile_size, tile_offset):
        self.image = pygame.image.load("tilemap.png")
        self.tile_count = tile_count
        self.tile_size = np.array(tile_size)
        self.tiles = defaultdict(lambda: Tile(tile_size, tile_offset))
        self.layer_default_tile = defaultdict(lambda: 0)

    def add_special_tile(self, tile, size, offset=None):
        for x in range(size[0]):
            for y in range(size[1]):
                dtile = self.get_x(tile) + x + (self.get_y(tile) + y) * self.tile_count[0]
                self.tiles[dtile].disabled = True
        if offset is None:
            offset = self.tiles[tile].offset
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

    def get_enabled_tiles(self, rng=None):
        if rng is None:
            rng = range(tile_count[0]*tile_count[1])
        return [tile for tile_nr, tile in self.tiles.items() if tile_nr in rng and not tile.disabled]

tilemap = Tilemap(pygame.image.load("tilemap.png"), (10,17), (64,64), (32,32))
# make the right-most tiles oversized so that the empty tiles to the right get .disabled = True
tilemap.add_special_tile(6, (3,1))
tilemap.add_special_tile(17, (3,1))
tilemap.add_special_tile(23, (7,1))
tilemap.add_special_tile(38, (2,1))
tilemap.add_special_tile(43, (7,1))
tilemap.add_special_tile(102, (8,1))
# handle oversized tiles and set their offsets to correct values
tilemap.add_special_tile(120, (1,1), (44,32))
tilemap.add_special_tile(137, (4,3), (96,160))
tilemap.add_special_tile(134, (3,3), (96,160))
tilemap.add_special_tile(143, (1,2), (32,96))
tilemap.add_special_tile(142, (1,2), (32,96))
tilemap.add_special_tile(123, (1,2), (32,96))
tilemap.add_special_tile(122, (1,2), (32,96))
tilemap.add_special_tile(131, (1,3), (32,160))
tilemap.add_special_tile(130, (1,3), (32,160))
# all tiles after 50 belong to layer 1, not 0!!
for tile in tilemap.get_enabled_tiles(range(50,170)):
    tile.layer = 1
tilemap.layer_default_tile[1] = 9

scroll = [200, 0]
a = np.array([[32, -32], [16, 16]])
ainv = np.linalg.inv(a)
positions = np.dot(a, np.indices(MAPSIZE).reshape((2, MAPWIDTH * MAPHEIGHT))).reshape((2, MAPWIDTH, MAPHEIGHT))

current_map = np.zeros((LAYERS,MAPWIDTH,MAPHEIGHT), dtype=np.int32)
current_map[1,:,:] = 9
current_layer = 1
current_tile = 120

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
                if current_layer == 0:
                    current_layer = 1
                elif current_layer == 1:
                    current_layer = 0
            elif event.key == K_0:
                current_tile = tilemap.layer_default_tile[current_layer]
        elif event.type == KEYUP:
            pass
        elif event.type == MOUSEBUTTONDOWN:
            pass
        elif event.type == MOUSEBUTTONUP:
            x,y = get_mouse_tile(event.pos)
            if x >= 0 and x < MAPWIDTH and y >= 0 and y < MAPHEIGHT:
                current_map[current_layer,x,y] = current_tile
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
                if x == mx and y == my and layer == current_layer:
                    draw_tile(layer, x, y, current_tile)
                else:
                    draw_tile(layer, x, y)

    #update the display
    pygame.display.update()
    DISPLAYSURF.fill((0,0,0))

pygame.quit()
sys.exit()
