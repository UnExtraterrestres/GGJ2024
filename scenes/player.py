import batFramework as bf
import itertools
from .game_constants import GameConstants as gconst
def horizontal_movement(parent_entity: bf.AnimatedSprite, speed):
    if parent_entity.actions.is_active("right"):
        parent_entity.set_flipX(False)
    elif parent_entity.actions.is_active("left"):
        parent_entity.set_flipX(True)
    else:
        return
    if parent_entity.flipX:
        parent_entity.velocity.x = -speed
    else:
        parent_entity.velocity.x = speed


class Idle(bf.State):
    def __init__(self) -> None:
        super().__init__("idle")

    def on_enter(self):
        # self.parent_entity.set_animState("idle")
        pass

    def update(self, dt):
        if self.parent_entity.velocity.y > gconst.GRAVITY * 1.5 * dt:
            self.state_machine.set_state("fall")
            self.parent_entity.on_ground = False
            return
        if (
            self.parent_entity.actions.is_active("up")
            and self.parent_entity.on_ground
        ):
            self.state_machine.set_state("jump")

        elif self.parent_entity.actions.is_active(
            "right"
        ) or self.parent_entity.actions.is_active("left"):
            self.state_machine.set_state("run")


class Run(bf.State):
    def __init__(self) -> None:
        super().__init__("run")
        self.incrementer = (i for i in itertools.count())

    def on_enter(self):
        # self.parent_entity.set_animState("run")
        pass

    def update(self, dt):
        if self.parent_entity.velocity.y > gconst.GRAVITY * 1.5 * dt:
            self.state_machine.set_state("fall")
            self.parent_entity.on_ground = False
            return
        if not self.parent_entity.actions.is_active(
            "right"
        ) and not self.parent_entity.actions.is_active("left"):
            self.state_machine.set_state("idle")
            return
        if self.parent_entity.actions.is_active("up"):
            self.state_machine.set_state("jump")
            return
        horizontal_movement(self.parent_entity, self.parent_entity.h_movement_speed)
        # if next(self.incrementer) % 10 == 0:
            # bf.AudioManager().play_sound("step", 0.5)


class Fall(bf.State):
    def __init__(self) -> None:
        super().__init__("fall")
        # self.h_movement_speed = 50

    def on_enter(self):
        # self.parent_entity.set_animState("fall")
        pass

    def update(self, dt):
        if self.parent_entity.on_ground:
            self.state_machine.set_state(
                "idle" if self.parent_entity.velocity.x == 0 else "run"
            )
            return
        horizontal_movement(
            self.parent_entity, self.parent_entity.h_movement_speed * 1.2
        )


class Jump(bf.State):
    def __init__(self) -> None:
        super().__init__("jump")
        self._jumped = False

    def on_enter(self):
        # self.parent_entity.set_animState("jump")
        self._jumped = False

    def update(self, dt):
        if self.parent_entity.velocity.y >= 0 and self._jumped:
            self.state_machine.set_state("fall")
            return
        if not self._jumped :#and self.parent_entity.float_counter >= 4:
            self.parent_entity.velocity.y = -self.parent_entity.jump_force
            self._jumped = True
            self.parent_entity.on_ground = False
            # bf.AudioManager().play_sound("jump", 0.5)
        horizontal_movement(
            self.parent_entity, self.parent_entity.h_movement_speed * 1.2
        )



class Player(bf.AnimatedSprite):
    def __init__(self):
        super().__init__()

        
        self.actions = bf.DirectionalKeyControls()


        self.add_animState("idle","assets/animations/player_run.png",(32,64),[4]*8)

        self.state_machine: bf.StateMachine = bf.StateMachine(self)
        self.state_machine.add_state(Idle())
        self.state_machine.add_state(Run())
        self.state_machine.add_state(Jump())
        self.state_machine.add_state(Fall())
        self.state_machine.set_state("idle")

        self.h_movement_speed = 190
        self.jump_force = 500
        self.on_ground = False
        
    def do_process_actions(self,event)->None:
        self.actions.process_event(event)

    def do_reset_actions(self)->None:
        self.actions.reset()

    def do_update(self,dt):


        self.state_machine.update(dt)
        self.velocity.y = min(
            self.velocity.y + gconst.GRAVITY * dt, (gconst.GRAVITY // 3)
        )
        # self.velocity.y += gconst.GRAVITY*
            

        level = self.parent_scene.get_sharedVar("level")

        near_tiles = [t for t in level.get_neighboring(*level.convert_world_to_grid(*self.rect.center)) if t and t.has_tags("collider")]
        near_rects = [t.rect for t in near_tiles]
        self.rect.y += self.velocity.y *dt
        index = self.rect.collidelist(near_rects)
        if index >= 0 :
            collider = near_tiles[index]
            if self.velocity.y != 0:
                if self.velocity.y >= 0:
                    if not self.on_ground:
                        self.on_ground = True
                    self.rect.bottom = collider.rect.top
                else:
                    self.rect.top = collider.rect.bottom
                self.velocity.y= 0

        
        near_tiles = [t for t in level.get_neighboring(*level.convert_world_to_grid(*self.rect.center)) if t and t.has_tags("collider")]
        near_rects = [t.rect for t in near_tiles]
        self.rect.x += self.velocity.x *dt
        index = self.rect.collidelist(near_rects)
        if index >= 0 :
            collider = near_tiles[index]
            if self.velocity.x != 0:
                if self.velocity.x >= 0:
                    self.rect.right = collider.rect.left
                else:
                    self.rect.left = collider.rect.right
                self.velocity.x = 0

        
        self.velocity.x *= gconst.FRICTION


        if abs(self.velocity.x) < 0.02:
            self.velocity.x = 0
        if abs(self.velocity.y) < 0.02:
            self.velocity.y = 0





