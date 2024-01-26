import batFramework as bf


class DialogueScene(bf.Scene):

    def __init__(self):
        super().__init__("dialogue")
        self.set_clear_color((0,0,0,128))

        self.left_sprite = bf.Sprite(None)
        self.left_sprite = bf.Sprite(None)
        self.dialogue_box = bf.DialogueBox()




    def do_when_added(self):
        b = bf.Button("MAIN",lambda : self.manager.set_scene("main")).add_constraints(bf.ConstraintCenter())

        self.root.add_child()

        self.root.add_child(b, bf.BasicDebugger())

    def clear(self)->None:
        self.left_sprite.set_visible(False)
        self.right_sprite.set_visible(False)
        self.dialogue_box.clear()
    def do_on_enter(self):
        s = self.manager.get_scene("main")
        s.set_visible(True)


    def set_left_sprite(self,file_name : str|None):
        if file_name is None : 
            self.left_sprite.set_visible(False)
        else:
            self.left_sprite.set_image(file_name)
    def set_right_sprite(self,file_name):
        if file_name is None : 
            self.right_sprite.set_visible(False)
        else:
            self.right_sprite.set_image(file_name) 
