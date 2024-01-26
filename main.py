import batFramework as bf
import pygame
import scenes

bf.init(
    (640, 480),
    pygame.SCALED,
    default_text_size=16,
    resource_path='data',
    fps_limit=60,
    window_title="Coin Coin"
    )


bf.Manager(
    scenes.MainScene(),
    scenes.DialogueScene()
).run()
