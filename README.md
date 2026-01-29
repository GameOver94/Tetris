# Tetris
A promotional Tetris game for Hausservice Haubenhofer

## Features

- Classic Tetris gameplay with office and bathroom furniture pieces
- Progressive difficulty with increasing speed
- High score persistence
- Sound effects and background music (optional)
- Pause functionality
- Start menu
- Visual effects for line clears

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

You can run the game using either of these methods:

```bash
# Method 1: Using pgzrun command (recommended)
pgzrun tetris.py

# Method 2: Using python directly
python tetris.py
```

## Controls

- **Arrow Keys**: Move pieces left/right, rotate, and soft drop
- **SPACE**: Hard drop (instant placement)
- **P**: Pause/Resume game
- **M**: Toggle music on/off
- **R**: Restart after game over

## Sound Files (Optional)

The game supports sound effects and background music. To enable sounds, add audio files to:
- `sounds/effects/` - Sound effects (move.wav, rotate.wav, lock.wav, line_clear.wav, tetris.wav, game_over.wav, level_up.wav)
- `sounds/music/` - Background music (background.ogg)

The game will work without these files but will have no audio.

## Testing

This project includes a comprehensive test suite that validates all game mechanics.

### Running Tests

Run all tests:
```bash
pytest test_tetris.py -v
```

Run specific test class:
```bash
pytest test_tetris.py::TestPiece -v
pytest test_tetris.py::TestScoringSystem -v
```

### Test Coverage

The test suite covers:
- **Piece Class**: Initialization, movement, rotation
- **Collision Detection**: Boundaries and locked pieces
- **Piece Locking**: Basic and partial locking
- **Line Clearing**: Detection and clearing logic
- **Scoring System**: Points for single, double, triple lines and Tetris
- **Level Progression**: Level up mechanics and speed increases
- **Game Over**: Detection when pieces reach the top
- **Integration Tests**: Full game flow scenarios

All tests use pytest and can be run without a display (headless mode).

## Architecture

The project is organized into separate modules:

- **game_logic.py**: Pure game logic without display dependencies (testable)
- **tetris.py**: Pygame Zero display and main game loop
- **test_tetris.py**: Comprehensive test suite
