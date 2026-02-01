#!/usr/bin/env python3
"""
Generate SVG for GitHub Space Shooter Game
Creates an interactive SVG with clickable buttons for game actions
"""

import json
import sys
from datetime import datetime

# Game constants
GRID_WIDTH = 10
GRID_HEIGHT = 10
CELL_SIZE = 50
BOARD_WIDTH = GRID_WIDTH * CELL_SIZE
BOARD_HEIGHT = GRID_HEIGHT * CELL_SIZE
MARGIN_TOP = 80
MARGIN_BOTTOM = 100
SVG_WIDTH = BOARD_WIDTH + 100
SVG_HEIGHT = BOARD_HEIGHT + MARGIN_TOP + MARGIN_BOTTOM

# Colors - matching the red/green cybersecurity theme
BG_COLOR = "#0d1117"
GRID_COLOR = "#30363d"
PLAYER_COLOR = "#00ff00"
ENEMY_COLOR = "#ff0000"
BULLET_COLOR = "#00ff00"
TEXT_COLOR = "#00ff00"
BUTTON_BG = "#1a1e24"
BUTTON_BORDER = "#00ff00"
BUTTON_HOVER = "#00ff0033"
GAME_OVER_COLOR = "#ff0000"

def load_game_state(file_path="game-state.json"):
    """Load game state from JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading game state: {e}", file=sys.stderr)
        # Return default state
        return {
            "playerPosition": 5,
            "enemies": [{"x": 2, "y": 1, "id": 1}, {"x": 7, "y": 2, "id": 2}],
            "bullets": [],
            "score": 0,
            "gameOver": False,
            "lastUpdate": datetime.now().isoformat()
        }

def create_button(x, y, width, height, text, action, enabled=True):
    """Create a clickable button SVG element"""
    issue_url = f"https://github.com/hotaro6754/hotaro6754/issues/new?labels=game-action-{action}&title=Space+Shooter:+{action.title()}"
    
    opacity = "1" if enabled else "0.3"
    pointer_events = "all" if enabled else "none"
    
    return f'''
    <a href="{issue_url}" target="_blank" style="pointer-events:{pointer_events};">
        <g opacity="{opacity}">
            <rect x="{x}" y="{y}" width="{width}" height="{height}" 
                  fill="{BUTTON_BG}" stroke="{BUTTON_BORDER}" stroke-width="2" rx="5"/>
            <text x="{x + width/2}" y="{y + height/2 + 5}" 
                  fill="{TEXT_COLOR}" font-family="'Courier New', monospace" 
                  font-size="14" font-weight="bold" text-anchor="middle">{text}</text>
        </g>
    </a>'''

def generate_svg(state):
    """Generate the complete SVG for the game"""
    
    svg_parts = []
    
    # SVG header
    svg_parts.append(f'''<svg width="{SVG_WIDTH}" height="{SVG_HEIGHT}" 
        xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    
    <!-- Background -->
    <rect width="{SVG_WIDTH}" height="{SVG_HEIGHT}" fill="{BG_COLOR}"/>
    
    <!-- Title -->
    <text x="{SVG_WIDTH/2}" y="30" fill="{TEXT_COLOR}" 
          font-family="'Courier New', monospace" font-size="24" 
          font-weight="bold" text-anchor="middle">🎮 SPACE SHOOTER 🎮</text>
    
    <!-- Score -->
    <text x="{SVG_WIDTH/2}" y="60" fill="{TEXT_COLOR}" 
          font-family="'Courier New', monospace" font-size="18" 
          text-anchor="middle">SCORE: {state['score']}</text>
    ''')
    
    # Game board background
    board_x = (SVG_WIDTH - BOARD_WIDTH) / 2
    board_y = MARGIN_TOP
    
    svg_parts.append(f'''
    <!-- Game Board -->
    <rect x="{board_x}" y="{board_y}" width="{BOARD_WIDTH}" height="{BOARD_HEIGHT}" 
          fill="{BG_COLOR}" stroke="{GRID_COLOR}" stroke-width="2"/>
    ''')
    
    # Draw grid lines
    for i in range(GRID_WIDTH + 1):
        x = board_x + i * CELL_SIZE
        svg_parts.append(f'<line x1="{x}" y1="{board_y}" x2="{x}" y2="{board_y + BOARD_HEIGHT}" stroke="{GRID_COLOR}" stroke-width="1" opacity="0.3"/>')
    
    for i in range(GRID_HEIGHT + 1):
        y = board_y + i * CELL_SIZE
        svg_parts.append(f'<line x1="{board_x}" y1="{y}" x2="{board_x + BOARD_WIDTH}" y2="{y}" stroke="{GRID_COLOR}" stroke-width="1" opacity="0.3"/>')
    
    # Draw enemies
    for enemy in state.get('enemies', []):
        ex = board_x + enemy['x'] * CELL_SIZE + CELL_SIZE/2
        ey = board_y + enemy['y'] * CELL_SIZE + CELL_SIZE/2
        svg_parts.append(f'''
        <text x="{ex}" y="{ey + 15}" fill="{ENEMY_COLOR}" 
              font-size="40" text-anchor="middle">👾</text>
        ''')
    
    # Draw bullets
    for bullet in state.get('bullets', []):
        bx = board_x + bullet['x'] * CELL_SIZE + CELL_SIZE/2
        by = board_y + bullet['y'] * CELL_SIZE + CELL_SIZE/2
        svg_parts.append(f'''
        <circle cx="{bx}" cy="{by}" r="5" fill="{BULLET_COLOR}"/>
        ''')
    
    # Draw player
    if not state.get('gameOver', False):
        px = board_x + state['playerPosition'] * CELL_SIZE + CELL_SIZE/2
        py = board_y + (GRID_HEIGHT - 1) * CELL_SIZE + CELL_SIZE/2
        svg_parts.append(f'''
        <text x="{px}" y="{py + 15}" fill="{PLAYER_COLOR}" 
              font-size="40" text-anchor="middle">🚀</text>
        ''')
    
    # Game Over message
    if state.get('gameOver', False):
        svg_parts.append(f'''
        <rect x="{board_x + 50}" y="{board_y + BOARD_HEIGHT/2 - 40}" 
              width="{BOARD_WIDTH - 100}" height="80" 
              fill="{BG_COLOR}" stroke="{GAME_OVER_COLOR}" stroke-width="3" rx="10" opacity="0.9"/>
        <text x="{SVG_WIDTH/2}" y="{board_y + BOARD_HEIGHT/2}" 
              fill="{GAME_OVER_COLOR}" font-family="'Courier New', monospace" 
              font-size="32" font-weight="bold" text-anchor="middle">GAME OVER!</text>
        <text x="{SVG_WIDTH/2}" y="{board_y + BOARD_HEIGHT/2 + 30}" 
              fill="{TEXT_COLOR}" font-family="'Courier New', monospace" 
              font-size="16" text-anchor="middle">Final Score: {state['score']}</text>
        ''')
    
    # Control buttons
    button_y = board_y + BOARD_HEIGHT + 20
    button_width = 100
    button_height = 40
    button_spacing = 10
    
    total_width = 4 * button_width + 3 * button_spacing
    start_x = (SVG_WIDTH - total_width) / 2
    
    game_active = not state.get('gameOver', False)
    
    svg_parts.append(create_button(start_x, button_y, button_width, button_height, 
                                   "◄ LEFT", "left", game_active))
    svg_parts.append(create_button(start_x + button_width + button_spacing, button_y, 
                                   button_width, button_height, "SHOOT 🔥", "shoot", game_active))
    svg_parts.append(create_button(start_x + 2 * (button_width + button_spacing), button_y, 
                                   button_width, button_height, "RIGHT ►", "right", game_active))
    svg_parts.append(create_button(start_x + 3 * (button_width + button_spacing), button_y, 
                                   button_width, button_height, "NEW GAME", "new", True))
    
    # Instructions
    instructions_y = button_y + button_height + 30
    svg_parts.append(f'''
    <text x="{SVG_WIDTH/2}" y="{instructions_y}" fill="{TEXT_COLOR}" 
          font-family="'Courier New', monospace" font-size="12" 
          text-anchor="middle" opacity="0.7">Click buttons to play! Destroy enemies before they reach you!</text>
    ''')
    
    # Close SVG
    svg_parts.append('</svg>')
    
    return ''.join(svg_parts)

def main():
    """Main function to generate and save SVG"""
    # Load game state
    state = load_game_state("game-state.json")
    
    # Generate SVG
    svg_content = generate_svg(state)
    
    # Save to file
    with open("game.svg", "w") as f:
        f.write(svg_content)
    
    print("SVG generated successfully!")
    print(f"Game state: Player at {state['playerPosition']}, Score: {state['score']}, " +
          f"Enemies: {len(state.get('enemies', []))}, Game Over: {state.get('gameOver', False)}")

if __name__ == "__main__":
    main()
