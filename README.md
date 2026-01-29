# Tetris
A promotional Tetris game for Hausservice Haubentaucher

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python tetris.py
```

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
