import batFramework as bf
import pygame
from .customScene import CustomScene


def load_credits():
    filepath = bf.ResourceManager().get_path("assets/intro.txt")
    res = []
    try:
        with open(filepath, 'r') as file:
            res = [line for line in file.readlines() if line != "\n"]
        return res
    except FileNotFoundError:
        return res


class IntroScene(CustomScene):

    def __init__(self):
        super().__init__("intro")
        self.set_clear_color((10, 10, 10))

    def do_when_added(self):
        # fond
        # self.root.add_child(bf.Image(""))

        # ajout du debugger
        self.root.add_child(bf.Debugger())

        # écriture des crédits
        labels = [bf.Label(line).set_text_size(14).add_constraints(bf.ConstraintCenterX()).set_text_color((255, 255, 0)).set_color((10, 10, 10)) for line in load_credits()]

        container = bf.Container(bf.Column(40), *labels).add_constraints(bf.ConstraintCenterX()).set_y(500)
        self.root.add_child(container)

        self.add_actions(bf.Action("EchapScene").add_key_control(pygame.K_ESCAPE))

    def do_update(self, dt):
        # défiler la caméra
        self.hud_camera.move_by(0, 1)
        if self.actions.is_active("EchapScene"):
            self.manager.set_scene("title")
