"""
HaHa Hausservice Haubenhofer Tetris Game
A promotional Tetris clone with office and bathroom furniture pieces

Built with Pygame Zero
"""

import pgzrun
import os
from pygame import Rect, transform, image
from game_logic import (
    Piece, SHAPES, PIECE_COLORS, GRID_WIDTH, GRID_HEIGHT,
    INITIAL_FALL_SPEED, SCORE_SOFT_DROP, SCORE_HARD_DROP,
    check_collision, lock_piece, check_lines, clear_lines, spawn_piece
)
from sprite_manager import sprite_manager
from sound_manager import sound_manager
from highscore_manager import highscore_manager

# Window configuration
WIDTH = 1280
HEIGHT = 960
TITLE = "HaHa Hausservice Haubenhofer Tetris"

# Colors (Brand colors from design document)
BACKGROUND_COLOR = (245, 245, 245)  # #F5F5F5 Light gray
UI_TEXT_COLOR = (44, 62, 80)  # #2C3E50 Dark navy/charcoal
PRIMARY_ACCENT = (0, 102, 204)  # #0066CC Bright blue
SECONDARY_ACCENT = (0, 153, 51)  # #009933 Green
GRID_BORDER = (204, 204, 204)  # #CCCCCC Light gray
GRID_BACKGROUND = (255, 255, 255)  # #FFFFFF White

# Grid configuration for display
BLOCK_SIZE = 48  # 48x48 pixels per block
GRID_X = 400  # X position of game grid
GRID_Y = 0  # Y position of game grid

GRID_RECT = Rect(GRID_X, GRID_Y, GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE)
NEXT_PIECE_BOX = Rect(950, 120, 240, 240)

# Load and prepare logo
logo_surface = None  # Keep reference for potential future use (e.g., re-scaling)
rotated_logo = None

def load_logo():
    """Load and rotate the logo for the left panel"""
    global logo_surface, rotated_logo
    
    # Try to load logo (prefer PNG placeholder, fallback to JPEG)
    logo_files = ['assets/logo_placeholder.png', 'assets/logo.png', 'assets/logo.jpeg']
    logo_loaded = False
    
    for logo_file in logo_files:
        if os.path.exists(logo_file):
            try:
                logo_surface = image.load(logo_file)
                logo_loaded = True
                print(f"Loaded logo from {logo_file}")
                break
            except (FileNotFoundError, IOError) as e:
                print(f"Error loading {logo_file}: {e}")
    
    if not logo_loaded:
        print("No logo file found")
        rotated_logo = None
        return
    
    try:
        # Calculate dimensions for the left panel
        # We want the logo to fit nicely in the left area (0-400px wide, 960px tall)
        # With 90 degree rotation, the logo width becomes height and vice versa
        
        # The rotated logo should fit within 400px width and 960px height
        # After rotation: original_height becomes width, original_width becomes height
        max_rotated_width = 380  # Leave some margin
        max_rotated_height = 940  # Leave some margin
        
        # Calculate what the original dimensions would need to be
        # rotated_width = original_height, rotated_height = original_width
        original_width = logo_surface.get_width()
        original_height = logo_surface.get_height()
        
        # Scale to fit the rotated dimensions
        scale_width = max_rotated_width / original_height
        scale_height = max_rotated_height / original_width
        scale_factor = min(scale_width, scale_height)
        
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        
        # Scale the logo
        scaled_logo = transform.scale(logo_surface, (new_width, new_height))
        
        # Rotate 90 degrees clockwise
        rotated_logo = transform.rotate(scaled_logo, -90)
        
    except (ValueError, TypeError) as e:
        print(f"Error processing logo dimensions: {e}")
        rotated_logo = None

# Game state
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
game_state = {
    'current_piece': None,
    'next_piece': None,
    'fall_timer': 0,
    'game_over': False,
    'paused': False,
    'menu': 'start',  # 'start', 'playing', 'paused', 'game_over'
    'score': 0,
    'level': 1,
    'lines_cleared': 0,
    'fall_speed': INITIAL_FALL_SPEED,
    'is_new_high_score': False,
    'line_clear_effect': [],  # List of (line_index, timer) for line clear animation
    'line_clear_duration': 0.3  # Duration of line clear effect in seconds
}

