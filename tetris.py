"""
HaHa Hausservice Haubenhofer Tetris Game
A promotional Tetris clone with office and bathroom furniture pieces

Built with Pygame Zero
"""

import pgzrun
from pygame import Rect
import random

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

# Grid configuration
BLOCK_SIZE = 48  # 48x48 pixels per block
GRID_WIDTH = 10  # 10 blocks wide
GRID_HEIGHT = 20  # 20 blocks tall
GRID_X = 400  # X position of game grid
GRID_Y = 0  # Y position of game grid

GRID_RECT = Rect(GRID_X, GRID_Y, GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE)
NEXT_PIECE_BOX = Rect(950, 120, 240, 240)

# Tetromino shapes (office and bathroom furniture themed)
SHAPES = {
    'I': [(0, 0), (1, 0), (2, 0), (3, 0)],  # Desk
    'O': [(0, 0), (1, 0), (0, 1), (1, 1)],  # Printer
    'T': [(0, 0), (1, 0), (2, 0), (1, 1)],  # Shower
    'L': [(0, 0), (0, 1), (0, 2), (1, 2)],  # Office Chair
    'J': [(1, 0), (1, 1), (1, 2), (0, 2)],  # Cabinet
    'S': [(1, 0), (2, 0), (0, 1), (1, 1)],  # Sink
    'Z': [(0, 0), (1, 0), (1, 1), (2, 1)]   # Toilet
}

# Colors for each piece type
PIECE_COLORS = {
    'I': (0, 255, 255),    # Cyan
    'O': (255, 255, 0),    # Yellow
    'T': (128, 0, 128),    # Purple
    'L': (255, 165, 0),    # Orange
    'J': (0, 0, 255),      # Blue
    'S': (0, 255, 0),      # Green
    'Z': (255, 0, 0)       # Red
}

# Game timing
FALL_SPEED = 0.5  # Seconds between automatic falls

# Game state
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
current_piece = None
next_piece = None
fall_timer = 0
game_over = False


class Piece:
    """Represents a Tetris piece (tetromino)"""
    
    def __init__(self, shape_type):
        """Initialize a piece with a given shape type"""
        self.shape_type = shape_type
        self.shape = SHAPES[shape_type].copy()
        self.color = PIECE_COLORS[shape_type]
        # Spawn at top center of grid
        self.x = GRID_WIDTH // 2 - 2
        self.y = 0
    
    def get_blocks(self):
        """Get the absolute positions of all blocks in this piece"""
        return [(self.x + dx, self.y + dy) for dx, dy in self.shape]
    
    def move(self, dx, dy):
        """Move the piece by the given offset"""
        self.x += dx
        self.y += dy
    
    def rotate(self):
        """Rotate the piece 90 degrees clockwise"""
        # Don't rotate O-piece (it's a square)
        if self.shape_type == 'O':
            return
        
        # Rotate each block around the origin
        # (x, y) -> (y, -x) for 90-degree clockwise rotation
        rotated = [(dy, -dx) for dx, dy in self.shape]
        
        # Normalize to keep top-left aligned
        min_x = min(x for x, y in rotated)
        min_y = min(y for x, y in rotated)
        self.shape = [(x - min_x, y - min_y) for x, y in rotated]


def check_collision(piece, dx=0, dy=0):
    """Check if the piece would collide with the grid or boundaries at the new position"""
    for bx, by in piece.get_blocks():
        new_x = bx + dx
        new_y = by + dy
        
        # Check boundaries
        if new_x < 0 or new_x >= GRID_WIDTH:
            return True
        if new_y >= GRID_HEIGHT:
            return True
        
        # Check collision with locked pieces (only if within grid)
        if new_y >= 0 and grid[new_y][new_x] != 0:
            return True
    
    return False


def lock_piece(piece):
    """Lock the current piece into the grid"""
    for bx, by in piece.get_blocks():
        if by >= 0:  # Only lock blocks that are visible
            grid[by][bx] = piece.shape_type


def spawn_piece():
    """Spawn a new piece"""
    global current_piece, next_piece, game_over, fall_timer
    
    if next_piece is None:
        # First piece - create both current and next
        current_piece = Piece(random.choice(list(SHAPES.keys())))
        next_piece = Piece(random.choice(list(SHAPES.keys())))
    else:
        # Use the next piece as current, generate new next
        current_piece = next_piece
        current_piece.x = GRID_WIDTH // 2 - 2
        current_piece.y = 0
        next_piece = Piece(random.choice(list(SHAPES.keys())))
        
        # Check for game over - if new piece collides immediately
        if check_collision(current_piece, 0, 0):
            game_over = True
    
    # Reset fall timer for consistent timing
    fall_timer = 0


