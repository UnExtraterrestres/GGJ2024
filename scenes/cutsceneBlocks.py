import batFramework as bf

class Say(bf.CutsceneBlock):
    def __init__(self,message,delay:int|None=None):
        super().__init__()
        self.message = message
        self.delay = delay
        self.timer = None
        if delay is not None:
            self.timer = bf.Timer(duration=delay,end_callback = self.end)
        self.waiting:bool = False
    def start(self):
        super().start()
        self.scene_link = bf.CutsceneManager().manager.get_scene("dialogue")
        self.scene_link.say(self.message)

    def next_message(self):
        self.scene_link.next_message()
        if self.scene_link.dialogue_box.is_queue_empty():
            self.end()
    def update(self,dt):
                    
        if self.scene_link.dialogue_box.is_current_message_over() and self.delay and not self.waiting:
            bf.Timer(duration = self.delay,end_callback=self.next_message).start()
            self.waiting = True
            return
class SayKey(Say):

    def start(self):
        bf.CutsceneBlock.start(self)
        self.scene_link = bf.CutsceneManager().manager.get_scene("dialogue")
        messages = bf.CutsceneManager().manager.get_sharedVar("dialogues",None)
        if messages is None : self.end()
        self.message= messages[self.message]
        self.scene_link.say(self.message)
