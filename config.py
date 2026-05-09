import pygame

# =============================================================================
# CORE SETTINGS
# =============================================================================
WIDTH, HEIGHT  = 1000, 800
FPS            = 60

# =============================================================================
# GAME STATES
# =============================================================================
STATE_MENU = "MENU"
STATE_DIFFICULTY = "DIFFICULTY"
STATE_HARDCORE_SELECT = "HARDCORE_SELECT"
STATE_TUTORIAL = "TUTORIAL"
STATE_PLAYING = "PLAYING"
STATE_PAUSED = "PAUSED"
STATE_GAMEOVER = "GAMEOVER"
STATE_DEATH_SEQUENCE = "DEATH_SEQUENCE"
STATE_SHOP = "SHOP"
STATE_SETTINGS = "SETTINGS"
STATE_CREDITS = "CREDITS"
STATE_CONFIRM_CHANGES = "CONFIRM_CHANGES"

# =============================================================================
# COLORS
# =============================================================================
COLOR_BG = (5, 5, 12)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_NEON_GREEN = (0, 255, 0)
COLOR_CYAN = (0, 255, 255)
COLOR_MAGENTA = (255, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_RED = (255, 0, 0)
COLOR_LIGHT_RED = (255, 50, 50)
COLOR_BRIGHT_RED = (255, 0, 60)
COLOR_DARK_RED = (100, 0, 20)
COLOR_GREY = (150, 150, 150)
COLOR_DARK_GREY = (100, 100, 100)
COLOR_DARK_BLUE = (20, 20, 40)
COLOR_VERY_DARK_PURPLE = (20, 10, 30)
COLOR_DARK_PURPLE = (10, 5, 15)
COLOR_SETTING_BG = (10, 10, 20)
COLOR_ORANGE = (255, 150, 0)
COLOR_BROWN = (150, 100, 0)

# =============================================================================
# UI LAYOUT & DIMENSIONS
# =============================================================================
HUD_SHIELD_RECT = (18, 58, 154, 19)
MENU_RECT_SIZE = (300, 200)
GAMEOVER_MENU_RECT_SIZE = (360, 200)
SETTINGS_MARGIN = 40

# =============================================================================
# DIFFICULTY & SCALING
# =============================================================================
DIFFICULTIES = ["EASY", "NORMAL", "HARDCORE"]
HARDCORE_TIERS = ["BRUTAL", "INSANE", "NIGHTMARE", "EXTINCTION"]
DIFFICULTY_SCALING = {
    "EASY": 0.7,
    "NORMAL": 1.0,
    "BRUTAL": 1.5,
    "INSANE": 2.0,
    "NIGHTMARE": 3.0,
    "EXTINCTION": 5.0
}

# =============================================================================
# PHYSICS & MOVEMENT
# =============================================================================
MOUSE_SENSITIVITY = 1.0
SHADERS_ENABLED = False
SPEED_NORMAL   = 0.7    
FRICTION       = 0.93   
RECOIL         = 2.0    
CAM_SMOOTHING  = 0.05    
BULLET_SPEED   = 18.0

# =============================================================================
# COMBAT & WEAPONS
# =============================================================================
WEAPON_SWITCH = 8

FIRE_RATE_NORMAL = 10
FIRE_RATE_EXPLOSION = 60
FIRE_RATE_SPREAD = 40
SPREAD_BULLET_COUNT = 10
SHIELD_DRAIN = 0.5
SHIELD_REGEN = 0.4
ENEMY_SPEED = 2.0
SHAKE_POWER = 8.0

EXPLOSION_POINT_MILESTONE = 200
SPREAD_POINT_MILESTONE = 400

EXPLOSION_AMMO_START = 5
EXPLOSION_AMMO_PER_KILL_MILESTONE = 56
EXPLOSION_AMMO_REGEN_AMOUNT = 1
SPREAD_AMMO_START = 3
SPREAD_AMMO_PER_KILL_MILESTONE = 30
SPREAD_AMMO_REGEN_AMOUNT = 4

# =============================================================================
# STAGE CONFIGURATION
# =============================================================================
STAGE_DURATION = 120 
MAX_STAGE = 5
STAGE_ENEMY_CAPS = {1: 20, 2: 30, 3: 40, 4: 50, 5: 60}
STAGE_SPEED_BOOST = 0.6 
STAGE_HP_CHANCE = {1: 0, 2: 0.2, 3: 0.4, 4: 0.6, 5: 0.8} 
STAGE_MAX_HP = {1: 1, 2: 2, 3: 3, 4: 5, 5: 8}

# =============================================================================
# GENERAL GAMEPLAY
# =============================================================================
LIVES = 5
SCORE_PER_KILL = 2
BOSS_SCORE_BASE = 1000
BOSS_SCORE_MULTIPLIER = 0.5
BOSS_AMMO_BONUS_PERCENT = 0.15
BITS_PER_KILL = 1
BITS_PER_BOSS = 100
BITS_PER_STAGE = 50
DEATH_SEQUENCE_GLITCH_INTENSITY = 0.8
GAMEOVER_TIMESHOW = 8000
DEATH_SEQUENCE_START_GLITCH = 4000
DEATH_SEQUENCE_START_FLASH = 5000



# =============================================================================
# SHOP PRICES
# =============================================================================
COST_HEAL_HP = 30
COST_MAX_HP = 50
COST_SPEED = 60
COST_REGEN = 40

# =============================================================================
# AUDIO
# =============================================================================
SOUND_FIRE = "fire.wav"
SOUND_SCORE = "Score.wav"
SOUND_EXPLOSION = "explosion.wav"
SOUND_BOUNCE = "bounce shield.wav"
SOUND_DAMAGE = "healthdamage.wav"
SOUND_CHECKPOINT = "Checkpoint.wav"
SOUND_SAM = "sam.wav"
SOUND_POINT_COUNT = "Point_Count[loop].wav"
SOUND_PAUSE = "pause.wav"
SOUND_P_PRESS = "p_press.wav"
SOUND_BANG = "bang.wav"

SOUND_SAM_S1 = "S.A.M/STAGE ONE.wav"
SOUND_SAM_S2 = "S.A.M/stage 2.wav"
SOUND_SAM_S3 = "S.A.M/stage3.wav"
SOUND_SAM_S4 = "S.A.M/stage 4.wav"
SOUND_SAM_S5_PART1 = "S.A.M/stage.wav"
SOUND_SAM_S5_PART2 = "S.A.M/five.wav"
SOUND_SAM_WIN = "S.A.M/you win.wav"

SAM_VOLUME = 0.65
MUSIC_MAIN_MENU = "mainmenu.mp3"
MUSIC_BG = "bg music.mp3"
MUSIC_GAMEOVER = "deathscreen.mp3"
MENU_VOLUME = 0.5
