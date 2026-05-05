import pygame

# Window and Game Settings
WIDTH, HEIGHT  = 1000, 800
FPS            = 60

SCORE_PER_KILL = 2

# Physics and Movement
SPEED_NORMAL   = 0.7    
FRICTION       = 0.93   
RECOIL         = 2.0    
CAM_SMOOTHING  = 0.05    
BULLET_SPEED   = 18.0

# Weapon Fire Rates
FIRE_RATE_NORMAL = 10
FIRE_RATE_EXPLOSION = 60  # Very slow
FIRE_RATE_SPREAD = 40    # Half of explosion
SPREAD_BULLET_COUNT = 10 # Number of bullets in spread shot

# Shield Settings
SHIELD_DRAIN   = 0.5
SHIELD_REGEN   = 0.4

# Enemy Settings
ENEMY_SPEED    = 2.0
SHAKE_POWER    = 8.0

# Weapon Ammo Settings
EXPLOSION_AMMO_START = 5
EXPLOSION_AMMO_PER_KILL_MILESTONE = 25 # 5 kills * 5 pts
EXPLOSION_AMMO_REGEN_AMOUNT = 1

SPREAD_AMMO_START = 3
SPREAD_AMMO_PER_KILL_MILESTONE = 75 # 15 kills * 5 pts
SPREAD_AMMO_REGEN_AMOUNT = 4

# Stage Configuration
STAGE_DURATION = 120 # 2 minutes
MAX_STAGE = 5
STAGE_ENEMY_CAPS = {1: 20, 2: 30, 3: 40, 4: 50, 5: 60}
STAGE_SPEED_BOOST = 0.6 
STAGE_HP_CHANCE = {1: 0, 2: 0.2, 3: 0.4, 4: 0.6, 5: 0.8} 
STAGE_MAX_HP = {1: 1, 2: 2, 3: 3, 4: 5, 5: 8}

# Game States
STATE_MENU = "MENU"
STATE_TUTORIAL = "TUTORIAL"
STATE_PLAYING = "PLAYING"
STATE_GAMEOVER = "GAMEOVER"

# Trolls
turn_off_trolls = False
TROLLS = [  
    "If I were you buddy, I'd quit.", 
    "Oh? Your back at it again.", 
    "I wonder. How long would you last?", 
    "What determination.", 
    "Goodluck. Or not.", 
    "I know your bad at games, but i never knew your were THIS bad.",
     "Are you even trying? Or is this your best?",
    "I have seen better play from a broken toaster.",
    "Maybe try a different hobby. Like breathing. Silently.",
    "I feel sorry for your keyboard. It deserves a better owner.",
    "Don't worry. Failure is just a habit for you now.",
     "Do you want me to write a 'baby mode' just for you? It's okay to admit it.",
    "I literally programmed the physics to help you, and you still messed it up.",
    "Every time you die, I lose a little bit of faith in humanity.",
    "I should have just made a 'Quit' button and saved us both the time.",
    "Are you doing this on purpose? No one is naturally this bad.",
    "I'm looking at the variables right now... yep, the 'Skill' value is still zero.",
    "If I knew you were going to be the player, I wouldn't have bothered optimizing the graphics.",
    "Maybe try playing something simpler. Like 'Checkers'. Actually, no, you'd lose that too.",
    "I'm literally rewriting the code to make it easier as we speak. You're welcome.",
    "You're the reason I'm considering a career change."
]

# Sound Paths
SOUND_FIRE = "fire.wav"
SOUND_SCORE = "Score.wav"
SOUND_EXPLOSION = "explosion.wav"
SOUND_BOUNCE = "bounce shield.wav"
SOUND_DAMAGE = "healthdamage.wav"
SOUND_CHECKPOINT = "Checkpoint.wav"
SOUND_SAM = "sam.wav"
SOUND_POINT_COUNT = "Point_Count[loop].wav"

# SAM Voice-overs
SOUND_SAM_S1 = "S.A.M/STAGE ONE.wav"
SOUND_SAM_S2 = "S.A.M/stage 2.wav"
SOUND_SAM_S3 = "S.A.M/stage3.wav"
SOUND_SAM_S4 = "S.A.M/stage 4.wav"
SOUND_SAM_S5_PART1 = "S.A.M/stage.wav"
SOUND_SAM_S5_PART2 = "S.A.M/five.wav"
SOUND_SAM_WIN = "S.A.M/you win.wav"

MUSIC_MAIN_MENU = "mainmenu.mp3"
MUSIC_BG = "bg music.mp3"

