# Shop System Design Document: The Crossroads

## Overview
Instead of a traditional store, the shop is now a "Crossroads" that appears between stages. The player is presented with a limited set of options and must choose only **one** upgrade or benefit to take forward.

## Core Mechanic: The Binary Choice
After defeating a boss, the player is presented with a single binary choice: **Option A vs Option B**. 

The game will randomly select one of the following "Clash Pairs":

### Possible Clash Pairs
1. **Fire Rate vs. Bullet Volume**
   - **Option A:** Increase Fire Rate (decrease cooldown).
   - **Option B:** Increase Bullet Volume (e.g., +2 bullets to Spread).

2. **Raw Power vs. Survivability**
   - **Option A:** Increase Bullet Speed or Damage.
   - **Option B:** Restore 1 HP.

3. **Utility vs. Mobility**
   - **Option A:** Faster Shield Regeneration.
   - **Option B:** Increase Movement Speed.

4. **High Risk vs. Stability**
   - **Option A (High Risk):** Massive power boost (e.g., Overclock) but with a permanent penalty (e.g., -1 Max HP).
   - **Option B (Stable):** Restore 1 HP.

5. **Greed vs. Growth**
   - **Option A:** Gain 500 BITS immediately (but next stage is 2x harder).
   - **Option B:** Permanent small boost to a random stat.

## Item Durations
Even with the forced choice, the effects can vary in length:
- **Instant:** Applied immediately (e.g., Heal).
- **Round-Based:** Lasts for the next stage only (e.g., Fire Rate boost for Stage 3).
- **Permanent:** Lasts for the rest of the game (e.g., Max HP increase).

## Technical Implementation Plan

### 1. `config.py`
- Define `STATE_SHOP = "SHOP"`.
- Create a `CHOICE_POOL` containing sets of mutually exclusive upgrades.
- Define the effects and penalties for each upgrade.

### 2. `main.py`
- **State Transition:** Transition to `STATE_SHOP` after boss defeat.
- **Selection Logic:** 
    - Randomly pick a "Choice Set" from the `CHOICE_POOL`.
    - Handle the selection of one option.
    - Apply the chosen effect and immediately transition back to `STATE_PLAYING`.
- **Buff Reset:** Clear round-based buffs at the start of the next stage.

### 3. `ui.py`
- Create `draw_shop(screen, font, options, current_index)`:
    - Display the options as distinct "cards" or "paths".
    - Clearly highlight the reward and the trade-off for each.
    - Use a "Pick One" header to emphasize the limitation.

### 4. `entities.py`
- Ensure `Enemy` and `Boss` classes can react to global modifiers (e.g., if a "Risk" choice increased enemy difficulty).

## Workflow
1. Redefine constants in `config.py` to support the choice-based system.
2. Implement the `draw_shop` UI as a choice-selection screen.
3. Integrate the choice logic into the `main.py` game loop.
4. Balance the "Choice Sets" to ensure no single option is always the "correct" pick.
