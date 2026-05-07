import pygame
import math
import random
import os
from config import *
from entities import Bullet, Enemy, ExplosionEffect
from ui import draw_hud, draw_menu, draw_tutorial, draw_game_over

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    pygame.init()
    pygame.mixer.init()
    
    # Create window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    pygame.display.set_caption("PEW PEW MANIA!")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Consolas", 22, bold=True)
    fullscreen = False

    # Load Sounds
    def load_sound(file):
        if os.path.exists(file):
            return pygame.mixer.Sound(file)
        return None

    pew_sound = load_sound(SOUND_FIRE)
    score_sound = load_sound(SOUND_SCORE)
    explosion_sound = load_sound(SOUND_EXPLOSION)
    bounce_sound = load_sound(SOUND_BOUNCE)
    damage_sound = load_sound(SOUND_DAMAGE)
    checkpoint_sound = load_sound(SOUND_CHECKPOINT)
    sam_sound = load_sound(SOUND_SAM)
    if sam_sound:
        sam_sound.set_volume(SAM_VOLUME) 
    point_count_sound = load_sound(SOUND_POINT_COUNT)
    pause_sound = load_sound(SOUND_PAUSE)
    p_press_sound = load_sound(SOUND_P_PRESS)
    bang_sound = load_sound(SOUND_BANG)
    
    # SAM Voice-overs

    sam_s1 = load_sound(SOUND_SAM_S1)
    sam_s2 = load_sound(SOUND_SAM_S2)
    sam_s3 = load_sound(SOUND_SAM_S3)
    sam_s4 = load_sound(SOUND_SAM_S4)
    sam_s5_1 = load_sound(SOUND_SAM_S5_PART1)
    sam_s5_2 = load_sound(SOUND_SAM_S5_PART2)
    sam_win = load_sound(SOUND_SAM_WIN)
    
    # Set low volume for all SAM voices
    for s in [sam_s1, sam_s2, sam_s3, sam_s4, sam_s5_1, sam_s5_2, sam_win]:
        if s: s.set_volume(SAM_VOLUME)
    
    # Music initialization
    pygame.mixer.music.load(MUSIC_MAIN_MENU)
    pygame.mixer.music.set_volume(MENU_VOLUME)
    pygame.mixer.music.play(-1)

    # Game State Variables
    pos = pygame.Vector2(0, 0)
    vel = pygame.Vector2(0, 0)
    camera = pygame.Vector2(0, 0)
    bullets, enemies = [], []
    stars = [pygame.Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(150)]
    score, energy, shake, cooldown = 0, 100, 0, 0
    explosion_effects = []
    current_weapon = 0 
    weapon_names = ["NORMAL", "EXPLOSION", "SPREAD"]
    weapon_switch_cooldown = 0
    hp = LIVES
    invincibility_start_time = 0
    invincibility_duration = 2500 
    last_score_milestone = 0
    last_explosion_ammo_milestone = 0
    last_spread_ammo_milestone = 0
    explosion_start_granted = False
    spread_start_granted = False
    shield_is_disabled = False
    explosion_effects = []
    current_stage = 1
    game_start_time = 0
    game_timer = 0
    current_state = STATE_MENU
    sam_s1_played = False
    sam_s5_part2_pending = False
    sam_s5_timer = 0
    pause_menu_index = 0
    pause_menu_options = ["QUIT", "MENU", "RETRY"]
    game_over_menu_index = 0
    game_over_menu_options = ["RETRY", "MENU", "QUIT"]
    background_surface = None
    death_sequence_start_time = 0
    game_over_fade_start_time = 0
    static_surface = pygame.Surface((WIDTH, HEIGHT))
    static_overlay = pygame.Surface((WIDTH, HEIGHT))
    static_overlay.set_alpha(150)
    static_overlay.fill((0, 0, 0))

    
    # Animation and FX variables
    animated_score = 0
    score_animation_speed = 2
    stage_blink_timer = 0
    music_playing = "MENU"

    try:
        while True:
            screen.fill((5, 5, 12))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    # Debug: print key press
                    # print(f"Key pressed: {event.key} | State: {current_state}")
                    if event.key == pygame.K_F11:
                        fullscreen = not fullscreen
                        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN if fullscreen else 0)
                    
                    if current_state == STATE_MENU:
                        if event.key == pygame.K_SPACE:
                            current_state = STATE_DIFFICULTY
                            menu_index = 0
                    
                    elif current_state == STATE_DIFFICULTY:
                        if event.key == pygame.K_w or event.key == pygame.K_UP:
                            menu_index = (menu_index - 1) % len(DIFFICULTIES)
                        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                            menu_index = (menu_index + 1) % len(DIFFICULTIES)
                        elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                            if DIFFICULTIES[menu_index] == "HARDCORE":
                                current_state = STATE_HARDCORE_SELECT
                                hardcore_index = 0
                            else:
                                selected_difficulty = DIFFICULTIES[menu_index]
                                current_state = STATE_TUTORIAL
                        elif event.key == pygame.K_ESCAPE:
                            if point_count_sound: point_count_sound.stop()
                            pygame.mixer.music.stop()
                            music_playing = "STOPPED"
                            current_state = STATE_MENU
                    
                    elif current_state == STATE_HARDCORE_SELECT:
                        if event.key == pygame.K_w or event.key == pygame.K_UP:
                            hardcore_index = (hardcore_index - 1) % len(HARDCORE_TIERS)
                        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                            hardcore_index = (hardcore_index + 1) % len(HARDCORE_TIERS)
                        elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                            selected_difficulty = HARDCORE_TIERS[hardcore_index]
                            current_state = STATE_TUTORIAL
                        elif event.key == pygame.K_ESCAPE:
                            current_state = STATE_DIFFICULTY
                    
                    elif current_state == STATE_TUTORIAL:
                        if event.key == pygame.K_SPACE:
                            pos = pygame.Vector2(0, 0)
                            vel = pygame.Vector2(0, 0)
                            enemies.clear()
                            bullets.clear()
                            score, energy, hp = 0, 100, LIVES
                            explosion_ammo, spread_ammo = 0, 0
                            invincibility_start_time = 0
                            last_score_milestone = 0
                            last_explosion_ammo_milestone = 0
                            last_spread_ammo_milestone = 0
                            explosion_start_granted = False
                            spread_start_granted = False
                            shield_is_disabled = False
                            explosion_effects.clear()
                            current_weapon = 0
                            current_stage = 1
                            game_start_time = pygame.time.get_ticks()
                            game_timer = 0
                            current_state = STATE_PLAYING
                            sam_s1_played = False
                            sam_s5_part2_pending = False
                            sam_s5_timer = 0
                            if point_count_sound: point_count_sound.stop()
                    
                    elif current_state == STATE_PLAYING:
                        if event.key == pygame.K_p:
                            current_state = STATE_PAUSED
                            pause_menu_index = 0
                            if pause_sound: pause_sound.play()
                            if p_press_sound: p_press_sound.play()
                    
                    elif current_state == STATE_PAUSED:
                        if event.key == pygame.K_p:
                            current_state = STATE_PLAYING
                        elif event.key == pygame.K_ESCAPE:
                            current_state = STATE_PLAYING
                        elif event.key == pygame.K_w or event.key == pygame.K_UP:
                            pause_menu_index = (pause_menu_index - 1) % len(pause_menu_options)
                        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                            pause_menu_index = (pause_menu_index + 1) % len(pause_menu_options)
                        elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                            if pause_menu_options[pause_menu_index] == "QUIT":
                                pygame.quit()
                                return
                            elif pause_menu_options[pause_menu_index] == "MENU":
                                if point_count_sound: point_count_sound.stop()
                                pygame.mixer.music.stop()
                                music_playing = "STOPPED"
                                current_state = STATE_MENU
                            elif pause_menu_options[pause_menu_index] == "RETRY":
                                pos = pygame.Vector2(0, 0)
                                vel = pygame.Vector2(0, 0)
                                enemies.clear()
                                bullets.clear()
                                score, energy, hp = 0, 100, LIVES
                                explosion_ammo, spread_ammo = 0, 0
                                invincibility_start_time = 0
                                last_score_milestone = 0
                                last_explosion_ammo_milestone = 0
                                last_spread_ammo_milestone = 0
                                explosion_start_granted = False
                                spread_start_granted = False
                                shield_is_disabled = False
                                explosion_effects.clear()
                                current_weapon = 0
                                current_stage = 1
                                game_start_time = pygame.time.get_ticks()
                                game_timer = 0
                                current_state = STATE_PLAYING
                                sam_s1_played = False
                                sam_s5_part2_pending = False
                                sam_s5_timer = 0
                                if point_count_sound: point_count_sound.stop()
                    
                    elif current_state == STATE_GAMEOVER:
                        if event.key == pygame.K_w or event.key == pygame.K_UP:
                            game_over_menu_index = (game_over_menu_index - 1) % len(game_over_menu_options)
                        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                            game_over_menu_index = (game_over_menu_index + 1) % len(game_over_menu_options)
                        elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                            if game_over_menu_options[game_over_menu_index] == "RETRY":
                                pos = pygame.Vector2(0, 0)
                                vel = pygame.Vector2(0, 0)
                                enemies.clear()
                                bullets.clear()
                                score, energy, hp = 0, 100, LIVES
                                explosion_ammo, spread_ammo = 0, 0
                                invincibility_start_time = 0
                                last_score_milestone = 0
                                last_explosion_ammo_milestone = 0
                                last_spread_ammo_milestone = 0
                                explosion_start_granted = False
                                spread_start_granted = False
                                shield_is_disabled = False
                                explosion_effects.clear()
                                current_weapon = 0
                                current_stage = 1
                                game_start_time = pygame.time.get_ticks()
                                game_timer = 0
                                current_state = STATE_PLAYING
                                sam_s1_played = False
                                sam_s5_part2_pending = False
                                sam_s5_timer = 0
                                if point_count_sound: point_count_sound.stop()
                            elif game_over_menu_options[game_over_menu_index] == "MENU":
                                if point_count_sound: point_count_sound.stop()
                                pygame.mixer.music.stop()
                                music_playing = "STOPPED"
                                current_state = STATE_MENU
                            
                            elif game_over_menu_options[game_over_menu_index] == "QUIT":
                                pygame.quit()
                                return
                        elif event.key == pygame.K_ESCAPE:
                            if point_count_sound: point_count_sound.stop()
                            pygame.mixer.music.stop()
                            music_playing = "STOPPED"
                            current_state = STATE_MENU

                    elif current_state == STATE_HARDCORE_SELECT:
                        if event.key == pygame.K_w or event.key == pygame.K_UP:
                            hardcore_index = (hardcore_index - 1) % len(HARDCORE_TIERS)
                        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                            hardcore_index = (hardcore_index + 1) % len(HARDCORE_TIERS)
                        elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                            selected_difficulty = HARDCORE_TIERS[hardcore_index]
                            current_state = STATE_TUTORIAL
                        elif event.key == pygame.K_ESCAPE:
                            current_state = STATE_DIFFICULTY

                    elif current_state == STATE_TUTORIAL:
                        if event.key == pygame.K_SPACE:
                            pos = pygame.Vector2(0, 0)
                            vel = pygame.Vector2(0, 0)
                            enemies.clear()
                            bullets.clear()
                            score, energy, hp = 0, 100, LIVES
                            explosion_ammo, spread_ammo = 0, 0
                            invincibility_start_time = 0
                            last_score_milestone = 0
                            last_explosion_ammo_milestone = 0
                            last_spread_ammo_milestone = 0
                            explosion_start_granted = False
                            spread_start_granted = False
                            shield_is_disabled = False
                            explosion_effects.clear()
                            current_weapon = 0
                            current_stage = 1
                            game_start_time = pygame.time.get_ticks()
                            game_timer = 0
                            current_state = STATE_PLAYING
                            sam_s1_played = False
                            sam_s5_part2_pending = False
                            sam_s5_timer = 0
                            if point_count_sound: point_count_sound.stop()



                    elif current_state == STATE_PLAYING:
                        if event.key == pygame.K_p:
                            current_state = STATE_PAUSED
                            pause_menu_index = 0
                            if pause_sound: pause_sound.play()
                            if p_press_sound: p_press_sound.play()

                    elif current_state == STATE_PAUSED:
                        if event.key == pygame.K_p:
                            current_state = STATE_PLAYING
                        elif event.key == pygame.K_ESCAPE:
                            current_state = STATE_PLAYING
                        elif event.key == pygame.K_w or event.key == pygame.K_UP:
                            pause_menu_index = (pause_menu_index - 1) % len(pause_menu_options)
                        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                            pause_menu_index = (pause_menu_index + 1) % len(pause_menu_options)
                        elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                            if pause_menu_options[pause_menu_index] == "QUIT":
                                pygame.quit()
                                return
                            elif pause_menu_options[pause_menu_index] == "MENU":
                                if point_count_sound: point_count_sound.stop()
                                pygame.mixer.music.stop()
                                music_playing = "STOPPED"
                                current_state = STATE_MENU
                            elif pause_menu_options[pause_menu_index] == "RETRY":
                                pos = pygame.Vector2(0, 0)
                                vel = pygame.Vector2(0, 0)
                                enemies.clear()
                                bullets.clear()
                                score, energy, hp = 0, 100, LIVES
                                explosion_ammo, spread_ammo = 0, 0
                                invincibility_start_time = 0
                                last_score_milestone = 0
                                last_explosion_ammo_milestone = 0
                                last_spread_ammo_milestone = 0
                                explosion_start_granted = False
                                spread_start_granted = False
                                shield_is_disabled = False
                                explosion_effects.clear()
                                current_weapon = 0
                                current_stage = 1
                                game_start_time = pygame.time.get_ticks()
                                game_timer = 0
                                current_state = STATE_PLAYING
                                sam_s1_played = False
                                sam_s5_part2_pending = False
                                sam_s5_timer = 0
                                if point_count_sound: point_count_sound.stop()


                    elif current_state == STATE_GAMEOVER:
                        if event.key == pygame.K_w or event.key == pygame.K_UP:
                            game_over_menu_index = (game_over_menu_index - 1) % len(game_over_menu_options)
                        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                            game_over_menu_index = (game_over_menu_index + 1) % len(game_over_menu_options)
                        elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                            if game_over_menu_options[game_over_menu_index] == "RETRY":
                                pos = pygame.Vector2(0, 0)
                                vel = pygame.Vector2(0, 0)
                                enemies.clear()
                                bullets.clear()
                                score, energy, hp = 0, 100, LIVES
                                explosion_ammo, spread_ammo = 0, 0
                                invincibility_start_time = 0
                                last_score_milestone = 0
                                last_explosion_ammo_milestone = 0
                                last_spread_ammo_milestone = 0
                                explosion_start_granted = False
                                spread_start_granted = False
                                shield_is_disabled = False
                                explosion_effects.clear()
                                current_weapon = 0
                                current_stage = 1
                                game_start_time = pygame.time.get_ticks()
                                game_timer = 0
                                current_state = STATE_PLAYING
                                sam_s1_played = False
                                sam_s5_part2_pending = False
                                sam_s5_timer = 0
                                if point_count_sound: point_count_sound.stop()
                            elif game_over_menu_options[game_over_menu_index] == "MENU":
                                if point_count_sound: point_count_sound.stop()
                                pygame.mixer.music.stop()
                                music_playing = "STOPPED"
                                current_state = STATE_MENU

                            elif game_over_menu_options[game_over_menu_index] == "QUIT":
                                pygame.quit()
                                return
                        elif event.key == pygame.K_ESCAPE:
                            if point_count_sound: point_count_sound.stop()
                            pygame.mixer.music.stop()
                            music_playing = "STOPPED"
                            current_state = STATE_MENU






            if current_state == STATE_PLAYING:
                scaling_factor = DIFFICULTY_SCALING.get(selected_difficulty, 1.0)
                # Music management
                if music_playing != "BG":
                    pygame.mixer.music.load(MUSIC_BG)
                    pygame.mixer.music.play(-1)
                    music_playing = "BG"

                # Timer and Stage logic (Countdown)
                current_time_ms = pygame.time.get_ticks()
                if game_start_time == 0:
                    game_start_time = current_time_ms
                
                elapsed_time = (current_time_ms - game_start_time) // 1000
                current_stage = (elapsed_time // STAGE_DURATION) + 1
                
                # Time remaining in current stage
                game_timer = STAGE_DURATION - (elapsed_time % STAGE_DURATION)
                if current_stage > MAX_STAGE:
                    game_timer = 0
                
                # Victory Condition: After completing Stage 5
                if current_stage > MAX_STAGE:
                    if sam_win: sam_win.play()
                    current_state = STATE_GAMEOVER
                    game_over_fade_start_time = pygame.time.get_ticks()
                    animated_score = 0
                    if point_count_sound and score > 0: point_count_sound.play(-1)
                    score_animation_speed = max(2, score // 150) if score > 500 else 2

                
                # Handle stage transition
                if 'prev_stage' not in locals():
                    prev_stage = 0 # Start at 0 to trigger S1 voice on start
                
                if current_stage > prev_stage:
                    checkpoint_sound.play() if checkpoint_sound else None
                    stage_blink_timer = 60 
                    shake = 30
                    
                    # SAM Voice announcements (S2-S5)
                    if current_stage == 2 and sam_s2: sam_s2.play()
                    elif current_stage == 3 and sam_s3: sam_s3.play()
                    elif current_stage == 4 and sam_s4: sam_s4.play()
                    elif current_stage == 5:
                        if sam_s5_1: sam_s5_1.play()
                        sam_s5_part2_pending = True
                        sam_s5_timer = pygame.time.get_ticks()

                prev_stage = current_stage

                # Special delay for Stage 1 SAM voice
                if current_stage == 1 and not sam_s1_played and elapsed_time >= 1.5:
                    if sam_s1: sam_s1.play()
                    sam_s1_played = True
                
                if sam_s5_part2_pending and pygame.time.get_ticks() - sam_s5_timer >= 1500:
                    if sam_s5_2: sam_s5_2.play()
                    sam_s5_part2_pending = False

                if stage_blink_timer > 0:
                    stage_blink_timer -= 1

                # Camera
                shake_off = pygame.Vector2(random.uniform(-shake, shake), random.uniform(-shake, shake))
                if shake > 0: shake *= 0.9
                camera.x += (pos.x - camera.x - WIDTH // 2) * CAM_SMOOTHING
                camera.y += (pos.y - camera.y - HEIGHT // 2) * CAM_SMOOTHING

                for s in stars:
                    sx, sy = (s.x - camera.x) % WIDTH, (s.y - camera.y) % HEIGHT
                    pygame.draw.circle(screen, (80, 80, 100), (int(sx), int(sy)), 1)

                mouse_btns = pygame.mouse.get_pressed()
                is_shielding = mouse_btns[2] and energy > 10 and not shield_is_disabled
                is_shooting = mouse_btns[0] and not is_shielding

                keys = pygame.key.get_pressed()
                if keys[pygame.K_e] and weapon_switch_cooldown <= 0:
                    available = [0]
                    if score >= 400: available.append(2)
                    if score >= 200: available.append(1)
                    cur_idx = available.index(current_weapon) if current_weapon in available else 0
                    current_weapon = available[(cur_idx + 1) % len(available)]
                    weapon_switch_cooldown = 15

                accel = pygame.Vector2(0, 0)
                if keys[pygame.K_w]: accel.y -= 1
                if keys[pygame.K_s]: accel.y += 1
                if keys[pygame.K_a]: accel.x -= 1
                if keys[pygame.K_d]: accel.x += 1

                if accel.length() > 0:
                    cur_speed = SPEED_NORMAL * 0.4 if is_shielding else SPEED_NORMAL
                    vel += accel.normalize() * cur_speed
                vel *= FRICTION
                pos += vel

                mx, my = pygame.mouse.get_pos()
                world_mx, world_my = mx + camera.x, my + camera.y
                angle = math.degrees(math.atan2(world_my - pos.y, world_mx - pos.x))

                if is_shooting and cooldown <= 0:
                    dir_vec = (pygame.Vector2(world_mx, world_my) - pos).normalize()
                    if current_weapon == 0:
                        if pew_sound: pew_sound.play()
                        bullets.append(Bullet(pos, dir_vec * BULLET_SPEED))
                        vel -= dir_vec * RECOIL
                        cooldown, shake = FIRE_RATE_NORMAL, SHAKE_POWER / 2
                    elif current_weapon == 1 and explosion_ammo > 0:
                        if pew_sound: pew_sound.play()
                        bullets.append(Bullet(pos, dir_vec * 10, "explosion", 72))
                        vel -= dir_vec * (RECOIL * 1.5)
                        explosion_ammo -= 1
                        cooldown, shake = FIRE_RATE_EXPLOSION, SHAKE_POWER
                    elif current_weapon == 2 and spread_ammo > 0:
                        if pew_sound: pew_sound.play()
                        for i in range(SPREAD_BULLET_COUNT):
                            spread_angle = (i - (SPREAD_BULLET_COUNT - 1) / 2) * 12
                            spread_vec = dir_vec.rotate(spread_angle)
                            bullets.append(Bullet(pos, spread_vec * BULLET_SPEED * 0.8))
                        vel -= dir_vec * RECOIL
                        spread_ammo -= 1
                        cooldown, shake = FIRE_RATE_SPREAD, SHAKE_POWER / 2

                if cooldown > 0: cooldown -= 1
                if weapon_switch_cooldown > 0: weapon_switch_cooldown -= 1

                if is_shielding:
                    energy = max(0, energy - SHIELD_DRAIN)
                    current_color = (255, 180, 0)
                    if energy <= 0:
                        shield_is_disabled, is_shielding = True, False
                else:
                    energy = min(100, energy + SHIELD_REGEN)
                    current_color = (0, 255, 255)
                    if not mouse_btns[2] and energy >= 40:
                        shield_is_disabled = False

                for b in bullets[:]:
                    b.update()
                    if b.type == "explosion":
                        for e in enemies[:]:
                            if b.pos.distance_to(e.pos) < 20:
                                if b in bullets: bullets.remove(b)
                                if explosion_sound: explosion_sound.play()
                                effect = ExplosionEffect(b.pos)
                                explosion_effects.append(effect)
                                for e2 in enemies[:]:
                                    if e2.pos.distance_to(effect.pos) < 150:
                                        enemies.remove(e2)
                                        score += SCORE_PER_KILL
                                if pos.distance_to(effect.pos) < 150 and (pygame.time.get_ticks() - invincibility_start_time) > invincibility_duration:
                                    if damage_sound: damage_sound.play()
                                    hp -= 1
                                    invincibility_start_time = pygame.time.get_ticks()
                                    shake = 25
                                    for nearby_e in enemies[:]:
                                        if nearby_e.pos.distance_to(pos) < 200:
                                            nearby_e.vel = (nearby_e.pos - pos).normalize() * 30
                                    if hp <= 0: 
                                         pygame.mixer.stop()
                                         pygame.mixer.music.stop()
                                         if sam_sound: sam_sound.play()
                                         current_state = STATE_DEATH_SEQUENCE
                                         if damage_sound: damage_sound.play()
                                         death_sequence_start_time = pygame.time.get_ticks()
                                         if bang_sound: bang_sound.play()


                                shake = SHAKE_POWER
                                break
                    elif any(e.pos.distance_to(b.pos) < 20 for e in enemies):
                        for e in enemies[:]:
                            if e.pos.distance_to(b.pos) < 20:
                                e.hp -= 1
                                if e.hp <= 0:
                                    enemies.remove(e)
                                    score += SCORE_PER_KILL
                                    shake = SHAKE_POWER
                                if b in bullets: bullets.remove(b)
                                break

                    if b in bullets:
                        if (b.lifetime is not None and b.lifetime <= 0) or b.pos.distance_to(pos) > 1500:
                            if b.type == "explosion":
                                if explosion_sound: explosion_sound.play()
                                effect = ExplosionEffect(b.pos)
                                explosion_effects.append(effect)
                                for e in enemies[:]:
                                    if e.pos.distance_to(effect.pos) < 150:
                                        enemies.remove(e)
                                        score += SCORE_PER_KILL
                                if pos.distance_to(effect.pos) < 150 and (pygame.time.get_ticks() - invincibility_start_time) > invincibility_duration:
                                    if damage_sound: damage_sound.play()
                                    hp -= 1
                                    invincibility_start_time = pygame.time.get_ticks()
                                    shake = 25
                                    for nearby_e in enemies[:]:
                                        if nearby_e.pos.distance_to(pos) < 200:
                                            nearby_e.vel = (nearby_e.pos - pos).normalize() * 30
                                    if hp <= 0: 
                                         pygame.mixer.stop()
                                         pygame.mixer.music.stop()
                                         if sam_sound: sam_sound.play()
                                         current_state = STATE_DEATH_SEQUENCE
                                         death_sequence_start_time = pygame.time.get_ticks()
                                         if bang_sound: bang_sound.play()


                                shake = SHAKE_POWER
                            bullets.remove(b)
                        else:
                            b.draw(screen, camera, shake_off)

                if random.random() < 0.04 * scaling_factor and len(enemies) < STAGE_ENEMY_CAPS[current_stage]:
                    spawn_angle = random.uniform(0, math.pi * 2)
                    spawn_pos = pos + pygame.Vector2(math.cos(spawn_angle), math.sin(spawn_angle)) * 800
                    enemies.append(Enemy(spawn_pos, current_stage, scaling_factor))

                for e in enemies[:]:
                    e.update(pos, current_stage)
                    e.draw(screen, camera, shake_off)
                    if e.pos.distance_to(pos) < 50:
                        if is_shielding:
                            e.vel = (e.pos - pos).normalize() * 15
                            shake = 10
                            if bounce_sound: bounce_sound.play()
                        elif e.pos.distance_to(pos) < 30 and not is_shielding and (pygame.time.get_ticks() - invincibility_start_time) > invincibility_duration:
                            if damage_sound: damage_sound.play()
                            hp -= 1
                            invincibility_start_time = pygame.time.get_ticks()
                            shake = 25
                            for nearby_e in enemies[:]:
                                if nearby_e.pos.distance_to(pos) < 200:
                                    nearby_e.vel = (nearby_e.pos - pos).normalize() * 30
                                    if hp <= 0: 
                                         pygame.mixer.stop()
                                         pygame.mixer.music.stop()
                                         #if sam_sound: sam_sound.play()
                                         current_state = STATE_DEATH_SEQUENCE
                                         death_sequence_start_time = pygame.time.get_ticks()
                                         if bang_sound: bang_sound.play()



                draw_pos = pos - camera + shake_off
                should_draw = True
                if (pygame.time.get_ticks() - invincibility_start_time) < invincibility_duration:
                    should_draw = ((pygame.time.get_ticks() // 100) % 2) == 0
                if should_draw:
                    if is_shielding: pygame.draw.circle(screen, (255, 180, 0), draw_pos, 45, 2)
                    pygame.draw.polygon(screen, current_color, [draw_pos + pygame.Vector2(30, 0).rotate(angle), 
                                                                   draw_pos + pygame.Vector2(-15, 15).rotate(angle), 
                                                                   draw_pos + pygame.Vector2(-15, -15).rotate(angle)])

                if current_weapon == 1 and not is_shielding:
                    radius_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                    pygame.draw.circle(radius_surf, (255, 100, 0, 30), draw_pos, 150, 2)
                    screen.blit(radius_surf, (0, 0))

                if hp <= 3:
                    vignette = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                    vignette.fill((255, 0, 0, int((4 - hp) * 40)))
                    screen.blit(vignette, (0, 0))

                for effect in explosion_effects[:]:
                    effect.update()
                    if effect.lifetime <= 0: explosion_effects.remove(effect)
                    else: effect.draw(screen, camera, shake_off)

                if score >= 200 and not explosion_start_granted:
                    explosion_ammo += EXPLOSION_AMMO_START
                    explosion_start_granted = True
                    last_explosion_ammo_milestone = (score // EXPLOSION_AMMO_PER_KILL_MILESTONE) * EXPLOSION_AMMO_PER_KILL_MILESTONE
                if score >= 400 and not spread_start_granted:
                    spread_ammo += SPREAD_AMMO_START
                    spread_start_granted = True
                    last_spread_ammo_milestone = (score // SPREAD_AMMO_PER_KILL_MILESTONE) * SPREAD_AMMO_PER_KILL_MILESTONE

                curr_exp_m = (score // EXPLOSION_AMMO_PER_KILL_MILESTONE) * EXPLOSION_AMMO_PER_KILL_MILESTONE
                if curr_exp_m > last_explosion_ammo_milestone and score >= 200:
                    explosion_ammo += EXPLOSION_AMMO_REGEN_AMOUNT
                    last_explosion_ammo_milestone = curr_exp_m
                
                curr_spr_m = (score // SPREAD_AMMO_PER_KILL_MILESTONE) * SPREAD_AMMO_PER_KILL_MILESTONE
                if curr_spr_m > last_spread_ammo_milestone and score >= 400:
                    spread_ammo += SPREAD_AMMO_REGEN_AMOUNT
                    last_spread_ammo_milestone = curr_spr_m

                if (score // 100) > last_score_milestone:
                    if score_sound: score_sound.play()
                    last_score_milestone = score // 100

                draw_hud(screen, font, score, hp, energy, current_weapon, weapon_names, explosion_ammo, spread_ammo, game_timer, current_stage, shield_is_disabled, blink=(stage_blink_timer > 0))
                background_surface = screen.copy()

            elif current_state == STATE_MENU:
                if music_playing != "MENU":
                    pygame.mixer.music.load(MUSIC_MAIN_MENU)
                    pygame.mixer.music.play(-1)
                    music_playing = "MENU"
                draw_menu(screen, font)
            elif current_state == STATE_DIFFICULTY:
                from ui import draw_difficulty_menu
                draw_difficulty_menu(screen, font, menu_index)
            elif current_state == STATE_HARDCORE_SELECT:
                from ui import draw_difficulty_menu
                draw_difficulty_menu(screen, font, hardcore_index, is_hardcore=True)
            elif current_state == STATE_TUTORIAL:
                if music_playing != "MENU":
                    pygame.mixer.music.load(MUSIC_MAIN_MENU)
                    pygame.mixer.music.play(-1)
                    music_playing = "MENU"
                draw_tutorial(screen, font)
            elif current_state == STATE_PAUSED:
                if background_surface is not None:
                    screen.blit(background_surface, (0, 0))
                from ui import draw_blur, draw_pause_menu
                draw_blur(screen)
                draw_pause_menu(screen, font, pause_menu_index, pause_menu_options)
            elif current_state == STATE_DEATH_SEQUENCE:
                # TV Static Effect
                current_time = pygame.time.get_ticks()
                elapsed = current_time - death_sequence_start_time
                
                static_surface.fill((0, 0, 0))
                is_flashing = False
                
                # Glitch intensity is on config.py as DEATH_SEQUENCE_START_GLITCH, but we want to control it dynamically based on time elapsed in the death sequence
                glitch_intensity = 0
                if elapsed > DEATH_SEQUENCE_START_GLITCH:
                    base_ramp = min(1.0, (elapsed - DEATH_SEQUENCE_START_GLITCH) / (GAMEOVER_TIMESHOW - DEATH_SEQUENCE_START_GLITCH  ))
                    noise = random.uniform(-0.2, 0.2) if random.random() < 0.3 else 0
                    glitch_intensity = max(0, min(1.0, base_ramp + noise))
                
                # 1. Base static - Lowest Layer
                static_count = 3000 + int(8000 * glitch_intensity)
                for _ in range(static_count):
                    color = random.randint(0, 180)
                    pygame.draw.rect(static_surface, (color, color, color), 
                                     (random.randint(0, WIDTH), random.randint(0, HEIGHT), 2, 2))
                
                # 2. Glitches - Middle Layer (In front of static, but behind the flash)
                if glitch_intensity > 0:
                    num_blocks = int(150 * glitch_intensity)
                    for _ in range(num_blocks):
                        color = random.choice([(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)])
                        w = random.randint(10, 500)
                        h = random.randint(2, 80)
                        pygame.draw.rect(static_surface, color, 
                                         (random.randint(-200, WIDTH), random.randint(-200, HEIGHT), w, h))
                
                # 3. White Flash - Top Layer (Covers everything)
                if elapsed > DEATH_SEQUENCE_START_FLASH:
                    t_rel = (elapsed - DEATH_SEQUENCE_START_FLASH) / (GAMEOVER_TIMESHOW - DEATH_SEQUENCE_START_FLASH)
                    flash_prob = t_rel**2
                    if random.random() < flash_prob:
                        is_flashing = True

                
                # Rapid, jittery screen shift
                shift_range = int(120 * glitch_intensity)
                offset_x = random.randint(-shift_range, shift_range) if shift_range > 0 else 0
                offset_y = random.randint(-shift_range, shift_range) if shift_range > 0 else 0
                
                if is_flashing:
                    screen.fill((255, 255, 255))
                else:
                    screen.blit(static_surface, (offset_x, offset_y))
                    screen.blit(static_overlay, (offset_x, offset_y))


                if elapsed >= GAMEOVER_TIMESHOW:
                    if sam_sound: sam_sound.play()
                    current_state = STATE_GAMEOVER
                    game_over_fade_start_time = pygame.time.get_ticks()
                    animated_score = 0
                    score_animation_speed = max(2, score // 150) if score > 500 else 2
                    if point_count_sound and score > 0: point_count_sound.play(-1)







            elif current_state == STATE_GAMEOVER:
                # Transition: White -> Red -> Black
                elapsed_go = pygame.time.get_ticks() - game_over_fade_start_time
                fade_duration = 3000 
                t = min(1.0, elapsed_go / fade_duration)
                
                if t < 0.2:
                    # White to Red (Fast transition)
                    local_t = t / 0.2
                    bg_color = (255, int(255 * (1 - local_t)), int(255 * (1 - local_t)))
                else:
                    # Red to Black (Slower fade)
                    local_t = (t - 0.2) / 0.8
                    bg_color = (int(255 * (1 - local_t)), 0, 0)
                
                screen.fill(bg_color)

                if music_playing != "GAMEOVER":
                    pygame.mixer.music.load(MUSIC_GAMEOVER)
                    pygame.mixer.music.play(-1)
                    music_playing = "GAMEOVER"
                
                # Score animation
                if animated_score < score:
                    animated_score += score_animation_speed
                    if animated_score >= score:
                        animated_score = score
                        if point_count_sound: point_count_sound.stop()
                
                draw_game_over(screen, font, animated_score)
                from ui import draw_game_over_menu
                draw_game_over_menu(screen, font, game_over_menu_index, game_over_menu_options)


            pygame.display.flip()
            clock.tick(FPS)
    except Exception as e:
        print(f"ERROR: {e}")
        print("Contact the Dev lol XD")
    finally:
        pygame.quit()
        print("Game closed.")


if __name__ == "__main__":
    main()
