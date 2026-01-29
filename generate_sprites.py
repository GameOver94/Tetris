#!/usr/bin/env python3
"""
Generate placeholder sprite images for Tetris furniture pieces.
Uses brand colors and creates recognizable furniture-themed sprites.
"""

import pygame
from pygame import Surface, draw, font
import os

# Initialize pygame
pygame.init()

# Brand colors
PRIMARY_BLUE = (0, 102, 204)      # #0066CC
SECONDARY_GREEN = (0, 153, 51)    # #009933
LIGHT_BLUE = (51, 204, 255)       # #33CCFF
DARK_TEXT = (44, 62, 80)          # #2C3E50
LIGHT_GRAY = (220, 220, 220)
MED_GRAY = (150, 150, 150)
DARK_GRAY = (80, 80, 80)
WHITE = (255, 255, 255)
BROWN = (139, 90, 43)
DARK_BROWN = (101, 67, 33)

BLOCK_SIZE = 48

def create_desk_sprite():
    """I-Piece: Office Desk - 4 blocks horizontal"""
    # Create a 4x1 desk sprite (192x48)
    sprite = Surface((BLOCK_SIZE * 4, BLOCK_SIZE), pygame.SRCALPHA)
    
    # Shadow
    draw.rect(sprite, (0, 0, 0, 40), (2, 7, BLOCK_SIZE * 4, 15))
    
    # Desktop (brown wood)
    draw.rect(sprite, BROWN, (0, 5, BLOCK_SIZE * 4, 15))
    draw.rect(sprite, DARK_BROWN, (0, 5, BLOCK_SIZE * 4, 3))  # Edge
    # Wood grain highlights
    draw.line(sprite, (160, 110, 60), (5, 10), (BLOCK_SIZE * 4 - 5, 10), 1)
    
    # Legs and drawers with depth
    for i in range(4):
        x_offset = i * BLOCK_SIZE
        # Shadow for drawer
        draw.rect(sprite, (0, 0, 0, 30), (x_offset + 6, 22, BLOCK_SIZE - 8, 25))
        # Drawer/cabinet body
        draw.rect(sprite, MED_GRAY, (x_offset + 4, 20, BLOCK_SIZE - 8, 25))
        draw.rect(sprite, DARK_GRAY, (x_offset + 4, 20, BLOCK_SIZE - 8, 2))
        # Highlight
        draw.rect(sprite, (180, 180, 180), (x_offset + 5, 21, BLOCK_SIZE - 10, 2))
        # Drawer handle with depth
        draw.rect(sprite, (50, 50, 50), (x_offset + 21, 31, 8, 3))
        draw.rect(sprite, DARK_GRAY, (x_offset + 20, 30, 8, 3))
    
    # Add text label
    try:
        text_font = font.Font(None, 16)
        text = text_font.render("DESK", True, WHITE)
        text_rect = text.get_rect(center=(BLOCK_SIZE * 2, BLOCK_SIZE - 8))
        sprite.blit(text, text_rect)
    except Exception:
        pass
    
    return sprite

def create_printer_sprite():
    """O-Piece: Printer/Copier - 2x2 blocks"""
    sprite = Surface((BLOCK_SIZE * 2, BLOCK_SIZE * 2), pygame.SRCALPHA)
    
    # Shadow
    draw.rect(sprite, (0, 0, 0, 40), (10, 22, BLOCK_SIZE * 2 - 16, BLOCK_SIZE * 2 - 28))
    
    # Main printer body (light gray)
    draw.rect(sprite, LIGHT_GRAY, (8, 20, BLOCK_SIZE * 2 - 16, BLOCK_SIZE * 2 - 30))
    draw.rect(sprite, MED_GRAY, (8, 20, BLOCK_SIZE * 2 - 16, 5))  # Top edge
    # Highlight
    draw.rect(sprite, WHITE, (9, 26, BLOCK_SIZE * 2 - 18, 2))
    
    # Paper tray (white) with depth
    draw.rect(sprite, (200, 200, 200), (14, 32, BLOCK_SIZE * 2 - 24, 40))
    draw.rect(sprite, WHITE, (12, 30, BLOCK_SIZE * 2 - 24, 40))
    draw.rect(sprite, MED_GRAY, (12, 30, BLOCK_SIZE * 2 - 24, 2))
    
    # Control panel (dark) with depth
    draw.rect(sprite, (40, 40, 40), (14, 77, 30, 15))
    draw.rect(sprite, DARK_GRAY, (12, 75, 30, 15))
    
    # Buttons (colored) with highlights
    draw.circle(sprite, (0, 100, 30), (21, 83), 3)
    draw.circle(sprite, SECONDARY_GREEN, (20, 82), 3)
    draw.circle(sprite, (0, 50, 150), (31, 83), 3)
    draw.circle(sprite, PRIMARY_BLUE, (30, 82), 3)
    
    # Label
    try:
        text_font = font.Font(None, 16)
        text = text_font.render("PRINTER", True, DARK_TEXT)
        text_rect = text.get_rect(center=(BLOCK_SIZE, 10))
        sprite.blit(text, text_rect)
    except Exception:
        pass
    
    return sprite

