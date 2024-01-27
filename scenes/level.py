import batFramework as bf
import pygame
from .game_constants import GameConstants as gconst
from typing import Self
class Tile(bf.Entity):
    def __init__(self):
        super().__init__((gconst.TILE_SIZE,gconst.TILE_SIZE))
        self.set_tileset_index(0,0)

    def set_tileset_index(self,x,y)->Self:
        self.tileset_position = x,y
        self.surface = bf.Tileset.get_tileset("main").get_tile(x,y)
        return self
    def custom_draw(self,camera)->tuple:
        return self.surface,camera.transpose(self.rect)

class Level(bf.Entity):
    def __init__(self,width=20,height=None):
        super().__init__(no_surface = True)
        if height is None : height = width
        self.height = height
        self.width = width
        self.tiles = [None for _ in range(width*height)]


    def get_drawn_tiles(self)->list:
        return [t for t in self.tiles if t is not None]


    def convert_from_grid(self,x,y)->int:
        return y * self.height + x

    def set_tile(self,x,y,tile)->bool:
        i = self.convert_from_grid(x,y)
        if i<0 or i>=len(self.tiles):return False
        self.tiles[i] = tile
        tile.set_position(x*gconst.TILE_SIZE,y*gconst.TILE_SIZE)
        return True


    def draw(self,camera):
        l = [t.custom_draw(camera) for t in self.tiles if t and camera.intersects(t.rect)]
        camera.surface.fblits(l)
        return len(l)
                
        
