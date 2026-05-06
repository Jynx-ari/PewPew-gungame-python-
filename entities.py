import pygame
import math
import random
from config import *

class Bullet:
    def __init__(self, pos, vel, bullet_type="normal", lifetime=None):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)
        self.type = bullet_type
        self.lifetime = lifetime

    def update(self):
        self.pos += self.vel
        if self.lifetime is not None:
            self.lifetime -= 1

    def draw(self, screen, camera, shake_off):
        screen_pos = self.pos - camera + shake_off
        if self.type == "explosion":
            pygame.draw.circle(screen, (255, 165, 0), screen_pos, 5)
        else:
            pygame.draw.circle(screen, (255, 255, 255), screen_pos, 3)

class Enemy:
    def __init__(self, pos, stage, scaling=1.0):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0, 0)
        self.scaling = scaling
        
        # Determine HP based on stage
        self.hp = 1
        if random.random() < STAGE_HP_CHANCE[stage]:
            self.hp = int(random.randint(2, STAGE_MAX_HP[stage]) * scaling)

    def update(self, player_pos, stage):
        current_enemy_speed = (ENEMY_SPEED + (stage - 1) * STAGE_SPEED_BOOST) * self.scaling
        desired_vel = (player_pos - self.pos).normalize() * current_enemy_speed
        self.vel += (desired_vel - self.vel) * 0.05
        self.pos += self.vel

    def draw(self, screen, camera, shake_off):
        screen_pos = self.pos - camera + shake_off
        border_width = 2 + (self.hp - 1) * 2
        pygame.draw.circle(screen, (255, 60, 60), screen_pos, 12, border_width)

class ExplosionEffect:
    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.lifetime = 30
        self.radius = 150

    def update(self):
        self.lifetime -= 1

    def draw(self, screen, camera, shake_off):
        if self.lifetime <= 0:
            return
        
        progress = 1 - (self.lifetime / 30)
        for i in range(3):
            radius = self.radius * (progress + i * 0.2)
            alpha = max(0, 200 - i * 60 - int(progress * 150))
            if alpha > 0:
                exp_screen_pos = self.pos - camera + shake_off
                # Optimized surface size
                surf_size = int(radius * 2)
                explosion_surf = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)
                pygame.draw.circle(explosion_surf, (255, 100, 0, alpha), (int(radius), int(radius)), int(radius), 2 if i == 0 else 1)
                screen.blit(explosion_surf, (int(exp_screen_pos.x - radius), int(exp_screen_pos.y - radius)))
