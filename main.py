import cProfile
import batFramework as bf
import pygame
import scenes

bf.init(
    (640, 480),
    pygame.SCALED,
    default_text_size=16,
    resource_path='data',
    default_font="fonts/p2p.ttf",
    fps_limit=60,
    window_title="Coin Coin"
    )

bf.Tileset.load_tileset("assets/tilesets/tileset.png", "main", scenes.gconst.TILE_SIZE)

bf.AudioManager().load_music("credits","credits.wav")
bf.AudioManager().load_music("witch","witch.wav")
bf.AudioManager().load_music("lutin","lutin.wav")

m = bf.Manager(
    scenes.TitleScene(),
    scenes.CreditScene(),
    scenes.MainScene(),
    scenes.MusicScene(),
    scenes.DialogueScene(),
    scenes.DialogueScene(),
    scenes.IntroScene(),
    scenes.CreditCreditScene(),
    scenes.PauseScene()
)

m.run()
