# Hausservice Haubentaucher - Tetris Game Design Document

## 1. Game Overview

**Title:** HaHa Hausservice Haubentaucher Tetris  
**Genre:** Puzzle Game (Tetris Clone)  
**Platform:** Desktop (Pygame Zero)  
**Target Audience:** Potential customers, promotional purposes  
**Theme:** Office and Bathroom furniture instead of classic Tetris blocks

## 2. Game Concept

A promotional Tetris clone where players arrange falling cleaning tools and household items instead of traditional tetrominos. The game maintains classic Tetris mechanics while incorporating the HaHa Hausservice Haubentaucher brand through themed sprites representing their cleaning and house service offerings.

## 3. Core Features

### 3.1 Essential Features
- **Classic Tetris Gameplay:** Line clearing, gravity, rotation, and movement
- **Office and Bathroom-themed Sprites:** Desks, monitors, office chairs, printers, showers, toilets, sinks
- **Score System:** Points for clearing lines and placing pieces
- **Progressive Difficulty:** Increasing fall speed as game progresses
- **Game Over Detection:** When pieces reach the top of the playfield
- **Next Piece Preview:** Shows upcoming cleaning tool/item
- **Brand Integration:** HaHa Hausservice Haubentaucher logo and brand colors (blue & green)

### 3.2 Optional Features (Future Enhancements)
- High score persistence
- Pause functionality
- Sound effects and background music
- Special effects for line clears
- Multiple difficulty levels
- Level progression system

## 4. Game Loop Structure

### 4.1 Main Game Loop
```
INITIALIZE:
  - Load sprites
  - Set up game grid (10x20)
  - Initialize score, level, and speed
  - Generate first piece and next piece

GAME LOOP:
  UPDATE:
    - Handle user input (move left/right, rotate, soft drop, hard drop)
    - Apply gravity (move piece down based on timer)
    - Check for collisions
    - Lock piece if it can't move down
    - Clear completed lines
    - Update score and level
    - Check game over condition
    - Spawn next piece

  DRAW:
    - Clear screen
    - Draw background
    - Draw game grid with locked pieces
    - Draw current falling piece
    - Draw UI elements (score, level, next piece, logo)
    - Update display

GAME OVER:
  - Display final score
  - Show restart option
```

### 4.2 Game States
- **MENU:** Initial screen (logo)
- **PLAYING:** Active gameplay
- **PAUSED:** Game paused (optional)
- **GAME_OVER:** End screen with score

## 5. Sprite Design

### 5.1 Office and Bathroom Furniture Pieces (Tetromino Equivalents)

All pieces will be based on the 7 classic tetromino shapes but represented as offes and bathroom items.
We are using a 2.5D pixel art style:

#### Piece 1: I-Piece (4x1) - "The Desk"
- **Visual:** A office desk with cabinet and drawer
- **Size:** 4 blocks long
- **Rotations:** Horizontal/Vertical
- **Dimensions:** 192x48 px

#### Piece 2: O-Piece (2x2) - "The Printer"
- **Visual:** A large photo copier
- **Size:** 2x2 blocks
- **Rotations:** None (square)
- **Dimensions:** 96x96 px

#### Piece 3: T-Piece - "The Shower"
- **Visual:** A shower or shower head
- **Size:** T-shaped
- **Rotations:** 4 orientations
- **Dimensions:** 144x96 px

#### Piece 4: L-Piece - "The Office Chair"
- **Visual:** A office chair
- **Size:** L-shaped
- **Rotations:** 4 orientations
- **Dimensions:** 96x144 px

#### Piece 5: J-Piece - "The Cabinet"
- **Visual:** A Arangement of Shelfs and filing Cabinets
- **Size:** J-shaped
- **Rotations:** 4 orientations
- **Dimensions:** 96x144 px

#### Piece 6: S-Piece - "The Sink"
- **Visual:** A Sink with its plumbing
- **Size:** S-shaped
- **Rotations:** 2 orientations
- **Dimensions:** 144x96 px

#### Piece 7: Z-Piece - "The Toilet"
- **Visual:** A clasic toilet with water tank
- **Size:** Z-shaped
- **Rotations:** 2 orientations
- **Dimensions:** 144x96 px

### 5.2 Sprite Specifications

