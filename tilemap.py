import pygame
from pygame import Rect
import numpy as np
from collections import defaultdict

class Tile:
    def __init__(self, size, offset):
        self.size = np.array(size)
        self.offset = offset
        self.disabled = False
        self.layer = 0

class TilemapEditor:
    def __init__(self, tilemap, size, offset=(0,0)):
        self.tilemap = tilemap
        self.compact_size = size
        self.compact = pygame.transform.scale(tilemap.image.copy(), size)
        self.tile_width = size[0]/tilemap.tile_count[0]
        self.tile_height = size[1]/tilemap.tile_count[1]
        print(self.tile_width, self.tile_height)
        self.current_layer = 0
        self.current_tile = 0
        self.offset = np.array(offset)

    def set_current_tile_under_pos(self, pos):
        x, y = (-self.offset + pos) / (self.tile_width, self.tile_height)
        if x in range(self.tilemap.tile_count[0]) and y in range(self.tilemap.tile_count[1]):
            tile = x+y*self.tilemap.tile_count[0]
            tile_obj = self.tilemap.tiles[tile]
            if tile_obj.disabled:
                tile = tile_obj.disabled-1
            self.current_tile = tile

    def draw(self, surf):
        surf.fill((0,0,0),self.get_rect())
        surf.blit(self.compact,
            dest=(0,0))
        pygame.draw.rect(surf, (255,0,0), self.get_tile_rect(self.current_tile), 2)

    def get_tile_rect(self, tile):
        x = self.tilemap.get_x(tile)
        y = self.tilemap.get_y(tile)
        size = self.tilemap.tiles[tile].size
        return Rect(x*self.tile_width+self.offset[0], y*self.tile_height+self.offset[1], self.tile_width*size[0], self.tile_height*size[1])

    def get_rect(self):
        return Rect((0,0)+self.compact.get_size())


class Tilemap:
    def __init__(self, image, tile_count, tile_size, tile_offset, layers):
        self.image = image
        self.tile_count = tile_count
        self.tile_size = np.array(tile_size)
        self.tiles = defaultdict(lambda: Tile((1,1), tile_offset))
        self.layer_default_tile = defaultdict(lambda: 0)
        self.layers = layers

    def setup_done(self):
        self.layer_tiles = dict()
        for layer in range(self.layers):
            self.layer_tiles[layer] = tilemap.get_enabled_tiles(layer=layer, get_nr=True)

    def add_special_tile(self, tile, size, offset=None):
        for x in range(size[0]):
            for y in range(size[1]):
                dtile = self.get_x(tile) + x + (self.get_y(tile) + y) * self.tile_count[0]
                # we add 1 so that not disabled is always False, even for tile nr 0
                self.tiles[dtile].disabled = tile + 1
        if offset is None:
            offset = self.tiles[tile].offset
        self.tiles[tile] = Tile(size, offset)

    def get_offset(self, tile):
        return self.tiles[tile].offset

    def get_x(self, tile):
        return tile%self.tile_count[0]

    def get_y(self, tile):
        return tile/self.tile_count[0]

    def get_rect(self, tile):
        size = self.tile_size * self.tiles[tile].size
        return Rect(
            self.get_x(tile)*self.tile_size[0],
            self.get_y(tile)*self.tile_size[1],
            size[0], size[1])

    def get_enabled_tiles(self, rng=None, layer=None, get_nr=False):
        if rng is None:
            rng = range(self.tile_count[0]*self.tile_count[1])
        if layer is None:
            layer = range(self.layers)
        else:
            layer = range(layer, layer+1)
        return [
            tile_nr if get_nr else tile
            for tile_nr, tile in self.tiles.items()
            if tile_nr in rng and not tile.disabled and tile.layer in layer
        ]

tilemap = Tilemap(pygame.image.load("tilemap.png"), (10,16), (64,64), (32,32), 2)
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
for tile in tilemap.get_enabled_tiles(range(50,160)):
    tile.layer = 1
tilemap.layer_default_tile[1] = 9
tilemap.setup_done()

