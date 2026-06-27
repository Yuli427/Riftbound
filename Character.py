import pygame
import math
import animation
import Helper 
import Constants as cons
from Weapon import Fire_ball, Charge ,Arrow
from Character_types import NO_GRAVITY_TYPES,BOSS,PLAYER



class Character():
    #char type=0 player, char type=1 normal enemy, char type=2 enemy without gravity
    def __init__(self,x,y,health,animation,char_type):
         self.setup_rect(x, y, char_type)
         self.load_animations(animation)

         self.setup_physics()
         self.setup_basic_stats(health, char_type)
         self.setup_combat_stats()
         self.setup_enemy_ai_state()
         self.setup_player_state()
    
    def setup_rect(self, x, y, char_type):
        if char_type == '3':  # charge demon
            self.rect = pygame.Rect(0, 0, 48, 90)
        else:
            self.rect = pygame.Rect(0, 0, 48, 70)

        self.rect.center = (x, y)


    def load_animations(self, animation_data):
        self.animations = {}

        for key in animation_data:
            self.animations[key] = Helper.load_image(
                self,
                animation_data[key][0],
                animation_data[key][1]
            )

        self.frames = self.animations['Idle']
        self.frame_index = 0
        self.animation_speed = 0.15
        self.animation_speed_enemy2 = 0.05
        self.image = self.frames[0]


    def setup_physics(self):
        self.vel_y = 0
        self.on_ground = False
        self.use_gravity = True
        self.camera_offsety = 0


    def setup_basic_stats(self, health, char_type):
        self.char_type = char_type
        self.facing_right = True
        self.health = health
        self.alive = True
        self.score = 0

        self.is_freezed = False
        self.freeze_timer = 1000
        self.last_freeze = 0

        self.hit = False
        self.last_hit = 0

        self.stunned = False
        self.stun_until = 0


    def setup_combat_stats(self):
        self.attack_cooldown = 0

        self.last_fireball_attack = 0
        self.last_lightning_attack = 0
        self.fireball_cooldown = 700
        self.lightning_cooldown = 2000

        self.charge_cooldown = 2000
        self.last_charge_attack = -2000

        self.max_health_boss = 100


    def setup_enemy_ai_state(self):
        self.enemy_state = 'Idle'
        self.enemy_height = 0
        self.remove_me = False

        self.aggro_target = None
        self.aggro_timer = 0

        self.has_teleported = False
        self.has_charged = False
        self.tornado_spawned = False


    def setup_player_state(self):
        self.player_state = 'Idle'
    




    def update(self):
        #check if character has died:
        if self.health<=0:
            self.health=0
            self.alive=False
        
        #reset player taking a hit
        hit_cooldown = 1000
        if self.char_type==PLAYER:
            if self.hit==True:
                if (pygame.time.get_ticks()-self.last_hit) > hit_cooldown:
                    self.hit=False
        
        # Attack cooldown
        if self.attack_cooldown>0:
            self.attack_cooldown-=1
        
        #Hurt timer
        #if self.hurt_timer>0 :
            #self.hurt_timer-=1
           

            
        
        #Stunned 
        if self.stunned==True and self.stun_until>0:
            self.stun_until-=1
        else:
            self.stunned=False
        
        
        if not self.player_state=='Freezed':
         Helper.animate(self)
    
       

    def move(self,dx,dy,world):
        if self.char_type not in NO_GRAVITY_TYPES or not self.alive :
         self.vel_y+=1
         dy=self.vel_y

        screen_scroll=[0,0]

        self.rect.x+=dx
        self.rect.y+=dy

        self.on_ground=False
        for tile in world.obstacle_tiles:
            if tile.colliderect(self.rect):

                if dy>0:

                    if(self.rect.bottom-dy)<=tile.top:
                        self.rect.bottom=tile.top
                        self.vel_y=0
                        self.on_ground=True

        if self.char_type==PLAYER:
            screen_scroll=self.handle_player_camera(dx,dy,world,screen_scroll)

        return screen_scroll
    

                

             

    def draw(self,surface):
        
        #create a rect for image
        image_rect=self.image.get_rect()
        #move the center of the image to the center of collision box
        

        if self.char_type==BOSS:
            scale_factor=1.5
            scaled_width = int(self.image.get_width() * scale_factor)
            scaled_height = int(self.image.get_height() * scale_factor)
            draw_image=pygame.transform.scale(self.image, (scaled_width, scaled_height))
            # 红色背景
            pygame.draw.rect(surface, cons.RED, (self.rect.x, self.rect.top - 60, self.rect.width, 5))
            # 绿色血量
            pygame.draw.rect(surface, (0,255,0), (self.rect.x, self.rect.top - 60, self.rect.width * (self.health / self.max_health_boss), 5))
        else:
            draw_image=self.image
        
        image_rect=draw_image.get_rect()
        image_rect.midbottom=self.rect.midbottom

        if self.facing_right==False:
             flipped_image=pygame.transform.flip(draw_image,True,False)
             surface.blit(flipped_image,image_rect)
        else:
             surface.blit(draw_image,image_rect)
        #pygame.draw.rect(surface,cons.RED,self.rect,1)  
        
   





        
        