def create_shower_sprite():
    """T-Piece: Shower head - T-shaped"""
    sprite = Surface((BLOCK_SIZE * 3, BLOCK_SIZE * 2), pygame.SRCALPHA)
    
    # Shower head (top horizontal part of T)
    draw.rect(sprite, MED_GRAY, (BLOCK_SIZE // 4, 5, BLOCK_SIZE * 3 - BLOCK_SIZE // 2, 20))
    
    # Shower pipe (vertical part of T)
    draw.rect(sprite, MED_GRAY, (BLOCK_SIZE + 10, 5, 28, BLOCK_SIZE + 20))
    
    # Water droplets (light blue)
    for i in range(5):
        x = BLOCK_SIZE // 2 + i * 10
        for j in range(3):
            y = 30 + j * 12
            draw.circle(sprite, LIGHT_BLUE, (x, y), 2)
    
    # Label
    try:
        text_font = font.Font(None, 16)
        text = text_font.render("SHOWER", True, DARK_TEXT)
        text_rect = text.get_rect(center=(BLOCK_SIZE * 1.5, BLOCK_SIZE * 2 - 10))
        sprite.blit(text, text_rect)
    except Exception:
        pass
    
    return sprite

def create_chair_sprite():
    """L-Piece: Office Chair - L-shaped"""
    sprite = Surface((BLOCK_SIZE * 2, BLOCK_SIZE * 3), pygame.SRCALPHA)
    
    # Backrest (vertical part of L)
    draw.rect(sprite, PRIMARY_BLUE, (8, 8, BLOCK_SIZE - 16, BLOCK_SIZE * 2 - 8))
    draw.rect(sprite, DARK_GRAY, (8, 8, BLOCK_SIZE - 16, 3))
    
    # Seat (horizontal part of L)
    draw.rect(sprite, PRIMARY_BLUE, (8, BLOCK_SIZE * 2, BLOCK_SIZE * 2 - 16, BLOCK_SIZE - 16))
    draw.rect(sprite, DARK_GRAY, (8, BLOCK_SIZE * 2, BLOCK_SIZE * 2 - 16, 3))
    
    # Base/wheels
    draw.circle(sprite, DARK_GRAY, (BLOCK_SIZE, BLOCK_SIZE * 3 - 8), 6)
    draw.circle(sprite, DARK_GRAY, (BLOCK_SIZE + 20, BLOCK_SIZE * 3 - 8), 6)
    
    # Label
    try:
        text_font = font.Font(None, 14)
        text = text_font.render("CHAIR", True, WHITE)
        text_rect = text.get_rect(center=(BLOCK_SIZE // 2, BLOCK_SIZE))
        sprite.blit(text, text_rect)
    except Exception:
        pass
    
    return sprite

def create_cabinet_sprite():
    """J-Piece: Filing Cabinet - J-shaped"""
    sprite = Surface((BLOCK_SIZE * 2, BLOCK_SIZE * 3), pygame.SRCALPHA)
    
    # Main cabinet body (J shape - vertical with horizontal at bottom left)
    # Vertical part
    draw.rect(sprite, MED_GRAY, (BLOCK_SIZE + 8, 8, BLOCK_SIZE - 16, BLOCK_SIZE * 2 - 8))
    # Horizontal part
    draw.rect(sprite, MED_GRAY, (8, BLOCK_SIZE * 2, BLOCK_SIZE * 2 - 16, BLOCK_SIZE - 16))
    
    # Drawer lines
    for i in range(4):
        y = 15 + i * 20
        draw.line(sprite, DARK_GRAY, (BLOCK_SIZE + 10, y), (BLOCK_SIZE * 2 - 10, y), 2)
        # Handles
        draw.rect(sprite, DARK_GRAY, (BLOCK_SIZE + 20, y + 5, 8, 4))
    
    # Label
    try:
        text_font = font.Font(None, 14)
        text = text_font.render("CABINET", True, WHITE)
        text_rect = text.get_rect(center=(BLOCK_SIZE * 1.5, BLOCK_SIZE * 2 + 20))
        sprite.blit(text, text_rect)
    except Exception:
        pass
    
    return sprite

def create_sink_sprite():
    """S-Piece: Sink with plumbing - S-shaped"""
    sprite = Surface((BLOCK_SIZE * 3, BLOCK_SIZE * 2), pygame.SRCALPHA)
    
    # Sink basin (white ceramic)
    # Top left and right parts
    draw.ellipse(sprite, WHITE, (BLOCK_SIZE + 10, 8, 60, 30))
    draw.ellipse(sprite, LIGHT_GRAY, (BLOCK_SIZE + 10, 10, 60, 28))
    
    # Faucet
    draw.circle(sprite, MED_GRAY, (BLOCK_SIZE + 40, 20), 8)
    draw.rect(sprite, MED_GRAY, (BLOCK_SIZE + 36, 10, 8, 12))
    
    # Pipes (S-shaped)
    draw.rect(sprite, MED_GRAY, (10, BLOCK_SIZE + 10, 25, 8))
    draw.rect(sprite, MED_GRAY, (BLOCK_SIZE * 2 + 10, BLOCK_SIZE + 10, 25, 8))
    
    # Label
    try:
        text_font = font.Font(None, 16)
        text = text_font.render("SINK", True, DARK_TEXT)
        text_rect = text.get_rect(center=(BLOCK_SIZE * 1.5, BLOCK_SIZE * 2 - 10))
        sprite.blit(text, text_rect)
    except Exception:
        pass
    
    return sprite

def create_toilet_sprite():
    """Z-Piece: Toilet - Z-shaped"""
    sprite = Surface((BLOCK_SIZE * 3, BLOCK_SIZE * 2), pygame.SRCALPHA)
    
    # Tank (top left)
    draw.rect(sprite, WHITE, (10, 8, BLOCK_SIZE - 10, 35))
    draw.rect(sprite, LIGHT_GRAY, (10, 8, BLOCK_SIZE - 10, 5))
    
    # Bowl (bottom right)
    draw.ellipse(sprite, WHITE, (BLOCK_SIZE + 20, BLOCK_SIZE + 5, 60, 35))
    draw.ellipse(sprite, LIGHT_BLUE, (BLOCK_SIZE + 25, BLOCK_SIZE + 10, 50, 25))
    
    # Connecting pipe
    draw.rect(sprite, LIGHT_GRAY, (BLOCK_SIZE - 5, 30, 35, 8))
    
    # Label
    try:
        text_font = font.Font(None, 16)
        text = text_font.render("TOILET", True, DARK_TEXT)
        text_rect = text.get_rect(center=(BLOCK_SIZE * 1.5, BLOCK_SIZE * 2 - 10))
        sprite.blit(text, text_rect)
    except Exception:
        pass
    
    return sprite

def main():
    """Generate all sprite images"""
    
    sprites = {
        'desk.png': create_desk_sprite(),
        'printer.png': create_printer_sprite(),
        'shower.png': create_shower_sprite(),
        'chair.png': create_chair_sprite(),
        'cabinet.png': create_cabinet_sprite(),
        'sink.png': create_sink_sprite(),
        'toilet.png': create_toilet_sprite()
    }
    
    # Save all sprites
    output_dir = 'images/pieces'
    os.makedirs(output_dir, exist_ok=True)
    
    for filename, sprite in sprites.items():
        filepath = os.path.join(output_dir, filename)
        pygame.image.save(sprite, filepath)
        print(f"Created: {filepath} ({sprite.get_width()}x{sprite.get_height()})")
    
    pygame.quit()
    print(f"\nSuccessfully generated {len(sprites)} sprite images!")

if __name__ == '__main__':
    main()
