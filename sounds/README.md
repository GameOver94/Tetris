# Sound Files

This directory contains sound effects and background music for the Tetris game.

## Directory Structure

```
sounds/
  ├── effects/     - Sound effects (.wav files)
  └── music/       - Background music (.ogg files)
```

## Required Files

### Sound Effects (sounds/effects/)
- `move.wav` - Played when moving pieces left/right
- `rotate.wav` - Played when rotating pieces
- `lock.wav` - Played when a piece locks into place
- `line_clear.wav` - Played when clearing 1-3 lines
- `tetris.wav` - Played when clearing 4 lines (Tetris!)
- `game_over.wav` - Played when game ends
- `level_up.wav` - Played when advancing to next level

### Background Music (sounds/music/)
- `background.ogg` - Main game background music (looped)

## Notes

- All sound effects should be in WAV format
- Background music should be in OGG format for better compression
- The game will work without sound files but will have no audio
- Sound files are optional - the game gracefully handles missing files
- You can toggle music on/off in-game by pressing 'M'
