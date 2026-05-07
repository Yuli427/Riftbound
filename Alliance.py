import pygame
import Helper
import math
import Constants as cons
import random

class Alliance(pygame.sprite.Sprite):
    def __init__(self, x, y, name, animation_data):
     pygame.sprite.Sprite.__init__(self)
     
     self.frame_index=0
     self.animation_speed=0.15
     self.animations={}
     for key in animation_data:
         self.animations[key]=Helper.load_image(self,animation_data[key][0],animation_data[key][1])
         self.frames=self.animations['Idle']
         self.image=self.frames[self.frame_index]

     self.rect=pygame.Rect(0,0,48,70)
     self.rect.center=(x,y)

     self.name=name
     self.state='Idle'
     self.health=100
     self.alive=True
     self.target=None
     self.hit=False
     self.last_hit=pygame.time.get_ticks()
     self.stunned=False
     self.stun_until=0

     self.followdist=100
     self.detect_range=500
     self.attack_range=50
     self.attack_cooldown=0
     self.dist_to_tile=150
     self.vel_y=0

     self.speed=cons.ENEMY_SPEED
     self.facing_right=False
     self.on_ground=False
     self.is_attacking=False
     self.is_jumping=False
     


     self.dy=0
     self.dx=0


     
   

    

#dx 指的是在 水平方向（X 轴）上的位移增量。dy 指的是在 垂直方向（Y 轴）上的位移增量。
    def update(self,player,enemy_list,world,screen_scroll):
       #判断目标---决定 dx / dy----执行 move()---应用 screen_scroll----更新动画
       
       if self.health<=0:
           self.health=0
           self.alive=False
           


       hit_cooldown = 1000
       if self.hit==True:
           if (pygame.time.get_ticks()-self.last_hit) > hit_cooldown:
                self.hit=False
                self.stunned=False
        

       if self.alive and not self.stunned:
           self.target=self.find_closest_enemy(enemy_list)

           if self.target :
                self.attack_logic(enemy_list,world)
           else:
                self.follow_logic(player,world)

       
       self.rect.x+=screen_scroll[0]
       self.rect.y+=screen_scroll[1]

       self.move(world)

       self.update_state()

       Helper.animate(self)

    

    

        

    def find_closest_enemy(self, enemy_list):   
       closest=None
       min_dist=self.detect_range
       for enemy in enemy_list:
          if enemy.alive==True and enemy.health>0:
             dist=math.sqrt(((self.rect.centerx-enemy.rect.centerx)**2) + ((self.rect.centery-enemy.rect.centery)**2)) 
             if dist<min_dist:
                #确认谁才是离你最近的敌人
                min_dist=dist
                closest=enemy
       return closest
    
    def follow_logic(self,player,world):
       
       #先算和玩家的距离
       x_dist=abs(self.rect.centerx-player.rect.centerx)
       y_dist=self.rect.centery-player.rect.centery

       if x_dist<self.followdist:
        self.dx=0
        return
       
       if y_dist>50 and self.on_ground:
        for tile in world.obstacle_tiles:
            if(tile.left<self.rect.centerx<tile.right) and self.rect.top-tile.bottom<self.dist_to_tile and tile.bottom<self.rect.top:
                            self.is_jumping=True
                            self.rect.bottom=tile.top
                            self.vel_y=-15
                            self.on_ground=True

    

       if self.rect.centerx>player.rect.centerx:
            self.dx=-self.speed
       elif self.rect.centerx<player.rect.centerx:    
            self.dx=self.speed
       else:
           self.dx=0
           
    #    if self.rect.centery>player.rect.centery:
    #         self.dy=-self.speed
    #    elif self.rect.centery<player.rect.centery:
    #         self.dy=self.speed

       if self.dx>0:
            self.facing_right=True
       elif self.dx<0:
            self.facing_right=False
       else:
           self.facing_right=True
      
       
   
    def attack_logic(self,enemylist,world):
        if not self.target:
            return

        dist = math.sqrt(
            (self.rect.centerx - self.target.rect.centerx) ** 2 +(self.rect.centery - self.target.rect.centery) ** 2)
        
        if dist>self.attack_range:

            if self.rect.centerx>self.target.rect.centerx:
                self.dx=-self.speed
            elif self.rect.centerx<self.target.rect.centerx:    
                self.dx=self.speed
            else:
                self.dx=0
            # if self.rect.centery>self.target.rect.centery:
            #     self.dy=-self.speed
            # if self.rect.centery<self.target.rect.centery:
            #     self.dy=self.speed
        
            if self.dx>0:
                self.facing_right=True
            elif self.dx<0:
                self.facing_right=False
            else:
                self.facing_right=True
            
        else:
            self.is_attacking=True
            self.dy=0
            self.dx=0
            if self.attack_cooldown<=0:
                damage=1
                self.target.health-=damage
                self.target.stunned=True
                self.target.stun_until=cons.STUN_TIME
                if self.target.health<=0:
                    self.target.alive=False
                    self.target.health=0
                self.attack_cooldown=20
            else:
                self.attack_cooldown-=1
            
      
      
    def move(self,world):
         self.vel_y+=1
         self.dy=self.vel_y
         # X axis
         self.rect.x+=self.dx
         self.rect.y+=self.dy

        

 
         self.on_ground=False
         for tile in world.obstacle_tiles:
            if tile.colliderect(self.rect):
                if self.dy>0:
                        self.rect.bottom=tile.top
                        self.vel_y=0
                        self.on_ground=True
    
           
  

    def update_state(self):    
        new_state=self.state
        
        if not self.alive:
            if self.state!="Dead":
                self.frames=self.animations['Dead']
                self.state='Dead'
                self.dx=0
                self.dy=0
            return
         #change character animation state
        if self.is_attacking:
            new_state='Attack'
            self.is_attacking=False
        elif self.hit==True:
            new_state='Stunned'
            self.stunned=True
            self.dx=0
            self.dy=0
        elif not self.on_ground and self.is_jumping:
            new_state='Jump'
        elif self.dx!=0 and self.on_ground:
             new_state='Follow'
        else:
            new_state='Idle'

        if new_state!=self.state:
            self.state=new_state
            self.frames=self.animations[new_state]
            self.frame_index=0
    
    # def update_animation(self):

    #     if self.state == 'Dead':
    #         self.frames = self.animations['Dead']
    #     elif self.state=='Stunned':
    #         self.frames=self.animations['Stunned']
    #     elif self.state == 'Attack':
    #         self.frames = self.animations['Attack']
    #     elif self.state == 'Follow':
    #         self.frames = self.animations['Walk']
    #     elif self.state == 'Run':
    #         self.frames = self.animations['Run']
    #     elif self.state=='Jump':
    #         self.frames = self.animations['Jump']
    #     else:
    #         self.frames = self.animations['Idle']
           



    def draw(self,surface):  
        #create a rect for image
        image_rect=self.image.get_rect()
        #move the center of the image to the center of collision box
        image_rect.midbottom=self.rect.midbottom

        if self.facing_right==False:
             flipped_image=pygame.transform.flip(self.image,True,False)
             surface.blit(flipped_image,image_rect)
        else:
             surface.blit(self.image,image_rect)
        pygame.draw.rect(surface,cons.RED,self.rect,1)  
        

  

