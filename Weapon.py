import pygame
import math
import random
import Helper
import Constants as cons


class Weapon():
    def __init__(self,image,arrow_image,animation,has_animation):
        self.original_image = image
        self.angle=0
        self.image= pygame.transform.rotate(self.original_image,self.angle)
        self.arrow_image=arrow_image
        self.rect=self.image.get_rect()
        self.fired=False
        self.last_fire= pygame.time.get_ticks()
    
    def update(self,player):
        shot_cooldown= 300
        arrow=None

        self.rect.center=player.rect.center
         
        #get the mouse position
        pos=pygame.mouse.get_pos()
        # Horizontal offset: mouse_x - character_center_x
        x_dist=pos[0]-self.rect.centerx
        # Vertical offset: mouse_y - character_center_y
        y_dist=-(pos[1]-self.rect.centery)# The minus sign flips Y because in Pygame Y increases downward
        self.angle=math.degrees(math.atan2(y_dist,x_dist))
        
        #shotting-get mouse click
        if pygame.mouse.get_pressed()[0] and self.fired==False and (pygame.time.get_ticks()-self.last_fire)>=shot_cooldown:
            #shoot from the center of the arrow
            arrow=Arrow(self.arrow_image,self.rect.centerx,self.rect.centery,self.angle)
            self.fired=True
            #set the last fire time to now
            self.last_fire=pygame.time.get_ticks()
    
        #reset mouse clik
        if pygame.mouse.get_pressed()[0]==False:
            self.fired=False


        return arrow


    def draw(self,surface):

        # Save the current center BEFORE rotating (rotation changes image size)
        old_center=self.rect.center
        # Rotate the weapon image for the current angle (creates a NEW Surface each frame)
        self.image= pygame.transform.rotate(self.original_image,self.angle)
        # Rebuild rect from the new rotated image, but keep the same center position
        self.rect=self.image.get_rect(center=old_center)

        surface.blit(self.image,self.rect)  


class Arrow(pygame.sprite.Sprite): 
    def __init__(self,image,x,y,angle,animation,arrow_type):
        pygame.sprite.Sprite.__init__(self)

        self.frame_index=0
        self.animation_speed=0.15

        self.type=arrow_type



        if animation==None:
             self.frames=[image]
             self.original_image=image
        else:
             self.animations={}
             for key in animation:
                 self.animations[key]=Helper.load_image(self,animation[key][0],animation[key][1])
             self.frames=self.animations['Idle']
             self.original_image=self.frames[self.frame_index]


        self.angle=angle
        self.image= pygame.transform.rotate(self.original_image,self.angle)
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
        #calculate horizantal and vertical speed based on angle
        self.dx=math.cos(math.radians(self.angle))*cons.ARROW_SPEED
        self.dy=-math.sin(math.radians(self.angle))*cons.ARROW_SPEED

    def update(self,player):
        #reset variable
        damage=0
        #reposition based on speed
        self.rect.x+=self.dx
        self.rect.y+=self.dy

        Helper.animate(self)

        #check if arrow has gone off screen
        if self.rect.right<0 or self.rect.left>cons.SCREEN_WIDTH or self.rect.bottom<0 or self.rect.top>cons.SCREEN_HEIGHT:
            self.kill()
        
        #check collision between arrow and enemy
        if self.type=='Freez':
         if player.rect.colliderect(self.rect) and player.alive:
                # damage= 10 + random.randint(-5,5)
                player.is_freezed=True
                player.last_freeze=pygame.time.get_ticks()
                self.kill()
                  # stop checking more enemies – one arrow should only hit one target
        


    def draw(self,surface):
      old_center=self.rect.center
      #minus 90 degree to adjust the arrow angle
      self.image=pygame.transform.rotate(self.original_image,self.angle-180)
      self.rect=self.image.get_rect(center=old_center)

      surface.blit(self.image,self.rect)



class Fire_ball(pygame.sprite.Sprite): 
    def __init__(self,image,x,y,target_x,target_y):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        x_dist=target_x-x
        y_dist=-(target_y-y) #y axis is flipped in py
        self.angel=math.degrees(math.atan2(y_dist,x_dist))
        self.image= pygame.transform.rotate(self.original_image,self.angel)
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
        #calculate horizantal and vertical speed based on angle
        self.dx=math.cos(math.radians(self.angel))*cons.FIRE_BALL_SPEED
        self.dy=-math.sin(math.radians(self.angel))*cons.FIRE_BALL_SPEED

    def update(self,screen_scroll,player):

        #reposition based on speed
        self.rect.x+=screen_scroll[0]+self.dx
        self.rect.y+=screen_scroll[1]+self.dy

        #check if arrow has gone off screen
        if self.rect.right<0 or self.rect.left>cons.SCREEN_WIDTH or self.rect.bottom<0 or self.rect.top>cons.SCREEN_HEIGHT:
            self.kill()
        

        #check collision between self and plater
        if player.rect.colliderect(self.rect) and player.hit == False:
            player.hit= True
            player.last_hit=pygame.time.get_ticks()
            player.health-=10
            self.kill()




    def draw(self,surface):
      old_center=self.rect.center
      #minus 90 degree to adjust the arrow angle
      
      self.rect=self.image.get_rect(center=old_center)

      surface.blit(self.image,self.rect)


