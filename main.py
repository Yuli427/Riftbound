import pygame
import random
from State import GameState
from assets import load_static_assets,L1_WAVES,L2_WAVES,L3_WAVES,L3_BOSS
import Constants as cons
import animation
import UI
from Player import Player
from level_loader import load_level_world
from Enemy import Enemy
from Weapon import Tornado,FireHazard
from Effects import dagameText
from item import Item
from Button import Button
from Alliance import Alliance as All


pygame.init()

game_name='Riftbound'
#open a window
screen=pygame.display.set_mode((cons.SCREEN_WIDTH,cons.SCREEN_HEIGHT))
pygame.display.set_caption(game_name)

clock= pygame.time.Clock()
state = GameState()
assets = load_static_assets()
#load assets
start_img = assets["start_img"]
resume_img = assets["resume_img"]
exit_img = assets["exit_img"]
restart_img = assets["restart_img"]

bg_img = assets["bg_img"]
bg_img_building = assets["bg_img_building"]
money_img = assets["money_img"]
money_icon_img = assets["money_icon_img"]
potion_img = assets["potion_img"]
fire_ball_image = assets["fire_ball_image"]
charge_image = assets["charge_image"]
font = assets["font"]
smaller_font = assets["smaller_font"]




state.item_spawn_cooldown=random.randint(3000,5000)

   
#define player movement variable
moving_left=False
moving_up=False
moving_right=False
moving_down=False
is_attacking=False
is_dashing=False
is_changing_character=False
is_jumping=False


#level loader
level_data = load_level_world(state.current_level)

world = level_data["world"]
world_data = level_data["world_data"]
layer_data = level_data["layer_data"]
object_data = level_data["object_data"]
platform_data = level_data["platform_data"]
tile_list = level_data["tile_list"]
obj_tile_list = level_data["obj_tile_list"]
spawn_tile = level_data["spawn_tile"]
Tornado_spawn_tile = level_data["tornado_spawn_tile"]

#create enemy list
enemy_list=[]
#enemy_list.append(enemy)
#enemy_list.append(boss)



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



#create screen fade 
intro_fade=UI.ScreenFade(1,(0,0,0),7)
death_fade=UI.ScreenFade(2,(0,0,0),7)



