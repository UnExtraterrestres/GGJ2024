import batFramework as bf
from .customScene import CustomScene
from .style import style
import pygame

class TitleScene(CustomScene):
    def __init__(self):
        super().__init__("title")
        self.set_clear_color("gray30")

    def do_when_added(self):
        self.root.add_child(bf.Image("assets/titre.png"))
        title2 = bf.Label("Oeuf-au-riz").set_text_size(36).set_y(200)

        title2.add_constraints(bf.ConstraintCenterX())

        self.root.add_child(title2)


        container = bf.Container(bf.Column(gap = 10).set_child_constraints(bf.ConstraintPercentageWidth(0.9,False),bf.ConstraintCenterX()))
        container.set_size(100,60).set_padding(10).set_y(self.hud_camera.get_center()[1]+80)
        container.add_constraints(bf.ConstraintCenterX())
        container.add_child(
            bf.Button("Music",lambda : self.manager.set_scene("music")),
            bf.Button("Credits", lambda : self.manager.set_scene("credits")),
            bf.Button("Quit", self.manager.stop)
        )
        
        self.root.add_child(container)
        self.root.propagate_function(style)


        
        # title2.set_text_color("yellow").set_color((0,0,0,0)).set_outline_width(0)
