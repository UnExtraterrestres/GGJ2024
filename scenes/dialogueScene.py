import batFramework as bf
from .customScene import CustomScene

class Test(bf.Cutscene):
    def __init__(self):
        super().__init__()
        self.add_blocks(
            bf.FunctionBlock(lambda : print("START")),
            bf.FunctionBlock(lambda : bf.CutsceneManager().disable_player_control()),
            bf.DelayBlock(5),
            bf.FunctionBlock(lambda : bf.CutsceneManager().enable_player_control()),
            bf.FunctionBlock(lambda : print("END"))
        )
class DialogueScene(CustomScene):

    def __init__(self):
        super().__init__("dialogue")
        self.set_clear_color((0,0,0,128))

        self.left_sprite = bf.Sprite(None)
        self.right_sprite = bf.Sprite(None)
        self.dialogue_box = bf.DialogueBox()
        self.dialogue_box.add_constraints(
            bf.ConstraintCenterX(),
            bf.ConstraintAnchorBottom(),
            bf.ConstraintPercentageWidth(0.8),
            bf.ConstraintPercentageHeight(0.3),
        )
        self.add_world_entity(self.left_sprite,self.right_sprite)
        self.root.add_child(self.dialogue_box)

    def do_when_added(self):
        b = bf.Button("MAIN",lambda : self.manager.set_scene("main"))
        b.add_constraints(bf.ConstraintCenter())
        b2 = bf.Button("PLAY",lambda : bf.CutsceneManager().play(Test()))
        b2.add_constraints(bf.ConstraintCenterY(),bf.ConstraintAnchorRight())
        self.root.add_child(b)
        self.root.add_child(b2)
        self.root.add_child(bf.BasicDebugger())

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

    def next(self)->None:
        self.dialogue_box.next_message()

    def say(self,message)->None:
        self.dialogue_box.say(message)
