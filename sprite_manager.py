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
        self.block_sprites = {}  # 48x48 block sprites for each piece type
        self.use_sprites = True
        
    def load_sprites(self):
        """Load all piece sprites from disk"""
        for shape_type, filepath in SPRITE_FILES.items():
            if os.path.exists(filepath):
                try:
                    sprite = image.load(filepath)
                    self.sprites[shape_type] = sprite
                    print(f"Loaded sprite for {shape_type}: {filepath}")
                except Exception as e:
                    print(f"Error loading sprite {filepath}: {e}")
                    self.use_sprites = False
            else:
                print(f"Sprite file not found: {filepath}")
                self.use_sprites = False
        
        # Create individual block sprites from the full piece sprites
        if self.use_sprites:
            self._create_block_sprites()
            
    def _create_block_sprites(self):
        """
        Create 48x48 block sprites from the full piece sprites.
        Extracts representative portions of each multi-block sprite for individual rendering.
        
        Extraction strategy:
        - I-piece (Desk): First segment of 4-block horizontal sprite
        - O-piece (Printer): Top-left quadrant of 2x2 sprite
        - T/S/Z pieces: Middle block from 3-block width sprites
        - L/J pieces: Bottom block from vertical portion
        """
        BLOCK_SIZE = 48
        
        for shape_type, sprite in self.sprites.items():
            # Create a new surface for the block
            block = Surface((BLOCK_SIZE, BLOCK_SIZE), SRCALPHA)
            
            # Extract representative portion based on piece type
            if shape_type == 'I':
                # Desk: extract one segment from the 4-block sprite
                block.blit(sprite, (0, 0), (0, 0, BLOCK_SIZE, BLOCK_SIZE))
                
            elif shape_type == 'O':
                # Printer: use one quadrant of the 2x2 sprite
                block.blit(sprite, (0, 0), (0, 0, BLOCK_SIZE, BLOCK_SIZE))
                
            elif shape_type in ['T', 'S', 'Z']:
                # Extract middle block from the sprite
                block.blit(sprite, (0, 0), (BLOCK_SIZE, 0, BLOCK_SIZE, BLOCK_SIZE))
                
            else:  # L, J shapes
                # Extract bottom block from vertical portion
                block.blit(sprite, (0, 0), (0, BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            
            # Add a subtle border to make blocks distinct
            border_color = (100, 100, 100)
            pygame.draw.rect(block, border_color, (0, 0, BLOCK_SIZE, BLOCK_SIZE), 1)
            
            self.block_sprites[shape_type] = block
    
    def get_block_sprite(self, shape_type):
        """Get the 48x48 sprite for a single block of the given piece type"""
        if self.use_sprites and shape_type in self.block_sprites:
            return self.block_sprites[shape_type]
        return None
    
    def has_sprites(self):
        """Check if sprites are loaded and ready to use"""
        return self.use_sprites and len(self.sprites) > 0

# Global sprite manager instance
sprite_manager = SpriteManager()
