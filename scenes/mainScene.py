import batFramework as bf
import pygame
from .player import Player
from .level import Level,Tile
from .npc import NPC
from .cutscenes import *




class MainScene(bf.Scene):

    def __init__(self):
        super().__init__("main")
        self.set_clear_color(bf.color.RIVER_BLUE)
        self.npc_list = [
            NPC().set_position(128,308).set_cutscene(Test())
        ]



    def do_when_added(self):
        self.level = Level()
        self.level.from_json(bf.ResourceManager().load_json_from_file("assets/level.json"))
        self.player = Player().set_center(*self.camera.get_center())
        self.add_world_entity(self.level,*self.npc_list,self.player)
        self.camera.set_follow_point(lambda : self.player.rect.move(0,-bf.const.RESOLUTION[1]*0.2).center)

        self.set_sharedVar("level",self.level)
        self.set_sharedVar("player",self.player)
    
        b = bf.Button("DIALOGUE",lambda : self.manager.set_scene("dialogue"))
        d = bf.BasicDebugger()
        self.root.add_child(b,d )
        self.level.set_tile(2,2,Tile().set_index(6,0).to_json())
        self.add_actions(bf.Action("EchapScene").add_key_control(pygame.K_ESCAPE))
        d.add_dynamic("state",lambda : self.player.state_machine.get_current_state().name)
    def do_update(self, dt):
        if self.actions.is_active("EchapScene"):
            self.manager.set_scene("pause")

    def do_on_exit(self):
        self.player.actions.hard_reset()
