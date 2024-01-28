import batFramework as bf
from typing import Self
import pygame
from math import cos



class NPC(bf.Sprite):
    bubble = None
    def __init__(self)->None:
        super().__init__(None)
        self.cutscene : bf.Cutscene = None
        self.add_tags("npc")
        if NPC.bubble is None:
            NPC.bubble = pygame.Surface((64,32)).convert_alpha()
            NPC.bubble.fill((0,0,0,0))
            bubble_rect = NPC.bubble.get_rect()
            pygame.draw.rect(NPC.bubble,bf.color.CLOUD_WHITE,bubble_rect,0,20)
            pygame.draw.rect(NPC.bubble,bf.color.SILVER,bubble_rect,3,20)
            circle_size = 4
            pygame.draw.circle(NPC.bubble,bf.color.DARK_GRAY,bubble_rect.center,circle_size)
            pygame.draw.circle(NPC.bubble,bf.color.DARK_GRAY,bubble_rect.move(-14,0).center,circle_size)
            pygame.draw.circle(NPC.bubble,bf.color.DARK_GRAY,bubble_rect.move(14,0).center,circle_size)

    def is_close(self,rect)->bool:
        return self.rect.inflate(32,32).colliderect(rect)
    
    def set_cutscene(self,cutscene:bf.Cutscene)->Self:
        self.cutscene = cutscene
        return self
    def play_cutscene(self):
        if self.cutscene : bf.CutsceneManager().play(self.cutscene)
        
    def draw_bubble(self,camera):
        base = 92
        offset = 8 * cos(pygame.time.get_ticks() * 0.003)

        player = self.parent_scene.get_sharedVar("player")
        distance = (self.rect.move(-player.rect.centerx,-player.rect.centery).center)
        max_size = self.rect#.inflate(16,16)
        factor = abs(distance[0]) / (max_size[0]/2),abs(distance[1]) / (max_size[1]/2)
        NPC.bubble.set_alpha(255- 255 * (factor[0]+factor[1])/2)
        camera.surface.blit(NPC.bubble,camera.transpose(self.rect.move(-NPC.bubble.get_width()//2,-base-offset)).midtop)
        
    def draw(self,camera)->int:
        res = super().draw(camera)

        if res == 0 : return res
        player = self.parent_scene.get_sharedVar("player")
        if player is None: return res
        if self.is_close(player.rect):
            self.draw_bubble(camera)
        return res + 1
