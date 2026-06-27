import pygame
import math
import animation
import Constants as cons
import Helper
from Character import Character
from Weapon import Fire_ball, Charge, Arrow
from Character_types import (
    RANGED_DEMON,
    CHARGE_DEMON,
    RUNNER_DEMON,
    FLYING_DEMON,
    BOSS,
    FLYING_TYPES
)



class Enemy(Character):
    def __init__(self, x, y, health, animation_data, char_type):
        super().__init__(x, y, health, animation_data, char_type)


    def ai(self, fireball_image, player, alliance, world, screen_scroll):
        self.apply_screen_scroll(screen_scroll)

        charge_place_holder = None
        fire_ball_place_holder = None
        Arrow_place_holder = None

        ai_dx = 0
        ai_dy = 0

        hit_wall, reached_edge = Helper.ground_ahead(self, world)

        dist = self.get_distance_to(player)
        dy_to_player = self.get_vertical_distance_to(player)
        line_blocked = self.is_line_blocked(player, world)

        if self.is_dead():
            self.enemy_state = 'Dead'

        else:
            self.enemy_state = 'Idle'

            if self.stunned:
                self.enemy_state = 'Stunned'

            elif self.char_type in FLYING_TYPES:
                ai_dx, ai_dy, charge_place_holder = self.flying_enemy_ai(player, dist)

            elif self.char_type == BOSS:
                ai_dx, ai_dy, Arrow_place_holder = self.boss_ai(player, dist)

            else:
                ai_dx, fire_ball_place_holder = self.ground_enemy_ai(
                    fireball_image,
                    player,
                    alliance,
                    dist,
                    dy_to_player,
                    line_blocked,
                    hit_wall,
                    reached_edge
                )

        self.apply_enemy_movement(ai_dx, ai_dy, world)
        self.update_enemy_animation(ai_dx)

        return charge_place_holder, fire_ball_place_holder, Arrow_place_holder


    def apply_screen_scroll(self, screen_scroll):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]


    def is_dead(self):
        return self.health <= 0 or not self.alive


    def get_distance_to(self, target):
        if target is None:
            return float('inf')

        return math.sqrt(
            ((self.rect.centerx - target.rect.centerx) ** 2) +
            ((self.rect.centery - target.rect.centery) ** 2)
        )


    def get_vertical_distance_to(self, target):
        if target is None:
            return float('inf')

        return abs(self.rect.centery - target.rect.centery)


    def is_line_blocked(self, target, world):
        if target is None:
            return True

        line_of_sight = (
            (self.rect.centerx, self.rect.centery),
            (target.rect.centerx, target.rect.centery)
        )

        for obstacle in world.obstacle_tiles:
            if obstacle.clipline(line_of_sight):
                return True

        return False


    def flying_enemy_ai(self, player, dist):
        ai_dx = 0
        ai_dy = 0
        charge_place_holder = None

        self.vel_y = 0

        if dist < 500:
            if dist > 50:
                self.enemy_state = 'Walk'

                dx_vec = player.rect.centerx - self.rect.centerx
                dy_vec = player.rect.centery - self.rect.centery

                if dist > 0:
                    ai_dx = (dx_vec / dist) * cons.ENEMY_FLY_SPPED
                    ai_dy = (dy_vec / dist) * cons.ENEMY_FLY_SPPED

                self.has_charged = False

            else:
                self.enemy_state = 'Attack'
                ai_dx = 0
                ai_dy = 0

                if not self.has_charged:
                    if self.char_type == CHARGE_DEMON:
                        charge_place_holder = Charge(
                            self,
                            animation.charge_animation,
                            self.rect.centerx,
                            self.rect.centery,
                            player.rect.centerx,
                            player.rect.centery
                        )

                    elif self.char_type == FLYING_DEMON:
                        charge_place_holder = Charge(
                            self,
                            animation.charge_pink_animation,
                            self.rect.centerx,
                            self.rect.centery,
                            player.rect.centerx,
                            player.rect.centery
                        )

                    self.has_charged = True
                    self.last_charge_attack = pygame.time.get_ticks()

        return ai_dx, ai_dy, charge_place_holder


    def boss_ai(self, player, dist):
        ai_dx = 0
        ai_dy = 0
        Arrow_place_holder = None

        self.vel_y = 0
        self.enemy_state = 'Walk'

        dx_vec = player.rect.centerx - self.rect.centerx
        dy_vec = player.rect.centery - self.rect.centery

        if dist == 0:
            dist = 0.1

        ai_dx = (dx_vec / dist) * cons.ENEMY_SPEED
        ai_dy = (dy_vec / dist) * cons.ENEMY_SPEED

        if dist > cons.LONG_DISTANCE_ATTACK_RANGE:
            self.enemy_state = 'Walk'

        else:
            if player.is_freezed:
                self.enemy_state = 'Attack'
                self.rect.centerx = player.rect.centerx + 50
                self.rect.centery = player.rect.centery

                if self.attack_cooldown <= 0:
                    player.health -= 30
                    player.hit = True
                    player.last_hit = pygame.time.get_ticks()
                    self.attack_cooldown = 60

            else:
                self.enemy_state = 'Ranged_Attack'

                if pygame.time.get_ticks() - self.last_lightning_attack >= self.lightning_cooldown:
                    angle = math.degrees(
                        math.atan2(
                            -(player.rect.centery - self.rect.centery),
                            player.rect.centerx - self.rect.centerx
                        )
                    )

                    Arrow_place_holder = Arrow(
                        None,
                        self.rect.centerx,
                        self.rect.centery,
                        angle,
                        animation.lightning_animation,
                        'Freez'
                    )

                    self.last_lightning_attack = pygame.time.get_ticks()

        return ai_dx, ai_dy, Arrow_place_holder


    def ground_enemy_ai(self, fireball_image, player, alliance, dist, dy_to_player,
                        line_blocked, hit_wall, reached_edge):
        ai_dx = 0
        fire_ball_place_holder = None

        dist_alliance = self.get_distance_to(alliance)
        dy_to_alliance = self.get_vertical_distance_to(alliance)

        if dist < cons.ATTACK_RANGE and dy_to_player < 20 and not line_blocked:
            self.enemy_state = 'Attack'
            ai_dx = 0

            if not player.hit:
                player.health -= 5
                player.hit = True
                player.last_hit = pygame.time.get_ticks()

        elif dist_alliance < cons.ATTACK_RANGE and dy_to_alliance < 20 and not line_blocked:
            self.enemy_state = 'Attack'
            ai_dx = 0

            if alliance is not None and not alliance.hit and alliance.alive:
                alliance.hit = True
                alliance.health -= 10
                alliance.last_hit = pygame.time.get_ticks()

        elif self.char_type == RANGED_DEMON and dist < 500:
            self.enemy_state = 'Ranged_Attack'

            if pygame.time.get_ticks() - self.last_fireball_attack >= self.fireball_cooldown:
                fire_ball_place_holder = Fire_ball(
                    fireball_image,
                    self.rect.centerx,
                    self.rect.centery,
                    player.rect.centerx,
                    player.rect.centery
                )

                self.last_fireball_attack = pygame.time.get_ticks()

        elif not line_blocked and dy_to_player < 60:
            ai_dx = self.chase_player(player, hit_wall, reached_edge)

        else:
            ai_dx = self.patrol(hit_wall, reached_edge)

        return ai_dx, fire_ball_place_holder


    def chase_player(self, player, hit_wall, reached_edge):
        if hit_wall or reached_edge:
            return 0

        if self.char_type == RUNNER_DEMON:
            self.enemy_state = 'Run'
            speed = cons.ENRO_SPEED
        else:
            self.enemy_state = 'Walk'
            speed = cons.ENEMY_SPEED

        if self.rect.centerx > player.rect.centerx:
            return -speed
        elif self.rect.centerx < player.rect.centerx:
            return speed

        return 0


    def patrol(self, hit_wall, reached_edge):
        self.enemy_state = 'Walk'

        if hit_wall or reached_edge:
            self.facing_right = not self.facing_right

        if self.facing_right:
            return cons.ENEMY_SPEED_SLOW

        return -cons.ENEMY_SPEED_SLOW


    def apply_enemy_movement(self, ai_dx, ai_dy, world):
        if self.enemy_state in ['Walk', 'Idle', 'Dead', 'Attack', 'Run', 'Stunned']:
            self.move(ai_dx, ai_dy, world)


    def update_enemy_animation(self, ai_dx):
        if self.enemy_state == 'Dead':
            self.frames = self.animations['Dead']

            if self.frame_index == len(self.frames) - 1:
                animation_finished = self.frame_index >= len(self.frames) - 1

                if animation_finished:
                    if self.on_ground:
                        self.remove_me = True

        elif self.enemy_state == 'Stunned':
            self.frames = self.animations['Stunned']

        elif self.enemy_state == 'Attack':
            self.frames = self.animations['Attack']

        elif self.enemy_state == 'Ranged_Attack':
            if self.char_type == 'Boss':
                self.frames = self.animations['Ranged_Attack']

                if ai_dx > 0:
                    self.facing_right = True
                else:
                    self.facing_right = False

            else:
                self.frames = self.animations['Attack']

        elif self.enemy_state == 'Walk':
            self.frames = self.animations['Walk']

            if ai_dx > 0:
                self.facing_right = True
            else:
                self.facing_right = False

        elif self.enemy_state == 'Run':
            self.frames = self.animations['Run']

            if ai_dx > 0:
                self.facing_right = True
            else:
                self.facing_right = False

        else:
            self.frames = self.animations['Idle']

    
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

                

