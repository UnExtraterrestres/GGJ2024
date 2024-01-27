import batFramework as bf
from .game_constants import GameConstants as gconst
from typing import Self



class Tile(bf.Entity):
    def __init__(self)->None:
        super().__init__((gconst.TILE_SIZE,gconst.TILE_SIZE))
        self.tileset_position = 0,0
        self.flip = (False,False)
        self.set_index(0,0)
    def set_flip(self,x:bool,y:bool)->Self:
        self.flip = (x,y)
        self.update_surface()
        return self
    def set_index(self,x,y)->Self:
        self.tileset_position = x,y
        self.update_surface()
        return self

    def update_surface(self):
        x,y = self.tileset_position
        self.surface = bf.Tileset.get_tileset("main").get_tile(x,y,self.flip[0],self.flip[1])
        
    def custom_draw(self,camera)->tuple:
        return self.surface,camera.transpose(self.rect)

    def to_json(self)->dict:
        return {
            "position":self.rect.topleft,
            "index":self.tileset_position,
            "tags":self.tags,
            "flip":self.flip
        }
        
    def from_json(self,data:dict)->Self:  
        self.set_index(*data["index"])
        self.tags.clear()
        self.add_tags(*data["tags"])
        self.set_flip(*data["flip"])
        self.set_position(*data["position"])
        return self
