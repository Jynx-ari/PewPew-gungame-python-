# PEW PEW MANIA!

**PEW PEW MANIA!** is a fast-paced space shooter game built with Python and Pygame. Survive waves of enemies across multiple stages, unlock powerful weapons, and manage your shield to stay alive.

## 🚀 Features

- **Multiple Weapons**:
  - **Normal**: Standard rapid fire.
  - **Explosion**: Slow fire rate but creates a massive area-of-effect blast (Unlocks at 200 score).
  - **Spread**: Fires multiple bullets in a fan pattern for wider coverage (Unlocks at 400 score).
- **Shield System**: Deploy a protective shield using the right mouse button to deflect enemies, but be careful—it drains your energy!
- **Stage Progression**: Survive 5 challenging stages. As you progress, enemies become faster and tougher.
- **S.A.M Voice-overs**: Features an integrated AI voice (S.A.M) that announces stage transitions and your ultimate victory.
- **Dynamic FX**: Smooth camera movement, screen shake on impact, and explosive visual effects.

## 🎮 Controls

| Key | Action |
| :--- | :--- |
| **WASD** | Move Player |
| **Mouse** | Aim & Shoot (Left Click) |
| **Right Click** | Deploy Shield |
| **E** | Switch Weapon |
| **Space** | Start Game / Retry |
| **F11** | Toggle Fullscreen |

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.x
- `pygame` library

### Setup
1. Clone the repository or download the source code.
2. Install the required dependency:
   ```bash
   pip install pygame
   ```

### Running the Game
Execute the main script to start playing:
```bash
python main.py
```

## 📈 Project Structure
- `main.py`: The main game loop and state management.
- `config.py`: Game constants, weapon settings, and audio paths.
- `entities.py`: Logic for bullets, enemies, and explosions.
- `ui.py`: HUD and menu rendering.
- `S.A.M/`: Directory containing voice-over audio files.
