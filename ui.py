import pygame
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
    title_surf = font.render("PEW PEW MANIA!", True, (255, 255, 255))
    prompt_surf = font.render("Press SPACE to Start", True, (200, 200, 200))
    screen.blit(title_surf, ((WIDTH - title_surf.get_width()) // 2, HEIGHT // 3))
    screen.blit(prompt_surf, ((WIDTH - prompt_surf.get_width()) // 2, HEIGHT // 2))

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

def draw_game_over(screen, font, current_animated_score):
    over_surf = font.render("GAME OVER", True, (255, 60, 60))
    score_surf = font.render(f"Final Score: {current_animated_score}", True, (255, 255, 255))
    retry_surf = font.render("Press SPACE to Retry", True, (200, 200, 200))
    screen.blit(over_surf, ((WIDTH - over_surf.get_width()) // 2, HEIGHT // 3))
    screen.blit(score_surf, ((WIDTH - score_surf.get_width()) // 2, HEIGHT // 2))
    screen.blit(retry_surf, ((WIDTH - retry_surf.get_width()) // 2, HEIGHT // 1.5))
