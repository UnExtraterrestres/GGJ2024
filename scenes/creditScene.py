import batFramework as bf
from .customScene import CustomScene


def load_credits(filepath: str):
    try:
        with open(filepath, 'r') as file:
            res = file.readlines()
            res = "".join(res)
        return res
    except FileNotFoundError:
        return "Coin coin"


class CreditScene(CustomScene):

    def __init__(self):
        super().__init__("credits")
        self.set_clear_color(bf.color.CLOUD_WHITE)

    def do_when_added(self):
        # fond
        # self.root.add_child(bf.Image(""))

        self.root.add_child(bf.Debugger())

        # écriture des crédits
        credits = bf.Label(load_credits("data/assets/credits.txt")).set_text_size(28)
        self.root.add_child(credits)
        credits.set_center(*self.hud_camera.rect.midbottom)
        credits.set_y(self.hud_camera.get_position()[1])

    def update(self, dt):
        # défiler la caméra
        self.hud_camera.move_by(0, 63*dt)
