#!/usr/bin/env python3
"""
Update game state based on actions
Handles game logic: movement, shooting, collisions, enemy spawning
"""

import json
import sys
import random
from datetime import datetime

# Game constants
GRID_WIDTH = 10
GRID_HEIGHT = 10

def load_game_state(file_path="game-state.json"):
    """Load game state from JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading game state: {e}", file=sys.stderr)
        return create_initial_state()

def save_game_state(state, file_path="game-state.json"):
    """Save game state to JSON file"""
    state['lastUpdate'] = datetime.now().isoformat()
    with open(file_path, 'w') as f:
        json.dump(state, f, indent=2)

def create_initial_state():
    """Create initial game state"""
    return {
        "playerPosition": 5,
        "enemies": [
            {"x": 2, "y": 1, "id": 1},
            {"x": 7, "y": 2, "id": 2}
        ],
        "bullets": [],
        "score": 0,
        "gameOver": False,
        "lastUpdate": datetime.now().isoformat()
    }

def move_left(state):
    """Move player left"""
    if state['playerPosition'] > 0:
        state['playerPosition'] -= 1
    return state

def move_right(state):
    """Move player right"""
    if state['playerPosition'] < GRID_WIDTH - 1:
        state['playerPosition'] += 1
    return state

def shoot(state):
    """Add a bullet at player position"""
    if not state['gameOver']:
        bullet_id = max([b.get('id', 0) for b in state.get('bullets', [])], default=0) + 1
        state['bullets'].append({
            "x": state['playerPosition'],
            "y": GRID_HEIGHT - 2,  # Just above player
            "id": bullet_id
        })
    return state

def update_bullets(state):
    """Move bullets up and remove those that go off screen"""
    new_bullets = []
    for bullet in state.get('bullets', []):
        bullet['y'] -= 1
        if bullet['y'] >= 0:  # Keep bullet if still on screen
            new_bullets.append(bullet)
    state['bullets'] = new_bullets
    return state

def spawn_enemy(state):
    """Randomly spawn a new enemy at the top"""
    if random.random() < 0.3:  # 30% chance to spawn
        enemy_id = max([e.get('id', 0) for e in state.get('enemies', [])], default=0) + 1
        x = random.randint(0, GRID_WIDTH - 1)
        state['enemies'].append({
            "x": x,
            "y": 0,
            "id": enemy_id
        })
    return state

def update_enemies(state):
    """Move enemies down"""
    new_enemies = []
    for enemy in state.get('enemies', []):
        enemy['y'] += 1
        if enemy['y'] < GRID_HEIGHT - 1:  # Not at player level yet
            new_enemies.append(enemy)
        else:
            # Enemy reached the player - game over
            state['gameOver'] = True
    state['enemies'] = new_enemies
    return state

def check_collisions(state):
    """Check for bullet-enemy collisions"""
    bullets_to_remove = set()
    enemies_to_remove = set()
    
    for bullet in state.get('bullets', []):
        for enemy in state.get('enemies', []):
            if bullet['x'] == enemy['x'] and bullet['y'] == enemy['y']:
                bullets_to_remove.add(bullet['id'])
                enemies_to_remove.add(enemy['id'])
                state['score'] += 10
    
    # Remove collided bullets and enemies
    state['bullets'] = [b for b in state['bullets'] if b['id'] not in bullets_to_remove]
    state['enemies'] = [e for e in state['enemies'] if e['id'] not in enemies_to_remove]
    
    return state

def process_action(state, action):
    """Process game action and update state"""
    
    if action == "new":
        # Reset game
        return create_initial_state()
    
    if state.get('gameOver', False):
        # No actions allowed when game is over except new game
        return state
    
    # Process action
    if action == "left":
        state = move_left(state)
    elif action == "right":
        state = move_right(state)
    elif action == "shoot":
        state = shoot(state)
    
    # Update game state (bullets, enemies, collisions)
    state = update_bullets(state)
    state = check_collisions(state)
    state = update_enemies(state)
    
    # Spawn new enemy
    if not state.get('gameOver', False):
        state = spawn_enemy(state)
    
    return state

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python update_game_state.py <action>")
        print("Actions: left, right, shoot, new")
        sys.exit(1)
    
    action = sys.argv[1].lower()
    
    # Load current state
    state = load_game_state("game-state.json")
    
    # Process action
    state = process_action(state, action)
    
    # Save updated state
    save_game_state(state, "game-state.json")
    
    print(f"Action '{action}' processed successfully!")
    print(f"Player: {state['playerPosition']}, Score: {state['score']}, " +
          f"Enemies: {len(state.get('enemies', []))}, Bullets: {len(state.get('bullets', []))}, " +
          f"Game Over: {state.get('gameOver', False)}")

if __name__ == "__main__":
    main()
