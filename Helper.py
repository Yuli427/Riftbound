import pygame
import Constants as cons

def load_image(self,filename,frame_num):

        sheet=pygame.image.load(filename)
        frames=[]
        frame_width=sheet.get_width()//frame_num
        frame_height=sheet.get_height()

        for i in range(frame_num):
            frame=sheet.subsurface(i*frame_width,0,frame_width,frame_height)
            frames.append(frame)
        return frames
        
    
def animate(self):
        #animation control
        self.frame_index+=self.animation_speed
        if self.frame_index>=len(self.frames):
            if not self.alive: #if player dead stop the frame index on the last frame
                 self.frame_index=len(self.frames)-1
            else:
                 self.frame_index=0
        self.image=self.frames[int(self.frame_index)]


def ground_ahead(self,world):
        
        # --- 边缘检测与墙壁检测 ---
        # 探测点：在移动方向前方 30 像素
        if self.facing_right==True:
            check_x=self.rect.centerx+30
        else:
            check_x=self.rect.centerx-30
        #脚下5像素
        check_y=self.rect.bottom+5
        reached_edge = True
        hit_wall=False

        for tile in world.obstacle_tiles:
            # 如果探测点下方有任何地板，说明没到边缘
            if  tile.collidepoint(check_x,check_y):
                reached_edge=False
            #自身腰部的位置左右是否有障碍物
            if tile.collidepoint(check_x,self.rect.centery):
                hit_wall=True
        return hit_wall, reached_edge
    