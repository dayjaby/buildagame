import pygame
from pygame import Rect
import numpy as np
from collections import defaultdict
import xml.etree.ElementTree as ET
import os

class Tile:
    def __init__(self, size, offset, collision=0, grass=0, **kwargs):
        self.size = np.array(size)
        self.offset = offset
        self.disabled = False
        self.layer = 0
        self.collision = int(collision)
        self.grass = bool(grass)

class Map:
    def __init__(self, tmx, tilemap):
        tree = ET.parse(tmx)
        root = tree.getroot()
        self.tilemap = tilemap
        self.width = int(root.attrib["width"])
        self.height = int(root.attrib["height"])
        self.tile_width = int(root.attrib["tilewidth"])
        self.tile_height = int(root.attrib["tileheight"])
        self.layers = len(root.findall("layer"))

        print(self.tilemap.get_rect(1))

        self.data = np.zeros((self.layers, self.width, self.height), dtype=np.int32)
        for i, layer in enumerate(root.findall("layer")):
            self.data[i, :, :] = np.fromstring(layer.find("data").text, sep=",", dtype=np.int32).reshape((self.height, self.width)).T - 1

        self.a = np.array([[self.tile_width, 0], [0, self.tile_height]])
        self.ainv = np.linalg.inv(self.a)
        self.positions = np.dot(self.a, np.indices((self.width, self.height)).reshape((2, self.width * self.height))).reshape((2, self.width, self.height))

    def draw(self, surface, scroll):
        for layer in range(0, self.layers):
            for x in range(self.width)[::-1]:
                for y in range(self.height):
                    tile = self.data[layer, x, y]
                    offx = offy = 0
                    if tile < 0:
                        continue

                    """if tile == 2040:
                        self.data[layer, x, y] = 2031
                        offy = 0
                    elif tile == 2031:
                        self.data[layer, x, y] = 2041
                        offy = 8
                    elif tile == 2041:
                        self.data[layer, x, y] = -1
                        self.data[layer, x, y+1] = 2031
                        offy = 16"""        #nach unten
                    """if tile == 2040:
                        self.data[layer, x, y] = 2028
                        offx = 0
                    elif tile == 2028:
                        self.data[layer, x, y] = 2030
                        offx = 8
                    elif tile == 2030:
                        self.data[layer, x, y] = -1
                        self.data[layer, x+1, y] = 2028
                        offx = 16"""        #nach rechts
                    """if tile == 2040:
                        self.data[layer, x, y] = 2042
                        offx = 0
                    elif tile == 2042:
                        self.data[layer, x, y] = 2044
                        offx = -8
                    elif tile == 2044:
                        self.data[layer, x, y] = -1
                        self.data[layer, x - 1, y] = 2042
                        offx = -16"""           #nach links
                    if tile == 2040:
                        self.data[layer, x, y] = 2027
                        offy = 0
                    elif tile == 2027:
                        collides = False
                        for layer2 in range(0, self.layers):
                            if self.data[layer2, x, y - 1] == -1:
                                continue
                            print(self.tilemap.tiles[self.data[layer2, x, y - 1]].collision)

                            if not (self.tilemap.tiles[self.data[layer2, x, y - 1]].collision & 4):
                                collides = True
                        if not collides:
                            self.data[layer, x, y] = 2025
                            offy = -8
                        else:
                            self.data[layer, x, y] = 2026
                    elif tile == 2025:
                        self.data[layer, x, y] = -1
                        self.data[layer, x, y - 1] = 2027
                        offy = -16              #nach oben


                    surface.blit(self.tilemap.image,
                                     dest=self.positions[:, x, y] + scroll - self.tilemap.get_offset(tile) + (offx, offy),
                                     area=self.tilemap.get_rect(tile))

class Tilemap:
    def __init__(self, tsx):

        tree = ET.parse(os.path.join("assets", tsx))
        root = tree.getroot()
        self.tile_count = (int(root.attrib["columns"]), int(root.attrib["tilecount"]) / int(root.attrib["columns"]))
        self.tile_size = np.array([int(root.attrib["tilewidth"]), int(root.attrib["tileheight"])])
        self.tiles = defaultdict(lambda: Tile((1, 1), (0, 0)))
        self.layer_default_tile = defaultdict(lambda: 0)
        self.layers = 10
        image = root.find("image")
        tilemap_file = os.path.join("assets", image.attrib["source"])
        for tile in root.findall("tile"):
            properties = tile.find("properties")
            tile_id = int(tile.attrib["id"])
            tile_properties = dict()
            for property in properties.findall("property"):
                property_name = property.attrib["name"]
                property_value = property.attrib["value"]
                print(property_name, property_value)
                tile_properties[property_name] = property_value
            self.tiles[tile_id] = Tile((1, 1), (0, 0), **tile_properties)

        self.image = pygame.image.load(tilemap_file)

    def setup_done(self):
        self.layer_tiles = dict()
        for layer in range(self.layers):
            self.layer_tiles[layer] = tilemap.get_enabled_tiles(layer=layer, get_nr=True)

    def get_offset(self, tile):
        return self.tiles[tile].offset

    def get_x(self, tile):
        return tile%self.tile_count[0]

    def get_y(self, tile):
        return int(tile/self.tile_count[0])

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

tilemap = Tilemap("tileset-shinygold.tsx")
