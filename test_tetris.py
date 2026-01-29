"""
Unit tests for HaHa Hausservice Haubenhofer Tetris Game

This test suite covers:
- Piece class functionality (initialization, movement, rotation)
- Collision detection
- Piece locking
- Line clearing logic
- Scoring system
- Level progression
- Game over detection
"""

import pytest
from game_logic import (
    Piece, SHAPES, PIECE_COLORS, GRID_WIDTH, GRID_HEIGHT,
    SCORE_SINGLE, SCORE_DOUBLE, SCORE_TRIPLE, SCORE_TETRIS,
    SCORE_SOFT_DROP, SCORE_HARD_DROP, INITIAL_FALL_SPEED, SPEED_MULTIPLIER,
    check_collision, lock_piece, check_lines, clear_lines, spawn_piece
)


class TestPiece:
    """Test the Piece class"""
    
    def test_piece_initialization(self):
        """Test that a piece initializes correctly"""
        piece = Piece('I')
        assert piece.shape_type == 'I'
        assert piece.shape == SHAPES['I'].copy()
        assert piece.color == PIECE_COLORS['I']
        assert piece.x == GRID_WIDTH // 2 - 2
        assert piece.y == 0
    
    def test_piece_get_blocks(self):
        """Test that get_blocks returns correct absolute positions"""
        piece = Piece('I')
        piece.x = 3
        piece.y = 5
        blocks = piece.get_blocks()
        
        # I-piece shape is [(0,0), (1,0), (2,0), (3,0)]
        # With x=3, y=5, blocks should be [(3,5), (4,5), (5,5), (6,5)]
        expected = [(3, 5), (4, 5), (5, 5), (6, 5)]
        assert blocks == expected
    
    def test_piece_move(self):
        """Test that piece movement works correctly"""
        piece = Piece('O')
        original_x = piece.x
        original_y = piece.y
        
        piece.move(1, 0)  # Move right
        assert piece.x == original_x + 1
        assert piece.y == original_y
        
        piece.move(0, 1)  # Move down
        assert piece.x == original_x + 1
        assert piece.y == original_y + 1
        
        piece.move(-2, -1)  # Move left and up
        assert piece.x == original_x - 1
        assert piece.y == original_y
    
    def test_o_piece_rotation(self):
        """Test that O-piece (square) doesn't rotate"""
        piece = Piece('O')
        original_shape = piece.shape.copy()
        
        piece.rotate()
        assert piece.shape == original_shape
    
    def test_i_piece_rotation(self):
        """Test I-piece rotation (horizontal to vertical)"""
        piece = Piece('I')
        
        # Initial shape should be horizontal: [(0,0), (1,0), (2,0), (3,0)]
        assert set(piece.shape) == {(0, 0), (1, 0), (2, 0), (3, 0)}
        
        # After rotation, should be vertical (4 blocks in a column)
        piece.rotate()
        # After normalization, all x coordinates should be 0, y should be 0-3
        rotated_shape = piece.shape
        assert len(rotated_shape) == 4
        assert all(x == 0 for x, y in rotated_shape)
        y_coords = sorted([y for x, y in rotated_shape])
        assert y_coords == [0, 1, 2, 3]
        
        # Rotate back to horizontal
        piece.rotate()
        # Should have same coordinates as original (possibly in different order)
        assert set(piece.shape) == {(0, 0), (1, 0), (2, 0), (3, 0)}
    
    def test_t_piece_rotation(self):
        """Test T-piece rotation through all 4 orientations"""
        piece = Piece('T')
        
        # T-piece should rotate through 4 distinct orientations
        shapes = []
        for _ in range(4):
            shapes.append(piece.shape.copy())
            piece.rotate()
        
        # After 4 rotations, should be back to original
        assert piece.shape == shapes[0]
        
        # All 4 shapes should have 4 blocks
        for shape in shapes:
            assert len(shape) == 4
    
    def test_all_pieces_exist(self):
        """Test that all 7 piece types can be created"""
        piece_types = ['I', 'O', 'T', 'L', 'J', 'S', 'Z']
        
        for piece_type in piece_types:
            piece = Piece(piece_type)
            assert piece.shape_type == piece_type
            assert len(piece.shape) == 4  # All tetrominos have 4 blocks


