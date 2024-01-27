import batFramework as bf
import pygame
from .customScene import CustomScene
from .style import style

class PauseScene(CustomScene):

    def __init__(self):
        super().__init__("pause")
        self.set_clear_color((0,0,0,128))



    def do_when_added(self):
        self.add_actions(bf.Action("EchapScene").add_key_control(pygame.K_ESCAPE))
        self.root.add_child(bf.BasicDebugger())

        title = bf.Label("Pause").set_text_size(28)
        self.root.add_child(title)
        title.set_center(*self.hud_camera.rect.move(0,40).midtop)
        
        container = bf.Container(bf.Column(gap = 10).set_child_constraints(bf.ConstraintPercentageWidth(0.9,False),bf.ConstraintCenterX()))
        container.set_size(100,60).set_padding(10).set_y(self.hud_camera.get_center()[1]+40)
        container.add_constraints(bf.ConstraintCenterX())
        container.add_child(
            bf.Button("Resume",lambda : self.manager.set_scene("main")),
            bf.Button("Menu",lambda : self.manager.set_scene("title")),
            bf.Button("Quit", self.manager.stop)
        )
        
        self.root.add_child(container)
        self.root.propagate_function(style)

    def do_on_enter(self):
        self.manager.get_scene("main").set_visible(True)

    def do_update(self, dt):
        if self.actions.is_active("EchapScene"):
            self.manager.set_scene("main")