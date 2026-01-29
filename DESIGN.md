# Hausservice Haubentaucher - Tetris Game Design Document

## 1. Game Overview

**Title:** Hausservice Haubentaucher Tetris  
**Genre:** Puzzle Game (Tetris Clone)  
**Platform:** Desktop (Pygame Zero)  
**Target Audience:** Potential customers, promotional purposes  
**Theme:** Office and bathroom furniture instead of classic Tetris blocks

## 2. Game Concept

A promotional Tetris clone where players arrange falling office and bathroom furniture pieces instead of traditional tetrominos. The game maintains classic Tetris mechanics while incorporating the Hausservice Haubentaucher brand through themed sprites representing their product offerings.

## 3. Core Features

### 3.1 Essential Features
- **Classic Tetris Gameplay:** Line clearing, gravity, rotation, and movement
- **Furniture-themed Sprites:** Office chairs, desks, showers, toilets, cabinets, etc.
- **Score System:** Points for clearing lines and placing pieces
- **Progressive Difficulty:** Increasing fall speed as game progresses
- **Game Over Detection:** When pieces reach the top of the playfield
- **Next Piece Preview:** Shows upcoming furniture piece
- **Brand Integration:** Hausservice Haubentaucher logo and colors

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
- **MENU:** Initial screen (can be simple or skip to game)
- **PLAYING:** Active gameplay
- **PAUSED:** Game paused (optional)
- **GAME_OVER:** End screen with score

## 5. Sprite Design

### 5.1 Furniture Pieces (Tetromino Equivalents)

All pieces will be based on the 7 classic tetromino shapes but represented as furniture:

#### Piece 1: I-Piece (4x1) - "The Desk"
- **Visual:** Long office desk
- **Color:** Brown wood texture
- **Size:** 4 blocks long
- **Rotations:** Horizontal/Vertical

#### Piece 2: O-Piece (2x2) - "The Cabinet"
- **Visual:** Square filing cabinet
- **Color:** Gray metal
- **Size:** 2x2 blocks
- **Rotations:** None (square)

#### Piece 3: T-Piece - "The Office Chair"
- **Visual:** Office chair (top view showing base and seat)
- **Color:** Black with silver wheels
- **Size:** T-shaped
- **Rotations:** 4 orientations

#### Piece 4: L-Piece - "The Shower Head"
- **Visual:** Shower fixture with pipe
- **Color:** Chrome silver/blue water
- **Size:** L-shaped
- **Rotations:** 4 orientations

#### Piece 5: J-Piece - "The Toilet"
- **Visual:** Toilet (side view)
- **Color:** White ceramic
- **Size:** J-shaped
- **Rotations:** 4 orientations

#### Piece 6: S-Piece - "The Sink"
- **Visual:** Bathroom sink with faucet
- **Color:** White/chrome
- **Size:** S-shaped
- **Rotations:** 2 orientations

#### Piece 7: Z-Piece - "The Bathtub"
- **Visual:** Bathtub (top view)
- **Color:** White/light blue
- **Size:** Z-shaped
- **Rotations:** 2 orientations

### 5.2 Sprite Specifications

**Block Size:** 30x30 pixels  
**Grid Dimensions:** 10 blocks wide × 20 blocks tall  
**Playfield Size:** 300x600 pixels  
**Sprite Format:** PNG with transparency  
**Color Palette:** Brand colors + furniture-appropriate colors

### 5.3 Sprite File Structure
```
images/
  ├── pieces/
  │   ├── desk.png          (I-piece)
  │   ├── cabinet.png       (O-piece)
  │   ├── chair.png         (T-piece)
  │   ├── shower.png        (L-piece)
  │   ├── toilet.png        (J-piece)
  │   ├── sink.png          (S-piece)
  │   └── bathtub.png       (Z-piece)
  ├── ui/
  │   ├── logo.png          (Hausservice Haubentaucher logo)
  │   ├── background.png    (Game background)
  │   └── block_empty.png   (Grid outline)
  └── effects/
      └── line_clear.png    (Optional: line clear effect)
```

## 6. UI Layout

### 6.1 Screen Layout (800x600 resolution)

```
┌─────────────────────────────────────────────────────────────┐
│  HAUSSERVICE HAUBENTAUCHER                    [LOGO]         │
├─────────────────┬─────────────────────┬─────────────────────┤
│                 │                     │  NEXT PIECE:        │
│                 │                     │  ┌─────────┐        │
│                 │                     │  │         │        │
│  (Empty)        │    GAME GRID        │  │  [img]  │        │
│                 │    (300x600)        │  │         │        │
│  Spacing        │                     │  └─────────┘        │
│                 │                     │                     │
│                 │                     │  SCORE: 0000        │
│                 │                     │  LEVEL: 1           │
│                 │                     │  LINES: 0           │
│                 │                     │                     │
│                 │                     │  CONTROLS:          │
│                 │                     │  ← → Move           │
│                 │                     │  ↑ Rotate           │
│                 │                     │  ↓ Soft Drop        │
│                 │                     │  SPACE Hard Drop    │
└─────────────────┴─────────────────────┴─────────────────────┘
```

