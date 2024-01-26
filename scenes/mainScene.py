import batFramework as bf


class MainScene(bf.Scene):

    def __init__(self):
        super().__init__("main")
        self.set_clear_color(bf.color.RIVER_BLUE)

    def do_when_added(self):
        b = bf.Button("DIALOGUE",lambda : self.manager.set_scene("dialogue"))
        self.root.add_child(b, bf.BasicDebugger())