#Level_text=UI.Text(10,15,f'Level:{level}',font,cons.PINK)
#create buttons
restart_button=Button(cons.SCREEN_WIDTH//2-145,cons.SCREEN_HEIGHT//2-50,restart_img)
start_button=Button(cons.SCREEN_WIDTH//2-145,cons.SCREEN_HEIGHT//2-150,start_img)
resume_button=Button(cons.SCREEN_WIDTH//2-145,cons.SCREEN_HEIGHT//2-150,resume_img)
exit_button=Button(cons.SCREEN_WIDTH//2-145,cons.SCREEN_HEIGHT//2+50,exit_img)
#main game loop



def reset_level(world, player, enemy_list, fireballs, charge, dagame_Text_group, item_group,
                world_data, object_data, platform_data, tile_list, obj_tile_list):
    
    
    global spawn_tile, Tornado_spawn_tile, layer_data
    
    state.finish_anime=cons.DEATH_PLAY
    state.show_dialog_timer=3000
    state.item_spawn_cooldown = random.randint(3000, 5000)

    state.is_purchased=False
    state.is_shopmenu = False
    state.not_purchased = False

    state.is_dialog_active=False
    state.wants_close_dialog = False
    state.dialog_message = ""

    enemy_list.clear()
    fireballs.empty()
    charge.empty()
    dagame_Text_group.empty()
    item_group.empty()
    item_group.add(money_icon)
    Fire_hazard_group.empty()
    Tornado_group.empty()

    state.reset_boss_state()
    state.reset_wave_state()


    #reset alliance
    alliance_group.empty()
  
    if state.has_alliance:
        alliance.rect.center = (450, 700)
        alliance.health = 100
        alliance.alive = True
        alliance.hit = False
        alliance.stunned = False
        alliance.vel_y = 0
        alliance.dx = 0
        alliance.dy = 0
        alliance_group.empty()
        alliance_group.add(alliance)


    # reload level world
    level_data = load_level_world(state.current_level)
    new_world = level_data["world"]

    # copy new world data into the existing world object
    world.__dict__.update(new_world.__dict__)

    world_data[:] = level_data["world_data"]
    object_data[:] = level_data["object_data"]
    platform_data[:] = level_data["platform_data"]
    tile_list[:] = level_data["tile_list"]
    obj_tile_list[:] = level_data["obj_tile_list"]

   
    layer_data = level_data["layer_data"]
    spawn_tile = level_data["spawn_tile"]
    Tornado_spawn_tile = level_data["tornado_spawn_tile"]

    world.scroll_x = 0
    world.scroll_y = 0
    

 

    # reset player
    player.rect.center = (200, 700)
    player.vel_y = 0
    player.health = 100
    player.alive = True
    player.hit = False
    player.stunned = False
    player.player_state = 'Idle'
    player.score = 0
    
    

   
def reset_to_boss_checkpoint(world, player, enemy_list):
    # clear group and list
    enemy_list.clear()
    fire_ball_group.empty()
    charge_group.empty()
    arrow_group.empty()
    Tornado_group.empty()
    Fire_hazard_group.empty()
    dagame_Text_group.empty()

    # reset player
    player.rect.center = (200, 700)
    player.vel_y = 0
    player.health = 100
    player.alive = True
    player.hit = False
    player.stunned = False
    player.is_freezed = False
    player.player_state = 'Idle'

    #empty alliance
    alliance_group.empty()

    # skip to L3 after boss spawned
    state.current_wave = len(L3_WAVES)
    state.wave_active = True
    state.is_boss_spawned = True
    state.phase2_triggered = False

    state.finish_anime = cons.DEATH_PLAY

    state.fire_spawn_timer = 1200
    state.turnado_spawn_timer = 9000

    # respawn boss
    sx, sy = random.choice(spawn_tile)
    x = sx + world.scroll_x
    y = sy + world.scroll_y

    boss = Enemy(x, y, 650, animation.Boss_animations, 'Boss')
    boss.max_health_boss = 650
    enemy_list.append(boss)



  
    
    
    

while state.choosing:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and state.player_name:
                state.choosing = False
            elif event.key == pygame.K_BACKSPACE:
                state.player_name = state.player_name[:-1]
            elif event.key == pygame.K_LEFT:
                state.selected_gender = 'Male'
            elif event.key == pygame.K_RIGHT:
                state.selected_gender = 'Female'
            else:
                if len(state.player_name) < 12:  
                    state.player_name += event.unicode
    
    #create player
    if state.selected_gender=='Female':
        player=Player(200,700,100,animation.School_girl_animations)
    else:
        player=Player(200,700,100,animation.School_boy1_animations,)
    screen.fill(cons.BACK_GROUND)
    UI.draw_choose_menu(screen, font, state.player_name, state.selected_gender, game_name,True)
    name_text=UI.Text(300,15,state.player_name,font,cons.PURPLE)
    pygame.display.update()
    
def create_enemy_from_spawn(anim, ctype, world, spawn_tile, health=100):
    sx, sy = random.choice(spawn_tile)

   
    x = sx + world.scroll_x
    y = sy + world.scroll_y

    return Enemy(x, y, health, anim, ctype)


def get_l1_enemy_health(ctype):
    if ctype == '1':
        return 100
    elif ctype == '2':
        return 90
    elif ctype == '3':
        return 130
    elif ctype == '4':
        return 150
    elif ctype == '5':
        return 120

    return 100

def spawn_wave(waves, current_wave, world, spawn_tile, enemy_list, use_l1_health=False):
    for anim, ctype, count in waves[current_wave]:
        for _ in range(count):
            if use_l1_health:
                health = get_l1_enemy_health(ctype)
                enemy = create_enemy_from_spawn(anim, ctype, world, spawn_tile, health)
            else:
                enemy = create_enemy_from_spawn(anim, ctype, world, spawn_tile)

            enemy_list.append(enemy)




while state.game_run:
    
    #control frame rate
    delta_time=clock.tick(cons.FPS)

    if state.start_game==False:
        screen.fill((0,0,0))
        if (start_button.draw(screen)):
            state.start_game=True
            #播放开场淡入动画
            state.start_intro=True
        #it become true only when hit the button, so we call draw method here to check the collision
        if(exit_button.draw(screen)):
            state.game_run=False
    elif state.is_shopmenu==True:
        if state.victory_timer>0:
            UI.draw_victory(screen,font)
            state.victory_timer-=delta_time
        if state.victory_timer<=0:
                screen.fill((0,0,0))
                UI.draw_shop_menu(screen, smaller_font, player.score,state.current_level)
                if state.is_purchased==True and alliance.name== 'Rin' :
                     player.score-=cons.Fujiwara_Rin
                     alliance_group.empty()
                     state.is_shopmenu=False
                     state.has_alliance=True
                     alliance=Rin
                elif state.is_purchased==True and alliance.name== 'Vesper' :
                     player.score-=cons.Vesper
                     alliance_group.empty()
                     state.is_shopmenu=False
                     alliance=Vesper
                     state.has_alliance=True
                elif state.is_purchased==True and alliance.name== 'Fuma' :
                     player.score-=cons.Himura
                     alliance_group.empty()
                     state.is_shopmenu=False
                     alliance=Fuma
                     state.has_alliance=True
                elif state.is_purchased==True and alliance.name=='Ares' :
                     player.score-=cons.Ares
                     alliance_group.empty()
                     state.is_shopmenu=False
                     alliance=Ares
                     state.has_alliance=True
                        #check if the level is complete'
                elif state.not_purchased:
                    state.is_shopmenu=False
                
                alliance_group.add(alliance)

                if state.level_complete_shop and not state.is_shopmenu:
                        state.level_complete_shop=False
                        state.opening_intro=True
                        state.victory_timer=cons.VICTORY_TIMER
                        

    elif state.is_dialog_active:
       if state.is_boss_spawned==True and state.current_level=='3':
           UI.draw_dialog(screen, font, alliance, f'The final BOSS has arrived! You must fight alone, {alliance.name} will not able to help you now.. ')
       elif state.show_goal_dialog_l1 and state.current_level=='1':
           UI.draw_dialog(screen, font, alliance, f'Goal: Eliminate all enemies and obtain {cons.L1_GOAL}. Remember you need to find them if you can\'t see them...')
       elif state.show_goal_dialog_l2 and state.current_level=='2':
           UI.draw_dialog(screen, font, alliance, f'Goal: Eliminate all enemies and obtain {cons.L2_GOAL}.')
       elif state.show_goal_dialog_l3 and state.current_level=='3':
           UI.draw_dialog(screen, font, alliance, 'Goal: Eliminate all enemies.')
       else:
           UI.draw_dialog(screen,font,alliance,state.dialog_message)
       if state.wants_close_dialog:
          state.is_dialog_active=False
          state.wants_close_dialog=False

    elif state.opening_intro:
         #if start intro=true fade screen
                if state.opening_intro_timer>0:
                  state.opening_intro_timer-=delta_time
                  UI.draw_text_screen(screen,font,'Loading...')
                  if state.opening_intro_timer<=0:
                        state.opening_intro=False
                        state.opening_intro_timer=cons.INTRO_TIMER
                        if state.current_level=='1':
                            state.set_level('2')
                            reset_level(world,player,enemy_list,fire_ball_group,charge_group,dagame_Text_group,item_group,world_data,object_data,platform_data,tile_list,obj_tile_list)
                        elif state.current_level=='2':
                            state.set_level('3')
                            reset_level(world,player,enemy_list,fire_ball_group,charge_group,dagame_Text_group,item_group,world_data,object_data,platform_data,tile_list,obj_tile_list) 
    elif state.game_over==True:
        if state.game_over_timer>0:
            state.game_over_timer-=delta_time
            UI.draw_text_screen(screen,font,'You won! good job.')
        else:
            screen.fill((0,0,0))
            if restart_button.draw(screen):
                state.game_over = False
                state.game_over_timer = cons.GAME_OVER_TIMER
                state.opening_intro = False
                state.set_level('1')
                state.reset_wave_state()
                state.reset_boss_state()
                state.show_goal_dialog_l1 = False
                state.show_goal_dialog_l2 = False
                state.show_goal_dialog_l3 = False
                state.is_dialog_active = False
                state.wants_close_dialog = False
                state.dialog_message = ""
                state.show_dialog_timer = 3000
                state.level_complete_shop = False
                enemy_list.clear()
                if not alliance_group.empty():
                 alliance_group.empty()
                reset_level(world, player, enemy_list, fire_ball_group, charge_group,
                            dagame_Text_group, item_group, world_data, object_data,
                            platform_data, tile_list, obj_tile_list)
            # elif exit_button.draw(screen):
            #     game_run=False

                

   
                
    else:
      if state.pause_game==True:
                screen.fill((0,0,0))
                if(resume_button.draw(screen)):
                    state.pause_game=False
                if(exit_button.draw(screen)):
                    state.game_run=False
      else:
         state.show_dialog_timer-=delta_time
         if state.show_dialog_timer<0:
            if not state.show_goal_dialog_l1 and not state.start_intro and state.is_level1 :
              state.is_dialog_active=True
              state.show_goal_dialog_l1=True
            elif not state.show_goal_dialog_l2 and not state.opening_intro and state.is_level2:
              state.is_dialog_active=True
              state.show_goal_dialog_l2=True
            elif not state.show_goal_dialog_l3 and state.is_level3:
              state.is_dialog_active=True
              state.show_goal_dialog_l3=True


        
         screen.blit(bg_img,(0,0))
         screen.blit(bg_img_building,(0,0))

         #world 
         world.draw(screen)

    
         if player.alive:
                
             #"上一帧是冻结的，但这一帧已经解冻了"的瞬间检测
             if state.was_freezed and not player.is_freezed:
                    key = pygame.key.get_pressed()
                    moving_left = key[pygame.K_a] #读取实际按键状态
                    moving_right = key[pygame.K_d]
                    is_attacking = False #重新设置乘false，重新触发，不要遗留被冻之前的值
                    is_dashing = False
                    is_jumping = False
             state.was_freezed=player.is_freezed
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
         

       

        
             

            
             if state.is_level1:
                #start it if wave is not active, it is active but player clean all the enemies
                if not state.wave_active or (state.wave_active and len(enemy_list)==0):
                    if state.wave_active:
                        state.current_wave+=1
                    #check if there is another wave
                    if state.current_wave<len(L1_WAVES):
                        state.wave_active=True
                        #spwan the enemy for this wave
                        spawn_wave(
                                        L1_WAVES,
                                        state.current_wave,
                                        world,
                                        spawn_tile,
                                        enemy_list,
                                        use_l1_health=True
                                    )
                            
                    else:
                        #if this is the last wave,deactivate the wave
                        state.wave_active=False
                        if not state.level_complete_shop and player.score>=cons.L1_GOAL:
                            state.level_complete_shop=True
                            state.is_shopmenu=True
             if state.is_level2:
                    #start it if wave is not active, it is active but player clean all the enemies
                    if not state.wave_active or (state.wave_active and len(enemy_list)==0):
                        if state.wave_active:
                            state.current_wave+=1
                       
                        if state.current_wave<len(L2_WAVES):
                            state.wave_active=True
                             # spawn enemies for this wave
                            spawn_wave(
                                L2_WAVES,
                                state.current_wave,
                                world,
                                spawn_tile,
                                enemy_list
                            )
                                            
                        else:
                            state.wave_active=False
                            if not state.level_complete_shop and player.score>=cons.L2_GOAL:
                                state.level_complete_shop=True
                                state.is_shopmenu=True
             
             if state.is_level3:
                    if not state.wave_active or (state.wave_active and len(enemy_list)==0):
                        if state.wave_active:
                            state.current_wave+=1
                       
                        if state.current_wave<len(L3_WAVES):
                            state.wave_active=True
                              # spawn enemies for this wave
                            spawn_wave(
                                L3_WAVES,
                                state.current_wave,
                                world,
                                spawn_tile,
                                enemy_list
                            )
                                        

                                
                        else:
                            if not state.is_boss_spawned:
                                state.is_boss_spawned=True
                                state.is_dialog_active=True
                                state.wave_active=True
                                for(anim,ctype,count) in L3_BOSS[0]:
                                    boss = create_enemy_from_spawn(
                                        anim,
                                        ctype,
                                        world,
                                        spawn_tile,
                                        health=650
                                    )
                                    boss.max_health_boss=650
                                    enemy_list.append(boss)
 
                                alliance_group.empty()
                                
                               
                        
                    if state.is_boss_spawned and len(enemy_list)>0:
                                        
                                        boss = enemy_list[0]  
                                    #if boss.health <= 50 and not phase2_triggered:
                                        
                                        state.phase2_triggered = True
                                        state.fire_spawn_timer-=delta_time
                                        state.turnado_spawn_timer-=delta_time
                                        if  boss.health <= boss.max_health_boss * 0.5:
                                            if state.turnado_spawn_timer<=0:
                                                    tornado_spawn_x=random.randint(200,800)
                                                    tornado = Tornado(tornado_spawn_x, 350, animation.wind_ball_animation)
                                                    Tornado_group.add(tornado)
                                                    state.turnado_spawn_timer=10000
                                            if state.fire_spawn_timer<=0:
                                                    sx1, sy1 = random.choice(Tornado_spawn_tile)
                                                    x1 = sx1 + world.scroll_x
                                                    y1 = sy1 + world.scroll_y
                                                    fire = FireHazard(x1, y1, animation.Fire_animation)
                                                    Fire_hazard_group.add(fire)
                                                    state.fire_spawn_timer=800
                                        if boss.alive==False:
                                                state.finish_anime-=delta_time
                                                if state.finish_anime<=0:                   
                                                 state.game_over=True
                                                  
                                               
                                                
 
            
             state.item_spawn_cooldown-=delta_time
             if state.current_level=='1' or state.current_level=='2':
                if state.item_spawn_cooldown<=0:
                    sx,sy=random.choice(spawn_tile)
                    x=sx+world.scroll_x
                    y=sy+world.scroll_y
                    money=Item(x,y+40,'1',money_img,animation.Money_animation,False)
                    if len(item_group)<=4:
                        item_group.add(money)

                    state.item_spawn_cooldown=random.randint(5000,7000)

             
             if player.health>=40:
                    state.potion_spawned=False

             else :
                 if not state.potion_spawned:
                        sx,sy=random.choice(spawn_tile)
                        x=sx+world.scroll_x
                        y=sy+world.scroll_y
                        potion=Item(x,y+40,'2',potion_img,None,False)
                        item_group.add(potion)
                        state.potion_spawned=True
            
                    
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
            


         if not player.alive:
          player.move(0, 0, world)
         player.update()
         player.draw(screen)
         player.update_player_state(dx,dy,is_attacking,is_dashing,is_jumping)



    
    #draw player health
         UI.draw_health_bar(screen,player,screen_scroll)
         UI.draw_square(screen)

    
        #enemy draw
         for enemy in enemy_list:
          if not enemy.remove_me:
              enemy.draw(screen)

         state.enemy_left = len(enemy_list)
         enemy_left_text = UI.Text(cons.SCREEN_WIDTH-300, 15, f'Enemies: {state.enemy_left}', font, cons.PURPLE)
         enemy_left_text.draw_text(screen)
    
    #item   
         for item in item_group:
             item.draw(screen)
         for item in item_group:
             item.update(screen_scroll,player)
             if item.pending_dialog:
                state.dialog_message=item.pending_dialog
                state.is_dialog_active=True
    

    #Text

    #Level_text.draw_text(screen)
         if state.current_level=='1':
          score_text=UI.Text(50,15,f'{player.score}/{cons.L1_GOAL}',font,cons.PURPLE)
          score_text.draw_text(screen)
          score_text.update(screen_scroll)
         elif state.current_level=='2':
          score_text=UI.Text(50,15,f'{player.score}/{cons.L2_GOAL}',font,cons.PURPLE)
          score_text.draw_text(screen)
          score_text.update(screen_scroll)
         name_text.update(screen_scroll)
         name_text.draw_text(screen)

    
    #show death screen
         if player.alive==False:
             if death_fade.fade(screen):
              died_during_boss = state.current_level == '3' and state.is_boss_spawned
              if restart_button.draw(screen):
                  death_fade.fade_counter=0
                  reset_level(world,player,enemy_list,fire_ball_group,charge_group,dagame_Text_group,item_group,world_data,object_data,platform_data,tile_list,obj_tile_list)
                  if died_during_boss:
                    reset_to_boss_checkpoint(world, player, enemy_list)

                  
            
            
         if state.start_intro==True:
             if intro_fade.fade(screen)==True:
                  state.start_intro=False
                  intro_fade.fade_counter=0
    


    #event handler
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            state.game_run=False
        #take keyboard presses
        
        if event.type ==pygame.KEYDOWN:
            if event.key==pygame.K_a:
                        moving_left=True
            if event.key==pygame.K_d:
                        moving_right=True
            if event.key==pygame.K_SPACE:
                        is_jumping=True
            if event.key==pygame.K_ESCAPE:
                 if state.is_shopmenu:
                     state.not_purchased=True
                 else:
                    state.pause_game=True
            if event.key==pygame.K_RETURN:
                if state.is_dialog_active:
                 state.wants_close_dialog=True

             #choose pal   
            # if event.key==pygame.K_0:
            if state.is_shopmenu:
                if event.key==pygame.K_1:
                    alliance=Rin
                    if player.score>=cons.Fujiwara_Rin:
                     state.is_purchased=True
                if event.key==pygame.K_2:
                    alliance=Vesper
                    if player.score>=cons.Vesper:
                     state.is_purchased=True
                if event.key==pygame.K_3:
                    alliance=Fuma
                    if player.score>=cons.Himura:
                     state.is_purchased=True
                if event.key==pygame.K_4:
                    alliance=Ares
                    if player.score>=cons.Ares:
                     state.is_purchased=True



            
        
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