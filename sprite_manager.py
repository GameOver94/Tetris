"""
Sprite manager for loading and managing furniture piece sprites
"""

import os
import pygame
from pygame import image, transform, Surface, SRCALPHA

# Mapping of shape types to sprite filenames
SPRITE_FILES = {
    'I': 'images/pieces/desk.png',
    'O': 'images/pieces/printer.png',
    'T': 'images/pieces/shower.png',
    'L': 'images/pieces/chair.png',
    'J': 'images/pieces/cabinet.png',
    'S': 'images/pieces/sink.png',
    'Z': 'images/pieces/toilet.png'
}

BLOCK_SIZE = 48


class Block:
    """
    Represents a single block within a piece, with sprite information.
    Tracks the original sprite position and rotation so it can be rendered correctly
    even after rotation or locking.
    """
    
    def __init__(self, shape_type, sprite_dx, sprite_dy, sprite_surface=None, rotation=0):
        """
        Initialize a block.
        
        Args:
            shape_type: The piece type this block belongs to ('I', 'O', etc.)
            sprite_dx: Original X position in the sprite (0-3 for I-piece, etc.)
            sprite_dy: Original Y position in the sprite
            sprite_surface: Pre-loaded 48x48 sprite surface for this block
            rotation: Current rotation angle in degrees (0, 90, 180, 270)
        """
        self.shape_type = shape_type
        self.sprite_dx = sprite_dx
        self.sprite_dy = sprite_dy
        self.sprite = sprite_surface
        self.rotation = rotation  # Current rotation: 0, 90, 180, or 270 degrees
    
    def copy(self):
        """Create a copy of this block"""
        return Block(self.shape_type, self.sprite_dx, self.sprite_dy, self.sprite, self.rotation)
    
    def rotate_clockwise(self):
        """Rotate the block 90 degrees clockwise"""
        self.rotation = (self.rotation + 90) % 360
    
    def __repr__(self):
        return f"Block({self.shape_type}, {self.sprite_dx}, {self.sprite_dy}, rot={self.rotation})"


class SpriteManager:
    """Manages loading and accessing sprite images for pieces"""
    
    def __init__(self):
        """Initialize sprite manager"""
        self.sprites = {}  # Full sprites: shape_type -> Surface
        self.block_sprites = {}  # Pre-split blocks: (shape_type, dx, dy) -> Surface
        self.rotated_sprites = {}  # Rotated versions: (shape_type, dx, dy, rotation) -> Surface
        self.use_sprites = True
        
    def load_sprites(self):
        """Load all piece sprites from disk and pre-split them into blocks"""
        for shape_type, filepath in SPRITE_FILES.items():
            if os.path.exists(filepath):
                try:
                    sprite = image.load(filepath)
                    self.sprites[shape_type] = sprite
                    print(f"Loaded sprite for {shape_type}: {filepath} ({sprite.get_width()}x{sprite.get_height()})")
                    
                    # Pre-split this sprite into individual blocks
                    self._split_sprite(shape_type, sprite)
                    
                except Exception as e:
                    print(f"Error loading sprite {filepath}: {e}")
                    self.use_sprites = False
            else:
                print(f"Sprite file not found: {filepath}")
                self.use_sprites = False
    
    def _split_sprite(self, shape_type, sprite):
        """
        Split a full piece sprite into individual 48x48 block sprites.
        Also creates rotated versions (90, 180, 270 degrees) for each block.
        
        Args:
            shape_type: The piece type ('I', 'O', etc.)
            sprite: The full sprite surface to split
        """
        # Calculate how many blocks wide and tall the sprite is
        width_blocks = sprite.get_width() // BLOCK_SIZE
        height_blocks = sprite.get_height() // BLOCK_SIZE
        
        # Extract each 48x48 block
        for dy in range(height_blocks):
            for dx in range(width_blocks):
                # Create a new surface for this block
                block_surface = Surface((BLOCK_SIZE, BLOCK_SIZE), SRCALPHA)
                
                # Extract the portion from the full sprite
                sprite_x = dx * BLOCK_SIZE
                sprite_y = dy * BLOCK_SIZE
                
                try:
                    block_surface.blit(sprite, (0, 0), (sprite_x, sprite_y, BLOCK_SIZE, BLOCK_SIZE))
                    
                    # Add a subtle border to make blocks distinct
                    border_color = (100, 100, 100)
                    pygame.draw.rect(block_surface, border_color, (0, 0, BLOCK_SIZE, BLOCK_SIZE), 1)
                    
                    # Store the original (0 degrees) block sprite
                    self.block_sprites[(shape_type, dx, dy)] = block_surface
                    self.rotated_sprites[(shape_type, dx, dy, 0)] = block_surface
                    
                    # Create and store rotated versions (90, 180, 270 degrees)
                    for rotation in [90, 180, 270]:
                        rotated = pygame.transform.rotate(block_surface, rotation)
                        self.rotated_sprites[(shape_type, dx, dy, rotation)] = rotated
                    
                except Exception as e:
                    print(f"Error splitting sprite at ({dx}, {dy}) for {shape_type}: {e}")
    
    def get_block_sprite(self, shape_type, dx, dy, rotation=0):
        """
        Get a pre-split 48x48 sprite for a specific block position with rotation.
        
        Args:
            shape_type: The type of piece ('I', 'O', 'T', 'L', 'J', 'S', 'Z')
            dx: X offset of the block within the piece shape
            dy: Y offset of the block within the piece shape
            rotation: Rotation angle in degrees (0, 90, 180, 270)
            
        Returns:
            A 48x48 Surface with the block sprite (rotated), or None
        """
        if not self.use_sprites:
            return None
        
        # Get the rotated version if available
        return self.rotated_sprites.get((shape_type, dx, dy, rotation))
    
    def create_block(self, shape_type, dx, dy, rotation=0):
        """
        Create a Block object with pre-loaded sprite.
        
        Args:
            shape_type: The piece type
            dx: X position in the original sprite
            dy: Y position in the original sprite
            rotation: Initial rotation angle in degrees (0, 90, 180, 270)
            
        Returns:
            A Block object with sprite loaded
        """
        sprite = self.get_block_sprite(shape_type, dx, dy, rotation)
        return Block(shape_type, dx, dy, sprite, rotation)
            
    def has_sprites(self):
        """Check if sprites are loaded and ready to use"""
        return self.use_sprites and len(self.sprites) > 0

# Global sprite manager instance
sprite_manager = SpriteManager()
