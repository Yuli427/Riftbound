import pygame
import csv
import json
import os
import random
import Constants as cons
import animation
import UI
from Character import Character
from Weapon import Weapon,Tornado,FireHazard
from Effects import dagameText
from item import Item
from World import World
from Button import Button
from Alliance import Alliance as All


pygame.init()

game_name='Nakana'
#open a window
screen=pygame.display.set_mode((cons.SCREEN_WIDTH,cons.SCREEN_HEIGHT))
pygame.display.set_caption(game_name)

#create clock for frame rate
clock= pygame.time.Clock()

#define game variables
start_game=False
pause_game=False
game_over=False
tileset_path = 'assets/object/obj.tsj'
tileset_dir = os.path.dirname(tileset_path)
start_intro=False
opening_intro=False
is_shopmenu=False
show_goal_dialog_l1=False
show_goal_dialog_l2=False
show_goal_dialog_l3=False
is_purchased=False
not_purchased=False

level_complete_shop = False
pending_level_load = False

opening_intro_timer=cons.INTRO_TIMER
game_over_timer=cons.GAME_OVER_TIMER
victory_timer=cons.VICTORY_TIMER

is_alived_agian=False
potion_spawned=False
is_dialog_active=False
wants_close_dialog=False
dialog_message=''
show_dialog_timer=3000

was_freezed = False
#initial choices
player_name = ''
selected_gender = 'Female'
choosing = True

enemy1_cooldown=random.randint(3000,5000)
enemy2_cooldown=0
enemy3_cooldown=0
enemy4_cooldown=0
enemy5_cooldown=0

item_spawn_cooldown=random.randint(3000,5000)

num_of_enemy_killed=0
enemy_left=0

enemy1_counter=0
enemy2_counter=0
enemy3_counter=0
enemy4_counter=0

current_wave = 0        # 当前是第几波（0表示还没开始）
wave_active = False     # 当前波是否正在进行
wave_cleared = False    # 当前波是否清完了
is_boss_spawned=False
phase2_triggered=False
turnado_spawn_timer=0
fire_spawn_timer=0





L1_WAVES = [
    [(animation.Demon1_animations, '1', 2)],
    [(animation.Demon1_animations, '1', 2),
     (animation.Demon4_animations, '4', 1)],
    [(animation.Demon1_animations, '1', 2),
     (animation.Demon4_animations, '4', 2)],
]

L2_WAVES = [
    [(animation.Demon1_animations, '1', 2),
     (animation.Demon2_animations, '2', 1)],
    [(animation.Demon1_animations, '1', 2),
     (animation.Demon2_animations, '2', 1),
     (animation.Demon3_animations, '3', 1)],
    [(animation.Demon2_animations, '2', 2),
     (animation.Demon3_animations, '3', 2)],
]

L3_WAVES = [
    [(animation.Demon1_animations, '1', 2),
     (animation.Demon5_animations, '5', 1)],
    [(animation.Demon4_animations, '4', 2),
     (animation.Demon5_animations, '5', 2)],
    [(animation.Demon1_animations, '1', 2),
     (animation.Demon4_animations, '4', 1),
     (animation.Demon5_animations, '5', 2)],
]
L3_BOSS=[[(animation.Boss_animations,'Boss',1),],]
   
#define player movement variable
moving_left=False
moving_up=False
moving_right=False
moving_down=False
is_attacking=False
is_dashing=False
is_changing_character=False
is_jumping=False
current_level='1'
is_level1=True
is_level2=False
is_level3=False

#load button image
start_img=pygame.image.load("assets/buttons/start_btn.png").convert()
resume_img=pygame.image.load("assets/buttons/resume_btn.png").convert()
exit_img=pygame.image.load("assets/buttons/exit_btn.jpg").convert()
restart_img=pygame.image.load("assets/buttons/restart_btn.png").convert()
#load background img
bg_img = pygame.image.load("assets/Background/Night/1.png").convert()
bg_img_building = pygame.image.load("assets/Background/Night/2.png").convert()
#scale background
bg_img=pygame.transform.scale(bg_img,(cons.SCREEN_WIDTH,cons.SCREEN_HEIGHT))
bg_img_building=pygame.transform.scale(bg_img_building,(cons.SCREEN_WIDTH,cons.SCREEN_HEIGHT))


#load items
cake_img=pygame.image.load('assets/food/Icon21_03.png').convert_alpha()
coffee_img=pygame.image.load('assets/food/Icon21_11.png').convert_alpha()
money_img=pygame.image.load('assets/items/Money.png').convert_alpha()
money_icon_img=pygame.image.load('assets/items/moneyicon.png').convert_alpha()
potion_img=pygame.image.load('assets/items/potion_red.png').convert_alpha()
money_icon_img = pygame.transform.scale(money_icon_img, (64, 64))
#load weapon
bow_image= pygame.image.load('assets/weapon/bow.png').convert_alpha()
arrow_image=pygame.image.load('assets/weapon/arrow.png').convert_alpha()
fire_ball_image=pygame.image.load('assets/weapon/fireball.png').convert_alpha()
charge_image=pygame.image.load('assets/weapon/Charge.png').convert_alpha()

