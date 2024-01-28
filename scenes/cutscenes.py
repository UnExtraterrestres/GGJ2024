import batFramework as bf
from .cutsceneBlocks import *


class Test(bf.Cutscene):
    def __init__(self):
        super().__init__()
        self.add_blocks(
            bf.FunctionBlock(lambda : print("START")),
            bf.FunctionBlock(lambda : bf.CutsceneManager().disable_player_control()),
            Say("HELLO GUYS ! what's up ?",1),
            SayKey("test",1),
            bf.FunctionBlock(lambda : bf.CutsceneManager().enable_player_control()),
            bf.FunctionBlock(lambda : print("END")),
            bf.FunctionBlock(lambda : bf.CutsceneManager().manager.set_scene("main"))
        )
