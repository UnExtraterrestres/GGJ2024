import batFramework as bf
import pygame
from .customScene import CustomScene


def load_credits():
    filepath = bf.ResourceManager().get_path("assets/credits.txt")
    res = []
    try:
        with open(filepath, 'r') as file:
            res = [line for line in file.readlines() if line != "\n"]
        return res
    except FileNotFoundError:
        return res


class CreditScene(CustomScene):

    def __init__(self):
        super().__init__("credits")
        self.set_clear_color(bf.color.CLOUD_WHITE)

    def do_when_added(self):
        # fond
        # self.root.add_child(bf.Image(""))

        # ajout du debugger
        self.root.add_child(bf.Debugger())

        # écriture des crédits
        labels = []
        for line in load_credits()[:100]:

            labels.append(bf.Label(line).set_text_size(14).add_constraints(bf.ConstraintCenterX()))
            labels.append(
                bf.Label("Chuck Norris").set_padding((0, 0, 0, 30)).set_text_size(10).add_constraints(bf.ConstraintCenterX()).set_text_color(bf.color.RIVER_BLUE)
            )

        self.container = bf.Container(bf.Column(10), *labels).add_constraints(bf.ConstraintCenterX())
        self.root.add_child(self.container)

        self.add_actions(bf.Action("EchapScene").add_key_control(pygame.K_ESCAPE))
        self.timer =         bf.Timer(0.9,loop = True,end_callback = lambda :  self.container.children.pop(0) if self.container.children else None).start()
        self.timer.pause()

    def do_on_enter(self):
        pass
        # self.timer.resume()
    def do_on_exit(self):
        self.timer.pause()
    def do_update(self, dt):
        # défiler la caméra
        speed = 2
        self.hud_camera.move_by(0,speed *  60*dt)
        if self.actions.is_active("EchapScene"):
            self.manager.set_scene("title")