#load font
font=pygame.font.Font('assets/font/AtariClassic.ttf',20)
smaller_font=pygame.font.Font('assets/font/AtariClassic.ttf',15)
JAPA_font=pygame.font.Font('assets/font/NotoSansJP-Bold.ttf',23)
#load tile
tile_list=[]
if is_level1:
    for x in range(cons.TILE_TYPES):
        if is_level1:
            #tile_image=pygame.image.load(f'assets/tiles/{x}.png').convert_alpha()
            tile_image=pygame.image.load(f'assets/level1_background_tile/Tile_{x+1:02d}.png').convert_alpha()
            #tile_image=pygame.transform.scale(tile_image,(cons.TILE_SIZE,cons.TILE_SIZE))
            tile_list.append(tile_image)
elif is_level2:
    for x in range(cons.TILE_TYPES):
        tile_image=pygame.image.load(f'assets/level2_background_tile/Tiles_{x+1:02d}.png').convert_alpha()
        #tile_image=pygame.transform.scale(tile_image,(cons.TILE_SIZE,cons.TILE_SIZE))
        tile_list.append(tile_image)
else:
   for x in range(cons.TILE_TYPES):
        tile_image=pygame.image.load(f'assets/level3_background_tile/Tile_{x+1:02d}.png').convert_alpha()
        #tile_image=pygame.transform.scale(tile_image,(cons.TILE_SIZE,cons.TILE_SIZE))
        tile_list.append(tile_image)

obj_tile_list=[] 
if is_level1:   
    for x in range(26):
    
            #tile_image=pygame.image.load(f'assets/tiles/{x}.png').convert_alpha()
            tile_image=pygame.image.load(f'assets/level1_obj_tile/{x+1}.png').convert_alpha()
            #tile_image=pygame.transform.scale(tile_image,(cons.TILE_SIZE,cons.TILE_SIZE))
            obj_tile_list.append(tile_image)
elif  is_level2:
    for x in range(26):
        #tile_image=pygame.image.load(f'assets/tiles/{x}.png').convert_alpha()
        tile_image=pygame.image.load(f'assets/level2_obj_tile/{x}.png').convert_alpha()
        #tile_image=pygame.transform.scale(tile_image,(cons.TILE_SIZE,cons.TILE_SIZE))
        obj_tile_list.append(tile_image)

else:
     for x in range(41):
        #tile_image=pygame.image.load(f'assets/tiles/{x}.png').convert_alpha()
        tile_image=pygame.image.load(f'assets/level3_obj_tile/{x+1}.png').convert_alpha()
        #tile_image=pygame.transform.scale(tile_image,(cons.TILE_SIZE,cons.TILE_SIZE))
        obj_tile_list.append(tile_image)




#WORLD(BACK GROUND)
world_data=[]
#column*row
for row in range (cons.ROWS):
   r=[-1]*cons.COLUMN
   world_data.append(r)
#load in level data and create a world
if is_level1:
    with open('levels/l1/level1_background.csv', newline='') as csvfile:
        #delimiter is what sperate it
        reader= csv.reader(csvfile,delimiter=',')
        for y,row in enumerate(reader):
            for x,tile in enumerate(row):
                world_data[y][x]=int(tile)
elif is_level2:
   with open('levels/l2/level2_background.csv', newline='') as csvfile:
        #delimiter is what sperate it
        reader= csv.reader(csvfile,delimiter=',')
        for y,row in enumerate(reader):
            for x,tile in enumerate(row):
                world_data[y][x]=int(tile)
else:
    with open('levels/l3/level3_background.csv', newline='') as csvfile:
        #delimiter is what sperate it
        reader= csv.reader(csvfile,delimiter=',')
        for y,row in enumerate(reader):
            for x,tile in enumerate(row):
                world_data[y][x]=int(tile)

layer_data=[]
for row in range (cons.ROWS):
   r=[-1]*cons.COLUMN
   layer_data.append(r)
with open('levels/l2/level2_layer.csv', newline='') as csvfile:
        #delimiter is what sperate it
        reader= csv.reader(csvfile,delimiter=',')
        for y,row in enumerate(reader):
            for x,tile in enumerate(row):
                layer_data[y][x]=int(tile)



#COLLISION TILES
platform_data = []
#column*row
for row in range (cons.ROWS):
   r=[-1]*cons.COLUMN
   platform_data.append(r)
if is_level1:
    #load in level data and create a world
    with open('levels/l1/level1_Platform.csv', newline='') as csvfile:
        #delimiter is what sperate it
        reader= csv.reader(csvfile,delimiter=',')
        for y,row in enumerate(reader):
            for x,tile in enumerate(row):
                platform_data[y][x]=int(tile)
elif is_level2:
       #load in level data and create a world
    with open('levels/l2/level2_Platform.csv', newline='') as csvfile:
        #delimiter is what sperate it
        reader= csv.reader(csvfile,delimiter=',')
        for y,row in enumerate(reader):
            for x,tile in enumerate(row):
                platform_data[y][x]=int(tile)
else:
    with open('levels/l3/level3_Platform.csv', newline='') as csvfile:
        #delimiter is what sperate it
        reader= csv.reader(csvfile,delimiter=',')
        for y,row in enumerate(reader):
            for x,tile in enumerate(row):
                platform_data[y][x]=int(tile)

#OBJECT TILES
object_data = []
#column*row
for row in range (cons.ROWS):
   r=[-1]*cons.COLUMN
   object_data.append(r)
if is_level1:
    #load in level data and create a world
    with open('levels/l1/level1_Objects.csv', newline='') as csvfile:
        #delimiter is what sperate it
        reader= csv.reader(csvfile,delimiter=',')
        for y,row in enumerate(reader):
            for x,tile in enumerate(row):
                object_data[y][x]=int(tile)
