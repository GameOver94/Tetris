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

class SpriteManager:
    """Manages loading and accessing sprite images for pieces"""
    
    def __init__(self):
        """Initialize sprite manager"""
        self.sprites = {}
        self.use_sprites = True
        
    def load_sprites(self):
        """Load all piece sprites from disk"""
        for shape_type, filepath in SPRITE_FILES.items():
            if os.path.exists(filepath):
                try:
                    sprite = image.load(filepath)
                    self.sprites[shape_type] = sprite
                    print(f"Loaded sprite for {shape_type}: {filepath} ({sprite.get_width()}x{sprite.get_height()})")
                except Exception as e:
                    print(f"Error loading sprite {filepath}: {e}")
                    self.use_sprites = False
            else:
                print(f"Sprite file not found: {filepath}")
                self.use_sprites = False
            
    def get_block_sprite_at_position(self, shape_type, dx, dy):
        """
        Get the 48x48 sprite for a specific block position within a piece.
        
        Args:
            shape_type: The type of piece ('I', 'O', 'T', 'L', 'J', 'S', 'Z')
            dx: X offset of the block within the piece shape (from SHAPES definition)
            dy: Y offset of the block within the piece shape (from SHAPES definition)
            
        Returns:
            A 48x48 Surface with the appropriate portion of the sprite, or None
        """
        BLOCK_SIZE = 48
        
        if not self.use_sprites or shape_type not in self.sprites:
            return None
        
        sprite = self.sprites[shape_type]
        
        # Create a new surface for this specific block
        block = Surface((BLOCK_SIZE, BLOCK_SIZE), SRCALPHA)
        
        # Calculate the position in the sprite to extract from
        # The sprite coordinates match the block coordinates in the piece shape
        sprite_x = dx * BLOCK_SIZE
        sprite_y = dy * BLOCK_SIZE
        
        # Extract the appropriate 48x48 portion from the full sprite
        try:
            block.blit(sprite, (0, 0), (sprite_x, sprite_y, BLOCK_SIZE, BLOCK_SIZE))
            
            # Add a subtle border to make blocks distinct
            border_color = (100, 100, 100)
            pygame.draw.rect(block, border_color, (0, 0, BLOCK_SIZE, BLOCK_SIZE), 1)
            
            return block
        except Exception as e:
            print(f"Error extracting sprite at ({dx}, {dy}) for {shape_type}: {e}")
            return None
    
    def get_representative_block_sprite(self, shape_type):
        """
        Get a representative 48x48 sprite for locked pieces.
        Uses a visually interesting portion of the sprite.
        
        Args:
            shape_type: The type of piece ('I', 'O', 'T', 'L', 'J', 'S', 'Z')
            
        Returns:
            A 48x48 Surface with a representative portion of the sprite, or None
        """
        # For locked pieces, use a representative block position
        # This provides visual variety while maintaining recognizability
        representative_positions = {
            'I': (1, 0),  # Second segment of desk
            'O': (0, 0),  # Top-left of printer
            'T': (1, 0),  # Middle of shower
            'L': (0, 1),  # Middle of chair
            'J': (1, 1),  # Middle of cabinet (fixed: was 0,1 which is invalid)
            'S': (1, 0),  # Middle of sink
            'Z': (1, 0),  # Middle of toilet
        }
        
        dx, dy = representative_positions.get(shape_type, (0, 0))
        return self.get_block_sprite_at_position(shape_type, dx, dy)
    
    def has_sprites(self):
        """Check if sprites are loaded and ready to use"""
        return self.use_sprites and len(self.sprites) > 0

# Global sprite manager instance
sprite_manager = SpriteManager()
