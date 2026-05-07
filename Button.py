import pygame

class Button():
    def __init__(self,x,y,image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
    
    def draw(self,surface):

        action=False
        
        #get mouse pos
        pos=pygame.mouse.get_pos()

        #check mouseover and clicked condition
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]: #the left button of mouse is pressed
                action=True

        surface.blit(self.image,self.rect)

        return action
    
