import pygame
import Constants as cons

#load heart
heart_empty=pygame.image.load('assets/hearts/emptyheart.png')
heart_half=pygame.image.load('assets/hearts/halfheart.png')
heart_full=pygame.image.load('assets/hearts/fullheart.png')


class ScreenFade():
    def __init__(self,direction,color,speed):
        self.direction=direction
        self.color=color
        self.speed=speed
        self.fade_counter=0
    
    def fade(self,screen):
        fade_complete=False

        self.fade_counter+=self.speed
        if self.direction==1:#whole screen fade
            pygame.draw.rect(screen,self.color,(0-self.fade_counter,0,cons.SCREEN_WIDTH//2,cons.SCREEN_HEIGHT))
            pygame.draw.rect(screen,self.color,(cons.SCREEN_WIDTH//2+self.fade_counter,0,cons.SCREEN_WIDTH,cons.SCREEN_HEIGHT))
            pygame.draw.rect(screen,self.color,(0,0-self.fade_counter,cons.SCREEN_WIDTH,cons.SCREEN_HEIGHT//2))
            pygame.draw.rect(screen,self.color,(0,cons.SCREEN_HEIGHT//2+self.fade_counter,cons.SCREEN_WIDTH,cons.SCREEN_HEIGHT))
        elif self.direction==2:#vertical screen fade
            pygame.draw.rect(screen,self.color,(0,0,cons.SCREEN_WIDTH,0+self.fade_counter))

        if self.fade_counter>=cons.SCREEN_WIDTH:
            fade_complete=True
        
        return fade_complete
        
class Text():
    def __init__(self, x, y, text, font, color, line_spacing=2):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.color = color
        self.line_spacing = line_spacing
        self.rect = pygame.Rect(x, y, 1, 1)

    def update(self,screen_scroll):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

    def draw_vertical_text(self,screen):
            y_offset=0

            for char in self.text:
                if char=='\n':
                    continue
                img=self.font.render(char,True,self.color) #render each char each time
                rect=img.get_rect(topleft=(self.x,self.y+y_offset))
                screen.blit(img,(self.rect.x,self.rect.y+y_offset))
                y_offset+=img.get_height()+self.line_spacing
    
    
    def draw_text(self,screen):
            img=self.font.render(self.text,True,self.color)
            screen.blit(img,(self.x,self.y))
            
    

def draw_health_bar(screen,player,screen_scroll):
    half_heart_drawn=False
    for i in range(5):
        x=player.rect.x-heart_full.get_width()+i*heart_full.get_width()
        y=player.rect.top-20

        if player.health>=((i+1)*20):
            screen.blit(heart_full,(x,y))
        elif (player.health)%20>0 and half_heart_drawn==False:
             screen.blit(heart_half,(x,y))
             half_heart_drawn=True
        else:
            screen.blit(heart_empty,(x,y))
        



def draw_grid(screen):
    for x in range(60):
        pygame.draw.line(screen,cons.WHITE,(x*cons.TILE_SIZE,0),(x*cons.TILE_SIZE,cons.SCREEN_HEIGHT))
        pygame.draw.line(screen,cons.WHITE,(0,x*cons.TILE_SIZE),(cons.SCREEN_WIDTH,x*cons.TILE_SIZE))


def draw_square(screen):
    hud_height=cons.SCREEN_HEIGHT//9
    #创建一个支持透明度的 Surface (宽度, 高度)
    hud_surface=pygame.Surface((cons.SCREEN_WIDTH,hud_height),pygame.SRCALPHA)
    #100 代表的是 Alpha（透明度） 通道的值
    pygame.draw.rect(hud_surface,(255,255,255,150),(0,0,cons.SCREEN_WIDTH,hud_height))
    screen.blit(hud_surface,(0,0))

def draw_shop_menu(screen, font, player_money, current_level):
    overlay = pygame.Surface((cons.SCREEN_WIDTH, cons.SCREEN_HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(150)
    screen.blit(overlay, (0, 0))

    if current_level == '1':
        lines = [
            "Guess what? You can buy friends in this game,",
            "even though you might not be able to in real life...",
            f"Your Money: ${player_money}",
            "",
            f"Press [1] to buy Fujiwara Rin    {cons.Fujiwara_Rin}",
            f"Press [2] to buy Vesper Blanche  {cons.Vesper}",
            f"Press [3] to buy Himura Fuma     {cons.Himura}",
            f"Press [4] to buy Ares            {cons.Ares}",
            "Press [ESC] to leave"
        ]
    else:
        lines = [
            "If you wish to replace your alliance with a new one,",
            "it is time to do so...",
            f"Your Money: ${player_money}",
            "",
            f"Press [1] to buy Fujiwara Rin    {cons.Fujiwara_Rin}",
            f"Press [2] to buy Vesper Blanche  {cons.Vesper}",
            f"Press [3] to buy Himura Fuma     {cons.Himura}",
            f"Press [4] to buy Ares            {cons.Ares}",
            "Press [ESC] to leave"
        ]

    line_height = font.get_height() + 10

    # Calculate text block size
    text_widths = [font.size(line)[0] for line in lines]
    menu_width = max(text_widths)

    total_height = len(lines) * line_height

    start_x = cons.SCREEN_WIDTH // 2 - menu_width // 2
    start_y = cons.SCREEN_HEIGHT // 2 - total_height // 2

    for i, line_content in enumerate(lines):
        color = (255, 215, 0) if 'Your Money' in line_content else cons.PURPLE

        line_text = Text(
            start_x,
            start_y + i * line_height,
            line_content,
            font,
            color
        )
        line_text.draw_text(screen)

def draw_text_screen(screen,font,message):
      overlay = pygame.Surface((cons.SCREEN_WIDTH, cons.SCREEN_HEIGHT))
      overlay.fill((0,0,0))
      overlay.set_alpha(150)
      screen.blit(overlay, (0,0))

      lines = [message]
      
      start_x = 30
      start_y = cons.SCREEN_HEIGHT//2
      line_height = 35
      
      for i,line_content in enumerate(lines):
       color=(255, 215, 0) if 'Your Money'in line_content else cons.PURPLE
       line_text=Text(start_x,start_y+(i*line_height),line_content,font,color)
       line_text.draw_text(screen)

def draw_victory(screen,font):
      overlay = pygame.Surface((cons.SCREEN_WIDTH, cons.SCREEN_HEIGHT))
      overlay.fill((0,0,0))
      overlay.set_alpha(150)
      screen.blit(overlay, (0,0))

      lines = [
        "You won! good job!"]
      
      start_x = cons.SCREEN_WIDTH//2-30
      start_y = cons.SCREEN_HEIGHT//2
      line_height = 35
      
      for i,line_content in enumerate(lines):
       color=(255, 215, 0) if 'Your Money'in line_content else cons.PURPLE
       line_text=Text(start_x,start_y+(i*line_height),line_content,font,color)
       line_text.draw_text(screen)
      
def draw_dialog(screen, font,sentence):
      
      
      overlay = pygame.Surface((cons.SCREEN_WIDTH, cons.SCREEN_HEIGHT//3))
      overlay.fill((0,0,0))
      overlay.set_alpha(60)
      # 画在屏幕底部
      screen.blit(overlay, (0, cons.SCREEN_HEIGHT - cons.SCREEN_HEIGHT//4))
    
     
      max_width = cons.SCREEN_WIDTH - 10  # 左右各留30像素边距
      words = sentence.split(' ')         # 按空格拆分单词
      lines = []
      current_line = ""

      for word in words:
            # 测试如果加上这个单词，长度是否超过限制
            test_line = current_line + word + " "
            if font.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                lines.append(current_line)  # 换行
                current_line = word + " "
      lines.append(current_line)          # 加入最后一行

      start_x = 20
      start_y = (cons.SCREEN_HEIGHT - cons.SCREEN_HEIGHT//5)
      line_height = 35
      
      for i,line_content in enumerate(lines):
       color=(255, 215, 0) if 'Your Money'in line_content else cons.PURPLE
       line_text=Text(start_x,start_y+(i*line_height),line_content,font,color)
       line_text.draw_text(screen)
    

def draw_choose_menu(screen, font, player_name, selected_gender, game_name, input_active):
    overlay = pygame.Surface((cons.SCREEN_WIDTH, cons.SCREEN_HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(150)
    screen.blit(overlay, (0, 0))

    center_x = cons.SCREEN_WIDTH // 2

    menu_width = 420
    menu_x = center_x - menu_width // 2

    title_y = 80
    name_label_y = 190
    input_box_y = 235
    gender_label_y = 320
    gender_btn_y = 365
    confirm_y = 470

    

    # title
    title = Text(center_x - 100, title_y, game_name, font, (255, 215, 0))
    title.draw_text(screen)

    # enter name text
    name_label = Text(menu_x, name_label_y, 'Enter your name:', font, cons.PURPLE)
    name_label.draw_text(screen)

    # enter name box
    input_box = pygame.Rect(menu_x, input_box_y, menu_width, 45)
    pygame.draw.rect(screen, cons.WHITE, input_box, 2)

    name_text = Text(menu_x + 12, input_box_y + 8, player_name, font, cons.WHITE)
    name_text.draw_text(screen)

    # gender text
    gender_label = Text(menu_x-100, gender_label_y, 'Press <- and -> to choose', font, cons.PURPLE)
    gender_label.draw_text(screen)

    # gender buttons
    male_x = menu_x
    female_x = menu_x + 180

    male_color = (255, 215, 0) if selected_gender == 'Male' else cons.WHITE
    female_color = (255, 215, 0) if selected_gender == 'Female' else cons.WHITE

    male_btn = Text(male_x, gender_btn_y, '[Male]', font, male_color)
    female_btn = Text(female_x, gender_btn_y, '[Female]', font, female_color)

    male_btn.draw_text(screen)
    female_btn.draw_text(screen)

    # confirm
    confirm = Text(menu_x-50, confirm_y, 'Press ENTER to start', font, cons.PURPLE)
    confirm.draw_text(screen)