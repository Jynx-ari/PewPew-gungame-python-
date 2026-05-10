# Future Implementations: New Weapons & Mechanics

## Requested Weapons

### 1. Burst Fire
- **Mechanic:** Fires a quick sequence of 3 bullets (a "burst") before entering a cooldown period.
- **Stats:** High burst fire-rate, but a significant cooldown between bursts.
- **Balance:** Great for concentrated damage, but leaves the player vulnerable during the cooldown.

### 2. Laser Beam
- **Mechanic:** Fires a long, thin line of energy that persists for a short duration.
- **Stats:** High damage (3+ HP per hit), fully penetratable (hits all enemies in the line).
- **Balance:** Extremely powerful in corridors or crowds, but very slow fire rate and requires precise aiming.

### 3. Nova / Circular Burst
- **Mechanic:** Fires a ring of bullets outwards in all directions (360 degrees) from the player.
- **Stats:** High bullet count, medium speed.
- **Balance:** Perfect for "get off me" situations when surrounded, but useless for targeted offense.

### 4. Homing Missiles
- **Mechanic:** Fires slow-moving projectiles that curve toward the nearest enemy within a defined range.
- **Stats:** Slow velocity, high impact damage.
- **Balance:** High accuracy, but slow travel time means enemies can move out of the way if they're fast enough.

---

## Luna's Suggested Additions (For Balance)

To ensure the game remains challenging and tactical, I suggest these additions:

### 5. The Railgun (Precision Power)
- **Mechanic:** An instantaneous, screen-width beam that destroys everything in its path.
- **Stats:** Massive damage, infinite penetration.
- **Balance:** Extreme cooldown (e.g., 3-5 seconds). It's a "panic button" or a strategic strike, not a primary weapon.

### 6. Orbital Sentries (Defensive Offense)
- **Mechanic:** 2-3 small drones orbit the player and fire small bullets at the nearest enemy automatically.
- **Stats:** Low damage, constant fire.
- **Balance:** Provides passive coverage, allowing the player to focus on dodging, but doesn't replace the need for active shooting.

### 7. Chain Lightning (Crowd Control)
- **Mechanic:** Fires a bolt that hits one enemy and then arcs to the 2 nearest enemies.
- **Stats:** Medium damage, limited range.
- **Balance:** Excellent for clearing clusters of low-HP enemies, but weak against single, high-HP targets (like bosses).

## Implementation Notes
- **Homing Logic:** Use a `find_nearest_enemy()` function that iterates through the `enemies` list and returns the one with the minimum `distance_to(bullet.pos)`.
- **Laser Logic:** Instead of a `Bullet` entity, use a `pygame.draw.line` and a collision check using a line-circle intersection formula.
- **Balance Pass:** Every new weapon should be tested against the `DIFFICULTY_SCALING` to ensure it doesn't make the game too easy on Hardcore.
