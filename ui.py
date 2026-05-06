import pygame
import math
from config import *

def draw_hud(screen, font, score, hp, energy, current_weapon, weapon_names, explosion_ammo, spread_ammo, game_timer, current_stage, shield_is_disabled, blink=False):
    # Top Center Timer & Stage
    timer_text = f"TIME: {game_timer // 60:02}:{game_timer % 60:02} | STAGE: {current_stage}"
    color = (255, 255, 255) if not blink else (255, 255, 0) # Yellow blink
    timer_surf = font.render(timer_text, True, color)
    screen.blit(timer_surf, ((WIDTH - timer_surf.get_width()) // 2, 20))

    # Shield Bar
    pygame.draw.rect(screen, (40, 40, 60), (20, 60, 150, 15))
    if not shield_is_disabled and energy > 10:
        energy_color = (255, 180, 0)
    elif shield_is_disabled and energy < 40:
        energy_color = (150, 100, 0)
    elif energy > 10:
        energy_color = (255, 180, 0)
    elif energy > 0:
        energy_color = (255, 100, 0)
    else:
        energy_color = (255, 0, 0)
    pygame.draw.rect(screen, energy_color, (20, 60, max(0, int(energy * 1.5)), 15))

    # Score
    score_color = (255, 255, 255)
    if (score % 100 < 10) and (score >= 100):
        current_time = pygame.time.get_ticks()
        flash_interval = 300
        score_color = (255, 215, 0) if ((current_time // flash_interval) % 2) == 0 else (255, 100, 0)
    screen.blit(font.render(f"SCORE: {score}", True, score_color), (20, 85))

    # HP
    screen.blit(font.render(f"HP: {hp}", True, (255, 100, 100)), (20, 110))

    # Weapon
    weapon_text = f"WEAPON: {weapon_names[current_weapon]}"
    weapon_color = (100, 200, 255)
    if score < 200:
        weapon_text += " (EXPLOSION @ 200)"
        weapon_color = (150, 150, 150)
    elif score < 400:
        weapon_text += " (SPREAD @ 400)"
        weapon_color = (150, 200, 255)
    screen.blit(font.render(weapon_text, True, weapon_color), (20, 135))

    # Ammo
    ammo_text = f"EXPLOSION: {explosion_ammo} | SPREAD: {spread_ammo}"
    screen.blit(font.render(ammo_text, True, (200, 200, 200)), (20, 160))
    screen.blit(font.render("Press E to switch", True, (150, 150, 150)), (20, 185))

def draw_menu(screen, font):
    current_time = pygame.time.get_ticks()
    
    # Title with shadow
    title_text = "PEW PEW MANIA!"
    title_main = font.render(title_text, True, (255, 255, 255))
    title_shadow = font.render(title_text, True, (150, 0, 50))
    
    # Slight float effect
    off_y = math.sin(current_time * 0.002) * 10
    screen.blit(title_shadow, ((WIDTH - title_main.get_width()) // 2 + 4, HEIGHT // 3 + 4 + off_y))
    screen.blit(title_main, ((WIDTH - title_main.get_width()) // 2, HEIGHT // 3 + off_y))
    
    # Pulsing prompt
    alpha = (math.sin(current_time * 0.005) + 1) / 2
    p_color = (150 + 105 * alpha, 10 * alpha, 50 * alpha)
    prompt_surf = font.render("PRESS SPACE TO INFILTRATE", True, p_color)
    screen.blit(prompt_surf, ((WIDTH - prompt_surf.get_width()) // 2, HEIGHT // 2 + 50))

def draw_difficulty_menu(screen, font, current_index, is_hardcore=False):
    screen.fill((10, 5, 15)) # Darker background
    items = HARDCORE_TIERS if is_hardcore else DIFFICULTIES
    title = "SELECT INTENSITY" if not is_hardcore else "CHOOSE YOUR DEMISE"
    
    # Header
    head_surf = font.render(title, True, (255, 0, 60))
    screen.blit(head_surf, (50, 50))
    
    for i, item in enumerate(items):
        selected = (i == current_index)
        x_base = 100 + (i * 20) # Slanted layout
        y_pos = 200 + (i * 60)
        
        if selected:
            # Slanted Background bar for selection
            bg_points = [
                (x_base - 40, y_pos - 10),
                (x_base + 400, y_pos - 25),
                (x_base + 420, y_pos + 40),
                (x_base - 20, y_pos + 50)
            ]
            pygame.draw.polygon(screen, (255, 0, 60), bg_points)
            text_color = (255, 255, 255)
            # Selection shake
            x_base += math.sin(pygame.time.get_ticks() * 0.02) * 3
        else:
            text_color = (150, 150, 150)
        
        item_surf = font.render(item, True, text_color)
        screen.blit(item_surf, (x_base, y_pos))

    back_prompt = font.render("ESC to go back", True, (100, 100, 100))
    screen.blit(back_prompt, (50, HEIGHT - 50))

def draw_tutorial(screen, font):
    tut_lines = [
        "CONTROLS:",
        "WASD - Move",
        "Mouse - Aim & Shoot",
        "Right Click - Shield",
        "E - Switch Weapon",
        "",
        "Explosion: Slow fire, huge blast",
        "Spread: Faster fire, multiple shots",
        "",
        "Press SPACE to begin!"
    ]
    for i, line in enumerate(tut_lines):
        line_surf = font.render(line, True, (200, 200, 200))
        screen.blit(line_surf, ((WIDTH - line_surf.get_width()) // 2, HEIGHT // 3 + i * 30))

def draw_blur(screen):
    # Scale down and back up for a cheap blur effect
    width, height = screen.get_size()
    small_size = (width // 4, height // 4)
    temp_surf = pygame.transform.smoothscale(screen, small_size)
    blurred_surf = pygame.transform.smoothscale(temp_surf, (width, height))
    screen.blit(blurred_surf, (0, 0))

def draw_pause_menu(screen, font, current_index, options):
    # Dim the background - REMOVED as requested
    # overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    # overlay.fill((0, 0, 0, 150))
    # screen.blit(overlay, (0, 0))

    # Draw the menu box
    menu_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 200)
    pygame.draw.rect(screen, (30, 30, 50), menu_rect)
    pygame.draw.rect(screen, (255, 0, 60), menu_rect, 3) # Red border

    title_surf = font.render("PAUSED", True, (255, 255, 255))
    screen.blit(title_surf, (menu_rect.centerx - title_surf.get_width() // 2, menu_rect.top + 20))

    for i, option in enumerate(options):
        color = (255, 0, 60) if i == current_index else (200, 200, 200)
        option_surf = font.render(option, True, color)
        screen.blit(option_surf, (menu_rect.centerx - option_surf.get_width() // 2, menu_rect.top + 60 + i * 40))

def draw_game_over(screen, font, current_animated_score):
    current_time = pygame.time.get_ticks()
    
    # Dark vignette / overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    # Dynamic scaling for "GAME OVER"
    scale = 1.0 + math.sin(current_time * 0.005) * 0.05
    
    title_text = "GAME OVER"
    # Use a larger font for the title if possible, otherwise just scale the surface
    title_surf = font.render(title_text, True, (255, 0, 60))
    w, h = title_surf.get_size()
    scaled_surf = pygame.transform.smoothscale(title_surf, (int(w * scale), int(h * scale)))
    
    # Shadow/Glow effect
    glow_surf = font.render(title_text, True, (100, 0, 20))
    gw, gh = glow_surf.get_size()
    scaled_glow = pygame.transform.smoothscale(glow_surf, (int(gw * scale), int(gh * scale)))

    screen.blit(scaled_glow, ((WIDTH - scaled_glow.get_width()) // 2 + 5, HEIGHT // 3 + 5))
    screen.blit(scaled_surf, ((WIDTH - scaled_surf.get_width()) // 2, HEIGHT // 3))

    # Score display with a simple line accent
    score_text = f"FINAL SCORE: {current_animated_score}"
    score_surf = font.render(score_text, True, (255, 255, 255))
    
    # Accent line
    line_w = 200
    pygame.draw.line(screen, (255, 0, 60), (WIDTH // 2 - line_w // 2, HEIGHT // 2 + 10), (WIDTH // 2 + line_w // 2, HEIGHT // 2 + 10), 2)
    
    screen.blit(score_surf, ((WIDTH - score_surf.get_width()) // 2, HEIGHT // 2 - 30))

def draw_game_over_menu(screen, font, current_index, options):
    # Stylized Menu Box
    menu_rect = pygame.Rect(WIDTH // 2 - 180, HEIGHT // 2 + 50, 360, 200)
    
    # Background with slight gradient/color
    pygame.draw.rect(screen, (20, 10, 30), menu_rect, border_radius=10)
    pygame.draw.rect(screen, (255, 0, 60), menu_rect, 3, border_radius=10)
    
    for i, option in enumerate(options):
        selected = (i == current_index)
        color = (255, 255, 255) if selected else (150, 150, 150)
        
        # Highlight bar for selected option
        if selected:
            bar_rect = pygame.Rect(menu_rect.x + 20, menu_rect.y + 40 + i * 50 - 10, menu_rect.width - 40, 30)
            pygame.draw.rect(screen, (60, 0, 20), bar_rect, border_radius=5)
            
            # Subtle shake for selected text
            offset_x = math.sin(pygame.time.get_ticks() * 0.02) * 2
        else:
            offset_x = 0
            
        option_surf = font.render(option, True, color)
        screen.blit(option_surf, (menu_rect.centerx - option_surf.get_width() // 2 + offset_x, menu_rect.top + 40 + i * 50))


    for i, option in enumerate(options):
        color = (255, 0, 60) if i == current_index else (200, 200, 200)
        option_surf = font.render(option, True, color)
        screen.blit(option_surf, (menu_rect.centerx - option_surf.get_width() // 2, menu_rect.top + 40 + i * 40))
