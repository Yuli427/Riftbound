import pygame
import math
import random
import animation
import Constants as cons
from Weapon import Fire_ball, Charge
from item import Item
import Helper 

class Character():
    #char type=0 player, char type=1 normal enemy, char type=2 enemy without gravity
    def __init__(self,x,y,health,animation,char_type):
        #x,y,w,h(w,h for collision box)
        if char_type=='2':
             self.rect=pygame.Rect(0,0,48,90)
             
             
        else:
            self.rect=pygame.Rect(0,0,48,70)
              #put the center of rect on x and y
            

        self.rect.center=(x,y)
       
        #左右各缩减 10 像素，上下各缩减 4 像素
        #self.hitbox = self.rect.inflate(-2, 0)
        #animation
        self.animations={}
        for key in animation:
         self.animations[key]=Helper.load_image(self,animation[key][0],animation[key][1])
        self.frames=self.animations['Idle']
        #animation setting initilization
        self.frame_index=0
        self.animation_speed=0.15
        self.animation_speed_enemy2=0.05
        self.image=self.frames[0]
        

        self.vel_y=0
        self.on_ground=False
        self.use_gravity=True


        #attributes
        self.char_type=char_type
        self.facing_right=True
        self.health=health
        self.alive=True
        self.score=0
        self.camera_offsety=0

        self.attack_cooldown=0

        self.hit=False
        self.last_hit=pygame.time.get_ticks()
        self.last_fireball_attack=0
        self.fireball_cooldown =700

        self.charge_cooldown=2000 
        self.last_charge_attack=-2000
       
          
        self.has_charged = False

        self.stunned=False
        self.stun_until=0



        self.enemy_state='Idle'
        self.enemy_height=0
        self.remove_me=False
        self.aggro_target = None
        self.aggro_timer = 0
       
        self.player_state='Idle'

        

    def update(self):
        #check if character has died:
        if self.health<=0:
            self.health=0
            self.alive=False
        
        #reset player taking a hit
        hit_cooldown = 1000
        if self.char_type=='0':
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
        
        

        Helper.animate(self)
    
       

    def move(self,dx,dy,world):
        if self.char_type!='3' or(self.char_type=='3' and not self.alive):
         #这里的 vel_y 代表 Vertical Velocity（纵向速度）+= 1：意味着每一帧循环，物体的向下速度都会增加 1 个单位。
         self.vel_y+=1
         #将当前计算出的“瞬时速度”赋值给一个临时变量 dy
         dy=self.vel_y
        
         

        screen_scroll=[0,0]
        #control diagonal speed
        
        #此代码可以在有对角线移动的人物时打开，但是我用了另一个办法
        #if dx!=0 and dy!=0:
             #dx= dx *(math.sqrt(2)/2)
             #dy= dy *(math.sqrt(2)/2)
        
        # X axis
        self.rect.x+=dx
        
        #Y axis
        self.rect.y+=dy


        #角色默认悬空，只有踩到东西才算on ground
        self.on_ground=False
        for tile in world.obstacle_tiles:
            if tile.colliderect(self.rect):
                #dy>0向下掉， 因为py坐标Y2-Y1>0 是下落，因为Y2下去的坐标必须是大于Y1的
                #虽然你是在“跳”，但只要你过了最高点开始回落，dy 就会变成正数（大于 0）。此时，程序就会进入 if dy > 0 的逻辑分支。出现向上跳但是dy>0的情况
                if dy>0:
                    #When jump from bottom to the top, it will check if (now y - dy) your previous bottom is under the platform or above, 
                    # <=tile.top means you were higher than tile so you can go on top of the tile(works for from top to bottom move )
                    if(self.rect.bottom-dy)<=tile.top:
                        self.rect.bottom=tile.top
                        #垂直速度归零
                        self.vel_y=0
                        self.on_ground=True
                #elif dy < 0:
                 #self.rect.top = tile.bottom
                 #self.vel_y = 0
                 #break    


               
            


        
        if self.char_type=='0':
            
        #    target_screen_x=cons.SCREEN_WIDTH  // 2
        #    target_screen_y=cons.SCREEN_HEIGHT // 2 + cons.CAMERA_OFFSET

        #    screen_scroll[0] = target_screen_x - self.rect.centerx
        #    screen_scroll[1] = target_screen_y - self.rect.centery

        #    self.rect.center = (target_screen_x,target_screen_y)
            

            if self.rect.left<=0:
                self.rect.left=0
                dx=0
            
            #because the world is moving but the screen is not, the end of the screen is the width of screen
            if self.rect.right>=cons.SCREEN_WIDTH:
                self.rect.right=cons.SCREEN_WIDTH
                dx=0


            #update scroll based on player pos
            #move camera left and right
        
            min_x=cons.SCREEN_WIDTH-world.world_width
            max_x=0

            if self.rect.right>(cons.SCREEN_WIDTH-cons.SCROLL_THRESH):
                if world.scroll_x>min_x:
                 screen_scroll[0]=(cons.SCREEN_WIDTH-cons.SCROLL_THRESH)-self.rect.right
                 self.rect.right=cons.SCREEN_WIDTH-cons.SCROLL_THRESH
                else:
                    screen_scroll[0]=0
        
            if self.rect.left<cons.SCROLL_THRESH:
                if world.scroll_x<max_x:
                 screen_scroll[0]=cons.SCROLL_THRESH-self.rect.left
                 self.rect.left=cons.SCROLL_THRESH
                else:
                    screen_scroll[0]=0

            
            #platform y-axis camera
            min_y=cons.SCREEN_HEIGHT-world.world_height
            max_y=0

            bottom_line = cons.SCREEN_HEIGHT - cons.SCROLL_THRESH
            if self.rect.bottom>bottom_line and dy>0:
                # world.scroll_y > min_y 说明还没滚到世界最底（例如 -150 > -200），还能继续滚
                if world.scroll_y>min_y:
                    overshoot=self.rect.bottom-bottom_line
                    step=min(overshoot,dy)
                    screen_scroll[1]=-step
                    self.rect.bottom=bottom_line
            
       

            top_line=cons.SCROLL_THRESH
            if self.rect.top<top_line and dy<0 and self.on_ground==False:
                # world.scroll_y < max_y 说明当前还没到世界顶部（例如 -50 < 0），还能继续往上滚
                if world.scroll_y<max_y:
                    overshoot=top_line-self.rect.top
                    step=min(overshoot,-dy)#dy is <0
                    screen_scroll[1]=step #world to down
                    self.camera_offsety+=step
                    self.rect.top=top_line
                else:
                    screen_scroll[1]=0

        
            #     step=min(self.camera_offsety,6)
            #     screen_scroll[1]=-step # when player back to ground world to up
            #     self.camera_offsety-=step
                
            
            
            # top down camera logic in y axis
            # if self.rect.top<cons.SCROLL_THRESH:
            #     screen_scroll[1]=cons.SCROLL_THRESH-self.rect.top
            #     self.rect.top=cons.SCROLL_THRESH
            
            # if self.rect.bottom>(cons.SCREEN_HEIGHT-cons.SCROLL_THRESH):
            #     screen_scroll[1]=(cons.SCREEN_HEIGHT-cons.SCROLL_THRESH)-self.rect.bottom
            #     self.rect.bottom=cons.SCREEN_HEIGHT-cons.SCROLL_THRESH
            

        return screen_scroll
            

             
    
    def ai(self,fireball_image,player,alliance,world,screen_scroll):
       
        now = pygame.time.get_ticks()
        clipped_line=()
        fire_ball_place_holder=None
        charge_place_holder=None
        
        ai_dx=0
        ai_dy=0
        #reposition enemy based on screen scroll
        self.rect.x+=screen_scroll[0]
        self.rect.y+=screen_scroll[1]   
        
        hit_wall,reached_edge=Helper.ground_ahead(self,world)
       
        #calculate distance between player
        dist=math.sqrt(((self.rect.centerx-player.rect.centerx)**2) + ((self.rect.centery-player.rect.centery)**2))
        dist_alliance=math.sqrt(((self.rect.centerx-alliance.rect.centerx)**2) + ((self.rect.centery-alliance.rect.centery)**2))

        #create a line of sight from the enemy to the player (start and end point) 
        line_of_sight=((self.rect.centerx,self.rect.centery),(player.rect.centerx,player.rect.centery))
        #check the obstacle on line of sight,if there is obstacle which means enemy should not see the player and do not approach to it
        for obstacle in world.obstacle_tiles:
            if obstacle.clipline(line_of_sight): #存的rect本身所以不用访问元素
                clipped_line=obstacle.clipline(line_of_sight)
                break  # if there is clipped line stop checking other tiles
        #dist < ATTACK_RANGE 的几何形状是一个圆, so if player in the circle enemy can hit it
        dy=abs(self.rect.centery-player.rect.centery)
        dy_alliance=abs(self.rect.centery-alliance.rect.centery) #当敌人在玩家上方时，dy 是正数；当敌人在玩家下方时，dy 就会变成负数。
        #default idle state
        if self.health<=0 or self.alive==False:
            self.enemy_state='Dead'
        else:
            self.enemy_state='Idle' 
        #state priority=stunned,attack,walk,idle
            if self.stunned:
                self.enemy_state='Stunned'
            elif self.char_type=='3':
             self.vel_y=0
             if dist<500:
                 if dist>50:
                     self.enemy_state='Walk'
                     # 计算怪到玩家的向量差,向量方向
                     dx_vec = player.rect.centerx - self.rect.centerx
                     dy_vec = player.rect.centery - self.rect.centery
                     # 归一化：方向 * 速度(normalization)   
                     if dist > 0:
                            ai_dx = (dx_vec / dist) * cons.ENEMY_SPEED
                            ai_dy = (dy_vec / dist) * cons.ENEMY_SPEED
                     self.has_charged=False
                     
                 else:
                  #当前时间 - 上次攻击时间 >= 冷却时间,如果上次时间为0的话，那要等到当前时间为冷却时间位置
                  self.enemy_state='Attack'
                  ai_dx=0
                  ai_dy=0
                  # 检查冷却：如果是第一次（last为负值）或冷却时间已到
                  if self.char_type=='3':
                    if not self.has_charged:
                        charge = Charge(self, animation.charge_animation, self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery)
                        charge_place_holder = charge
                        self.has_charged=True
                        self.last_charge_attack = now
            else:
                #attack player 
                if dist<cons.ATTACK_RANGE and dy<20 and not clipped_line:
                  self.enemy_state='Attack'
                  ai_dx=0
                  if player.hit==False:
                     #print(f"[DMG] id={id(self)} hp={self.health} alive={getattr(self,'alive',None)} "f"dist={dist:.1f} dy={dy} "f"enemy=({self.rect.centerx},{self.rect.centery}) "f"player=({player.rect.centerx},{player.rect.centery}) "f"t={pygame.time.get_ticks()}")
                     #player.health-=10
                     player.hit=True
                     player.last_hit=pygame.time.get_ticks()
                     #boss enemy shoot fireballs
                elif dist_alliance<cons.ATTACK_RANGE and dy_alliance<20 and not clipped_line:
                  self.enemy_state='Attack'
                  if alliance.hit==False and alliance.alive:
                      alliance.hit=True
                      alliance.health-=40
                      alliance.last_hit=pygame.time.get_ticks()

                elif self.char_type=='2' and dist<500:
                  self.enemy_state='Ranged_Attack'
                  if pygame.time.get_ticks()-self.last_fireball_attack>=self.fireball_cooldown:
                         fireball=Fire_ball(fireball_image,self.rect.centerx,self.rect.centery,player.rect.centerx,player.rect.centery)
                         fire_ball_place_holder=fireball
                         self.last_fireball_attack=pygame.time.get_ticks()
            
                elif not clipped_line:#if the enemy can see the player and they are far from player, they go towards the player
                    
                    #先检查是否有路没有的话不走dx=0
                    if hit_wall or reached_edge:
                        ai_dx=0
                    else:
                    #有的话向玩家走
                    #能看到玩家 → 目标明确，到边缘就停 ai_dx=0，不需要翻转
                     if self.char_type=='4':
                            self.enemy_state='Run'
                            #make enemy move to player
                            if self.rect.centerx>player.rect.centerx:
                                ai_dx=-cons.ENRO_SPEED
                            elif self.rect.centerx<player.rect.centerx:    
                                ai_dx=cons.ENRO_SPEED
                            else:
                                ai_dx=0
                     else:
                            self.enemy_state='Walk'
                            #make enemy move to player
                            if self.rect.centerx>player.rect.centerx:
                                ai_dx=-cons.ENEMY_SPEED
                            elif self.rect.centerx<player.rect.centerx:    
                                ai_dx=cons.ENEMY_SPEED
                            else:
                                ai_dx=0


                else: #游走的时候需要反转
                    self.enemy_state='Walk'

                    if hit_wall or reached_edge:
                        self.facing_right=not self.facing_right
                        
                    if self.facing_right:
                            ai_dx=cons.ENEMY_SPEED
                    elif not self.facing_right:
                            ai_dx=-cons.ENEMY_SPEED
                    

   
        #因为重力在move，所以无论什么情况都得调用
        if self.enemy_state in ['Walk', 'Idle', 'Dead', 'Attack','Run']:
         self.move(ai_dx,ai_dy,world)
    

        #enemy stat         
        if self.enemy_state=='Dead':
            self.frames=self.animations['Dead']
            if self.frame_index==len(self.frames)-1:
                animation_finished = self.frame_index >= len(self.frames) - 1
                if animation_finished:
                    if self.on_ground:
                        self.remove_me=True
        elif self.enemy_state=='Stunned':
            self.frames=self.animations['Stunned']
        elif self.enemy_state=='Attack' or self.enemy_state=='Ranged_Attack':
            self.frames=self.animations['Attack']
        elif self.enemy_state=='Walk':
            self.frames=self.animations['Walk']
            if ai_dx>0:
                self.facing_right=True
            else:
                self.facing_right=False
        elif self.enemy_state=='Run':
            self.frames=self.animations['Run']
            if ai_dx>0:
                self.facing_right=True
            else:
                self.facing_right=False
        else:
            self.frames=self.animations['Idle']
        
        

      
        return charge_place_holder,fire_ball_place_holder


    def draw(self,surface):
        
        #create a rect for image
        image_rect=self.image.get_rect()
        #move the center of the image to the center of collision box
        image_rect.midbottom=self.rect.midbottom
        
        if self.char_type=='2':
            image_rect.center=self.rect.center
            #把图片向上移动，不用移动hitbox
            #image_rect.centery=self.rect.centery-15
            image_rect.centery = self.rect.centery
        
        
        if self.facing_right==False:
             flipped_image=pygame.transform.flip(self.image,True,False)
             surface.blit(flipped_image,image_rect)
        else:
             surface.blit(self.image,image_rect)
        pygame.draw.rect(surface,cons.RED,self.rect,1)  
        
   

    def update_player_state(self,dx,dy,is_attacking,is_dashing,is_jumping):    
        new_state=self.player_state
        #physical changes 物理逻辑：跳跃触发（放在前面，不影响动画判断）
        if is_jumping==True and self.on_ground:
             self.vel_y=-20
             self.on_ground=False

        if not self.alive:
            if self.player_state!="Dead":
                self.frames=self.animations['Dead']
                self.player_state='Dead'
            return
         #change character animation state
        if is_attacking==True:
            new_state='Attack'
            is_attacking=False
        elif self.hit==True:
            new_state='Hurt'
        elif is_dashing==True:
            new_state='Dash'
            is_dashing=False
        elif not self.on_ground:
            new_state='Jump'
        elif dx!=0 and self.on_ground:
             new_state='Walk'
             if dx<0:
                 self.facing_right=False
             else:
                 self.facing_right=True
        elif dx==0 and dy==0 and self.alive==True:
            new_state='Idle'

        if new_state!=self.player_state:
            self.player_state=new_state
            self.frames=self.animations[new_state]
            self.frame_index=0

            
        
    def attack(self,enemylist):
        damage=0
        damage_pos=None
        hit_enemy=None
        
        # in cooldown can not attack
        if self.attack_cooldown>0:
            return 0, None, None
        
        #reset cooldown time
        self.attack_cooldown=10

      
        for enemy in enemylist:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                damage=random.randint(80,100)
                enemy.health-=damage
                hit_enemy=enemy
                damage_pos=enemy.rect
         

        return damage,damage_pos,hit_enemy


    def apply_knockback(self,player,world):
      #decide which direction should enemy knockback
      if self.rect.centerx>=player.rect.centerx:
        push_dx=cons.KNOCKBACK_PX
      else:
        push_dx=-cons.KNOCKBACK_PX    
        
    #move the enemy pos my push_dx
      self.move(push_dx,0,world)
        
      self.stunned=True
      self.stun_until=cons.STUN_TIME



        
        