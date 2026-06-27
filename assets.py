import pygame
import animation
import Constants as cons
from Character_types import NORMAL_DEMON,RANGED_DEMON,CHARGE_DEMON,RUNNER_DEMON,FLYING_DEMON,BOSS

def load_static_assets():
    assets = {}

    # Buttons
    assets["start_img"] = pygame.image.load("assets/buttons/start_btn.png").convert()
    assets["resume_img"] = pygame.image.load("assets/buttons/resume_btn.png").convert()
    assets["exit_img"] = pygame.image.load("assets/buttons/exit_btn.jpg").convert()
    assets["restart_img"] = pygame.image.load("assets/buttons/restart_btn.png").convert()

    # Backgrounds
    bg_img = pygame.image.load("assets/Background/Night/1.png").convert()
    bg_img_building = pygame.image.load("assets/Background/Night/2.png").convert()

    assets["bg_img"] = pygame.transform.scale(
        bg_img,
        (cons.SCREEN_WIDTH, cons.SCREEN_HEIGHT)
    )

    assets["bg_img_building"] = pygame.transform.scale(
        bg_img_building,
        (cons.SCREEN_WIDTH, cons.SCREEN_HEIGHT)
    )

    # Items
    assets["cake_img"] = pygame.image.load("assets/food/Icon21_03.png").convert_alpha()
    assets["coffee_img"] = pygame.image.load("assets/food/Icon21_11.png").convert_alpha()
    assets["money_img"] = pygame.image.load("assets/items/Money.png").convert_alpha()
    assets["money_icon_img"] = pygame.image.load("assets/items/moneyicon.png").convert_alpha()
    assets["potion_img"] = pygame.image.load("assets/items/potion_red.png").convert_alpha()

    assets["money_icon_img"] = pygame.transform.scale(
        assets["money_icon_img"],
        (64, 64)
    )

    # Weapons
    assets["bow_image"] = pygame.image.load("assets/weapon/bow.png").convert_alpha()
    assets["arrow_image"] = pygame.image.load("assets/weapon/arrow.png").convert_alpha()
    assets["fire_ball_image"] = pygame.image.load("assets/weapon/fireball.png").convert_alpha()
    assets["charge_image"] = pygame.image.load("assets/weapon/Charge.png").convert_alpha()

    # Fonts
    assets["font"] = pygame.font.Font("assets/font/AtariClassic.ttf", 20)
    assets["smaller_font"] = pygame.font.Font("assets/font/AtariClassic.ttf", 15)
    assets["JAPA_font"] = pygame.font.Font("assets/font/NotoSansJP-Bold.ttf", 23)

    return assets

NORMAL_DEMON = '1'
RANGED_DEMON = '2'
CHARGE_DEMON = '3'
RUNNER_DEMON = '4'
FLYING_DEMON = '5'
BOSS = 'Boss'


L1_WAVES = [
    [(animation.Demon1_animations, NORMAL_DEMON, 1)],

    
     [
         (animation.Demon1_animations, NORMAL_DEMON, 2),
         (animation.Demon4_animations, RUNNER_DEMON, 1),
     ],
     [
         (animation.Demon1_animations, NORMAL_DEMON, 2),
         (animation.Demon4_animations, RUNNER_DEMON, 2),
     ],
]


L2_WAVES = [
    [
        (animation.Demon1_animations, NORMAL_DEMON, 2),
        (animation.Demon3_animations, CHARGE_DEMON, 2),
    ],

    
     [
         (animation.Demon1_animations, NORMAL_DEMON, 2),
         (animation.Demon2_animations, RANGED_DEMON, 1),
     ],
     [
         (animation.Demon1_animations, NORMAL_DEMON, 2),
         (animation.Demon2_animations, RANGED_DEMON, 1),
         (animation.Demon3_animations, CHARGE_DEMON, 1),
     ],
]


L3_WAVES = [
    [
        #(animation.Demon1_animations, NORMAL_DEMON, 2),
        #(animation.Demon5_animations, FLYING_DEMON, 2),
    ],

    
     [
         #(animation.Demon5_animations, FLYING_DEMON, 1),
     ],
     [
         #(animation.Demon4_animations, RUNNER_DEMON, 2),
         (animation.Demon5_animations, FLYING_DEMON, 2),
     ],
]


L3_BOSS = [
    [
        (animation.Boss_animations, BOSS, 1),
    ],
]