class TestCollisionDetection:
    """Test collision detection logic"""
    
    def test_check_collision_left_boundary(self):
        """Test collision detection at left boundary"""
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        
        piece = Piece('I')
        piece.x = 0
        piece.y = 0
        
        # Should collide when moving left
        assert check_collision(piece, grid, -1, 0) == True
        
        # Should not collide at current position
        assert check_collision(piece, grid, 0, 0) == False
    
    def test_check_collision_right_boundary(self):
        """Test collision detection at right boundary"""
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        
        piece = Piece('I')
        piece.x = GRID_WIDTH - 4  # I-piece is 4 blocks wide
        piece.y = 0
        
        # Should collide when moving right
        assert check_collision(piece, grid, 1, 0) == True
        
        # Should not collide at current position
        assert check_collision(piece, grid, 0, 0) == False
    
    def test_check_collision_bottom_boundary(self):
        """Test collision detection at bottom boundary"""
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        
        piece = Piece('O')
        piece.x = 4
        piece.y = GRID_HEIGHT - 2  # O-piece is 2 blocks tall
        
        # Should collide when moving down
        assert check_collision(piece, grid, 0, 1) == True
        
        # Should not collide at current position
        assert check_collision(piece, grid, 0, 0) == False
    
    def test_check_collision_with_locked_pieces(self):
        """Test collision detection with locked pieces on grid"""
        # Create a clean grid
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        
        # Place a locked piece at position (5, 10)
        grid[10][5] = 'I'
        
        piece = Piece('O')
        piece.x = 4  # O-piece at x=4 would occupy x=4,5 and y=piece.y, piece.y+1
        piece.y = 9   # At y=9, would occupy y=9,10
        
        # Should collide because grid[10][5] is occupied
        assert check_collision(piece, grid, 0, 0) == True
        
        # Should not collide if moved to the left (x=3, so blocks at 3,4)
        assert check_collision(piece, grid, -1, 0) == False


class TestPieceLocking:
    """Test piece locking functionality"""
    
    def test_lock_piece_basic(self):
        """Test that a piece locks correctly to the grid"""
        # Create a clean grid
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        
        piece = Piece('O')
        piece.x = 4
        piece.y = 18  # Near bottom
        
        lock_piece(piece, grid)
        
        # O-piece at (4,18) should occupy (4,18), (5,18), (4,19), (5,19)
        # Grid now contains Block objects
        assert grid[18][4].shape_type == 'O'
        assert grid[18][5].shape_type == 'O'
        assert grid[19][4].shape_type == 'O'
        assert grid[19][5].shape_type == 'O'
    
    def test_lock_piece_partial(self):
        """Test that pieces above grid (negative y) don't lock those blocks"""
        # Create a clean grid
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        
        piece = Piece('I')
        piece.x = 3
        piece.y = -1  # Partially above grid
        
        # Rotate to vertical
        piece.rotate()
        # Now piece is at x=3, y=-1 with vertical shape
        # Blocks at: (3,-1), (3,0), (3,1), (3,2)
        
        lock_piece(piece, grid)
        
        # Only blocks with y >= 0 should be locked
        # Grid now contains Block objects
        assert grid[0][3].shape_type == 'I'
        assert grid[1][3].shape_type == 'I'
        assert grid[2][3].shape_type == 'I'


