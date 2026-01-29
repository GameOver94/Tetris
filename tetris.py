"""
HaHa Hausservice Haubenhofer Tetris Game
A promotional Tetris clone with office and bathroom furniture pieces

Built with Pygame Zero
"""

import pgzrun

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


def draw():
    """Main draw function - called by Pygame Zero every frame"""
    # Clear screen with background color
    screen.fill(BACKGROUND_COLOR)
    
    # Draw game title
    screen.draw.text(
        "HAHA HAUSSERVICE HAUBENHOFER",
        topleft=(50, 30),
        fontsize=36,
        color=UI_TEXT_COLOR
    )
    
    # Draw game grid background
    grid_rect = (GRID_X, GRID_Y, GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE)
    screen.draw.filled_rect(grid_rect, GRID_BACKGROUND)
    
    # Draw grid border
    screen.draw.rect(grid_rect, GRID_BORDER)
    
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
    
    # Draw UI panel labels
    screen.draw.text(
        "NEXT PIECE:",
        topleft=(950, 80),
        fontsize=24,
        color=UI_TEXT_COLOR
    )
    
    # Draw next piece box
    next_piece_box = (950, 120, 240, 240)
    screen.draw.filled_rect(next_piece_box, GRID_BACKGROUND)
    screen.draw.rect(next_piece_box, GRID_BORDER)
    
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
        "← → Move",
        "↑ Rotate",
        "↓ Soft Drop",
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


def update():
    """Main update function - called by Pygame Zero every frame"""
    # Game logic will be added in Phase 2
    pass


def on_key_down(key):
    """Handle keyboard input"""
    # Input handling will be added in Phase 2
    pass


# Run the game
pgzrun.go()
