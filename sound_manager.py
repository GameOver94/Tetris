"""
Sound manager for loading and playing sound effects and music
"""

import os
import pygame
from pygame import mixer

# Sound effect files mapping
SOUND_EFFECTS = {
    'move': 'sounds/effects/move.wav',
    'rotate': 'sounds/effects/rotate.wav',
    'lock': 'sounds/effects/lock.wav',
    'line_clear': 'sounds/effects/line_clear.wav',
    'tetris': 'sounds/effects/tetris.wav',
    'game_over': 'sounds/effects/game_over.wav',
    'level_up': 'sounds/effects/level_up.wav'
}

# Background music file
BACKGROUND_MUSIC = 'sounds/music/background.ogg'


class SoundManager:
    """Manages loading and playing sound effects and background music"""
    
    def __init__(self):
        """Initialize sound manager"""
        self.sound_effects = {}
        self.music_enabled = True
        self.sfx_enabled = True
        self.music_volume = 0.3
        self.sfx_volume = 0.5
        self.initialized = False
        
        # Try to initialize pygame mixer
        try:
            if not mixer.get_init():
                mixer.init()
            self.initialized = True
            print("Sound system initialized")
        except Exception as e:
            print(f"Failed to initialize sound system: {e}")
            self.initialized = False
    
    def load_sounds(self):
        """Load all sound effects from disk"""
        if not self.initialized:
            print("Sound system not initialized, skipping sound loading")
            return
        
        # Load sound effects
        for name, filepath in SOUND_EFFECTS.items():
            if os.path.exists(filepath):
                try:
                    sound = mixer.Sound(filepath)
                    sound.set_volume(self.sfx_volume)
                    self.sound_effects[name] = sound
                    print(f"Loaded sound effect: {name}")
                except Exception as e:
                    print(f"Error loading sound {filepath}: {e}")
            else:
                # Sound file doesn't exist, but we'll continue without it
                pass
        
        # Load background music
        if os.path.exists(BACKGROUND_MUSIC):
            try:
                mixer.music.load(BACKGROUND_MUSIC)
                mixer.music.set_volume(self.music_volume)
                print(f"Loaded background music: {BACKGROUND_MUSIC}")
            except Exception as e:
                print(f"Error loading music {BACKGROUND_MUSIC}: {e}")
    
    def play_sound(self, sound_name):
        """
        Play a sound effect.
        
        Args:
            sound_name: Name of the sound effect to play
        """
        if not self.initialized or not self.sfx_enabled:
            return
        
        sound = self.sound_effects.get(sound_name)
        if sound:
            try:
                sound.play()
            except Exception as e:
                print(f"Error playing sound {sound_name}: {e}")
    
    def play_music(self, loop=True):
        """
        Start playing background music.
        
        Args:
            loop: Whether to loop the music (-1 for infinite loop, or number of times)
        """
        if not self.initialized or not self.music_enabled:
            return
        
        try:
            loops = -1 if loop else 0
            mixer.music.play(loops)
        except Exception as e:
            print(f"Error playing music: {e}")
    
    def stop_music(self):
        """Stop background music"""
        if not self.initialized:
            return
        
        try:
            mixer.music.stop()
        except Exception as e:
            print(f"Error stopping music: {e}")
    
    def pause_music(self):
        """Pause background music"""
        if not self.initialized:
            return
        
        try:
            mixer.music.pause()
        except Exception as e:
            print(f"Error pausing music: {e}")
    
    def unpause_music(self):
        """Resume background music"""
        if not self.initialized:
            return
        
        try:
            mixer.music.unpause()
        except Exception as e:
            print(f"Error unpausing music: {e}")
    
    def set_music_volume(self, volume):
        """
        Set music volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        if not self.initialized:
            return
        
        self.music_volume = max(0.0, min(1.0, volume))
        try:
            mixer.music.set_volume(self.music_volume)
        except Exception as e:
            print(f"Error setting music volume: {e}")
    
    def set_sfx_volume(self, volume):
        """
        Set sound effects volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        if not self.initialized:
            return
        
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sound_effects.values():
            try:
                sound.set_volume(self.sfx_volume)
            except Exception as e:
                print(f"Error setting sfx volume: {e}")
    
    def toggle_music(self):
        """Toggle music on/off"""
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            # Only try to play if we actually have music loaded
            # Check if music is loaded by trying to get its position
            try:
                # If music was loaded successfully, this won't raise an error
                if os.path.exists(BACKGROUND_MUSIC):
                    self.play_music()
            except Exception:
                # Music not loaded, silently skip
                pass
        else:
            self.stop_music()
    
    def toggle_sfx(self):
        """Toggle sound effects on/off"""
        self.sfx_enabled = not self.sfx_enabled
    
    def has_sounds(self):
        """Check if any sounds are loaded"""
        return self.initialized and len(self.sound_effects) > 0


# Global sound manager instance
sound_manager = SoundManager()
