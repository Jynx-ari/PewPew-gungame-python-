# WILL ADD - PEW PEW MANIA! Feature Ideas (Sorted: Easiest to Hardest)

This list tracks potential features to add to the game, sorted from easiest to implement to hardest.

## Easiest (Quick Wins)

### 1. Difficulty Modes
- **Description**: Already in HARDCORE_TIERS (e.g., no shields, infinite enemies, faster spawns, reduced energy regen).
- **Implementation**: Fine-tune existing tiers with modifiers, dynamic scaling in spawn/logic.
- **Priority**: Medium - Appeals to skilled players.

### 2. Visual Polish
- **Description**: Particles for explosions, bullet trails, animated backgrounds.
- **Implementation**: Pygame surfaces for effects, update draw methods.
- **Priority**: Low - Improves feel without mechanics.

### 3. Achievement System
- **Description**: Track milestones (e.g., 100 kills, survive 5 stages) for unlocks or stats.
- **Implementation**: Dict/file-based storage, check on events, UI display.
- **Priority**: Low - Nice-to-have for engagement.

### 4. Enemy AI Improvements (Optional)
- **Description**: Since circling can be a valid skill, keep it but add unpredictability (e.g., random offsets) to encourage varied tactics. Alternatively, skip this to preserve player freedom.
- **Implementation**: If implementing, modify Enemy.update() in entities.py with slight random drift. Otherwise, remove to let players experiment.
- **Priority**: Low - Circling as a skill promotes creativity.

## Medium Difficulty

### 5. Power-ups
- **Description**: Droppable items from enemies (e.g., temporary invincibility, ammo refill, speed boost).
- **Implementation**: Random spawn on enemy death, collect on contact, timer-based effects.
- **Priority**: Medium - Enhances replayability.

### 6. More Weapons
- **Description**: New types like chain lightning, homing shots, or piercing bullets.
- **Implementation**: Extend weapon logic, unlock via score thresholds.
- **Priority**: High - Expands weapon variety.

### 7. New Enemy Type: Juggernaut
- **Description**: Large enemy that splits into more enemies when killed (exponential growth). Earn a point per kill, unlike high-HP enemies.
- **Implementation**: New enemy subclass with split logic on death, limit splits to prevent infinite.
- **Priority**: High - Adds unique challenge and strategy.

### 8. Environmental Hazards
- **Description**: Obstacles like asteroids (damage on hit) or black holes (pull player).
- **Implementation**: Static/dynamic entities that affect player movement/health.
- **Priority**: Low - Adds strategy without core changes.

### 9. Boss Encounters
- **Description**: Boss with every stage, each with unique patterns (e.g., fast-moving, shielded, multi-phase, teleporting).
- **Implementation**: Extend enemy class for bosses, trigger at stage end, scale HP/behavior.
- **Priority**: Medium - Increases challenge.

## Hardest (Major Systems)

### 10. Exploration Incentives (Infinite World Adaptation)
- **Description**: Since the map is infinite, reward exploration through dynamic events and relative zones. Examples: treasure chests spawning at random distances after milestones, "safe bubbles" that temporarily reduce enemy spawns when moving far from start, or bonuses for maintaining high speeds/varied paths.
- **Implementation**: Use player position tracking (e.g., distance from origin) to trigger events. Spawn collectibles via timers or conditions, create temporary "bonus fields" that activate based on exploration metrics.
- **Priority**: Medium - Encourages exploration and varied strategies beyond circling.

### 11. Currency & Upgrades
- **Description**: Earn coins from enemy kills or stage completions (separate from score).
- **Implementation**: Add coin variable, drop logic on kills, shop UI after stages for permanent buffs (e.g., +HP, +speed, weapon upgrades).
- **Priority**: High - Adds progression depth.

### 12. Settings Menu
- **Description**: User preferences for volume controls, key bindings, graphics toggles (e.g., CRT effects), and difficulty presets.
- **Implementation**: New game state with UI sliders/buttons, save/load settings from file (e.g., JSON), integrate into main menu.
- **Priority**: Medium - Improves accessibility and customization.

### 13. CRT Visual Effects
- **Description**: Retro CRT monitor effects like scanlines, phosphor glow, vignette, and screen curvature for nostalgic feel.
- **Implementation**: Create overlay surfaces with shaders/simulated effects, blend onto screen in main draw loop.
- **Priority**: Low - Enhances visual style without gameplay changes.

### 14. Inter-Stage Shop
- **Description**: Pause after each stage for a shop where players use coins (from current/previous levels) to buy upgrades like increased HP, speed, or weapon boosts.
- **Implementation**: New game state triggered post-stage victory, UI with buyable options, deduct coins and apply buffs permanently.
- **Priority**: High - Ties into currency system for progression.



## Notes
- Update this file as we implement or discard ideas.
- Focus on one feature at a time to keep code clean.
- Test thoroughly after each addition.