class Charge(pygame.sprite.Sprite):
    def __init__(self,owner,animation_data,x,y,target_x,target_y):
        pygame.sprite.Sprite.__init__(self)
        
        self.owner=owner
        # 计算角度（用于旋转特效方向，指向玩家）    
        x_dist = target_x - owner.rect.centerx
        y_dist = -(target_y - owner.rect.centery) 
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        self.frame_index=0
        self.animation_speed=0.15
        self.animations={}
        for key in animation_data:
            self.animations[key]=Helper.load_image(self,animation_data[key][0],animation_data[key][1])
        self.frames=self.animations['Idle']
        self.image=self.frames[self.frame_index]
        #如果不是facing right 把图片镜面反转，初始化的时候update之前就翻转
        if not self.owner.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
        
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
        

        self.duration=1000
        self.start_time=pygame.time.get_ticks()

    def update_position(self):
    
        if self.owner.facing_right:
            new_x=self.owner.rect.centerx+45
        else:
            new_x=self.owner.rect.centerx-45

        self.rect.center = (new_x, self.owner.rect.centery+3)


    def update(self,screen_scroll,player):
        self.rect.x+=screen_scroll[0]
        self.rect.y+=screen_scroll[1]

        self.update_position()
        Helper.animate(self)
        
        #获取当前帧的图片
        raw_image = self.frames[int(self.frame_index)]
        
        # 如果不是在左边，就把图片左右反过来
        if not self.owner.facing_right:
            self.image = pygame.transform.flip(raw_image, True, False)
        else:
            self.image = raw_image
        #就是现在时间 - Charge创建时的时间 = Charge已经存在了多少毫秒
        if pygame.time.get_ticks()-self.start_time>self.duration:
            self.kill()
            return
        
        if not self.owner.alive or self.owner.health<=0:
            self.kill()
            return
        if self.owner.char_type == '5':
         damage_box = self.rect.inflate(40, 90)   # enemy5 飞行怪，纵向判定大一点
        else:
         damage_box = self.rect.inflate(20, 40)   # 普通 charge 怪

        if player.rect.colliderect(damage_box) and player.hit == False and player.alive:
            player.health -= random.randint(15, 20)
            player.hit = True
            player.last_hit = pygame.time.get_ticks()
           
            
            
    
    def draw(self,surface):
         surface.blit(self.image,self.rect)

    

   
class Tornado(pygame.sprite.Sprite):
    def __init__(self, x, y, animation):
        pygame.sprite.Sprite.__init__(self)
        
        self.frame_index = 0
        self.animation_speed = 0.15
        
        # 跟 Item 一样的加载方式
        self.animations = {}
        for key in animation:
            self.animations[key] = Helper.load_image(self, animation[key][0], animation[key][1])
        self.frames = self.animations['Idle']
        self.image = self.frames[self.frame_index]
    
        #self.rect=pygame.Rect(x,y,50,50)
        self.rect=self.image.get_rect()
        #self.rect.midbottom = (x, y)
        self.rect.center=(x,y)
        self.rect=self.rect.inflate(-10,-20)
        self.speed = 3
        self.vel_y=0
        self.on_ground=False
        self.facing_right = True
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 20000
        self.attack_cooldown = 0
        self.dy=0
        self.dx=0
    
    def move(self,dx,dy,world):
        
         self.vel_y+=1
         dy=self.vel_y

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


    



    def update(self, screen_scroll, player, world):
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()
            return

        # 跟随 scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]


        
        hit_wall, reached_edge=Helper.ground_ahead(self,world)
        if hit_wall or reached_edge:
              self.facing_right = not self.facing_right
        
                # 左右移动
        if self.facing_right:
            self.dx= self.speed
        else:
            self.dx= -self.speed
        
        self.move(self.dx,self.dy,world)
                

        # 伤害玩家
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.rect.colliderect(player.rect):
            if self.attack_cooldown <= 0:
                player.hit = True
                player.last_hit = pygame.time.get_ticks()
                self.attack_cooldown = 60

        Helper.animate(self)

    def draw(self, surface):
        draw_image = self.image
        if not self.facing_right:
            draw_image = pygame.transform.flip(self.image, True, False)
        surface.blit(draw_image, self.rect)
        pygame.draw.rect(surface, cons.RED, self.rect, 1)


class FireHazard(pygame.sprite.Sprite):
    def __init__(self, x, y, animation):
        pygame.sprite.Sprite.__init__(self)
        
        self.frame_index = 0
        self.animation_speed = 0.15

        # 跟 Item 一样的加载方式
        self.animations = {}
        for key in animation:
            self.animations[key] = Helper.load_image(self, animation[key][0], animation[key][1])
        self.frames = self.animations['Idle']
        self.image = self.frames[self.frame_index]

        self.rect=self.image.get_rect()
        #self.rect.center=(x,y+cons.ENEMY_HEIGHT)
        self.rect.midbottom = (x, y)

        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 20000
        self.attack_cooldown = 0


    def update(self, screen_scroll, player):
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()
            return

        # 跟随 scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # 伤害玩家
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.rect.colliderect(player.rect):
            if self.attack_cooldown <= 0:
                player.hit = True
                player.last_hit = pygame.time.get_ticks()
                self.attack_cooldown = 60

        Helper.animate(self)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, cons.RED, self.rect, 1)

