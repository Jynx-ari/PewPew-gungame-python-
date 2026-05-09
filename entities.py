import pygame
import math
import random
from config import *

class Bullet:
    _surfaces = {}

    @classmethod
    def get_surface(cls, bullet_type, color):
        key = (bullet_type, color)
        if key not in cls._surfaces:
            radius = 3 if bullet_type != "explosion" else 5
            size = radius * 2 + 2
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (radius + 1, radius + 1), radius)
            cls._surfaces[key] = surf.convert_alpha()
        return cls._surfaces[key]

    def __init__(self, pos, vel, bullet_type="normal", lifetime=None, color=None):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)
        self.type = bullet_type
        self.lifetime = lifetime
        self.color = color if color else (255, 255, 255) if bullet_type != "explosion" else (255, 165, 0)

    def update(self):
        self.pos += self.vel
        if self.lifetime is not None:
            self.lifetime -= 1

    def draw(self, screen, camera, shake_off):
        screen_pos = self.pos - camera + shake_off
        surf = self.get_surface(self.type, self.color)
        screen.blit(surf, (int(screen_pos.x - surf.get_width() // 2), int(screen_pos.y - surf.get_height() // 2)))

class Enemy:
    def __init__(self, pos, stage, scaling=1.0):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0, 0)
        self.scaling = scaling
        
        # Determine HP based on stage
        self.hp = 1
        if random.random() < STAGE_HP_CHANCE[stage]:
            self.hp = int(random.randint(2, STAGE_MAX_HP[stage]) * scaling)

    def update(self, player_pos, stage, all_enemies):
        current_enemy_speed = (ENEMY_SPEED + (stage - 1) * STAGE_SPEED_BOOST) * self.scaling
        desired_vel = (player_pos - self.pos).normalize() * current_enemy_speed

        # Add repulsion from nearby enemies to prevent clustering
        repulsion_force = pygame.Vector2(0, 0)
        for other in all_enemies:
            if other is not self:
                dist = self.pos.distance_to(other.pos)
                if dist < 50 and dist > 0:
                    repel_dir = (self.pos - other.pos).normalize()
                    strength = (50 - dist) / 50  # Stronger when closer
                    repulsion_force += repel_dir * strength * 0.5  # Adjust multiplier as needed

        desired_vel += repulsion_force

        self.vel += (desired_vel - self.vel) * 0.05
        self.pos += self.vel

    def draw(self, screen, camera, shake_off):
        screen_pos = self.pos - camera + shake_off
        border_width = 2 + (self.hp - 1) * 2
        pygame.draw.circle(screen, (255, 60, 60), screen_pos, 12, border_width)

class Boss(Enemy):
    def __init__(self, pos, stage, scaling=1.0):
        super().__init__(pos, stage, scaling)
        self.stage = stage
        self.phase = 1
        self.attack_timer = 0
        self.hp = (100 + (stage - 1) * 100) * scaling  # Base 100, +100 per stage
        self.max_hp = self.hp
        self.bullets = []  # Boss-specific bullets
        self.is_boss = True
        self.phase_timer = 0

    def update(self, player_pos, stage, all_enemies):
        self.attack_timer += 1
        self.phase_timer += 1
        
        # Scaling factors based on stage
        # rate_mult decreases attack intervals (makes them faster)
        rate_mult = max(0.3, 1.0 - (self.stage - 1) * 0.15)
        # bullet_speed_mult increases bullet speed as stage increases
        bullet_speed_mult = 1.0 + (self.stage - 1) * 0.2
        speed_boost = 2 + (self.stage - 1) * 0.5
        
        # Evolution: Change phase based on HP
        if self.hp < self.max_hp * 0.6:
            self.phase = 2
        if self.hp < self.max_hp * 0.3:
            self.phase = 3
        
        if self.stage == 1:  # Bullet Barrage Beginner
            if self.phase == 1:
                if self.attack_timer % int(60 * rate_mult) == 0:
                    for i in range(8):
                        angle = (i / 8) * 360
                        vel = pygame.Vector2(math.cos(math.radians(angle)), math.sin(math.radians(angle))) * 5 * bullet_speed_mult
                        self.bullets.append(Bullet(self.pos, vel, lifetime=300, color=(255, 50, 100)))
            else:
                # Phase 2/3: Spirals
                if self.attack_timer % int(5 * rate_mult) == 0:
                    angle = (self.attack_timer * 10) % 360
                    vel = pygame.Vector2(math.cos(math.radians(angle)), math.sin(math.radians(angle))) * 6 * bullet_speed_mult
                    self.bullets.append(Bullet(self.pos, vel, lifetime=300, color=(255, 50, 100)))
        elif self.stage == 2:  # Laser Sweeper
            if self.phase == 1:
                # Focus Pulse: Targeted tight-cone bursts that oscillate slightly
                if self.attack_timer % int(60 * rate_mult) == 0:
                    player_dir = (player_pos - self.pos).normalize()
                    base_angle = math.degrees(math.atan2(player_dir.y, player_dir.x))
                    oscillation = math.sin(self.attack_timer * 0.1) * 20
                    for i in range(7):
                        angle = base_angle + oscillation + (i - 3) * 5
                        vel = pygame.Vector2(math.cos(math.radians(angle)), math.sin(math.radians(angle))) * 6 * bullet_speed_mult
                        self.bullets.append(Bullet(self.pos, vel, lifetime=300, color=(255, 50, 100)))
            elif self.phase == 2:
                # Expanding Spiral: bullets in a spiral pattern
                if self.attack_timer % int(4 * rate_mult) == 0:
                    angle = (self.attack_timer * 15) % 360
                    vel = pygame.Vector2(math.cos(math.radians(angle)), math.sin(math.radians(angle))) * 5 * bullet_speed_mult
                    self.bullets.append(Bullet(self.pos, vel, lifetime=300, color=(255, 50, 100)))
            else:
                # Phase 3: Nova Bursts & Targeted Shots
                if self.attack_timer % int(120 * rate_mult) == 0:
                    for i in range(20):
                        angle = (i / 20) * 360
                        vel = pygame.Vector2(math.cos(math.radians(angle)), math.sin(math.radians(angle))) * 4 * bullet_speed_mult
                        self.bullets.append(Bullet(self.pos, vel, lifetime=300, color=(255, 50, 100)))
                if self.attack_timer % int(40 * rate_mult) == 0:
                    vel = (player_pos - self.pos).normalize() * 8 * bullet_speed_mult
                    self.bullets.append(Bullet(self.pos, vel, lifetime=300, color=(255, 50, 100)))
        elif self.stage == 3:  # Homing Horde
            if self.phase == 1:
                if self.attack_timer % int(90 * rate_mult) == 0:
                    for i in range(5):
                        vel = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * 4 * bullet_speed_mult
                        self.bullets.append(Bullet(self.pos, vel, lifetime=300, color=(255, 50, 100)))
            else:
                # Phase 2/3: Ring of bullets
                if self.attack_timer % int(150 * rate_mult) == 0:
                    for i in range(16):
                        angle = (i / 16) * 360
                        vel = pygame.Vector2(math.cos(math.radians(angle)), math.sin(math.radians(angle))) * 4 * bullet_speed_mult
                        self.bullets.append(Bullet(self.pos, vel, lifetime=300, color=(255, 50, 100)))
        elif self.stage == 4:  # Danmaku Dancer
            if self.phase == 1:
                if self.attack_timer % int(100 * rate_mult) == 0:
                    for i in range(12):
                        angle = (i / 12) * 360
                        vel = pygame.Vector2(math.cos(math.radians(angle)), math.sin(math.radians(angle))) * 5 * bullet_speed_mult
                        self.bullets.append(Bullet(self.pos, vel, lifetime=300, color=(255, 50, 100)))
            else:
                # Phase 2/3: Rapid targeted bursts
                if self.attack_timer % int(40 * rate_mult) == 0:
                    vel = (player_pos - self.pos).normalize() * 7 * bullet_speed_mult
                    self.bullets.append(Bullet(self.pos, vel, lifetime=300, color=(255, 50, 100)))
                # Occasionally fire explosion bullets
                if self.attack_timer % int(200 * rate_mult) == 0:
                    vel = (player_pos - self.pos).normalize() * 4 * bullet_speed_mult
                    self.bullets.append(Bullet(self.pos, vel, bullet_type="explosion", lifetime=300, color=(255, 100, 0)))
        elif self.stage == 5:  # Final Fusion
            # Mix of all based on timer
            if self.attack_timer % int(60 * rate_mult) == 0:
                for i in range(12):
                    angle = (self.attack_timer + (i / 12) * 360)
                    vel = pygame.Vector2(math.cos(math.radians(angle)), math.sin(math.radians(angle))) * 6 * bullet_speed_mult
                    self.bullets.append(Bullet(self.pos, vel, lifetime=300, color=(255, 50, 100)))
            if self.attack_timer % int(100 * rate_mult) == 0:
                vel = (player_pos - self.pos).normalize() * 8 * bullet_speed_mult
                self.bullets.append(Bullet(self.pos, vel, lifetime=300, color=(255, 50, 100)))
            # Frequent explosion bullets
            if self.attack_timer % int(150 * rate_mult) == 0:
                vel = (player_pos - self.pos).normalize() * 5 * bullet_speed_mult
                self.bullets.append(Bullet(self.pos, vel, bullet_type="explosion", lifetime=300, color=(255, 100, 0)))


        # Update boss bullets
        self.bullets = [b for b in self.bullets if b.lifetime is None or b.lifetime > 0]
        for b in self.bullets:
            b.update()
            if b.pos.distance_to(player_pos) > 2000:
                b.lifetime = 0

        # Basic movement toward player - Scaled speed
        desired_vel = (player_pos - self.pos).normalize() * speed_boost
        self.vel += (desired_vel - self.vel) * 0.05
        self.pos += self.vel

    def draw(self, screen, camera, shake_off):
        screen_pos = self.pos - camera + shake_off
        border_width = int(4 + (self.hp // 20))
        pygame.draw.circle(screen, (255, 0, 0), screen_pos, 20, border_width)  # Bigger, redder

        # Draw bullets
        for b in self.bullets:
            b.draw(screen, camera, shake_off)

class ExplosionEffect:
    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.lifetime = 30
        self.radius = 150
        # Pre-create a surface large enough for the max expansion
        self.surf = pygame.Surface((420, 420), pygame.SRCALPHA)

    def update(self):
        self.lifetime -= 1

    def draw(self, screen, camera, shake_off):
        if self.lifetime <= 0:
            return
        
        progress = 1 - (self.lifetime / 30)
        self.surf.fill((0, 0, 0, 0))
        
        exp_screen_pos = self.pos - camera + shake_off
        
        for i in range(3):
            radius = self.radius * (progress + i * 0.2)
            alpha = max(0, 200 - i * 60 - int(progress * 150))
            if alpha > 0:
                # Draw relative to the center of the 420x420 surface
                pygame.draw.circle(self.surf, (255, 100, 0, alpha), (210, 210), int(radius), 2 if i == 0 else 1)
        
        screen.blit(self.surf, (int(exp_screen_pos.x - 210), int(exp_screen_pos.y - 210)))
