import batFramework as bf




class Player(bf.AnimatedSprite):
    def __init__(self):
        super().__init__()

        self.speed = 60
        
        self.actions = bf.DirectionalKeyControls()

        self.add_animState("idle","assets/animations/player_run.png",(32,64),[4]*8)


    def do_process_actions(self,event)->None:
        self.actions.process_event(event)


    def do_reset_actions(self)->None:
        self.actions.reset()

    def do_update(self,dt):

        if self.velocity.length() < 0.1:
            self.velocity.update(0,0)
        else:
            self.velocity *= 0.8
            
        if self.actions.is_active("right"):
            self.velocity.x += self.speed
        if self.actions.is_active("left"):
            self.velocity.x -= self.speed

        self.move_by_velocity(dt)
