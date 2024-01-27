import batFramework as bf
import pygame
from .customScene import CustomScene
from random import randint


def load_credits():
    filepath = bf.ResourceManager().get_path("assets/credits.txt")
    res = []
    try:
        with open(filepath, 'r') as file:
            res = [line for line in file.readlines() if line != "\n"]
        return res
    except FileNotFoundError:
        return res


def author():

    potential_authors = [
        "Léo Vandrepol",
        "Baturay Turan",
        "Willfrid Foucon",
        "Chuck Norris"
    ]

    return potential_authors[randint(0, len(potential_authors))-1]


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
        for line in load_credits()[:]:

            labels.append(bf.Label(line).set_text_size(14).add_constraints(bf.ConstraintCenterX()))
            labels.append(
                bf.Label(author()).set_padding((0, 0, 0, 30)).set_text_size(10).add_constraints(bf.ConstraintCenterX()).set_text_color(bf.color.RIVER_BLUE)
            )

        container = bf.Container(bf.Column(10), *labels).add_constraints(bf.ConstraintCenterX())
        self.root.add_child(container)

        self.add_actions(bf.Action("EchapScene").add_key_control(pygame.K_ESCAPE))

    def do_update(self, dt):
        # défiler la caméra
        self.hud_camera.move_by(0, 63*dt)
        if self.actions.is_active("EchapScene"):
            self.manager.set_scene("title")
