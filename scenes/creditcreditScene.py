import batFramework as bf
import pygame
import threading
from .style import style
from .customScene import CustomScene
from random import randint


def load_credits():
    filepath = bf.ResourceManager().get_path("assets/creditcredit.txt")
    res = []
    try:
        with open(filepath, 'r') as file:
            res = [line for line in file.readlines() if line != "\n"]
        return res
    except FileNotFoundError:
        return res


class CreditCreditScene(CustomScene):

    def __init__(self):
        super().__init__("creditcredit")
        self.set_clear_color(bf.color.CLOUD_WHITE)
        self.loaded_credits = load_credits()
        self.labels = []
        self.loaded = False

    def do_when_added(self):
        # fond
        # self.root.add_child(bf.Image(""))

        self.hud_camera.zoom(0.5)

        # ajout du debugger
        self.root.add_child(bf.Debugger())

        # écriture des crédits

        for line in self.loaded_credits[:10]:
            self.labels.append(bf.Label(line).set_text_size(14).add_constraints(bf.ConstraintCenterX()))

        self.container = bf.Container(bf.Column(10), *self.labels).add_constraints(bf.ConstraintCenterX())
        self.root.add_child(self.container)

        self.add_actions(bf.Action("EchapScene").add_key_control(pygame.K_ESCAPE))
        self.timer = bf.Timer(0.9, loop=True, end_callback=lambda: self.container.children.pop(
            0) if self.container.children else None).start()
        self.timer.pause()

    def create_labels(self):
        for line in self.loaded_credits[10:101]:
            self.container.add_child(
                bf.Label(line).set_text_size(14).add_constraints(bf.ConstraintCenterX())
            )
        self.container.add_child(
            style(bf.Button("Menu", lambda : self.manager.set_scene("title")))
        )

        self.loaded = True

    def do_on_enter(self):
        if self.loaded is False:
            thread = threading.Thread(target=lambda: self.create_labels())
            thread.start()
        pass

    def do_on_exit(self):
        self.timer.pause()

    def do_update(self, dt):
        if self.hud_camera.transpose(self.container.rect).bottom > 40:
            self.hud_camera.move_by(0,1)

        #print(self.hud_camera.rect)
        if self.actions.is_active("EchapScene"):
            self.manager.set_scene("title")

        # print(self.hud_camera.transpose(self.container.rect).bottom)