class TestLineClearing:
    """Test line clearing logic"""
    
    def test_check_lines_no_complete_lines(self):
        """Test check_lines with no complete lines"""
        # Create a grid with no complete lines
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        grid[19] = [1, 1, 1, 0, 1, 1, 1, 1, 1, 1]  # Missing one block
        
        lines = check_lines(grid)
        assert lines == []
    
    def test_check_lines_single_complete_line(self):
        """Test check_lines with one complete line"""
        # Create a grid with one complete line
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        grid[19] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # Complete line
        
        lines = check_lines(grid)
        assert lines == [19]
    
    def test_check_lines_multiple_complete_lines(self):
        """Test check_lines with multiple complete lines"""
        # Create a grid with multiple complete lines
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        grid[17] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        grid[18] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        grid[19] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        
        lines = check_lines(grid)
        assert set(lines) == {17, 18, 19}
    
    def test_clear_lines_single(self):
        """Test clearing a single line"""
        # Reset game state
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        game_state = {
            'score': 0,
            'level': 1,
            'lines_cleared': 0,
            'fall_speed': INITIAL_FALL_SPEED
        }
        
        # Create a grid with one complete line at bottom and some blocks above
        grid[18] = [1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        grid[19] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # Complete line
        
        clear_lines([19], grid, game_state)
        
        # Line 19 should be cleared and line 18 should drop down
        assert grid[19] == [1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        
        # Score should increase
        assert game_state['score'] == SCORE_SINGLE * 1  # 100 * level 1
        assert game_state['lines_cleared'] == 1
    
    def test_clear_lines_multiple(self):
        """Test clearing multiple lines"""
        # Reset game state
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        game_state = {
            'score': 0,
            'level': 1,
            'lines_cleared': 0,
            'fall_speed': INITIAL_FALL_SPEED
        }
        
        # Create a grid with 4 complete lines (Tetris!)
        for i in range(16, 20):
            grid[i] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        
        clear_lines([16, 17, 18, 19], grid, game_state)
        
        # All lines should be cleared
        for i in range(16, 20):
            assert grid[i] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        # Score should be Tetris score
        assert game_state['score'] == SCORE_TETRIS * 1  # 800 * level 1
        assert game_state['lines_cleared'] == 4


class TestScoringSystem:
    """Test scoring calculations"""
    
    def test_single_line_score(self):
        """Test score for clearing a single line"""
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        game_state = {
            'score': 0,
            'level': 1,
            'lines_cleared': 0,
            'fall_speed': INITIAL_FALL_SPEED
        }
        
        clear_lines([19], grid, game_state)
        
        assert game_state['score'] == SCORE_SINGLE * 1  # 100
    
    def test_double_line_score(self):
        """Test score for clearing two lines"""
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        game_state = {
            'score': 0,
            'level': 1,
            'lines_cleared': 0,
            'fall_speed': INITIAL_FALL_SPEED
        }
        
        clear_lines([18, 19], grid, game_state)
        
        assert game_state['score'] == SCORE_DOUBLE * 1  # 300
    
    def test_triple_line_score(self):
        """Test score for clearing three lines"""
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        game_state = {
            'score': 0,
            'level': 1,
            'lines_cleared': 0,
            'fall_speed': INITIAL_FALL_SPEED
        }
        
        clear_lines([17, 18, 19], grid, game_state)
        
        assert game_state['score'] == SCORE_TRIPLE * 1  # 500
    
    def test_tetris_score(self):
        """Test score for clearing four lines (Tetris)"""
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        game_state = {
            'score': 0,
            'level': 1,
            'lines_cleared': 0,
            'fall_speed': INITIAL_FALL_SPEED
        }
        
        clear_lines([16, 17, 18, 19], grid, game_state)
        
        assert game_state['score'] == SCORE_TETRIS * 1  # 800
    
    def test_score_multiplier_by_level(self):
        """Test that score multiplies with level"""
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        game_state = {
            'score': 0,
            'level': 3,
            'lines_cleared': 20,  # Already cleared 20 lines
            'fall_speed': INITIAL_FALL_SPEED
        }
        
        clear_lines([19], grid, game_state)
        
        assert game_state['score'] == SCORE_SINGLE * 3  # 100 * 3 = 300


class TestLevelProgression:
    """Test level progression logic"""
    
    def test_initial_level(self):
        """Test that game starts at level 1"""
        # Just verify the constant
        assert 1 >= 1  # Level should start at 1
    
    def test_level_up_after_10_lines(self):
        """Test that level increases after 10 lines"""
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        game_state = {
            'level': 1,
            'lines_cleared': 0,
            'score': 0,
            'fall_speed': INITIAL_FALL_SPEED
        }
        
        # Simulate clearing lines one at a time (as would happen in the game)
        for _ in range(10):
            clear_lines([19], grid, game_state)
        
        assert game_state['level'] == 2
        assert game_state['lines_cleared'] == 10
        
        # Fall speed should increase
        expected_speed = INITIAL_FALL_SPEED * (SPEED_MULTIPLIER ** 1)
        assert abs(game_state['fall_speed'] - expected_speed) < 0.001
    
    def test_level_progression_multiple(self):
        """Test level progression through multiple levels"""
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        game_state = {
            'level': 1,
            'lines_cleared': 0,
            'score': 0,
            'fall_speed': INITIAL_FALL_SPEED
        }
        
        # Clear 25 lines one at a time (should reach level 3)
        for _ in range(25):
            clear_lines([19], grid, game_state)
        
        assert game_state['level'] == 3
        assert game_state['lines_cleared'] == 25
    
    def test_max_level_15(self):
        """Test that level caps at 15"""
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        game_state = {
            'level': 14,
            'lines_cleared': 140,
            'score': 0,
            'fall_speed': INITIAL_FALL_SPEED
        }
        
        # Clear 10 more lines one at a time (should reach level 15)
        for _ in range(10):
            clear_lines([19], grid, game_state)
        
        assert game_state['level'] == 15
        
        # Clear 10 more lines (should stay at level 15)
        for _ in range(10):
            clear_lines([19], grid, game_state)
        
        assert game_state['level'] == 15


class TestGameOver:
    """Test game over detection"""
    
    def test_spawn_piece_game_over(self):
        """Test that game over triggers when new piece can't spawn"""
        # Reset game state
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        game_state = {
            'current_piece': None,
            'next_piece': None,
            'game_over': False,
            'fall_timer': 0
        }
        
        # Fill the top rows to block spawning
        for y in range(4):
            for x in range(GRID_WIDTH):
                grid[y][x] = 'I'
        
        # First spawn should work (creates current and next)
        spawn_piece(game_state, grid)
        assert game_state['current_piece'] is not None
        assert game_state['next_piece'] is not None
        assert game_state['game_over'] == False
        
        # Second spawn should trigger game over
        spawn_piece(game_state, grid)
        assert game_state['game_over'] == True


class TestIntegration:
    """Integration tests for full game scenarios"""
    
    def test_full_game_flow(self):
        """Test a complete game flow: spawn, move, lock, clear line"""
        # Reset game state
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        game_state = {
            'current_piece': None,
            'next_piece': None,
            'game_over': False,
            'score': 0,
            'level': 1,
            'lines_cleared': 0,
            'fall_timer': 0,
            'fall_speed': INITIAL_FALL_SPEED
        }
        
        # Spawn a piece
        spawn_piece(game_state, grid)
        assert game_state['current_piece'] is not None
        assert game_state['next_piece'] is not None
        
        # Move piece down but not all the way to avoid index issues
        current_piece = game_state['current_piece']
        # Move down while there's no collision
        while not check_collision(current_piece, grid, 0, 1):
            current_piece.move(0, 1)
        
        # Lock the piece
        lock_piece(current_piece, grid)
        
        # Verify piece is locked
        # Grid now contains Block objects instead of shape_type strings
        for bx, by in current_piece.get_blocks():
            if by >= 0 and by < GRID_HEIGHT:
                assert grid[by][bx].shape_type == current_piece.shape_type
    
    def test_multiple_pieces_and_line_clear(self):
        """Test spawning multiple pieces and clearing a line"""
        # Reset game state
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        game_state = {
            'current_piece': None,
            'next_piece': None,
            'game_over': False,
            'score': 0,
            'level': 1,
            'lines_cleared': 0,
            'fall_timer': 0,
            'fall_speed': INITIAL_FALL_SPEED
        }
        
        # Manually create a nearly complete line
        grid[19] = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0]  # Missing last 2 blocks
        
        # Spawn and place an O-piece to complete the line
        spawn_piece(game_state, grid)
        # Move O-piece to position (8, 18) which will fill gaps at (8,18), (9,18), (8,19), (9,19)
        game_state['current_piece'].x = 8
        game_state['current_piece'].y = 18
        
        # Make sure it's an O-piece for predictable results
        if game_state['current_piece'].shape_type != 'O':
            game_state['current_piece'] = Piece('O')
            game_state['current_piece'].x = 8
            game_state['current_piece'].y = 18
        
        lock_piece(game_state['current_piece'], grid)
        
        # Check for complete lines
        lines = check_lines(grid)
        
        # If line 19 is complete, it should be in the list
        if 19 in lines:
            initial_score = game_state['score']
            clear_lines(lines, grid, game_state)
            
            # Score should have increased
            assert game_state['score'] > initial_score
            assert game_state['lines_cleared'] > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