elif is_level2:
       #load in level data and create a world
    with open('levels/l2/level2_Objects.csv', newline='') as csvfile:
        #delimiter is what sperate it
        reader= csv.reader(csvfile,delimiter=',')
        for y,row in enumerate(reader):
            for x,tile in enumerate(row):
                object_data[y][x]=int(tile)
else:
     with open('levels/l3/level3_Objects.csv', newline='') as csvfile:
        #delimiter is what sperate it
        reader= csv.reader(csvfile,delimiter=',')
        for y,row in enumerate(reader):
            for x,tile in enumerate(row):
                object_data[y][x]=int(tile)



# #LOAD JSON
# object_images={}
# with open ('assets/object/obj.tsj','r',encoding='utf-8') as f:
#     object_data=json.load(f)
# for img in object_data['tiles']:
#     tile_id=img['id']
#     img_path=img['image']
#     full_path=os.path.normpath(os.path.join(tileset_dir,img_path))
#     image=pygame.image.load(full_path).convert_alpha()
#     object_images[tile_id]=image
    



#create world
world=World()
world.process_data(world_data,layer_data,object_data,platform_data,tile_list,obj_tile_list,is_level2,is_level1)

spawn_tile = []
tile_set = {(tile.centerx, tile.top) for tile in world.obstacle_tiles}
for tile in world.obstacle_tiles:
    cx = tile.centerx
    top = tile.top
    left1  = (cx - cons.TILE_SIZE, top) in tile_set
    right1 = (cx + cons.TILE_SIZE, top) in tile_set
    if left1 or right1:
        spawn_tile.append((tile.centerx, tile.top - cons.ENEMY_HEIGHT))

Tornado_spawn_tile=[]
tile_set = {(tile.centerx, tile.top) for tile in world.obstacle_tiles}
for tile in world.obstacle_tiles:
    cx = tile.centerx
    top = tile.top
    left1  = (cx - cons.TILE_SIZE, top) in tile_set
    left2  = (cx - cons.TILE_SIZE*2, top) in tile_set
    left3  = (cx - cons.TILE_SIZE*3, top) in tile_set
    right1 = (cx + cons.TILE_SIZE, top) in tile_set
    right2 = (cx + cons.TILE_SIZE*2, top) in tile_set
    right3 = (cx + cons.TILE_SIZE*3, top) in tile_set

    right_ok=right1 and right2 and right3
    left_ok=left1 and left2 and left3
    if right_ok or left_ok:
        Tornado_spawn_tile.append((tile.centerx, tile.top))

#create enemy
#enemy=Character(200,700,100,animation.Demon1_animations,'1')
#boss=Character(600,700,100,animation.Demon3_animations,'Boss')

#create enemy list
enemy_list=[]
#enemy_list.append(enemy)
#enemy_list.append(boss)


#create weapon
#bow= Weapon(bow_image,arrow_image,None,False)


#cake=Item(200,330,'0',cake_img,None,False)
coffee=Item(32,400,'1',coffee_img,None,False)
money_icon=Item(30,25,'0',money_icon_img,None,True)
#score_cake=Item(cons.SCREEN_WIDTH-220,25,'0',cake_img,None,True)
Rin=All(450,700,'Rin',animation.Rin_animations)
Vesper=All(450,700,'Vesper',animation.Vesper_animations)
Fuma=All(450,700,'Fuma',animation.Fuma_animations)
Ares=All(450,700,'Ares',animation.Ares_animations)
#default
alliance=Rin
#create sprite groups
alliance_group=pygame.sprite.Group()
arrow_group=pygame.sprite.Group()
dagame_Text_group=pygame.sprite.Group()
item_group=pygame.sprite.Group()
fire_ball_group=pygame.sprite.Group()
charge_group=pygame.sprite.Group()
Tornado_group=pygame.sprite.Group()
Fire_hazard_group=pygame.sprite.Group()
#item_group.add(cake)
item_group.add(money_icon)
fire_ball_group.add()
alliance_group.add()


#create screen fade 
intro_fade=UI.ScreenFade(1,(0,0,0),7)
death_fade=UI.ScreenFade(2,(0,0,0),7)

#create text
vertical_text=UI.Text(452,130,'未\n来\nの\n世\n界',JAPA_font,cons.WHITE)


