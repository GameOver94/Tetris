# Hausservice Haubenhofer - Tetris Game Design Document

## 1. Game Overview

**Title:** HaHa Hausservice Haubenhofer Tetris  
**Genre:** Puzzle Game (Tetris Clone)  
**Platform:** Desktop (Pygame Zero)  
**Target Audience:** Potential customers, promotional purposes  
**Theme:** Cleaning tools and household items instead of classic Tetris blocks

## 2. Game Concept

A promotional Tetris clone where players arrange falling cleaning tools and household items instead of traditional tetrominos. The game maintains classic Tetris mechanics while incorporating the HaHa Hausservice Haubenhofer brand through themed sprites representing their cleaning and house service offerings.

## 3. Core Features

### 3.1 Essential Features
- **Classic Tetris Gameplay:** Line clearing, gravity, rotation, and movement
- **Cleaning-themed Sprites:** Mops, vacuums, washing machines, toilets, squeegees, hoses, ladders
- **Score System:** Points for clearing lines and placing pieces
- **Progressive Difficulty:** Increasing fall speed as game progresses
- **Game Over Detection:** When pieces reach the top of the playfield
- **Next Piece Preview:** Shows upcoming cleaning tool/item
- **Brand Integration:** HaHa Hausservice Haubenhofer logo and brand colors (blue & green)

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

### 5.1 Cleaning Tool Pieces (Tetromino Equivalents)

All pieces will be based on the 7 classic tetromino shapes but represented as cleaning tools and household items:

#### Piece 1: I-Piece (4x1) - "The Squeegee"
- **Visual:** Window cleaning squeegee or cleaning rod
- **Color:** Blue handle with silver blade
- **Size:** 4 blocks long
- **Rotations:** Horizontal/Vertical
- **Rationale:** Long, straight tool perfect for the I-shape

#### Piece 2: O-Piece (2x2) - "The Washing Machine"
- **Visual:** Front-loading washing machine (front view)
- **Color:** White with blue/green accent (brand colors)
- **Size:** 2x2 blocks
- **Rotations:** None (square)
- **Rationale:** Square appliance fits the O-shape perfectly

#### Piece 3: T-Piece - "The Mop"
- **Visual:** Mop with handle and mop head (side view)
- **Color:** Blue handle with white/gray mop head
- **Size:** T-shaped
- **Rotations:** 4 orientations
- **Rationale:** T-shape naturally represents mop handle + head

#### Piece 4: L-Piece - "The Vacuum Cleaner"
- **Visual:** Upright vacuum cleaner (side view)
- **Color:** Blue and gray with green accent
- **Size:** L-shaped
- **Rotations:** 4 orientations
- **Rationale:** L-shape works well for vacuum body + handle

#### Piece 5: J-Piece - "The Toilet"
- **Visual:** Toilet with tank (side view)
- **Color:** White ceramic with blue water
- **Size:** J-shaped
- **Rotations:** 4 orientations
- **Rationale:** J-shape matches toilet bowl + tank configuration

#### Piece 6: S-Piece - "The Hose"
- **Visual:** Coiled garden/cleaning hose
- **Color:** Green with silver fittings
- **Size:** S-shaped
- **Rotations:** 2 orientations
- **Rationale:** S-curve naturally represents a coiled hose

#### Piece 7: Z-Piece - "The Ladder"
- **Visual:** Ladder (side view, leaning)
- **Color:** Gray/silver metal
- **Size:** Z-shaped
- **Rotations:** 2 orientations
- **Rationale:** Z-shape represents ladder rungs in perspective

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
  │   ├── squeegee.png      (I-piece)
  │   ├── washer.png        (O-piece)
  │   ├── mop.png           (T-piece)
  │   ├── vacuum.png        (L-piece)
  │   ├── toilet.png        (J-piece)
  │   ├── hose.png          (S-piece)
  │   └── ladder.png        (Z-piece)
  ├── ui/
  │   ├── logo.png          (HaHa Hausservice Haubenhofer logo)
  │   ├── background.png    (Game background)
  │   └── block_empty.png   (Grid outline)
  └── effects/
      └── line_clear.png    (Optional: line clear effect)
```

## 6. UI Layout

### 6.1 Screen Layout (1280x960 resolution)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  HAHA HAUSSERVICE HAUBENHOFER                          [LOGO]            │
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
- [ ] Design cleaning tool sprites (squeegee, washer, mop, vacuum, toilet, hose, ladder)
- [ ] Implement sprite rendering (48x48 pixel blocks)
- [ ] Add UI elements (score, level, next piece)
- [ ] Add HaHa Hausservice Haubenhofer logo
- [ ] Polish visual appearance with brand colors

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
1. All 7 cleaning tool pieces can spawn, move, rotate, and lock
2. Lines clear correctly and score updates
3. Game over triggers when pieces reach the top
4. Level progression works and speed increases
5. UI displays all necessary information
6. Cleaning tool sprites are recognizable and themed appropriately
7. HaHa Hausservice Haubenhofer branding is visible and prominent
8. Brand colors (blue #0066CC, green #009933) are used consistently
9. No major bugs or crashes
10. Code is clean and maintainable

## 11. Notes & Considerations

### 11.1 Brand Integration
- Ensure HaHa Hausservice Haubenhofer logo (assets/logo.jpeg) is prominently displayed
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

### 11.3 Future Possibilities
- Web version using Pygame Zero to HTML export
- Mobile responsive design
- Multiplayer/competitive mode
- Custom cleaning tool piece creator
- Integration with company website
- Animated mascot (diving bird) for special achievements

---

**Document Version:** 2.0  
**Last Updated:** 2026-01-29  
**Status:** Planning Phase - Updated with 48x48 blocks and revised sprite mappings
