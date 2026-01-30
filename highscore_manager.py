"""
High score manager for persisting high scores to disk
"""

import json
import os

HIGHSCORE_FILE = 'highscore.json'


class HighScoreManager:
    """Manages loading and saving high scores"""
    
    def __init__(self):
        """Initialize high score manager"""
        self.high_score = 0
        self.load()
    
    def load(self):
        """Load high score from disk"""
        if os.path.exists(HIGHSCORE_FILE):
            try:
                with open(HIGHSCORE_FILE, 'r') as f:
                    data = json.load(f)
                    self.high_score = data.get('high_score', 0)
                    print(f"Loaded high score: {self.high_score}")
            except Exception as e:
                print(f"Error loading high score: {e}")
                self.high_score = 0
        else:
            print("No high score file found, starting fresh")
    
    def save(self, score):
        """
        Save high score to disk if it's a new high score.
        
        Args:
            score: Current score to check and potentially save
            
        Returns:
            bool: True if this is a new high score
        """
        is_new_high = score > self.high_score
        
        if is_new_high:
            self.high_score = score
            try:
                with open(HIGHSCORE_FILE, 'w') as f:
                    json.dump({'high_score': self.high_score}, f)
                print(f"New high score saved: {self.high_score}")
            except Exception as e:
                print(f"Error saving high score: {e}")
        
        return is_new_high
    
    def get_high_score(self):
        """Get the current high score"""
        return self.high_score


# Global high score manager instance
highscore_manager = HighScoreManager()
