import batFramework as bf
import pygame
import threading
from .customScene import CustomScene
from .style import style
from random import choice
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
        self.loaded_credits = load_credits()
        self.labels = []
        self.loaded = False
        self.stopped = False


    def do_when_added(self):
        self.root.add_child(bf.Debugger())
        self.hud_camera.move_by(0,-500)
        for line in self.loaded_credits[:10]:

            self.labels.append(bf.Label(line).set_text_size(14).add_constraints(bf.ConstraintCenterX()))
            self.labels.append(
                bf.Label(choice(["Chuck Norris","Baturay TURAN","Leo VANDREPOLE","Wilfrid FOUCON"])).set_padding((0, 0, 0, 30)).set_text_size(10).add_constraints(bf.ConstraintCenterX()).set_text_color(bf.color.RIVER_BLUE)
            )

        self.container = bf.Container(bf.Column(10), *self.labels).add_constraints(bf.ConstraintCenterX())
        self.root.add_child(self.container)

        self.add_actions(
            bf.Action("EchapScene").add_key_control(pygame.K_ESCAPE),
            bf.Action("speed").add_key_control(pygame.K_DOWN).set_holding(),

            )
        self.timer = bf.Timer(0.9, loop=True, end_callback=lambda:  self.container.children.pop(0) if self.container.children else None).start()
        self.timer.pause()
        

    def create_labels(self):
        for line in self.loaded_credits[10:100]:
            self.container.add_child(
                bf.Label(line).set_text_size(14).add_constraints(bf.ConstraintCenterX()),
                bf.Label(choice(["Chuck Norris","Baturay TURAN","Leo VANDREPOLE","Wilfrid FOUCON"])).set_padding((0, 0, 0, 30)).set_text_size(10).add_constraints(bf.ConstraintCenterX()).set_text_color(bf.color.RIVER_BLUE)
                )
        self.container.add_child(
            style(bf.Button("Credits", lambda : self.manager.set_scene("creditcredit")))
        )
        self.loaded = True

    def do_on_enter(self):
        if self.loaded is False:
            thread = threading.Thread(target=lambda: self.create_labels())
            thread.start()
        pass
        bf.AudioManager().play_music("credits",loop=-1)
        if self.stopped:
            self.stopped = False
            self.hud_camera.set_position(0,-500)
        
    def do_on_exit(self):
        self.timer.pause()

    def do_update(self, dt):
        
        if self.hud_camera.transpose(self.container.rect).bottom > 40:
            self.hud_camera.move_by(0,10 if self.actions.is_active("speed") else 1)
        else:
            self.stopped = True
        if self.actions.is_active("EchapScene"):
            self.manager.set_scene("title")
        # print(self.hud_camera.transpose(self.container.rect).bottom)