**Block Size:** 48x48 pixels  
**Grid Dimensions:** 10 blocks wide × 20 blocks tall  
**Playfield Size:** 480x960 pixels  
**Sprite Format:** PNG with transparency  
**Color Palette:** Brand colors (blue #0066CC, green #009933) + item-appropriate colors

### 5.3 Sprite File Structure
```
images/
  ├── pieces/
  │   ├── desk.png        (I-piece)
  │   ├── priner.png      (O-piece)
  │   ├── shower.png      (T-piece)
  │   ├── chair.png       (L-piece)
  │   ├── cabinet.png     (J-piece)
  │   ├── sink.png        (S-piece)
  │   └── toilet.png      (Z-piece)
  ├── ui/
  │   ├── logo.png          (HaHa Hausservice Haubentaucher logo)
  │   ├── background.png    (Game background)
  └── effects/
      └── line_clear.png    (Optional: line clear effect)
```

## 6. UI Layout

### 6.1 Screen Layout (1280x960 resolution)

```
┌────────────────────────────────────────────────────────────────────────┐
│  HAHA HAUSSERVICE HAUBENTAUCHER                        [LOGO]          │
├───────────────────┬─────────────────────────┬──────────────────────────┤
│                   │                         │  NEXT PIECE:             │
│                   │                         │  ┌──────────────┐        │
│                   │                         │  │              │        │
│                   │                         │  │    [img]     │        │
│  (Empty)          │     GAME GRID           │  │              │        │
│                   │     (480x960)           │  └──────────────┘        │
│  Spacing          │                         │                          │
│                   │                         │  SCORE: 0000             │
│                   │                         │  LEVEL: 1                │
│                   │                         │  LINES: 0                │
│                   │                         │                          │
│                   │                         │  CONTROLS:               │
│                   │                         │  ← → Move                │
│                   │                         │  ↑ Rotate                │
│                   │                         │  ↓ Soft Drop             │
│                   │                         │  SPACE Hard Drop         │
└───────────────────┴─────────────────────────┴──────────────────────────┘
```

### 6.2 UI Element Positions (Pygame Zero coordinates)

- **Screen Size:** 1280x960 pixels
- **Game Grid:** x=400, y=0, size=480x960
- **Logo:** x=50, y=30
- **Next Piece Box:** x=950, y=100, size=240x240
- **Score Display:** x=950, y=400
- **Level Display:** x=950, y=450
- **Lines Display:** x=950, y=500
- **Controls Info:** x=950, y=600

### 6.3 Color Scheme

**Primary Colors (Brand - from logo):**
- Background: #F5F5F5 (Light gray)
- UI Text: #2C3E50 (Dark navy/charcoal - from logo banner)
- Primary Accent: #0066CC (Bright blue - from "HaHa" text and houses)
- Secondary Accent: #009933 (Green - from "HAUSSERVICE" text)
- Light Blue Accent: #33CCFF (Cyan - from logo accents)

**Grid:**
- Border: #CCCCCC (Light gray)
- Background: #FFFFFF (White)

## 7. Game Mechanics

### 7.1 Controls
- **Arrow Left:** Move piece left
- **Arrow Right:** Move piece right
- **Arrow Up:** Rotate piece clockwise
- **Arrow Down:** Soft drop (faster fall)
- **Spacebar:** Hard drop (instant placement)
- **P:** Pause (optional)
- **R:** Restart after game over

### 7.2 Scoring System
- **Single Line:** 100 points × level
- **Double Lines:** 300 points × level
- **Triple Lines:** 500 points × level
- **Tetris (4 lines):** 800 points × level
- **Soft Drop:** 1 point per cell
- **Hard Drop:** 2 points per cell

### 7.3 Level Progression
- Start at Level 1
- Every 10 lines cleared = Level up
- Each level increases fall speed by 10%
- Maximum level: 15

### 7.4 Game Rules
- Grid size: 10 columns × 20 rows
- Pieces spawn at top center (column 3-6)
- Game over when new piece cannot spawn
- Lines clear when completely filled
- Standard rotation system (SRS - Super Rotation System simplified)
- Wall kicks for rotation near boundaries

## 8. Technical Specifications

### 8.1 Technology Stack
- **Framework:** Pygame Zero
- **Language:** Python 3.12+
- **Graphics:** PNG sprites
- **Configuration:** Simple Python variables

### 8.2 File Structure
```
tetris/
├── DESIGN.md              (this file)
├── README.md              (project readme)
├── requirements.txt       (dependencies)
├── game_logic.py          (core game mechanics - no display dependencies)
├── tetris.py              (Pygame Zero display and main game loop)
├── test_tetris.py         (comprehensive test suite)
├── images/                (sprite directory)
│   ├── pieces/
│   ├── ui/
│   └── effects/
└── sounds/                (optional, future)
    ├── music/
    └── effects/
```

### 8.3 Code Architecture

**Separation of Concerns:**

The codebase is organized into distinct modules for better testability and maintainability:

1. **game_logic.py** - Pure game mechanics
   - Piece class (movement, rotation)
   - Collision detection
   - Line clearing and scoring
   - Level progression
   - No Pygame Zero dependencies
   - Fully testable in headless mode

2. **tetris.py** - Display and game loop
   - Pygame Zero integration
   - Drawing functions
   - Input handling
   - Main game loop (update/draw)
   - Imports game logic from game_logic.py

3. **test_tetris.py** - Test suite
   - 30 comprehensive tests
   - Tests game_logic module
   - Runs without display

**Core Components (game_logic.py):**
1. **Constants:** Grid size, shapes, colors, scoring rules
2. **Piece Class:** Represents furniture pieces with shape, color, position, rotation
3. **Game State:** Current piece, grid, score, level, next piece
4. **Input Handlers:** Keyboard controls
5. **Update Logic:** Movement, collision, line clearing, spawning
6. **Draw Functions:** Render grid, pieces, UI elements
7. **Helper Functions:** Rotation, collision detection, line clearing

**Key Functions:**
- `draw()` - Main render function (Pygame Zero convention)
- `update()` - Main game loop function (Pygame Zero convention)
- `on_key_down(key)` - Handle keyboard input (Pygame Zero convention)
- `check_collision()` - Detect piece collisions
- `rotate_piece()` - Handle piece rotation
- `lock_piece()` - Place piece on grid
- `clear_lines()` - Remove completed lines
- `spawn_piece()` - Create new falling piece

### 8.4 Data Structures

**Piece Shapes (using coordinates):**
```python
SHAPES = {
    'I': [(0,0), (1,0), (2,0), (3,0)],  # Squeegee
    'O': [(0,0), (1,0), (0,1), (1,1)],  # Washing Machine
    'T': [(0,0), (1,0), (2,0), (1,1)],  # Mop
    'L': [(0,0), (0,1), (0,2), (1,2)],  # Vacuum
    'J': [(1,0), (1,1), (1,2), (0,2)],  # Toilet
    'S': [(1,0), (2,0), (0,1), (1,1)],  # Hose
    'Z': [(0,0), (1,0), (1,1), (2,1)]   # Ladder
}
```

**Grid:**
- 2D list (20 rows × 10 columns)
- 0 = empty cell
- 1-7 = locked piece type

## 9. Development Roadmap

### Phase 1: Core Setup ✓ (Current Phase)
- [x] Create design document
- [x] Set up project structure
- [x] Install Pygame Zero
- [x] Create basic window

### Phase 2: Game Logic ✓ (Completed)
- [x] Implement grid system
- [x] Create piece class with basic shapes
- [x] Implement piece movement (left, right, down)
- [x] Add collision detection
- [x] Implement piece rotation
- [x] Add piece locking to grid

### Phase 3: Line Clearing & Scoring ✓ (Completed)
- [x] Implement line detection
- [x] Add line clearing animation
- [x] Create scoring system
- [x] Add level progression
- [x] Implement game over detection

### Phase 4: UI & Graphics ✓ (Completed)
- [x] Create placeholder sprites (colored blocks)
- [x] Design cleaning furniture sprites
- [x] Implement sprite rendering (48x48 pixel blocks)
- [x] Add UI elements (score, level, next piece)
- [x] Add HaHa Hausservice Haubentaucher logo
- [x] Polish visual appearance with brand colors

### Phase 5: Polish & Testing ✓ (Completed)
- [x] Add controls display
- [x] Implement restart functionality
- [x] Test all game mechanics
- [x] Balance difficulty curve
- [x] Bug fixes and optimization

### Phase 6: Optional Enhancements ✓ (Completed)
- [x] Add sound effects
- [x] Add background music
- [x] Implement pause menu
- [x] Add high score persistence
- [x] Create start menu
- [x] Add special effects (line clear animations)

## 10. Success Criteria

The game will be considered complete when:
1. All 7 furniture pieces can spawn, move, rotate, and lock
2. Lines clear correctly and score updates
3. Game over triggers when pieces reach the top
4. Level progression works and speed increases
5. UI displays all necessary information
6. Cleaning tool sprites are recognizable and themed appropriately
7. HaHa Hausservice Haubentaucher branding is visible and prominent
8. Brand colors (blue #0066CC, green #009933) are used consistently
9. No major bugs or crashes
10. Code is clean and maintainable

## 11. Notes & Considerations

### 11.1 Brand Integration
- Ensure HaHa Hausservice Haubentaucher logo (assets/logo.jpeg) is prominently displayed
- Use brand colors consistently: Blue (#0066CC) and Green (#009933) from logo
- Cleaning tool choices reflect their house cleaning and service offerings
- Keep aesthetic professional yet playful, matching the friendly mascot style
- Logo features Haubentaucher (crested grebe) mascot with cleaning tools

### 11.2 Simplicity Priority
- Pygame Zero chosen for rapid development
- 48x48 pixel blocks provide good visibility without being too large
- Start with basic graphics (can upgrade later)
- Focus on core gameplay first
- Add polish incrementally

---

**Document Version:** 3.0  
**Last Updated:** 2026-01-29  
**Status:** Phase 6 Complete - All optional enhancements implemented