def draw():
    """Main draw function - called by Pygame Zero every frame"""
    # Clear screen with background color
    screen.fill(BACKGROUND_COLOR)
    
    # Draw game title (rotated 90 degrees on left border)
    screen.draw.text(
        "HAHA HAUSSERVICE HAUBENHOFER",
        center=(40, HEIGHT // 2),
        fontsize=36,
        color=UI_TEXT_COLOR,
        angle=90
    )
    
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
            if grid[y][x] != 0:
                # Draw a filled block
                block_rect = Rect(
                    GRID_X + x * BLOCK_SIZE,
                    GRID_Y + y * BLOCK_SIZE,
                    BLOCK_SIZE,
                    BLOCK_SIZE
                )
                color = PIECE_COLORS[grid[y][x]]
                screen.draw.filled_rect(block_rect, color)
                screen.draw.rect(block_rect, GRID_BORDER)
    
    # Draw current falling piece
    if current_piece:
        for bx, by in current_piece.get_blocks():
            if by >= 0:  # Only draw blocks that are visible
                block_rect = Rect(
                    GRID_X + bx * BLOCK_SIZE,
                    GRID_Y + by * BLOCK_SIZE,
                    BLOCK_SIZE,
                    BLOCK_SIZE
                )
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
    if next_piece:
        # Calculate center position for next piece
        preview_offset_x = NEXT_PIECE_BOX.x + NEXT_PIECE_BOX.width // 2 - BLOCK_SIZE
        preview_offset_y = NEXT_PIECE_BOX.y + NEXT_PIECE_BOX.height // 2 - BLOCK_SIZE
        
        for dx, dy in next_piece.shape:
            block_rect = Rect(
                preview_offset_x + dx * BLOCK_SIZE,
                preview_offset_y + dy * BLOCK_SIZE,
                BLOCK_SIZE,
                BLOCK_SIZE
            )
            screen.draw.filled_rect(block_rect, next_piece.color)
            screen.draw.rect(block_rect, GRID_BORDER)
    
    # Draw score display
    screen.draw.text(
        "SCORE: 0",
        topleft=(950, 400),
        fontsize=28,
        color=UI_TEXT_COLOR
    )
    
    screen.draw.text(
        "LEVEL: 1",
        topleft=(950, 450),
        fontsize=28,
        color=UI_TEXT_COLOR
    )
    
    screen.draw.text(
        "LINES: 0",
        topleft=(950, 500),
        fontsize=28,
        color=UI_TEXT_COLOR
    )
    
    # Draw controls
    screen.draw.text(
        "CONTROLS:",
        topleft=(950, 600),
        fontsize=24,
        color=UI_TEXT_COLOR
    )
    
    controls_text = [
        "LEFT/RIGHT Move",
        "UP Rotate",
        "DOWN Soft Drop",
        "SPACE Hard Drop"
    ]
    
    y_offset = 640
    for control in controls_text:
        screen.draw.text(
            control,
            topleft=(950, y_offset),
            fontsize=20,
            color=UI_TEXT_COLOR
        )
        y_offset += 30
    
    # Draw game over message if game is over
    if game_over:
        # Draw semi-transparent overlay
        overlay_rect = Rect(GRID_X, GRID_Y + GRID_HEIGHT * BLOCK_SIZE // 2 - 100, 
                           GRID_WIDTH * BLOCK_SIZE, 200)
        screen.draw.filled_rect(overlay_rect, (0, 0, 0, 180))
        
        screen.draw.text(
            "GAME OVER",
            center=(GRID_X + GRID_WIDTH * BLOCK_SIZE // 2, 
                   GRID_Y + GRID_HEIGHT * BLOCK_SIZE // 2 - 30),
            fontsize=48,
            color=(255, 255, 255)
        )
        
        screen.draw.text(
            "Press R to Restart",
            center=(GRID_X + GRID_WIDTH * BLOCK_SIZE // 2, 
                   GRID_Y + GRID_HEIGHT * BLOCK_SIZE // 2 + 30),
            fontsize=24,
            color=(255, 255, 255)
        )


def update(dt):
    """Main update function - called by Pygame Zero every frame"""
    global fall_timer, current_piece
    
    # Don't update if game is over
    if game_over:
        return
    
    # Initialize the first piece if needed
    if current_piece is None:
        spawn_piece()
        return
    
    # Update fall timer
    fall_timer += dt
    
    # Automatic falling
    if fall_timer >= FALL_SPEED:
        fall_timer = 0
        
        # Try to move piece down
        if not check_collision(current_piece, 0, 1):
            current_piece.move(0, 1)
        else:
            # Piece can't move down - lock it and spawn new piece
            lock_piece(current_piece)
            spawn_piece()


def on_key_down(key):
    """Handle keyboard input"""
    global current_piece, grid, game_over, fall_timer, next_piece
    
    # Restart game if game over
    if game_over and key == keys.R:
        # Reset game state
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        current_piece = None
        next_piece = None
        fall_timer = 0
        game_over = False
        return
    
    if current_piece is None or game_over:
        return
    
    # Move left
    if key == keys.LEFT:
        if not check_collision(current_piece, -1, 0):
            current_piece.move(-1, 0)
    
    # Move right
    elif key == keys.RIGHT:
        if not check_collision(current_piece, 1, 0):
            current_piece.move(1, 0)
    
    # Rotate
    elif key == keys.UP:
        # Save current state in case rotation fails
        old_shape = current_piece.shape.copy()
        current_piece.rotate()
        
        # Check if rotation is valid
        if check_collision(current_piece, 0, 0):
            # Try wall kicks
            wall_kick_offsets = [(-1, 0), (1, 0), (-2, 0), (2, 0), (0, -1)]
            kick_successful = False
            
            for dx, dy in wall_kick_offsets:
                if not check_collision(current_piece, dx, dy):
                    current_piece.move(dx, dy)
                    kick_successful = True
                    break
            
            # If no wall kick worked, revert rotation
            if not kick_successful:
                current_piece.shape = old_shape
    
    # Soft drop (move down faster)
    elif key == keys.DOWN:
        if not check_collision(current_piece, 0, 1):
            current_piece.move(0, 1)
    
    # Hard drop (instant placement)
    elif key == keys.SPACE:
        # Move piece down until it collides
        while not check_collision(current_piece, 0, 1):
            current_piece.move(0, 1)
        
        # Lock the piece and spawn new one
        lock_piece(current_piece)
        spawn_piece()


# Run the game
pgzrun.go()
