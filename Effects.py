import pygame

class dagameText(pygame.sprite.Sprite):
    def __init__(self,x,y,damage,color,font):
        #call parent init method to register
        pygame.sprite.Sprite.__init__(self)
        self.image=font.render(damage,True,color)
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
        self.counter=0
    
    def update(self,screen_scroll):
        #reposition enemy based on screen scroll
        self.rect.x+=screen_scroll[0]
        self.rect.y+=screen_scroll[1]
        #move damage text up by 3 pixle
        self.rect.y-=3
        #delete the counter after few seconds
        self.counter+=1
        if self.counter>30:
            self.kill()