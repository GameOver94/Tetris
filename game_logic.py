"""
Game logic module for HaHa Hausservice Haubenhofer Tetris Game
Contains all game mechanics without display dependencies
"""

import random
from sprite_manager import Block

# Grid configuration
GRID_WIDTH = 10  # 10 blocks wide
GRID_HEIGHT = 20  # 20 blocks tall

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
INITIAL_FALL_SPEED = 0.5  # Initial seconds between automatic falls
SPEED_MULTIPLIER = 0.9  # Speed multiplier per level (10% faster)

# Scoring constants
SCORE_SINGLE = 100
SCORE_DOUBLE = 300
SCORE_TRIPLE = 500
SCORE_TETRIS = 800
SCORE_SOFT_DROP = 1
SCORE_HARD_DROP = 2


class Piece:
    """Represents a Tetris piece (tetromino) with sprite-aware blocks"""
    
    def __init__(self, shape_type, sprite_manager=None):
        """
        Initialize a piece with a given shape type.
        
        Args:
            shape_type: The type of piece ('I', 'O', 'T', etc.)
            sprite_manager: Optional sprite manager to create blocks with sprites
        """
        self.shape_type = shape_type
        self.color = PIECE_COLORS[shape_type]
        
        # Spawn at top center of grid
        self.x = GRID_WIDTH // 2 - 2
        self.y = 0
        
        # Create blocks with sprite information
        # blocks is a list of ((dx, dy), Block) tuples
        # where (dx, dy) is a tuple for the position relative to piece origin
        # and Block contains the sprite information
        self.blocks = []
        for dx, dy in SHAPES[shape_type]:
            if sprite_manager:
                block = sprite_manager.create_block(shape_type, dx, dy)
            else:
                block = Block(shape_type, dx, dy, None)
            self.blocks.append(((dx, dy), block))
    
    @property
    def shape(self):
        """Get the shape coordinates (for backward compatibility)"""
        return [pos for pos, block in self.blocks]
    
    def get_blocks(self):
        """Get the absolute positions of all blocks in this piece"""
        return [(self.x + dx, self.y + dy) for (dx, dy), block in self.blocks]
    
    def get_block_at_position(self, dx, dy):
        """Get the Block object at a specific relative position"""
        for (pos_x, pos_y), block in self.blocks:
            if pos_x == dx and pos_y == dy:
                return block
        return None
    
    def move(self, dx, dy):
        """Move the piece by the given offset"""
        self.x += dx
        self.y += dy
    
    def rotate(self):
        """
        Rotate the piece 90 degrees clockwise.
        Blocks maintain their sprite information through rotation.
        """
        # Don't rotate O-piece (it's a square)
        if self.shape_type == 'O':
            return
        
        # Rotate each block position around the origin
        # (x, y) -> (y, -x) for 90-degree clockwise rotation
        rotated_blocks = []
        for (dx, dy), block in self.blocks:
            new_dx = dy
            new_dy = -dx
            rotated_blocks.append(((new_dx, new_dy), block))
        
        # Normalize to keep top-left aligned
        min_x = min(dx for (dx, dy), block in rotated_blocks)
        min_y = min(dy for (dx, dy), block in rotated_blocks)
        
        self.blocks = [
            ((dx - min_x, dy - min_y), block) 
            for (dx, dy), block in rotated_blocks
        ]


def check_collision(piece, grid, dx=0, dy=0):
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


def lock_piece(piece, grid):
    """
    Lock the current piece into the grid.
    Stores Block objects to preserve sprite information.
    """
    for (dx, dy), block in piece.blocks:
        bx = piece.x + dx
        by = piece.y + dy
        if by >= 0:  # Only lock blocks that are visible
            grid[by][bx] = block


def check_lines(grid):
    """Check for completed lines and return a list of line indices to clear"""
    lines_to_clear = []
    
    # Check each row from bottom to top
    for y in range(GRID_HEIGHT):
        if all(grid[y][x] != 0 for x in range(GRID_WIDTH)):
            lines_to_clear.append(y)
    
    return lines_to_clear


def clear_lines(lines_to_clear, grid, game_state):
    """Clear completed lines and move rows down
    
    Args:
        lines_to_clear: List of line indices to clear
        grid: The game grid
        game_state: Dictionary containing score, level, lines_cleared, fall_speed
    """
    if not lines_to_clear:
        return
    
    # Sort lines in descending order (bottom to top, highest index first)
    # This ensures we delete from bottom to top so indices don't shift
    lines_to_clear.sort(reverse=True)
    
    # Remove completed lines from bottom to top
    for y in lines_to_clear:
        del grid[y]
    
    # Add empty lines at the top for each cleared line
    for _ in range(len(lines_to_clear)):
        grid.insert(0, [0 for _ in range(GRID_WIDTH)])
    
    # Update lines cleared count
    num_lines = len(lines_to_clear)
    game_state['lines_cleared'] += num_lines
    
    # Calculate score based on number of lines cleared (1-4 lines standard in Tetris)
    if num_lines == 1:
        game_state['score'] += SCORE_SINGLE * game_state['level']
    elif num_lines == 2:
        game_state['score'] += SCORE_DOUBLE * game_state['level']
    elif num_lines == 3:
        game_state['score'] += SCORE_TRIPLE * game_state['level']
    elif num_lines >= 4:  # 4 or more lines (Tetris)
        game_state['score'] += SCORE_TETRIS * game_state['level']
    
    # Level up every 10 lines
    new_level = (game_state['lines_cleared'] // 10) + 1
    if new_level > game_state['level'] and new_level <= 15:  # Max level 15
        game_state['level'] = new_level
        # Increase fall speed by 10% each level
        game_state['fall_speed'] = INITIAL_FALL_SPEED * (SPEED_MULTIPLIER ** (game_state['level'] - 1))


def spawn_piece(game_state, grid, sprite_manager=None):
    """Spawn a new piece
    
    Args:
        game_state: Dictionary containing current_piece, next_piece, game_over, fall_timer
        grid: The game grid
        sprite_manager: Optional sprite manager to create pieces with sprites
    """
    if game_state['next_piece'] is None:
        # First piece - create both current and next
        game_state['current_piece'] = Piece(random.choice(list(SHAPES.keys())), sprite_manager)
        game_state['next_piece'] = Piece(random.choice(list(SHAPES.keys())), sprite_manager)
    else:
        # Use the next piece as current, generate new next
        game_state['current_piece'] = game_state['next_piece']
        game_state['current_piece'].x = GRID_WIDTH // 2 - 2
        game_state['current_piece'].y = 0
        game_state['next_piece'] = Piece(random.choice(list(SHAPES.keys())), sprite_manager)
        
        # Check for game over - if new piece collides immediately
        if check_collision(game_state['current_piece'], grid, 0, 0):
            game_state['game_over'] = True
    
    # Reset fall timer for consistent timing
    game_state['fall_timer'] = 0