#Level_text=UI.Text(10,15,f'Level:{level}',font,cons.PINK)
#create buttons
restart_button=Button(cons.SCREEN_WIDTH//2-145,cons.SCREEN_HEIGHT//2-50,restart_img)
start_button=Button(cons.SCREEN_WIDTH//2-145,cons.SCREEN_HEIGHT//2-150,start_img)
resume_button=Button(cons.SCREEN_WIDTH//2-145,cons.SCREEN_HEIGHT//2-150,resume_img)
exit_button=Button(cons.SCREEN_WIDTH//2-145,cons.SCREEN_HEIGHT//2+50,exit_img)
#main game loop
game_run=True


def reset_level(world, player, enemy_list, fireballs, charge, dagame_Text_group, item_group,
                world_data, object_data, platform_data, tile_list, obj_tile_list):
    
    global show_dialog_timer
    global is_dialog_active
    global is_purchased
    global current_wave
    global wave_active
    global enemy_left
    global is_level1
    global is_level2
    global is_level3
    show_dialog_timer=3000
    is_purchased=False
    is_dialog_active=False
    enemy_left=0
    current_wave = 0
    wave_active = False
    enemy_list.clear()
    fireballs.empty()
    charge.empty()
    dagame_Text_group.empty()
    item_group.empty()
    item_group.add(money_icon)
    Fire_hazard_group.empty()
    Tornado_group.empty()
    

    # 重新读CSV
    def read_csv(path):
        data = [[-1] * cons.COLUMN for _ in range(cons.ROWS)]
        with open(path, newline='') as f:
            for y, row in enumerate(csv.reader(f)):
                for x, tile in enumerate(row):
                    data[y][x] = int(tile)
        return data

    if is_level1:
        new_world_data    = read_csv('levels/l1/level1_background.csv')
        new_platform_data = read_csv('levels/l1/level1_Platform.csv')
        new_object_data   = read_csv('levels/l1/level1_Objects.csv')
        new_layer_data = [[-1] * cons.COLUMN for _ in range(cons.ROWS)] #empty
    elif is_level2:
        new_world_data    = read_csv('levels/l2/level2_background.csv')
        new_platform_data = read_csv('levels/l2/level2_Platform.csv')
        new_object_data   = read_csv('levels/l2/level2_Objects.csv')
        new_layer_data    = read_csv('levels/l2/level2_layer.csv')
    else:
        new_world_data    = read_csv('levels/l3/level3_background.csv')
        new_platform_data = read_csv('levels/l3/level3_Platform.csv')
        new_object_data   = read_csv('levels/l3/level3_Objects.csv')
        new_layer_data = [[-1] * cons.COLUMN for _ in range(cons.ROWS)]

    # 重新加载tile图片
    tile_list.clear()
    obj_tile_list.clear()
    if is_level1:
        for x in range(cons.TILE_TYPES):
            tile_list.append(pygame.image.load(f'assets/level1_background_tile/Tile_{x+1:02d}.png').convert_alpha())
        for x in range(26):
            obj_tile_list.append(pygame.image.load(f'assets/level1_obj_tile/{x+1}.png').convert_alpha())
    elif is_level2:
        for x in range(cons.TILE_TYPES):
            tile_list.append(pygame.image.load(f'assets/level2_background_tile/Tiles_{x+1:02d}.png').convert_alpha())
        for x in range(26):
            obj_tile_list.append(pygame.image.load(f'assets/level2_obj_tile/{x}.png').convert_alpha())
    else:
        for x in range(cons.TILE_TYPES):
            tile_list.append(pygame.image.load(f'assets/level3_background_tile/Tile_{x+1:02d}.png').convert_alpha())
        for x in range(41):
            obj_tile_list.append(pygame.image.load(f'assets/level3_obj_tile/{x+1}.png').convert_alpha())

    # 重建世界
    world.map_tiles.clear()
    world.object_tiles.clear()
    world.obstacle_tiles.clear()


    world.process_data(new_world_data, new_layer_data, new_object_data, new_platform_data,
                       tile_list, obj_tile_list, is_level2, is_level1)
    
    world.scroll_x = 0
    world.scroll_y = 0

    # enemy spwan
    global spawn_tile
    spawn_tile = []
    tile_set = {(tile.centerx, tile.top) for tile in world.obstacle_tiles}
    for tile in world.obstacle_tiles:
        cx = tile.centerx
        top = tile.top
        left1  = (cx - cons.TILE_SIZE, top) in tile_set
        right1 = (cx + cons.TILE_SIZE, top) in tile_set
        if left1 or right1:
            spawn_tile.append((tile.centerx, tile.top - cons.ENEMY_HEIGHT))
    
    #fire and tornado spawn
    global Tornado_spawn_tile
    Tornado_spawn_tile=[]
    tile_set = {(tile.centerx, tile.top) for tile in world.obstacle_tiles}
    for tile in world.obstacle_tiles:
        cx = tile.centerx
        top = tile.top
        left1  = (cx - cons.TILE_SIZE, top) in tile_set
        left2  = (cx - cons.TILE_SIZE*2, top) in tile_set
        left3  = (cx - cons.TILE_SIZE*3, top) in tile_set
        right1 = (cx + cons.TILE_SIZE, top) in tile_set
        right2 = (cx + cons.TILE_SIZE*2, top) in tile_set
        right3 = (cx + cons.TILE_SIZE*3, top) in tile_set

        right_ok=right1 and right2 and right3
        left_ok=left1 and left2 and left3
        if right_ok or left_ok:
            Tornado_spawn_tile.append((tile.centerx, tile.top))

    # 重置玩家
    player.rect.center = (200, 700)
    player.vel_y = 0
    player.health = 100
    player.alive = True
    player.hit = False
    player.stunned = False
    player.player_state = 'Idle'
    #player.score = 0

   
 
    

while choosing:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and player_name:
                choosing = False
            elif event.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]
            elif event.key == pygame.K_LEFT:
                selected_gender = 'Male'
            elif event.key == pygame.K_RIGHT:
                selected_gender = 'Female'
            else:
                if len(player_name) < 12:  
                    player_name += event.unicode
    
    #create player
    if selected_gender=='Female':
        player=Character(200,700,75,animation.School_girl_animations,'0')
    else:
        player=Character(200,700,75,animation.School_boy1_animations,'0')
    screen.fill(cons.BACK_GROUND)
    UI.draw_choose_menu(screen, font, player_name, selected_gender, game_name,True)
    name_text=UI.Text(200,15,player_name,font,cons.PURPLE)
    pygame.display.update()
    
    
while game_run:
    
    #control frame rate
    delta_time=clock.tick(cons.FPS)

    if start_game==False:
        screen.fill((0,0,0))
        if (start_button.draw(screen)):
            start_game=True
            #播放开场淡入动画
            start_intro=True
        #it become true only when hit the button, so we call draw method here to check the collision
        if(exit_button.draw(screen)):
            game_run=False
    elif is_shopmenu==True:
        if victory_timer>0:
            UI.draw_victory(screen,font)
            victory_timer-=delta_time
        if victory_timer<=0:
                screen.fill((0,0,0))
                UI.draw_shop_menu(screen, smaller_font, player.score,current_level)
                if is_purchased==True and alliance.name== 'Rin' :
                     player.score-=cons.Fujiwara_Rin
                     alliance_group.empty()
                     is_shopmenu=False
                     alliance_group.add(Rin)
                elif is_purchased==True and alliance.name== 'Vesper' :
                     player.score-=cons.Vesper
                     alliance_group.empty()
                     is_shopmenu=False
                     alliance_group.add(Vesper)
                elif is_purchased==True and alliance.name== 'Fuma' :
                     player.score-=cons.Himura
                     alliance_group.empty()
                     is_shopmenu=False
                     alliance_group.add(Fuma)
                elif is_purchased==True and alliance.name=='Ares' :
                     player.score-=cons.Ares
                     alliance_group.empty()
                     is_shopmenu=False
                     alliance_group.add(Ares)
                        #check if the level is complete
                elif not_purchased:
                    is_shopmenu=False

                if level_complete_shop and not is_shopmenu:
                        level_complete_shop=False
                        opening_intro=True
                        victory_timer=cons.VICTORY_TIMER
                        

    elif is_dialog_active:
       if is_boss_spawned==True and current_level=='3':
           UI.draw_dialog(screen, font, alliance, 'The final BOSS has arrived!')
       elif show_goal_dialog_l1 and current_level=='1':
           UI.draw_dialog(screen, font, alliance, f'Goal: Eliminate all enemies and obtain {cons.L1_GOAL}. Remember you need to find them if you can\'t see them...')
       elif show_goal_dialog_l2 and current_level=='2':
           UI.draw_dialog(screen, font, alliance, f'Goal: Eliminate all enemies and obtain {cons.L2_GOAL}.')
       elif show_goal_dialog_l3 and current_level=='3':
           UI.draw_dialog(screen, font, alliance, 'Goal: Eliminate all enemies.')
       else:
           UI.draw_dialog(screen,font,alliance,dialog_message)
       if wants_close_dialog:
          is_dialog_active=False
          wants_close_dialog=False

    elif opening_intro:
         #if start intro=true fade screen
                if opening_intro_timer>0:
                  opening_intro_timer-=delta_time
                  UI.draw_text_screen(screen,font,'Loading...')
                  if opening_intro_timer<=0:
                        opening_intro=False
                        opening_intro_timer=cons.INTRO_TIMER
                        if current_level=='1':
                            is_level1=False 
                            is_level2=True
                            current_level='2'  
                            reset_level(world,player,enemy_list,fire_ball_group,charge_group,dagame_Text_group,item_group,world_data,object_data,platform_data,tile_list,obj_tile_list)
                        elif current_level=='2':
                            is_level2=False
                            is_level3=True
                            current_level='3'
                            reset_level(world,player,enemy_list,fire_ball_group,charge_group,dagame_Text_group,item_group,world_data,object_data,platform_data,tile_list,obj_tile_list) 
    elif game_over==True:
        if game_over_timer>0:
            game_over_timer-=delta_time
            UI.draw_text_screen(screen,font,'You won! good job.')
        else:
            screen.fill((0,0,0))
            if restart_button.draw(screen):
                game_over = False
                game_over_timer = cons.GAME_OVER_TIMER
                opening_intro = False
                is_level1 = True
                is_level2 = False
                is_level3 = False
                current_level = '1'
                current_wave = 0
                wave_active = False
                is_boss_spawned = False
                phase2_triggered = False
                show_goal_dialog_l1 = False
                show_goal_dialog_l2 = False
                show_goal_dialog_l3 = False
                show_dialog_timer = 3000
                level_complete_shop = False
                enemy_list.clear()
                alliance_group.clear()
                reset_level(world, player, enemy_list, fire_ball_group, charge_group,
                            dagame_Text_group, item_group, world_data, object_data,
                            platform_data, tile_list, obj_tile_list)
            # elif exit_button.draw(screen):
            #     game_run=False

                

   
                
    else:
      if pause_game==True:
                screen.fill((0,0,0))
                if(resume_button.draw(screen)):
                    pause_game=False
                if(exit_button.draw(screen)):
                    game_run=False
      else:
          
         
         


         show_dialog_timer-=delta_time
         if show_dialog_timer<0:
            if not show_goal_dialog_l1 and not start_intro and is_level1 :
              is_dialog_active=True
              show_goal_dialog_l1=True
            elif not show_goal_dialog_l2 and not opening_intro and is_level2:
              is_dialog_active=True
              show_goal_dialog_l2=True
            elif not show_goal_dialog_l3 and is_level3:
              is_dialog_active=True
              show_goal_dialog_l3=True

        #  surviving_time+=delta_time
        #  total_sec=surviving_time//1000
        #  minutes = total_sec // 60
        #  seconds = total_sec % 60
        #  time_text = f"{minutes:02d}:{seconds:02d}"
        
         screen.blit(bg_img,(0,0))
         screen.blit(bg_img_building,(0,0))
         #screen.blit(object_images[0],(300,400))

         #screen.fill(cons.BACK_GROUND)
    
         #draw grid
         #UI.draw_grid(screen)
    
         #world 
         world.draw(screen)

    
         if player.alive:
                
             #"上一帧是冻结的，但这一帧已经解冻了"的瞬间检测
             if was_freezed and not player.is_freezed:
                    key = pygame.key.get_pressed()
                    moving_left = key[pygame.K_a] #读取实际按键状态
                    moving_right = key[pygame.K_d]
                    is_attacking = False #重新设置乘false，重新触发，不要遗留被冻之前的值
                    is_dashing = False
                    is_jumping = False
             was_freezed=player.is_freezed
             if player.is_freezed:
                    moving_left = False
                    moving_right = False
                    is_attacking = False
                    is_dashing = False
                    is_jumping = False
        #handle player movement
             dx=0
             dy=0
             if moving_right==True:
                 dx = cons.SPEED
             if moving_left==True:
                 dx = -cons.SPEED
            #if moving_up==True:
                #dy = -cons.SPEED
            #if moving_down==True:
                #dy = cons.SPEED
   
       
        #apply screen scroll
             screen_scroll=player.move(dx,dy,world)

        #clamp camera to world bounds
             new_x=world.scroll_x+screen_scroll[0]
             new_y=world.scroll_y+screen_scroll[1]

             min_x=cons.SCREEN_WIDTH-world.world_width
             min_y=cons.SCREEN_HEIGHT-world.world_height

             max_x=0
             max_y=0

             if new_x<min_x:
                 screen_scroll[0]=min_x-world.scroll_x
             elif new_x>max_x:
                 screen_scroll[0]=max_x-world.scroll_x
        
             if new_y<min_y:
                 screen_scroll[1]=min_y-world.scroll_y
             elif new_y>max_y:
                 screen_scroll[1]=max_y-world.scroll_y
        

            #camera
             world.update(screen_scroll)

             world.scroll_x+=screen_scroll[0]
             world.scroll_y+=screen_scroll[1]
         
        
            # # #enemy spawn
            #  spawn_tile=[]
            #  tile_set = {(tile.centerx, tile.top) for tile in world.obstacle_tiles}
            #  for tile in world.obstacle_tiles:
            #        cx = tile.centerx
            #        top = tile.top
            #        left1  = (cx - cons.TILE_SIZE, top) in tile_set
            #        right1 = (cx + cons.TILE_SIZE, top) in tile_set

            #  #append the obstacle tiles x and y instead of rect, make it more precise
            #        if left1 or right1:
            #         spawn_tile.append((tile.centerx,tile.top-cons.ENEMY_HEIGHT))
        
            #  x,y=random.choice(spawn_tile)
       

        
             

            
             if is_level1:
                #start it if wave is not active, it is active but player clean all the enemies
                if not wave_active or (wave_active and len(enemy_list)==0):
                    if wave_active:
                        current_wave+=1
                    #check if there is another wave
                    if current_wave<len(L1_WAVES):
                        wave_active=True
                        #spwan the enemy for this wave
                        for(anim,ctype,count) in L1_WAVES[current_wave]:
                            for _ in range(count): #不会用到i就用_
                                sx,sy=random.choice(spawn_tile)
                                #因为spawn tile的位置已改变， 玩家移动过了，scroll 不是0，原始坐标已经偏离屏幕，所以刷在看不到的地方
                                x=sx+world.scroll_x
                                y=sy+world.scroll_y
                                enemy=Character(x,y,100,anim,ctype)
                                enemy_list.append(enemy)

                           
                    else:
                        #if this is the last wave,deactivate the wave
                        wave_active=False
                        if not level_complete_shop and player.score>=cons.L1_GOAL:
                            level_complete_shop=True
                            is_shopmenu=True
             if is_level2:
                    current_level='2'
                    #start it if wave is not active, it is active but player clean all the enemies
                    if not wave_active or (wave_active and len(enemy_list)==0):
                        if wave_active:
                            current_wave+=1
                       
                        if current_wave<len(L2_WAVES):
                            wave_active=True
                            for(anim,ctype,count) in L2_WAVES[current_wave]:
                                for _ in range(count): 
                                    sx,sy=random.choice(spawn_tile)
                                    x=sx+world.scroll_x
                                    y=sy+world.scroll_y
                                    enemy=Character(x,y,100,anim,ctype)
                                    enemy_list.append(enemy)
                               
                        else:
                            wave_active=False
                            if not level_complete_shop and player.score>=cons.L2_GOAL:
                                level_complete_shop=True
                                is_shopmenu=True
             if is_level3:
                    current_level='3'
                    if not wave_active or (wave_active and len(enemy_list)==0):
                        if wave_active:
                            current_wave+=1
                       
                        if current_wave<len(L3_WAVES):
                            wave_active=True
                            for(anim,ctype,count) in L3_WAVES[current_wave]:
                                for _ in range(count): 
                                    sx,sy=random.choice(spawn_tile)
                                    x=sx+world.scroll_x
                                    y=sy+world.scroll_y
                                    enemy=Character(x,y,100,anim,ctype)
                                    enemy_list.append(enemy)
                                
                        else:
                            if not is_boss_spawned:
                                is_boss_spawned=True
                                is_dialog_active=True
                                wave_active=True
                                for(anim,ctype,count) in L3_BOSS[0]:
                                    for _ in range(count): 
                                        sx,sy=random.choice(spawn_tile)
                                        x=sx+world.scroll_x
                                        y=sy+world.scroll_y
                                        boss=Character(x,y,100,anim,ctype)
                                        enemy_list.append(boss)
                                
                               
                        
                    if is_boss_spawned and len(enemy_list)>0:
                                        boss = enemy_list[0]  
                                    #if boss.health <= 50 and not phase2_triggered:
                                        
                                        phase2_triggered = True
                                        fire_spawn_timer-=delta_time
                                        turnado_spawn_timer-=delta_time
                                        if  boss.health<=50:
                                            if turnado_spawn_timer<=0:
                                                    tornado_spawn_x=random.randint(200,800)
                                                    tornado = Tornado(tornado_spawn_x, 350, animation.wind_ball_animation)
                                                    Tornado_group.add(tornado)
                                                    turnado_spawn_timer=2000
                                            if fire_spawn_timer<=0:
                                                    sx1, sy1 = random.choice(Tornado_spawn_tile)
                                                    x1 = sx1 + world.scroll_x
                                                    y1 = sy1 + world.scroll_y
                                                    fire = FireHazard(x1, y1, animation.Fire_animation)
                                                    Fire_hazard_group.add(fire)
                                                    fire_spawn_timer=800
                                            if boss.alive==False:
                                                game_over=True
                                               
                                                
                        
                                    
                                        
                               


                               
                           


                # if enemy1_cooldown<=0 and len(enemy_list)<3 :
                #     enemy=Character(x,y,100,animation.Demon1_animations,'1')
                #     enemy_list.append(enemy)
                #     enemy1_counter+=1
                #     enemy1_cooldown=random.randint(3000,5000)
                
                # #enro
                # if enemy1_counter>=2 and enemy4_cooldown<=0:
                #   enemy4=Character(x,y,100,animation.Demon4_animations,'4')
                #   enemy_list.append(enemy4)
                #   enemy4_cooldown=random.randint(5000,10000)


            #enemy fireball
             #if enemy1_counter>=2 and enemy2_cooldown<=0:
                 #enemy2=Character(x,y,150,animation.Demon2_animations,'2')
                 #enemy_list.append(enemy2)
                 #enemy2_counter+=1
                 #enemy2_cooldown=random.randint(5000,10000)
                 #enemy1_on=False
            
            #charge
             #if enemy1_counter>=2 and enemy3_cooldown<=0:
                 #enemy3=Character(x,y,150,animation.Demon3_animations,'3')
                 #enemy_list.append(enemy3)
                 #enemy3_cooldown=random.randint(10000,20000)
            
               
             #if enemy1_counter>=2 and enemy5_cooldown<=0:
                 #enemy5=Character(x,y,100,animation.Demon5_animations,'5')
                 #enemy_list.append(enemy5)
                 #enemy5_cooldown=random.randint(3000,5000)


               
                 
                 
             
            
             item_spawn_cooldown-=delta_time
             if item_spawn_cooldown<=0:
                 sx,sy=random.choice(spawn_tile)
                 x=sx+world.scroll_x
                 y=sy+world.scroll_y
                 money=Item(x,y+40,'1',money_img,animation.Money_animation,False)
                 if len(item_group)<=4:
                     item_group.add(money)

                 item_spawn_cooldown=random.randint(3000,5000)
             
             if alliance.alive:
                potion_spawned=False

             if alliance.alive==False:
               if not potion_spawned:
                    sx,sy=random.choice(spawn_tile)
                    x=sx+world.scroll_x
                    y=sy+world.scroll_y
                    potion=Item(x,y+40,'2',potion_img,None,False)
                    item_group.add(potion)
                    potion_spawned=True
            
                    
             if is_attacking==True and not player.is_freezed:
                damage,damage_pos,enemy=player.attack(enemy_list)
                if damage:
                      damage_text=dagameText(damage_pos.centerx,damage_pos.y,str(damage),cons.RED,font)
                      dagame_Text_group.add(damage_text)
                if enemy:
                     #if there is a enemy hit my player then apply knockback
                      enemy.apply_knockback(player,world)
                      if enemy.health<=0:
                                              #because alive is gonna update in update method，想用 alive 也可以，但必须在扣血那一刻同步更新 alive，而不是等 update。
                          enemy.enemy_state='Dead'  #不在这里移除是因为这只在“玩家攻击那一刻”才 remove

                
                          
                     
                         
        
             dagame_Text_group.update(screen_scroll)
             dagame_Text_group.draw(screen)
        

        #enemy update
             for enemy in enemy_list:
                 enemy.update() #make sure call the update first to make alive=false
                 if enemy.remove_me==True:
                     enemy_list.remove(enemy)
                     continue
                 #fireball=enemy.ai(fire_ball_image,player,world,screen_scroll)
                 charge,fireball,arrow=enemy.ai(fire_ball_image,player,alliance,world,screen_scroll)
                 if fireball:
                  fire_ball_group.add(fireball)
                 if charge:
                  charge_group.add(charge)
                 if arrow:
                   arrow_group.add(arrow)
                   
            
            #print(enemy.alive)
            #print(len(enemy_list))

        #fire ball draw and update
             for fireball in fire_ball_group:
              fireball.update(screen_scroll,player)
             for fireball in fire_ball_group:
              fireball.draw(screen)
             for arrows in arrow_group:
                 arrows.update(player)
             for arrows in arrow_group:
                 arrows.draw(screen)
             for charge in charge_group:
              charge.update(screen_scroll,player)
             for charge in charge_group:
              charge.draw(screen)
             for all in alliance_group:
                all.update(player,enemy_list,world,screen_scroll)
             for all in alliance_group:
                all.draw(screen)
             for fire in Fire_hazard_group:
                 fire.update(screen_scroll,player)
             for fire in Fire_hazard_group:
                 fire.draw(screen)
             for t in Tornado_group:
                t.update(screen_scroll, player, world)
             for t in Tornado_group:
                t.draw(screen)
            


    
         player.update()
         player.draw(screen)
         player.update_player_state(dx,dy,is_attacking,is_dashing,is_jumping)



    
    #draw player health
         UI.draw_health_bar(screen,player,screen_scroll)
         UI.draw_square(screen)
    #weapon
    # bow.draw(screen)
    # arrow=bow.update(player)
    # if arrow:
    #   arrow_group.add(arrow)
    # for arrow in arrow_group:
    #     arrow.draw(screen)
    # for arrow in arrow_group:
    #     damage,damage_pos,enemy=arrow.update(enemy_list)
    #     if damage:
    #         damage_text=dagameText(damage_pos.centerx,damage_pos.y,str(damage),cons.RED,font)
    #         dagame_Text_group.add(damage_text)
    #         #check if hit a enemy or not(there is a enemy or not then check if it is alive)
    #     if enemy and enemy.alive==False:
    #         enemy_list.remove(enemy)
    
        #enemy draw
         for enemy in enemy_list:
          if not enemy.remove_me:
              enemy.draw(screen)

         enemy_left = len(enemy_list)
         enemy_left_text = UI.Text(cons.SCREEN_WIDTH-300, 15, f'Enemies: {enemy_left}', font, cons.PURPLE)
         enemy_left_text.draw_text(screen)
    
    #item
         for item in item_group:
             item.draw(screen)
         for item in item_group:
             item.update(screen_scroll,player,alliance)
             if item.pending_dialog:
                dialog_message=item.pending_dialog
                is_dialog_active=True
    

    #Text
         if is_level1:
          vertical_text.draw_vertical_text(screen)
          vertical_text.update(screen_scroll)
    #Level_text.draw_text(screen)
         if current_level=='1':
          score_text=UI.Text(50,15,f'{player.score}/{cons.L1_GOAL}',font,cons.PURPLE)
         elif current_level=='2':
          score_text=UI.Text(50,15,f'{player.score}/{cons.L2_GOAL}',font,cons.PURPLE)
         score_text.draw_text(screen)
         score_text.update(screen_scroll)
         name_text.update(screen_scroll)
         name_text.draw_text(screen)

    
    #show death screen
         if player.alive==False:
             if death_fade.fade(screen):
              if restart_button.draw(screen):
                  death_fade.fade_counter=0
                  reset_level(world,player,enemy_list,fire_ball_group,charge_group,dagame_Text_group,item_group,world_data,object_data,platform_data,tile_list,obj_tile_list)
                  
            
            
         if start_intro==True:
             if intro_fade.fade(screen)==True:
                  start_intro=False
                  intro_fade.fade_counter=0
    


    #event handler
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game_run=False
        #take keyboard presses
        
        if event.type ==pygame.KEYDOWN:
            if event.key==pygame.K_a:
                        moving_left=True
            if event.key==pygame.K_d:
                        moving_right=True
            if event.key==pygame.K_SPACE:
                        is_jumping=True
            if event.key==pygame.K_ESCAPE:
                 if is_shopmenu:
                     not_purchased=True
                 else:
                    pause_game=True
            if event.key==pygame.K_RETURN:
                if is_dialog_active:
                 wants_close_dialog=True

             #choose pal   
            # if event.key==pygame.K_0:
            if is_shopmenu:
                if event.key==pygame.K_1:
                    alliance=Rin
                    if player.score>=cons.Fujiwara_Rin:
                     is_purchased=True
                if event.key==pygame.K_2:
                    alliance=Vesper
                    if player.score>=cons.Vesper:
                     is_purchased=True
                if event.key==pygame.K_3:
                    alliance=Fuma
                    if player.score>=cons.Himura:
                     is_purchased=True
                if event.key==pygame.K_4:
                    alliance=Ares
                    if player.score>=cons.Ares:
                     is_purchased=True



            
        
        if event.type ==pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                 is_attacking=True

                
        
        if event.type ==pygame.KEYUP:
            if event.key==pygame.K_a:
                moving_left=False
            if event.key==pygame.K_d:
                moving_right=False
            if event.key==pygame.K_w:
                moving_up=False
            if event.key==pygame.K_s:
                moving_down=False
            if event.key==pygame.K_SPACE:
                is_jumping=False
            

        if event.type ==pygame.MOUSEBUTTONUP:
            if event.button==1:
                is_attacking=False
                




    pygame.display.update()

pygame.quit()