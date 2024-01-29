import batFramework as bf
from .customScene import CustomScene
from .style import style
import pygame

class MusicScene(CustomScene):
    def __init__(self):
        super().__init__("music")
        self.add_actions(bf.Action("EchapScene").add_key_control(pygame.K_ESCAPE))

    def do_when_added(self):
        self.set_clear_color(bf.color.RIVER_BLUE)
        b0 = bf.Button("BACK",lambda :self.manager.set_scene("title"))
        b1 = bf.Button("OST-1 : Lutin",lambda :bf.AudioManager().play_music("lutin",loop=-1))
        b2 = bf.Button("OST-2 : Witch",lambda : bf.AudioManager().play_music("witch",loop=-1))

        c = bf.Container(bf.Column(gap=8).set_child_constraints(bf.ConstraintCenterX(),bf.ConstraintPercentageWidth(1,keep_autoresize=False)))
        c.add_child(b0,b1,b2)
        f = bf.Frame(100,100).add_constraints(bf.ConstraintCenter())#,bf.ConstraintPercentageWidth(0.5))#,bf.ConstraintPercentageHeight(0.4))
        f.add_child(c)
        
        self.root.add_child(f)

        self.root.propagate_function(style)

    def do_update(self,dt):
        if self.actions.is_active("EchapScene"):
            self.manager.set_scene("title")
