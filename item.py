import pygame
import Helper
import UI
import Audio
import Constants as cons


class Item(pygame.sprite.Sprite):
    def __init__(self,x,y,item_type,image,animation,is_icon=False):
        pygame.sprite.Sprite.__init__(self)

        
        self.frame_index=0
        self.animation_speed=0.15
        self.update_time=pygame.time.get_ticks()
        self.pending_dialog=''



        if animation==None:
             self.frames=[image]
             self.image=image
        else:
             self.animations={}
             for key in animation:
                 self.animations[key]=Helper.load_image(self,animation[key][0],animation[key][1])
             self.frames=self.animations['Idle']
             self.image=self.frames[self.frame_index]
        
        self.item_type=item_type
        if not is_icon:
            self.rect=pygame.Rect(0,0,20,20)
        else:
           self.rect=self.image.get_rect()
        self.rect.center=(x,y)
        self.is_icon=is_icon
        
        
    def draw(self,surface):
        surface.blit(self.image,self.rect)
        #pygame.draw.rect(surface,cons.RED,self.rect,1)  
    

    def update(self,screen_scroll,player,is_boss_spawned):
            
            Helper.animate(self)
            if not self.is_icon:
             #reposition based on screen scroll
             self.rect.x+=screen_scroll[0]
             self.rect.y+=screen_scroll[1]

            if player.rect.colliderect(self.rect):
                #icon
                if self.item_type=='0':
                 return
                #money    
                elif self.item_type=='1':
                     player.score+=100
                     Audio.pickup.play()
                     #player.health+=10
                     #if player.health>100:
                          #player.health=100
                #potion
                elif self.item_type=='2':
                     player.alive=True
                     if not is_boss_spawned:
                      player.health+=30
                     else:
                      player.health+=50
                     Audio.health_recharge.play()
                self.kill()


    


