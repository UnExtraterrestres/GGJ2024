import batFramework as bf


class MainScene(bf.Scene):

    def __init__(self):
        super().__init__("main")

    def do_when_added(self):
        self.root.add_child(bf.BasicDebugger())
