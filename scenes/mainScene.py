import batFramework as bf
from .player import Player
from .level import Level,Tile


class MainScene(bf.Scene):

    def __init__(self):
        super().__init__("main")
        self.set_clear_color(bf.color.RIVER_BLUE)
        self.level = Level()
        self.player = Player().set_center(*self.camera.get_center())
        self.add_world_entity(self.level,self.player)
        self.camera.set_follow_point(lambda : self.player.rect.move(0,-bf.const.RESOLUTION[1]*0.2).center)


    def do_when_added(self):
        b = bf.Button("DIALOGUE",lambda : self.manager.set_scene("dialogue"))
        self.root.add_child(b, bf.BasicDebugger())
        self.level.set_tile(2,2,Tile().set_index(6,0).to_json())
