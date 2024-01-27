import batFramework as bf
import pygame
from .game_constants import GameConstants as gconst
from typing import Self
from .tile import Tile


class Level(bf.Entity):
    def __init__(self,width=20,height=None):
        super().__init__(no_surface = True)
        if height is None : height = width
        self.height = height
        self.width = width
        self.tiles = [None for _ in range(width*height)]

    def get_bounding_box(self):
        yield pygame.Rect(*self.rect.topleft,gconst.TILE_SIZE*self.width,gconst.TILE_SIZE*self.height)

    def get_drawn_tiles(self)->list:
        return [t for t in self.tiles if t is not None]

    def convert_from_grid(self,x,y)->int:
        return y * self.height + x

    def set_tile(self,x,y,tile_data:dict)->bool:
        if self.is_out_of_bounds(x,y):return False
        i = self.convert_from_grid(x,y)
        tile =Tile().from_json(tile_data)
        self.tiles[i] = tile
        tile.set_position(x*gconst.TILE_SIZE,y*gconst.TILE_SIZE)
        return True

    def is_out_of_bounds(self,x,y)->bool:
        return  y <0 or y>=self.height or x<0 or x >= self.width     

    def get_tile(self,x,y)->Tile|None:
        if self.is_out_of_bounds(x,y):return None
        return self.tiles[self.convert_from_grid(x,y)]                


    def remove_tile(self,x,y)->bool:
        if self.is_out_of_bounds(x,y):return False
        self.tiles[self.convert_from_grid(x,y)] = None
        return True
        

    def get_neighboring(self,x,y)->list:
        res = []
        for h in [-1,0,1]:
            for v in [-1,0,1]:
                res.append(self.get_tile(x+h,y+v))
        return res

    def to_json(self)->dict:
        return {
            "size":(self.width,self.height),
            "tiles":[t.to_json() for t in self.tiles]
        }

    def convert_world_to_grid(self,x,y)->tuple[int,int]:
        return int(x//gconst.TILE_SIZE),int(y//gconst.TILE_SIZE)
    
    def draw(self,camera):
        l = [t.custom_draw(camera) for t in self.tiles if t and camera.intersects(t.rect)]
        camera.surface.fblits(l)
        return len(l)
                
        
