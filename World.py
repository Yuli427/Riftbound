import pygame
import Constants as cons

class World():
    def __init__(self):
        # A list that stores render data for every tile in the level.
        # Each entry looks like: [image, rect, x, y]
        self.map_tiles=[]
        self.object_tiles=[]
        self.obstacle_tiles=[]

        self.scroll_x=0
        self.scroll_y=0

        self.world_width=cons.COLUMN*cons.TILE_SIZE
        self.world_height=cons.ROWS*cons.TILE_SIZE



        

    
    def process_data(self,world_data,layer_data,object_data,platform_data,tile_list,obj_tile_list,is_level2,is_level1):
        # Number of rows in world data
        self.level_length=len(world_data)

        #BACKGROUND TILE
        # Loop through each row in the level data
        for y,row in enumerate(world_data):
             # Loop through each tile index in the current row
            for x,tile in enumerate(row):
                #image is the image of this tile
                image=tile_list[tile]
                #create rect for this image
                image_rect=image.get_rect()
                #calculate x and y of tile
                image_x=x*cons.TILE_SIZE
                image_y=y*cons.TILE_SIZE

                #image rect.top left coordinate= x and y of tile
                image_rect.x=image_x
                image_rect.y=image_y
                #image rect center= x,y of tile
                #image_rect.center=(image_x,image_y)
                tile_data=[image,image_rect,image_x,image_y]
                
                #check tile is not -1
                if tile>=0:
                 self.map_tiles.append(tile_data)

                #COLLISION TILE
                # Read the value from the collision/platform layer at grid cell (x, y).
                # platform_data is a 2D grid where each number indicates whether this tile should have collision.
                platform_tile=platform_data[y][x]
                if platform_tile>=0: # If this cell is solid, we create a Rect hitbox for collision detection (not for rendering).
                   # Convert grid coordinates (x, y) into world pixel coordinates by multiplying by TILE_SIZE.
                   rect=pygame.Rect(x*cons.TILE_SIZE,y*cons.TILE_SIZE,cons.TILE_SIZE,cons.TILE_SIZE)
                   self.obstacle_tiles.append(rect) 
        if is_level2:
            for y,row in enumerate(layer_data):
                    # Loop through each tile index in the current row
                    for x,tile in enumerate(row):
                        #image is the image of this tile
                        image=tile_list[tile]
                        #create rect for this image
                        image_rect=image.get_rect()
                        #calculate x and y of tile
                        image_x=x*cons.TILE_SIZE
                        image_y=y*cons.TILE_SIZE

                        #image rect.top left coordinate= x and y of tile
                        image_rect.x=image_x
                        image_rect.y=image_y
                        #image rect center= x,y of tile
                        #image_rect.center=(image_x,image_y)
                        tile_data=[image,image_rect,image_x,image_y]
                        
                        #check tile is not -1
                        if tile>=0:
                         self.map_tiles.append(tile_data)
        
        #OBJECT TILE
        for y,row in enumerate(object_data):
             # Loop through each tile index in the current row
            for x,tile in enumerate(row):
                #1-based csv， index-1 
                if is_level1:
                 image=obj_tile_list[tile-1]
                else:
                 image=obj_tile_list[tile]
                #image = pygame.transform.scale(image, (cons.TILE_SIZE*1.5, cons.TILE_SIZE*1.5))

                #create rect for this image
                image_rect=image.get_rect()

                #calculate x and y of tile,top left coordinate
                image_x=x*cons.TILE_SIZE
                image_y=y*cons.TILE_SIZE

                #find midbottom coordinate
                anchor_x=image_x+cons.TILE_SIZE//2
                anchor_y=image_y+cons.TILE_SIZE
                
                tile_data=[image,image_rect,anchor_x,anchor_y]
                
                #check tile is not -1
                if tile>=0:
                 self.object_tiles.append(tile_data)
        
        
       
                


    def draw(self,surface):

        for tile in self.map_tiles:
            #index 0 is image, index 1 is rect
            surface.blit(tile[0],tile[1])
        
        for tile in self.object_tiles:
           surface.blit(tile[0],tile[1])
           
    def update(self,screen_scroll):
        # Move all rendered map tiles by the camera scroll amount
        for tile in self.map_tiles:
            #update the x coordinate of the image by adding x value of screen_scroll
            tile[2]+=screen_scroll[0]
            #update the y coordinate of image by adding y value of screen_scroll
            tile[3]+=screen_scroll[1]
            
            # Update the render rect to match the new top-left position
            tile[1].topleft=(tile[2],tile[3])
        
        # Move all collision rectangles by the same scroll amount
        for tile in self.obstacle_tiles:
           tile.x+=screen_scroll[0]
           tile.y+=screen_scroll[1]

        #Move object tiles too
        for tile in self.object_tiles:
            #update the x coordinate of the image by adding x value of screen_scroll
            tile[2]+=screen_scroll[0]
            #update the y coordinate of image by adding y value of screen_scroll
            tile[3]+=screen_scroll[1]
            
            # Update the render rect to match the new midbottom position
            tile[1].midbottom=(tile[2],tile[3])
        


    def draw_background(self,screen,bg):
        # Get the background image dimensions (in pixels)
        bg_w = bg.get_width()
        bg_h = bg.get_height()
        
        #把一张背景图当“瓷砖”一样重复铺满整个屏幕
        #x 从 0 开始，每次加 一张背景图的宽度 bg_w,0, bg_w, 2*bg_w, 3*bg_w, ...,y同理
        for x in range(0, cons.SCREEN_WIDTH, bg_w):
         for y in range(0, cons.SCREEN_HEIGHT, bg_h):
           #这里的 (x, y) 就等价于一个 Rect 的 topleft
           screen.blit(bg, (x, y))


 