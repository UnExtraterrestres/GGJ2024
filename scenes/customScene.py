import batFramework as bf
import pygame

class CustomScene(bf.Scene):
    def __init__(self,name:str)->None:
        super().__init__(name)

    def do_early_process_event(self,event)->bool:
        v = self.get_sharedVar("player_has_control",None)
        if v is not None and v == False :
            if event.type in [
                pygame.KEYDOWN,
                pygame.KEYUP,
                pygame.MOUSEMOTION,
                pygame.MOUSEBUTTONDOWN,
                pygame.MOUSEBUTTONUP
            ]:
                return True
        return False