# Load logo on startup
load_logo()

# Load piece sprites
sprite_manager.load_sprites()
print(f"Sprite rendering: {'enabled' if sprite_manager.has_sprites() else 'disabled (using colors)'}")

# Load sounds
sound_manager.load_sounds()
print(f"Sound effects: {'enabled' if sound_manager.has_sounds() else 'disabled (no sound files)'}")


def draw_start_menu():
    """Draw the start menu screen"""
    # Draw logo in the center if available
    if rotated_logo:
        # Center the logo
        logo_x = (WIDTH - rotated_logo.get_width()) // 2
        logo_y = HEIGHT // 2 - 200
        screen.blit(rotated_logo, (logo_x, logo_y))
    
    # Draw title
    screen.draw.text(
        "HaHa HAUSSERVICE HAUBENHOFER",
        center=(WIDTH // 2, 150),
        fontsize=40,
        color=PRIMARY_ACCENT
    )
    
    screen.draw.text(
        "TETRIS",
        center=(WIDTH // 2, 200),
        fontsize=60,
        color=SECONDARY_ACCENT
    )
    
    # Draw high score
    high_score = highscore_manager.get_high_score()
    screen.draw.text(
        f"HIGH SCORE: {high_score}",
        center=(WIDTH // 2, HEIGHT // 2 + 100),
        fontsize=32,
        color=UI_TEXT_COLOR
    )
    
    # Draw instructions
    screen.draw.text(
        "Press SPACE to Start",
        center=(WIDTH // 2, HEIGHT // 2 + 200),
        fontsize=36,
        color=PRIMARY_ACCENT
    )
    
    screen.draw.text(
        "Press M to Toggle Music",
        center=(WIDTH // 2, HEIGHT // 2 + 250),
        fontsize=24,
        color=UI_TEXT_COLOR
    )
    
    # Draw controls
    controls_text = [
        "CONTROLS:",
        "LEFT/RIGHT - Move",
        "UP - Rotate",
        "DOWN - Soft Drop",
        "SPACE - Hard Drop",
        "P - Pause"
    ]
    
    y_offset = HEIGHT - 280
    for i, control in enumerate(controls_text):
        fontsize = 28 if i == 0 else 20
        color = PRIMARY_ACCENT if i == 0 else UI_TEXT_COLOR
        screen.draw.text(
            control,
            center=(WIDTH // 2, y_offset),
            fontsize=fontsize,
            color=color
        )
        y_offset += 30


def draw_pause_menu():
    """Draw the pause menu overlay"""
    # Draw semi-transparent overlay
    overlay_rect = Rect(GRID_X, GRID_Y, GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE)
    screen.draw.filled_rect(overlay_rect, (0, 0, 0, 180))
    
    screen.draw.text(
        "PAUSED",
        center=(GRID_X + GRID_WIDTH * BLOCK_SIZE // 2, 
               GRID_Y + GRID_HEIGHT * BLOCK_SIZE // 2 - 50),
        fontsize=48,
        color=(255, 255, 255)
    )
    
    screen.draw.text(
        "Press P to Resume",
        center=(GRID_X + GRID_WIDTH * BLOCK_SIZE // 2, 
               GRID_Y + GRID_HEIGHT * BLOCK_SIZE // 2 + 20),
        fontsize=24,
        color=(255, 255, 255)
    )
    
    screen.draw.text(
        "Press M to Toggle Music",
        center=(GRID_X + GRID_WIDTH * BLOCK_SIZE // 2, 
               GRID_Y + GRID_HEIGHT * BLOCK_SIZE // 2 + 60),
        fontsize=20,
        color=(255, 255, 255)
    )


def handle_piece_lock():
    """
    Handle locking a piece and all related effects.
    Returns True if game is over, False otherwise.
    """
    # Lock the piece
    lock_piece(game_state['current_piece'], grid)
    sound_manager.play_sound('lock')
    
    # Check and clear any completed lines
    completed_lines = check_lines(grid)
    if completed_lines:
        # Track level before clearing lines
        old_level = game_state['level']
        
        # Start line clear effect animation
        game_state['line_clear_effect'] = [(line_idx, 0.0) for line_idx in completed_lines]
        
        # Play appropriate sound based on number of lines
        if len(completed_lines) >= 4:
            sound_manager.play_sound('tetris')
        else:
            sound_manager.play_sound('line_clear')
        
        clear_lines(completed_lines, grid, game_state)
        
        # Check if we leveled up
        if game_state['level'] > old_level:
            sound_manager.play_sound('level_up')
    
    # Spawn new piece
    spawn_piece(game_state, grid, sprite_manager)
    
    # Check if game over and handle it
    if game_state['game_over']:
        sound_manager.play_sound('game_over')
        sound_manager.stop_music()
        # Check and save high score
        game_state['is_new_high_score'] = highscore_manager.save(game_state['score'])
        return True
    
    return False


def draw():
    """Main draw function - called by Pygame Zero every frame"""
    # Clear screen with background color
    screen.fill(BACKGROUND_COLOR)
    
    # Draw start menu
    if game_state['menu'] == 'start':
        draw_start_menu()
        return
    
    # Draw logo in the left spacing area (rotated 90 degrees)
    if rotated_logo:
        # Position the logo centered in the left area
        # Left area is 0-400px wide, logo should be centered vertically and horizontally
        logo_x = (GRID_X - rotated_logo.get_width()) // 2
        logo_y = (HEIGHT - rotated_logo.get_height()) // 2
        screen.blit(rotated_logo, (logo_x, logo_y))
    
    # Draw game grid background
    screen.draw.filled_rect(GRID_RECT, GRID_BACKGROUND)
    
    # Draw grid border
    screen.draw.rect(GRID_RECT, GRID_BORDER)
    
    # Draw grid lines (vertical)
    for x in range(1, GRID_WIDTH):
        line_x = GRID_X + (x * BLOCK_SIZE)
        screen.draw.line(
            (line_x, GRID_Y),
            (line_x, GRID_Y + GRID_HEIGHT * BLOCK_SIZE),
            GRID_BORDER
        )
    
    # Draw grid lines (horizontal)
    for y in range(1, GRID_HEIGHT):
        line_y = GRID_Y + (y * BLOCK_SIZE)
        screen.draw.line(
            (GRID_X, line_y),
            (GRID_X + GRID_WIDTH * BLOCK_SIZE, line_y),
            GRID_BORDER
        )
    
    # Draw locked pieces on the grid
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            cell = grid[y][x]
            if cell != 0:
                block_x = GRID_X + x * BLOCK_SIZE
                block_y = GRID_Y + y * BLOCK_SIZE
                
                # Check if cell contains a Block object (new system) or just a string (old system)
                if hasattr(cell, 'sprite') and hasattr(cell, 'rotation'):
                    # New system with rotation: get rotated sprite from sprite_manager
                    rotated_sprite = sprite_manager.get_block_sprite(
                        cell.shape_type, cell.sprite_dx, cell.sprite_dy, cell.rotation
                    )
                    if rotated_sprite:
                        screen.blit(rotated_sprite, (block_x, block_y))
                    else:
                        # Fallback to colored blocks
                        block_rect = Rect(block_x, block_y, BLOCK_SIZE, BLOCK_SIZE)
                        color = PIECE_COLORS[cell.shape_type]
                        screen.draw.filled_rect(block_rect, color)
                        screen.draw.rect(block_rect, GRID_BORDER)
                elif hasattr(cell, 'sprite') and cell.sprite:
                    # Old system: use the block's pre-loaded sprite (no rotation)
                    screen.blit(cell.sprite, (block_x, block_y))
                elif hasattr(cell, 'shape_type'):
                    # Block object without sprite - use color fallback
                    block_rect = Rect(block_x, block_y, BLOCK_SIZE, BLOCK_SIZE)
                    color = PIECE_COLORS[cell.shape_type]
                    screen.draw.filled_rect(block_rect, color)
                    screen.draw.rect(block_rect, GRID_BORDER)
                else:
                    # Old system: cell is a shape_type string
                    block_rect = Rect(block_x, block_y, BLOCK_SIZE, BLOCK_SIZE)
                    color = PIECE_COLORS[cell]
                    screen.draw.filled_rect(block_rect, color)
                    screen.draw.rect(block_rect, GRID_BORDER)
    
    # Draw line clear effects
    for line_index, effect_timer in game_state['line_clear_effect']:
        # Calculate alpha based on timer (fade out effect)
        alpha = int(255 * (1 - effect_timer / game_state['line_clear_duration']))
        
        # Create a flashing effect with alternating colors
        flash_cycle = int(effect_timer * 20) % 2  # Fast flash
        if flash_cycle == 0:
            effect_color = (255, 255, 255, alpha)  # White
        else:
            effect_color = (255, 215, 0, alpha)  # Gold
        
        # Draw the line effect overlay
        line_rect = Rect(GRID_X, GRID_Y + line_index * BLOCK_SIZE, 
                        GRID_WIDTH * BLOCK_SIZE, BLOCK_SIZE)
        screen.draw.filled_rect(line_rect, effect_color)
    
    # Draw current falling piece
    current_piece = game_state['current_piece']
    if current_piece:
        for (dx, dy), block in current_piece.blocks:
            bx = current_piece.x + dx
            by = current_piece.y + dy
            if by >= 0:  # Only draw blocks that are visible
                block_x = GRID_X + bx * BLOCK_SIZE
                block_y = GRID_Y + by * BLOCK_SIZE
                
                # Use the block's rotated sprite, fallback to color
                if hasattr(block, 'rotation'):
                    # Get rotated sprite from sprite_manager
                    rotated_sprite = sprite_manager.get_block_sprite(
                        block.shape_type, block.sprite_dx, block.sprite_dy, block.rotation
                    )
                    if rotated_sprite:
                        screen.blit(rotated_sprite, (block_x, block_y))
                    else:
                        # Fallback to colored blocks
                        block_rect = Rect(block_x, block_y, BLOCK_SIZE, BLOCK_SIZE)
                        screen.draw.filled_rect(block_rect, current_piece.color)
                        screen.draw.rect(block_rect, GRID_BORDER)
                elif block.sprite:
                    # Old system without rotation
                    screen.blit(block.sprite, (block_x, block_y))
                else:
                    # Fallback to colored blocks
                    block_rect = Rect(block_x, block_y, BLOCK_SIZE, BLOCK_SIZE)
                    screen.draw.filled_rect(block_rect, current_piece.color)
                    screen.draw.rect(block_rect, GRID_BORDER)
    
    # Draw UI panel labels
    screen.draw.text(
        "NEXT PIECE:",
        topleft=(950, 80),
        fontsize=24,
        color=UI_TEXT_COLOR
    )
    
    # Draw next piece box
    screen.draw.filled_rect(NEXT_PIECE_BOX, GRID_BACKGROUND)
    screen.draw.rect(NEXT_PIECE_BOX, GRID_BORDER)
    
    # Draw next piece preview
    next_piece = game_state['next_piece']
    if next_piece:
        # Calculate the bounds of the piece
        min_x = min(dx for dx, dy in next_piece.shape)
        max_x = max(dx for dx, dy in next_piece.shape)
        min_y = min(dy for dx, dy in next_piece.shape)
        max_y = max(dy for dx, dy in next_piece.shape)
        
        # Calculate piece dimensions in pixels
        piece_width = (max_x - min_x + 1) * BLOCK_SIZE
        piece_height = (max_y - min_y + 1) * BLOCK_SIZE
        
        # Center the piece in the preview box
        preview_offset_x = NEXT_PIECE_BOX.x + (NEXT_PIECE_BOX.width - piece_width) // 2 - min_x * BLOCK_SIZE
        preview_offset_y = NEXT_PIECE_BOX.y + (NEXT_PIECE_BOX.height - piece_height) // 2 - min_y * BLOCK_SIZE
        
        for (dx, dy), block in next_piece.blocks:
            block_x = preview_offset_x + dx * BLOCK_SIZE
            block_y = preview_offset_y + dy * BLOCK_SIZE
            
            # Use the block's rotated sprite, fallback to color
            if hasattr(block, 'rotation'):
                # Get rotated sprite from sprite_manager
                rotated_sprite = sprite_manager.get_block_sprite(
                    block.shape_type, block.sprite_dx, block.sprite_dy, block.rotation
                )
                if rotated_sprite:
                    screen.blit(rotated_sprite, (block_x, block_y))
                else:
                    # Fallback to colored blocks
                    block_rect = Rect(block_x, block_y, BLOCK_SIZE, BLOCK_SIZE)
                    screen.draw.filled_rect(block_rect, next_piece.color)
                    screen.draw.rect(block_rect, GRID_BORDER)
            elif block.sprite:
                # Old system without rotation
                screen.blit(block.sprite, (block_x, block_y))
            else:
                # Fallback to colored blocks
                block_rect = Rect(block_x, block_y, BLOCK_SIZE, BLOCK_SIZE)
                screen.draw.filled_rect(block_rect, next_piece.color)
                screen.draw.rect(block_rect, GRID_BORDER)
    
    # Draw score display
    screen.draw.text(
        f"SCORE: {game_state['score']}",
        topleft=(950, 400),
        fontsize=28,
        color=UI_TEXT_COLOR
    )
    
    # Draw high score
    screen.draw.text(
        f"HIGH SCORE: {highscore_manager.get_high_score()}",
        topleft=(950, 440),
        fontsize=24,
        color=SECONDARY_ACCENT
    )
    
    screen.draw.text(
        f"LEVEL: {game_state['level']}",
        topleft=(950, 490),
        fontsize=28,
        color=UI_TEXT_COLOR
    )
    
    screen.draw.text(
        f"LINES: {game_state['lines_cleared']}",
        topleft=(950, 540),
        fontsize=28,
        color=UI_TEXT_COLOR
    )
    
    # Draw controls
    screen.draw.text(
        "CONTROLS:",
        topleft=(950, 640),
        fontsize=24,
        color=UI_TEXT_COLOR
    )
    
    controls_text = [
        "LEFT/RIGHT Move",
        "UP Rotate",
        "DOWN Soft Drop",
        "SPACE Hard Drop",
        "P Pause",
        "M Toggle Music"
    ]
    
    y_offset = 680
    for control in controls_text:
        screen.draw.text(
            control,
            topleft=(950, y_offset),
            fontsize=18,
            color=UI_TEXT_COLOR
        )
        y_offset += 28
    
    # Draw game over message if game is over
    if game_state['game_over']:
        # Draw semi-transparent overlay
        overlay_rect = Rect(GRID_X, GRID_Y + GRID_HEIGHT * BLOCK_SIZE // 2 - 100, 
                           GRID_WIDTH * BLOCK_SIZE, 200)
        screen.draw.filled_rect(overlay_rect, (0, 0, 0, 180))
        
        screen.draw.text(
            "GAME OVER",
            center=(GRID_X + GRID_WIDTH * BLOCK_SIZE // 2, 
                   GRID_Y + GRID_HEIGHT * BLOCK_SIZE // 2 - 50),
            fontsize=48,
            color=(255, 255, 255)
        )
        
        # Show if new high score
        if game_state.get('is_new_high_score', False):
            screen.draw.text(
                "NEW HIGH SCORE!",
                center=(GRID_X + GRID_WIDTH * BLOCK_SIZE // 2, 
                       GRID_Y + GRID_HEIGHT * BLOCK_SIZE // 2 - 10),
                fontsize=28,
                color=(255, 215, 0)  # Gold color
            )
        
        screen.draw.text(
            f"Final Score: {game_state['score']}",
            center=(GRID_X + GRID_WIDTH * BLOCK_SIZE // 2, 
                   GRID_Y + GRID_HEIGHT * BLOCK_SIZE // 2 + 30),
            fontsize=28,
            color=(255, 255, 255)
        )
        
        screen.draw.text(
            "Press R to Restart",
            center=(GRID_X + GRID_WIDTH * BLOCK_SIZE // 2, 
                   GRID_Y + GRID_HEIGHT * BLOCK_SIZE // 2 + 70),
            fontsize=24,
            color=(255, 255, 255)
        )
    
    # Draw pause menu if paused
    elif game_state.get('paused', False):
        draw_pause_menu()


def update(dt):
    """Main update function - called by Pygame Zero every frame"""
    # Don't update if on start menu
    if game_state['menu'] == 'start':
        return
    
    # Update line clear effects even when paused or game over
    if game_state['line_clear_effect']:
        updated_effects = []
        for line_index, effect_timer in game_state['line_clear_effect']:
            new_timer = effect_timer + dt
            if new_timer < game_state['line_clear_duration']:
                updated_effects.append((line_index, new_timer))
        game_state['line_clear_effect'] = updated_effects
    
    # Don't update if game is over or paused
    if game_state['game_over'] or game_state.get('paused', False):
        return
    
    # Initialize the first piece if needed
    if game_state['current_piece'] is None:
        spawn_piece(game_state, grid, sprite_manager)
        return
    
    # Update fall timer
    game_state['fall_timer'] += dt
    
    # Automatic falling
    if game_state['fall_timer'] >= game_state['fall_speed']:
        game_state['fall_timer'] = 0
        
        # Try to move piece down
        if not check_collision(game_state['current_piece'], grid, 0, 1):
            game_state['current_piece'].move(0, 1)
        else:
            # Piece can't move down - handle locking and effects
            handle_piece_lock()


def on_key_down(key):
    """Handle keyboard input"""
    # Start menu handling
    if game_state['menu'] == 'start':
        if key == keys.SPACE:
            # Start the game
            game_state['menu'] = 'playing'
            sound_manager.play_music(loop=True)
            return
        elif key == keys.M:
            # Toggle music
            sound_manager.toggle_music()
            return
    
    # Music toggle (works in any state)
    if key == keys.M:
        sound_manager.toggle_music()
        return
    
    # Pause handling
    if key == keys.P and not game_state['game_over'] and game_state['menu'] == 'playing':
        game_state['paused'] = not game_state.get('paused', False)
        if game_state['paused']:
            sound_manager.pause_music()
        else:
            sound_manager.unpause_music()
        return
    
    # Don't process other keys if paused
    if game_state.get('paused', False):
        return
    
    # Restart game if game over
    if game_state['game_over'] and key == keys.R:
        # Reset game state
        global grid
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        game_state['current_piece'] = None
        game_state['next_piece'] = None
        game_state['fall_timer'] = 0
        game_state['game_over'] = False
        game_state['paused'] = False
        game_state['menu'] = 'playing'
        game_state['score'] = 0
        game_state['level'] = 1
        game_state['lines_cleared'] = 0
        game_state['fall_speed'] = INITIAL_FALL_SPEED
        game_state['is_new_high_score'] = False
        sound_manager.play_music(loop=True)
        return
    
    if game_state['current_piece'] is None or game_state['game_over']:
        return
    
    current_piece = game_state['current_piece']
    
    # Move left
    if key == keys.LEFT:
        if not check_collision(current_piece, grid, -1, 0):
            current_piece.move(-1, 0)
            sound_manager.play_sound('move')
    
    # Move right
    elif key == keys.RIGHT:
        if not check_collision(current_piece, grid, 1, 0):
            current_piece.move(1, 0)
            sound_manager.play_sound('move')
    
    # Rotate
    elif key == keys.UP:
        # Save current state in case rotation fails
        old_blocks = [((dx, dy), block) for (dx, dy), block in current_piece.blocks]
        current_piece.rotate()
        
        # Check if rotation is valid
        if check_collision(current_piece, grid, 0, 0):
            # Try wall kicks
            wall_kick_offsets = [(-1, 0), (1, 0), (-2, 0), (2, 0), (0, -1)]
            kick_successful = False
            
            for dx, dy in wall_kick_offsets:
                if not check_collision(current_piece, grid, dx, dy):
                    current_piece.move(dx, dy)
                    kick_successful = True
                    break
            
            # If no wall kick worked, revert rotation
            if not kick_successful:
                current_piece.blocks = old_blocks
            else:
                sound_manager.play_sound('rotate')
        else:
            sound_manager.play_sound('rotate')
    
    # Soft drop (move down faster)
    elif key == keys.DOWN:
        if not check_collision(current_piece, grid, 0, 1):
            current_piece.move(0, 1)
            game_state['score'] += SCORE_SOFT_DROP  # 1 point per cell
    
    # Hard drop (instant placement)
    elif key == keys.SPACE:
        # Count cells dropped for scoring
        cells_dropped = 0
        
        # Move piece down until it collides
        while not check_collision(current_piece, grid, 0, 1):
            current_piece.move(0, 1)
            cells_dropped += 1
        
        # Add hard drop score (2 points per cell)
        game_state['score'] += cells_dropped * SCORE_HARD_DROP
        
        # Handle piece locking and all related effects
        handle_piece_lock()


# Run the game
pgzrun.go()
