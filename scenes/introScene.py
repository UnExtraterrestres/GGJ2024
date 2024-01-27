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
        self.set_clear_color(bf.color.DARK_BLUE)

    def do_when_added(self):
        # fond
        # self.root.add_child(bf.Image(""))

        # ajout du debugger
        self.root.add_child(bf.Debugger())

        # écriture des crédits
        labels = [bf.Label(line).set_text_size(14).add_constraints(bf.ConstraintCenterX()).set_text_color(bf.color.CLOUD_WHITE).set_color(bf.color.DARK_BLUE) for line in load_credits()]

        container = bf.Container(bf.Column(40), *labels).add_constraints(bf.ConstraintCenterX())
        self.root.add_child(container)

        self.add_actions(bf.Action("EchapScene").add_key_control(pygame.K_ESCAPE))

    def do_update(self, dt):
        # défiler la caméra
        self.hud_camera.move_by(0, 63*dt)
        if self.actions.is_active("EchapScene"):
            self.manager.set_scene("title")