### 6.2 UI Element Positions (Pygame Zero coordinates)

- **Screen Size:** 800x600 pixels
- **Game Grid:** x=250, y=0, size=300x600
- **Logo:** x=50, y=30
- **Next Piece Box:** x=600, y=100
- **Score Display:** x=600, y=280
- **Level Display:** x=600, y=320
- **Lines Display:** x=600, y=360
- **Controls Info:** x=600, y=420

### 6.3 Color Scheme

**Primary Colors (Brand):**
- Background: #F5F5F5 (Light gray)
- UI Text: #333333 (Dark gray)
- Accent: #0066CC (Blue - adjust to match Hausservice Haubentaucher branding)

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
- **Language:** Python 3.8+
- **Graphics:** PNG sprites
- **Configuration:** Simple Python variables

### 8.2 File Structure
```
tetris/
├── DESIGN.md              (this file)
├── README.md              (project readme)
├── requirements.txt       (dependencies)
├── tetris.py             (main game file)
├── images/               (sprite directory)
│   ├── pieces/
│   ├── ui/
│   └── effects/
└── sounds/               (optional, future)
    ├── music/
    └── effects/
```

### 8.3 Code Structure (tetris.py)

**Core Components:**
1. **Constants:** Grid size, colors, block size, speeds
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
    'I': [(0,0), (1,0), (2,0), (3,0)],  # Desk
    'O': [(0,0), (1,0), (0,1), (1,1)],  # Cabinet
    'T': [(0,0), (1,0), (2,0), (1,1)],  # Chair
    'L': [(0,0), (0,1), (0,2), (1,2)],  # Shower
    'J': [(1,0), (1,1), (1,2), (0,2)],  # Toilet
    'S': [(1,0), (2,0), (0,1), (1,1)],  # Sink
    'Z': [(0,0), (1,0), (1,1), (2,1)]   # Bathtub
}
```

**Grid:**
- 2D list (20 rows × 10 columns)
- 0 = empty cell
- 1-7 = locked piece type

## 9. Development Roadmap

### Phase 1: Core Setup ✓ (Current Phase)
- [x] Create design document
- [ ] Set up project structure
- [ ] Install Pygame Zero
- [ ] Create basic window

### Phase 2: Game Logic
- [ ] Implement grid system
- [ ] Create piece class with basic shapes
- [ ] Implement piece movement (left, right, down)
- [ ] Add collision detection
- [ ] Implement piece rotation
- [ ] Add piece locking to grid

### Phase 3: Line Clearing & Scoring
- [ ] Implement line detection
- [ ] Add line clearing animation
- [ ] Create scoring system
- [ ] Add level progression
- [ ] Implement game over detection

### Phase 4: UI & Graphics
- [ ] Create placeholder sprites (colored blocks)
- [ ] Design furniture sprites
- [ ] Implement sprite rendering
- [ ] Add UI elements (score, level, next piece)
- [ ] Add Hausservice Haubentaucher logo
- [ ] Polish visual appearance

### Phase 5: Polish & Testing
- [ ] Add controls display
- [ ] Implement restart functionality
- [ ] Test all game mechanics
- [ ] Balance difficulty curve
- [ ] Bug fixes and optimization

### Phase 6: Optional Enhancements
- [ ] Add sound effects
- [ ] Add background music
- [ ] Implement pause menu
- [ ] Add high score persistence
- [ ] Create start menu
- [ ] Add special effects

## 10. Success Criteria

The game will be considered complete when:
1. All 7 furniture pieces can spawn, move, rotate, and lock
2. Lines clear correctly and score updates
3. Game over triggers when pieces reach the top
4. Level progression works and speed increases
5. UI displays all necessary information
6. Furniture sprites are recognizable and themed
7. Hausservice Haubentaucher branding is visible
8. Game is playable and fun
9. No major bugs or crashes
10. Code is clean and maintainable

## 11. Notes & Considerations

### 11.1 Brand Integration
- Ensure Hausservice Haubentaucher logo is prominently displayed
- Use brand colors if specified
- Furniture choices reflect their service offerings
- Keep aesthetic professional yet playful

### 11.2 Simplicity Priority
- Pygame Zero chosen for rapid development
- Start with basic graphics (can upgrade later)
- Focus on core gameplay first
- Add polish incrementally

### 11.3 Future Possibilities
- Web version using Pygame Zero to HTML export
- Mobile responsive design
- Multiplayer/competitive mode
- Custom furniture piece creator
- Integration with company website

---

**Document Version:** 1.0  
**Last Updated:** 2026-01-29  
**Status:** Planning Phase
