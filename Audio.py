import pygame
from pygame import mixer

mixer.init()

LEVEL1_BGM = "assets/audio/Moonlit.wav"
LEVEL2_BGM = "assets/audio/level2.mp3"
LEVEL3_BGM = "assets/audio/level3.mp3"
BOSS_BGM = "assets/audio/boss.mp3"
current_music = None


def play_music(path, volume=0.5, fade_ms=1000):
    global current_music

    if current_music == path:
        return

    current_music = path
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1, 0.0, fade_ms)


def stop_music(fade_ms=1000):
    global current_music

    pygame.mixer.music.fadeout(fade_ms)
    current_music = None

#sound

pickup = pygame.mixer.Sound("assets/audio/jump.wav")
pickup.set_volume(0.2)

health_recharge=pygame.mixer.Sound("assets/audio/potion.wav")
health_recharge.set_volume(0.3)

hurt_sound=pygame.mixer.Sound("assets/audio/hurt.mp3")
hurt_sound.set_volume(0.3)

punch_sound=pygame.mixer.Sound("assets/audio/punch.mp3")
punch_sound.set_volume(0.5)

ghost=pygame.mixer.Sound("assets/audio/ghost.mp3")
ghost.set_volume(0.2)

squirt=pygame.mixer.Sound("assets/audio/squirt.mp3")
squirt.set_volume(0.3)

fireball=pygame.mixer.Sound("assets/audio/fireball.mp3")
fireball.set_volume(0.3)

laser=pygame.mixer.Sound("assets/audio/laser.mp3")
laser.set_volume(0.4)

cry=pygame.mixer.Sound("assets/audio/cry.mp3")
cry.set_volume(0.3)

burnout=pygame.mixer.Sound("assets/audio/burnout.mp3")
burnout.set_volume(0.3)

tornado=pygame.mixer.Sound("assets/audio/tornado.mp3")
tornado.set_volume(0.3)

victory=pygame.mixer.Sound("assets/audio/victory.mp3")
victory.set_volume(0.5)