import batFramework as bf
import pygame
from scenes import *
from math import cos
bf.init(
    (640, 480),
    pygame.SCALED,
    default_text_size=16,
    resource_path='data',
    fps_limit=60,
    window_title="Coin Coin"
    )

bf.Tileset.load_tileset("assets/tilesets/tileset.png","main",gconst.TILE_SIZE)

class TilePickerScene(CustomScene):
    def __init__(self):
        super().__init__("pick")
        self.set_clear_color((0,0,0,128))
        self.add_actions(
            bf.Action("pick").add_key_control(pygame.K_p),
            bf.Action("click").add_mouse_control(1)
        )

    def do_on_enter(self):
        self.collision_toggle.set_value(self.get_sharedVar("tile").has_tag("collider"))
    
    def do_when_added(self):

        
        self.collision_toggle = bf.Toggle(
            "Collisions",
            callback = lambda val: self.get_sharedVar("tile").add_tags("collider") if val else  self.get_sharedVar("tile").remove_tags("collider")
        )
        self.collision_toggle.set_padding(8).set_color(bf.color.WASHED_BLUE).set_text_color(bf.color.CLOUD_WHITE)

        side_container = bf.Container(
            bf.Column(gap=10)
        )
        
        side_container.add_child(self.collision_toggle)


        side_panel = bf.Frame(10,10,fit_to_children = False).add_constraints(
            bf.ConstraintPercentageWidth(0.4),
            bf.ConstraintPercentageHeight(1),
            bf.ConstraintAnchorBottomRight()
        )

        side_panel.set_color(bf.color.DARK_BLUE).set_padding(10)
        side_panel.add_child(side_container)

        self.tileset_image = bf.Image("assets/tilesets/tileset.png")

        self.indicator = bf.Shape(gconst.TILE_SIZE,gconst.TILE_SIZE)

        self.indicator.set_outline_color(bf.color.DARK_GREEN).set_outline_width(4)


        self.root.add_child(
            self.tileset_image,
            self.indicator,
            side_panel,
            bf.BasicDebugger()
        )

        
    def do_on_enter(self):
        self.manager.get_scene_at(1).set_visible(True)

    def do_update(self,dt):
        if self.actions.is_active("pick"):
            self.manager.set_scene("editor")
            return 
            
        if self.actions.is_active("click"):
            x,y = self.hud_camera.convert_screen_to_world(*pygame.mouse.get_pos())
            if x >= 0 and x <= self.tileset_image.rect.w and y>= 0 and y<=self.tileset_image.rect.h:
                ix,iy = int(x//gconst.TILE_SIZE),int(y//gconst.TILE_SIZE)
                self.get_sharedVar("tile").set_index(ix,iy)                
        

        index = self.get_sharedVar("tile").tileset_position
        scaled = gconst.TILE_SIZE + abs(0.2 *gconst.TILE_SIZE * cos(pygame.time.get_ticks() * 0.01))
        self.indicator.set_size(scaled,scaled)
        pos = index[0]*gconst.TILE_SIZE,index[1]*gconst.TILE_SIZE
        pos = pos[0]+gconst.TILE_SIZE//2,pos[1]+gconst.TILE_SIZE//2
        interpolated = pos[0]+(pos[0]-self.indicator.rect.centerx)*dt,pos[1]+(pos[1]-self.indicator.rect.centery)*dt
        self.indicator.set_center(*interpolated)
        
        

class EditorScene(CustomScene):

    def __init__(self)->None:
        super().__init__("editor")
        self.set_clear_color(bf.color.RIVER_BLUE)

        self.current_tile = Tile().set_index(6,0)
        self.level = Level(200,40)
        self.add_world_entity(self.level,self.current_tile)
        self.actions = bf.DirectionalKeyControls()
        self.camera.set_min_zoom(0.1)
        self.add_actions(
            bf.Action("pick").add_key_control(pygame.K_p),
            bf.Action("click").add_mouse_control(1).set_holding(),
            bf.Action("m_click").add_mouse_control(2),
            bf.Action("right_click").add_mouse_control(3).set_holding(),
            bf.Action("save").add_key_control(pygame.K_s),
            bf.Action("open").add_key_control(pygame.K_o),
            bf.Action("control").add_key_control(pygame.K_LCTRL,pygame.K_RCTRL).set_holding(),
            bf.Action("more").add_key_control(pygame.K_z).set_holding(),
            bf.Action("minus").add_key_control(pygame.K_a).set_holding()
        )
        
        self.right_last_click : tuple[int,int] = (0,0)
        self.velocity = pygame.math.Vector2(0,0)
        self.camera_speed = 2
        self.flip_value = 0
    def do_when_added(self):
        self.root.add_child(bf.BasicDebugger())
        self.set_sharedVar("tile",self.current_tile)

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
        if self.actions.is_active("more"):
            self.camera.zoom_by(0.1)
        if self.actions.is_active("minus"):
            self.camera.zoom_by(-0.1)
            print(self.camera.zoom_factor)
        self.camera.move_by(*self.velocity)
        self.current_tile.set_center(*self.camera.convert_screen_to_world(*pygame.mouse.get_pos()))
        
        if self.actions.is_active("click"):
            x,y = self.level.convert_world_to_grid(*self.camera.convert_screen_to_world(*pygame.mouse.get_pos()))
            if self.level.is_out_of_bounds(x,y) : return

            t = self.level.get_tile(x,y)

            if t is not None and  t.to_json() == self.current_tile.to_json() : return 
            print(x,y)
            self.level.set_tile(x,y,self.current_tile.to_json())

        if self.actions.is_active("right_click"):
            x,y = self.level.convert_world_to_grid(*self.camera.convert_screen_to_world(*pygame.mouse.get_pos()))
            if self.level.is_out_of_bounds(x,y) : return
            self.level.remove_tile(x,y)

        if self.actions.is_active("m_click"):
            self.flip_value = (self.flip_value+1) %4
            self.current_tile.set_flip(self.flip_value & 1,self.flip_value & 2)

        if self.actions.is_active("control","save"):
            bf.ResourceManager().save_json_to_file("assets/level.json",self.level.to_json())
        if self.actions.is_active("control","open"):
            data = bf.ResourceManager().load_json_from_file("assets/level.json")
            self.level.from_json(data)
               
bf.Manager(EditorScene(),TilePickerScene()).run()
