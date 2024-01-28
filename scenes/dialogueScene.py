import batFramework as bf
from .customScene import CustomScene
from .cutscenes import *


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

        def stylize_label(entity):
            entity.set_color(bf.color.DARK_BLUE)
            entity.set_outline_color(bf.color.WASHED_BLUE)
            entity.set_outline_width(3).set_border_radius((0,0,20,0))
            entity.set_text_color(bf.color.CLOUD_WHITE)

        stylize_label(self.dialogue_box)
        self.dialogue_box.set_padding((20,20))

        self.name_tag = bf.Label("HELLO")      
        stylize_label(self.name_tag)
        self.add_world_entity(self.left_sprite,self.right_sprite)
        self.root.add_child(self.dialogue_box,self.name_tag)
        self.name_tag.set_border_radius((0,4,4,0)).set_padding((20,10))
        self.name_tag.set_position(*self.dialogue_box.rect.move(0,-self.name_tag.rect.h+3).topleft)  



    def do_when_added(self):
        b = bf.Button("MAIN",lambda : self.manager.set_scene("main"))
        b.add_constraints(bf.ConstraintCenter())
        self.set_sharedVar("dialogues",bf.ResourceManager().load_json_from_file("assets/dialogues.json"))
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

    def next_message(self)->None:
        self.dialogue_box.next_message()

    def say(self,message)->None:
        self.dialogue_box.say(message)
