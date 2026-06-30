import pygame
import random
import Constants as cons
import Audio
from Character import Character
from Character_types import PLAYER


class Player(Character):
    def __init__(self, x, y, health, animation, char_type=PLAYER):
        super().__init__(x, y, health, animation, char_type)
        self.attack_anim_until = 0
        self.attack_anim_duration = 700
        self.attack_combo_count = 0
        self.combo_max = 3
        self.combo_cooldown = 100
        self.last_attack_time = 0
        self.combo_reset_time = 800
        
        


    def handle_player_camera(self, dx, dy, world, screen_scroll):
        # Keep player inside screen x bounds
        if self.rect.left <= 0:
            self.rect.left = 0
            dx = 0

        if self.rect.right >= cons.SCREEN_WIDTH:
            self.rect.right = cons.SCREEN_WIDTH
            dx = 0

        # Horizontal camera scroll
        min_x = cons.SCREEN_WIDTH - world.world_width
        max_x = 0

        if self.rect.right > cons.SCREEN_WIDTH - cons.SCROLL_THRESH:
            if world.scroll_x > min_x:
                screen_scroll[0] = (cons.SCREEN_WIDTH - cons.SCROLL_THRESH) - self.rect.right
                self.rect.right = cons.SCREEN_WIDTH - cons.SCROLL_THRESH
            else:
                screen_scroll[0] = 0

        if self.rect.left < cons.SCROLL_THRESH:
            if world.scroll_x < max_x:
                screen_scroll[0] = cons.SCROLL_THRESH - self.rect.left
                self.rect.left = cons.SCROLL_THRESH
            else:
                screen_scroll[0] = 0

        # Vertical camera scroll
        min_y = cons.SCREEN_HEIGHT - world.world_height
        max_y = 0

        bottom_line = cons.SCREEN_HEIGHT - cons.SCROLL_THRESH

        if self.rect.bottom > bottom_line and dy > 0:
            if world.scroll_y > min_y:
                overshoot = self.rect.bottom - bottom_line
                step = min(overshoot, dy)
                screen_scroll[1] = -step
                self.rect.bottom = bottom_line

        top_line = cons.SCROLL_THRESH

        if self.rect.top < top_line and dy < 0 and not self.on_ground:
            if world.scroll_y < max_y:
                overshoot = top_line - self.rect.top
                step = min(overshoot, -dy)
                screen_scroll[1] = step
                self.camera_offsety += step
                self.rect.top = top_line
            else:
                screen_scroll[1] = 0

        return screen_scroll


    def update_player_state(self, dx, dy, is_attacking, is_dashing, is_jumping):
        new_state = self.player_state

        if not self.alive:
            if self.player_state != "Dead":
                self.frames = self.animations['Dead']
                self.player_state = 'Dead'
            return

        if self.is_freezed:
            if pygame.time.get_ticks() - self.last_freeze > self.freeze_timer:
                self.is_freezed = False
            else:
                new_state = 'Freezed'
                self.player_state = new_state
                return

        if is_jumping and self.on_ground:
            self.vel_y = -20
            self.on_ground = False

        now = pygame.time.get_ticks()

        if now < self.attack_anim_until:
            self.player_state='Attack'
            self.frames=self.animations['Attack']
            return
            
        if is_attacking and self.attack_cooldown<=0:
            self.player_state='Attack'
            self.attack_anim_until=now+self.attack_anim_duration
            self.frames=self.animations['Attack']
            self.frame_index=0
            Audio.punch_sound.play()
            if dx < 0:
                self.facing_right = False
            elif dx > 0:
                self.facing_right = True
            return
        elif self.hit:
            new_state = 'Hurt'
        elif is_dashing:
            new_state = 'Dash'
        elif not self.on_ground:
            new_state = 'Jump'
        elif dx != 0 and self.on_ground:
            new_state = 'Walk'
            if dx < 0:
                self.facing_right = False
            elif dx >0:
                self.facing_right = True

        elif dx == 0 and dy == 0 and self.alive:
            new_state = 'Idle'

        if new_state != self.player_state:
            if new_state == 'Freezed':
                self.frames = self.animations['Hurt']
                self.frame_index = 0
            else:
                self.player_state = new_state
                self.frames = self.animations[new_state]
                self.frame_index = 0


    def attack(self, enemylist):
        damage = 0
        damage_pos = None
        hit_enemy = None

        now=pygame.time.get_ticks()
        # if attack is not continous set count to zero
        if now- self.last_attack_time>self.combo_reset_time:
            self.attack_combo_count=0

        self.last_attack_time=now
        self.attack_combo_count+=1

        # if count reaches max, attack cooldown will decrease in charater update
        # player can attack agian after cooldown
        if self.attack_combo_count>=self.combo_max: 
            self.attack_cooldown=self.combo_cooldown
            self.attack_combo_count=0

        #create attack rect
        attack_width = 70
        attack_height = self.rect.height
        if self.facing_right:
            attack_rect = pygame.Rect(
                self.rect.right,
                self.rect.y,
                attack_width,
                attack_height
            )
        else:
            attack_rect = pygame.Rect(
                self.rect.left-attack_width,
                self.rect.y,
                attack_width,
                attack_height
            )


        for enemy in enemylist:
            if enemy.rect.colliderect(attack_rect) and enemy.alive:
                damage = random.randint(25, 35)
                enemy.health -= damage
                hit_enemy = enemy
                damage_pos = enemy.rect

        return damage, damage_pos, hit_enemy