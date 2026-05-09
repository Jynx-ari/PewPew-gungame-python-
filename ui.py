import pygame
import math
from config import *

def draw_hud(screen, font, score, hp, energy, current_weapon, weapon_names, explosion_ammo, spread_ammo, game_timer, current_stage, shield_is_disabled, blink=False):
    sw, sh = screen.get_size()
    # Top Center Timer & Stage
    timer_text = f"TIME: {game_timer // 60:02}:{game_timer % 60:02} | STAGE: {current_stage}"
    color = COLOR_NEON_GREEN if not blink else COLOR_YELLOW # Neon Green blink
    timer_surf = font.render(timer_text, True, color)
    screen.blit(timer_surf, ((sw - timer_surf.get_width()) // 2, 20))
    
    # Shield Bar with Retro Border
    pygame.draw.rect(screen, COLOR_WHITE, HUD_SHIELD_RECT, 2) # White border
    pygame.draw.rect(screen, COLOR_DARK_BLUE, (HUD_SHIELD_RECT[0], HUD_SHIELD_RECT[1], HUD_SHIELD_RECT[2], HUD_SHIELD_RECT[3]))
    if not shield_is_disabled and energy > 10:
        energy_color = COLOR_CYAN # Cyan
    elif shield_is_disabled and energy < 40:
        energy_color = COLOR_BROWN
    elif energy > 10:
        energy_color = COLOR_CYAN
    elif energy > 0:
        energy_color = COLOR_ORANGE
    else:
        energy_color = COLOR_RED
    pygame.draw.rect(screen, energy_color, (HUD_SHIELD_RECT[0], HUD_SHIELD_RECT[1], max(0, int(energy * 1.5)), HUD_SHIELD_RECT[3]))
    
    # Score
    score_color = COLOR_NEON_GREEN # Neon Green
    if (score % 100 < 10) and (score >= 100):
        current_time = pygame.time.get_ticks()
        flash_interval = 300
        score_color = COLOR_YELLOW if ((current_time // flash_interval) % 2) == 0 else COLOR_ORANGE
    screen.blit(font.render(f"SCORE: {score}", True, score_color), (20, 85))
    
    # HP
    screen.blit(font.render(f"HP: {hp}", True, COLOR_LIGHT_RED), (20, 110))
    
    # Weapon
    weapon_text = f"WEAPON: {weapon_names[current_weapon]}"
    weapon_color = COLOR_MAGENTA # Magenta
    if score < EXPLOSION_POINT_MILESTONE:
        weapon_text += f" (EXPLOSION @ {EXPLOSION_POINT_MILESTONE})"
        weapon_color = COLOR_GREY
    elif score < SPREAD_POINT_MILESTONE:
        weapon_text += f" (SPREAD @ {SPREAD_POINT_MILESTONE})"
        weapon_color = (150, 200, 255)
    screen.blit(font.render(weapon_text, True, weapon_color), (20, 135))
    
    # Ammo
    ammo_text = f"EXPLOSION: {explosion_ammo} | SPREAD: {spread_ammo}"
    screen.blit(font.render(ammo_text, True, COLOR_NEON_GREEN), (20, 160))
    screen.blit(font.render("Press E to switch", True, COLOR_GREY), (20, 185))

def draw_menu(screen, font, current_index):
    sw, sh = screen.get_size()
    current_time = pygame.time.get_ticks()
    
    # Title with shadow
    title_text = "PEW PEW MANIA!"
    title_main = font.render(title_text, True, COLOR_CYAN) # Cyan
    title_shadow = font.render(title_text, True, (150, 0, 50))
    
    # Slight float effect
    off_y = math.sin(current_time * 0.002) * 10
    screen.blit(title_shadow, ((sw - title_main.get_width()) // 2 + 4, sh // 3 + 4 + off_y))
    screen.blit(title_main, ((sw - title_main.get_width()) // 2, sh // 3 + off_y))
    
    menu_options = ["PLAY", "SETTINGS", "CREDITS"]
    
    for i, option in enumerate(menu_options):
        selected = (i == current_index)
        color = COLOR_NEON_GREEN if selected else COLOR_GREY # Neon Green if selected
        
        # Selection effect
        offset_x = math.sin(current_time * 0.01) * 5 if selected else 0
        
        option_surf = font.render(option, True, color)
        screen.blit(option_surf, (sw // 2 - option_surf.get_width() // 2 + offset_x, sh // 2 + i * 60))

def draw_difficulty_menu(screen, font, current_index, is_hardcore=False):
    screen.fill(COLOR_DARK_PURPLE) # Darker background
    items = HARDCORE_TIERS if is_hardcore else DIFFICULTIES
    title = "SELECT INTENSITY" if not is_hardcore else "CHOOSE YOUR DEMISE"
    
    # Header
    head_surf = font.render(title, True, COLOR_CYAN) # Cyan
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
            pygame.draw.polygon(screen, COLOR_NEON_GREEN, bg_points) # Neon Green
            text_color = COLOR_BLACK # Contrast black
            # Selection shake
            x_base += math.sin(pygame.time.get_ticks() * 0.02) * 3
        else:
            text_color = COLOR_GREY
        
        item_surf = font.render(item, True, text_color)
        screen.blit(item_surf, (x_base, y_pos))
    
    back_prompt = font.render("ESC to go back", True, COLOR_DARK_GREY)
    screen.blit(back_prompt, (50, HEIGHT - 50))

def draw_credits(screen, font):
    sw, sh = screen.get_size()
    title_surf = font.render("CREDITS", True, COLOR_CYAN)
    screen.blit(title_surf, (sw // 2 - title_surf.get_width() // 2, sh // 4))
    
    credits_text = "Developed by an awesome team!"
    credits_surf = font.render(credits_text, True, COLOR_GREY)
    screen.blit(credits_surf, (sw // 2 - credits_surf.get_width() // 2, sh // 2))
    
    back_prompt = font.render("Press ESC to go back", True, COLOR_DARK_GREY)
    screen.blit(back_prompt, (sw // 2 - back_prompt.get_width() // 2, sh - 50))

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
    # Draw the menu box
    menu_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 200)
    pygame.draw.rect(screen, COLOR_DARK_BLUE, menu_rect)
    pygame.draw.rect(screen, COLOR_CYAN, menu_rect, 3) # Cyan border
    
    title_surf = font.render("PAUSED", True, COLOR_WHITE)
    screen.blit(title_surf, (menu_rect.centerx - title_surf.get_width() // 2, menu_rect.top + 20))
    
    for i, option in enumerate(options):
        color = COLOR_CYAN if i == current_index else COLOR_GREY
        option_surf = font.render(option, True, color)
        screen.blit(option_surf, (menu_rect.centerx - option_surf.get_width() // 2, menu_rect.top + 60 + i * 40))

def draw_game_over(screen, font, current_animated_score):
    current_time = pygame.time.get_ticks()
    
    # Dark vignette / overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    # Dynamic scaling for "GAME OVER"
    scale = 2.0 + math.sin(current_time * 0.005) * 0.1
    
    title_text = "GAME OVER"
    title_surf = font.render(title_text, True, COLOR_BRIGHT_RED)
    w, h = title_surf.get_size()
    scaled_surf = pygame.transform.smoothscale(title_surf, (int(w * scale), int(h * scale)))
    
    # Shadow/Glow effect
    glow_surf = font.render(title_text, True, COLOR_DARK_RED)
    gw, gh = glow_surf.get_size()
    scaled_glow = pygame.transform.smoothscale(glow_surf, (int(gw * scale), int(gh * scale)))
    
    screen.blit(scaled_glow, ((WIDTH - scaled_glow.get_width()) // 2 + 5, HEIGHT // 3 + 5))
    screen.blit(scaled_surf, ((WIDTH - scaled_surf.get_width()) // 2, HEIGHT // 3))
    
    # Score display with a simple line accent
    score_text = f"FINAL SCORE: {current_animated_score}"
    score_surf = font.render(score_text, True, COLOR_WHITE)
    
    # Accent line
    line_w = 200
    pygame.draw.line(screen, COLOR_BRIGHT_RED, (WIDTH // 2 - line_w // 2, HEIGHT // 2 + 10), (WIDTH // 2 + line_w // 2, HEIGHT // 2 + 10), 2)
    
    screen.blit(score_surf, ((WIDTH - score_surf.get_width()) // 2, HEIGHT // 2 - 30))

def draw_game_over_menu(screen, font, current_index, options):
    # Stylized Menu Box
    menu_rect = pygame.Rect(WIDTH // 2 - 180, HEIGHT // 2 + 50, 360, 200)
    
    # Background with slight gradient/color
    pygame.draw.rect(screen, COLOR_VERY_DARK_PURPLE, menu_rect, border_radius=10)
    pygame.draw.rect(screen, COLOR_BRIGHT_RED, menu_rect, 3, border_radius=10)
    
    for i, option in enumerate(options):
        selected = (i == current_index)
        color = COLOR_WHITE if selected else COLOR_GREY
        
        # Highlight bar for selected option
        if selected:
            bar_rect = pygame.Rect(menu_rect.x + 20, menu_rect.y + 40 + i * 50 - 10, menu_rect.width - 40, 30)
            pygame.draw.rect(screen, COLOR_DARK_RED, bar_rect, border_radius=5)
            
            # Subtle shake for selected text
            offset_x = math.sin(pygame.time.get_ticks() * 0.02) * 2
        else:
            offset_x = 0
            
        option_surf = font.render(option, True, color)
        screen.blit(option_surf, (menu_rect.centerx - option_surf.get_width() // 2 + offset_x, menu_rect.top + 40 + i * 50))

def draw_settings_menu(screen, font, settings, temp_settings, active_element):
    sw, sh = screen.get_size()
    
    # Settings Background with Margin
    margin = SETTINGS_MARGIN
    rect_width, rect_height = sw - (margin * 2), sh - (margin * 2)
    rect_x, rect_y = margin, margin
    
    pygame.draw.rect(screen, COLOR_SETTING_BG, (rect_x, rect_y, rect_width, rect_height))
    pygame.draw.rect(screen, COLOR_WHITE, (rect_x, rect_y, rect_width, rect_height), 2)
    
    # Header
    title_surf = font.render("settings", True, COLOR_CYAN)
    screen.blit(title_surf, (rect_x + 20, rect_y + 20))
    
    # Top Horizontal Line
    pygame.draw.line(screen, (255, 0, 255), (rect_x + 20, rect_y + 60), (rect_x + rect_width - 20, rect_y + 60), 2)
    
    # Vertical Separator Line
    sep_x = rect_x + 200
    pygame.draw.line(screen, (255, 0, 255), (sep_x, rect_y + 60), (sep_x, rect_y + rect_height - 20), 1)
    
    # Mouse Sensitivity Row
    row_y = rect_y + 100
    label_sens = font.render("mouse sensitivity", True, COLOR_GREY)
    screen.blit(label_sens, (rect_x + 20, row_y))
    
    slider_x_start, slider_x_end = sep_x + 40, rect_x + rect_width - 100
    slider_width = slider_x_end - slider_x_start
    pygame.draw.line(screen, COLOR_DARK_GREY, (slider_x_start, row_y + 10), (slider_x_end, row_y + 10), 2)
    
    # Handle position
    handle_x = slider_x_start + (temp_settings['mouse_sens'] - 0.1) / (5.0 - 0.1) * slider_width
    handle_color = COLOR_NEON_GREEN if active_element == "mouse_sens" else COLOR_WHITE
    pygame.draw.circle(screen, handle_color, (int(handle_x), row_y + 10), 6)
    
    # Sensitivity Value
    val_surf = font.render(f"{temp_settings['mouse_sens']:.1f}", True, COLOR_WHITE)
    screen.blit(val_surf, (slider_x_end + 10, row_y))
    
    # Enable CRT Row
    cb_y = row_y + 80
    label_crt = font.render("Enable CRT", True, COLOR_GREY)
    screen.blit(label_crt, (rect_x + 20, cb_y))
    
    cb_rect = pygame.Rect(sep_x + 40, cb_y + 5, 20, 20)
    pygame.draw.rect(screen, COLOR_WHITE, cb_rect, 2)
    if temp_settings['shaders_enabled']:
        pygame.draw.rect(screen, COLOR_NEON_GREEN, cb_rect.inflate(-6, -6))
    
    note_surf = font.render("*Note: Must have OpenGL support GPU", True, (150, 150, 150))
    screen.blit(note_surf, (cb_rect.right + 20, cb_y + 5))
    
    back_prompt = font.render("Press ESC to go back", True, COLOR_DARK_GREY)
    screen.blit(back_prompt, (sw // 2 - back_prompt.get_width() // 2, sh - 50))

def draw_confirmation_popup(screen, font, confirm_index):
    sw, sh = screen.get_size()
    
    # Darken background
    overlay = pygame.Surface((sw, sh), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    # Popup box
    box_w, box_h = 400, 200
    box_x, box_y = (sw - box_w) // 2, (sh - box_h) // 2
    pygame.draw.rect(screen, COLOR_DARK_BLUE, (box_x, box_y, box_w, box_h))
    pygame.draw.rect(screen, COLOR_BRIGHT_RED, (box_x, box_y, box_w, box_h), 3)
    
    msg = "UNSAVED CHANGES DETECTED!"
    msg_surf = font.render(msg, True, COLOR_WHITE)
    screen.blit(msg_surf, (sw // 2 - msg_surf.get_width() // 2, box_y + 40))
    
    options = ["APPLY CHANGES", "DISCARD"]
    for i, opt in enumerate(options):
        color = COLOR_NEON_GREEN if i == confirm_index else COLOR_GREY
        opt_surf = font.render(opt, True, color)
        screen.blit(opt_surf, (sw // 2 - opt_surf.get_width() // 2, box_y + 100 + i * 50))
