import batFramework as bf
from .customScene import CustomScene
from .style import style
import pygame

class TitleScene(CustomScene):
    def __init__(self):
        super().__init__("title")
        self.set_clear_color("gray30")

    def do_when_added(self):
        self.root.add_child(bf.Image("assets/sprites/bg1.jpg"))
        title2 = bf.Label("Oeufauriz").set_text_size(36).set_y(100)
        self.root.add_child(title2)
        title2.set_text_color("yellow")
        title2.add_constraints(bf.ConstraintCenterX())



        container = bf.Container(bf.Column(gap = 10).set_child_constraints(bf.ConstraintPercentageWidth(0.9,False),bf.ConstraintCenterX()))
        container.set_size(100,60).set_padding(10).set_y(self.hud_camera.get_center()[1]+40)
        container.add_constraints(bf.ConstraintCenterX())
        container.add_child(
            bf.Button("Play",lambda : self.manager.set_scene("main")),
            bf.Button("Credits", lambda : self.manager.set_scene("credits")),
            bf.Button("Quit", self.manager.stop)
        )
        
        self.root.add_child(container)
        self.root.propagate_function(style)


        
