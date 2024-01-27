import batFramework as bf
import pygame
from scenes import *
bf.init(
    (640, 480),
    pygame.SCALED,
    default_text_size=16,
    resource_path='data',
    fps_limit=60,
    window_title="Coin Coin"
    )

bf.Tileset.load_tileset("assets/tilesets/tileset.png","main",gconst.TILE_SIZE)

class TilePickerScene(bf.Scene):
    def __init__(self):
        super().__init__("pick")
        self.set_clear_color((0,0,0,128))
        self.add_actions(bf.Action("pick").add_key_control(pygame.K_p))

    def do_when_added(self):
        self.root.add_child(bf.Image("assets/tilesets/tileset.png"))
        self.root.add_child(bf.BasicDebugger())

    def do_on_enter(self):
        self.manager.get_scene_at(1).set_visible(True)

    def do_update(self,dt):
        if self.actions.is_active("pick"):
            self.manager.set_scene("editor")

class EditorScene(bf.Scene):

    def __init__(self)->None:
        super().__init__("editor")
        self.set_clear_color(bf.color.RIVER_BLUE)

        self.current_tile = Tile()
        self.level = Level()
        self.level.set_tile(2,2,Tile().set_index(6,0).to_json())
        self.add_world_entity(self.level,self.current_tile)
        self.actions = bf.DirectionalKeyControls()
        self.add_actions(
            bf.Action("pick").add_key_control(pygame.K_p),
            bf.Action("click").add_mouse_control(1).set_holding(),
            bf.Action("m_click").add_mouse_control(2),
            bf.Action("right_click").add_mouse_control(3).set_holding(),
        )
        self.right_last_click : tuple[int,int] = (0,0)
        self.velocity = pygame.math.Vector2(0,0)
        self.camera_speed = 2
        self.flip_value = 0
    def do_when_added(self):
        self.root.add_child(bf.BasicDebugger())

    def do_update(self,dt):
        if self.actions.is_active("pick"):
            self.manager.set_scene("pick")
            return
        if self.velocity.length() < 0.1:
            self.velocity.update(0,0)
        else:
            self.velocity *= 0.8
            
        if self.actions.is_active("right"):
            self.velocity.x += self.camera_speed
        if self.actions.is_active("left"):
            self.velocity.x -= self.camera_speed
        if self.actions.is_active("down"):
            self.velocity.y += self.camera_speed
        if self.actions.is_active("up"):
            self.velocity.y -= self.camera_speed

        self.camera.move_by(*self.velocity)
        self.current_tile.set_center(*self.camera.convert_screen_to_world(*pygame.mouse.get_pos()))
        
        if self.actions.is_active("click"):
            x,y = self.level.convert_world_to_grid(*self.camera.convert_screen_to_world(*pygame.mouse.get_pos()))
            if self.level.is_out_of_bounds(x,y) : return

            t = self.level.get_tile(x,y)

            if t is not None and  t.to_json() == self.current_tile.to_json() : return 
            
            self.level.set_tile(x,y,self.current_tile.to_json())

        if self.actions.is_active("right_click"):
            x,y = self.level.convert_world_to_grid(*self.camera.convert_screen_to_world(*pygame.mouse.get_pos()))
            if self.level.is_out_of_bounds(x,y) : return
            self.level.remove_tile(x,y)

        if self.actions.is_active("m_click"):
            self.flip_value = (self.flip_value+1) %4
            self.current_tile.set_flip(self.flip_value & 1,self.flip_value & 2)
bf.Manager(EditorScene(),TilePickerScene()).run()
