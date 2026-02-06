import numpy as np

class Player: # class 
    def __init__(self, name:str, piece:int): 
        self.name = name #attributes
        self.piece = piece # attributes

    def get_move(self, board):
        """Prompt the player for a move."""
        while True:
            try:
                return int(input(f"{self.name}, choose a column (0-6): "))
            except ValueError:
                print("Please enter a number between 0 and 6")

class Agent:
    def __init__(self, name:str, piece:int, opponent_piece:int = 1):
        self.name = name
        self.piece = piece
        self.opponent_piece = opponent_piece
    
    def get_valid_cols(self, board):
        valid_cols = [c for c in range(board.shape[1]) if board[5][c]==0]        
        return valid_cols
    
    def ai_get_next_open_row(self, board, col):
        """Get the next open row in a column."""
        for r in range(board.shape[0]):
            if board[r][col] == 0:
                return r
        return None
    
    def ai_winning_move(self, board, piece): #Checking if the move being played will end the game
        rows, cols = board.shape
        # Horizontal
        for r in range(rows):
            for c in range(cols-3):
                if (board[r][c]==piece and board[r][c+1]==piece and board[r][c+2]==piece and board[r][c+3]==piece):
                    return True
        # Vertical
        for c in range(cols):
            for r in range(rows-3):
                if (board[r][c]==piece and board[r+1][c]==piece and board[r+2][c]==piece and board[r+3][c]==piece):
                    return True
        # Positively sloped diagonal
        for r in range(rows-3):
            for c in range(cols-3):
                if (board[r][c]==piece and board[r+1][c+1]==piece and board[r+2][c+2]==piece and board[r+3][c+3]==piece):
                    return True
        # Negatively sloped diagonal
        for r in range(3,rows):
            for c in range(cols-3):
                if (board[r][c]==piece and board[r-1][c+1]==piece and board[r-2][c+2]==piece and board[r-3][c+3]==piece):
                    return True
        
        return False
    
    def simulate_drop(self, board, col, piece):
        """Simulate a board in the background to check play moves on, thereby checking if the move being played is a winning one"""
        r = self.ai_get_next_open_row(board, col)

        if r is None:
            return None
        
        sim_board = board.copy()
        sim_board[r][col] = piece

        return sim_board
    
    def get_move(self, board):
        #The agent's "intelligence" is located here

        valid_cols = self.get_valid_cols(board)
        if not valid_cols:
            raise ValueError("No more moves available, the board is full!");
    
        #0.) Checks for any moves that *give* the opponent a chance to end the game (for example, putting a piece next to where a 3-diagonal exists, allowing the user to end the game on the next turn)
        bad_moves = []
        for col in valid_cols:
            ai_turn = self.simulate_drop(board, col, self.piece)
            if ai_turn is not None:
                opp_valid_cols = [c for c in range(ai_turn.shape[1]) if ai_turn[5][c]==0]
                for opp_col in opp_valid_cols:
                    user_turn = self.simulate_drop(ai_turn, opp_col, self.opponent_piece)
                    if user_turn is not None and self.ai_winning_move(user_turn, self.opponent_piece):
                        bad_moves.append(col)
                        break
        
        safe_moves = [c for c in valid_cols if c not in bad_moves]

        #1.) A winning move is available. Play the winning move
        for col in valid_cols:
            turn = self.simulate_drop(board, col, self.piece)
            if turn is not None and self.ai_winning_move(turn, self.piece):
                return col

        #2.) Opponent has a winning move available on their turn. Block the opponent from making that move
        for col in valid_cols:
            turn = self.simulate_drop(board, col, self.opponent_piece)
            if turn is not None and self.ai_winning_move(turn, self.opponent_piece):
                return col
        
        #3.) In case none of the above moves are available, the agent tries to choose a column closest to the center, to maximise future possibilities
        candidate_moves = safe_moves if safe_moves else valid_cols
        center = board.shape[1]//2
        preferred_order = sorted(candidate_moves, key= lambda x: abs(x-center))
        best_col = preferred_order[0]
        if best_col == center:
            return best_col
        # Choosing randomly between the columns closest to the center if the center itself isn't available
        min_dist = abs(best_col - center)
        closest = [c for c in preferred_order if abs(c-center) == min_dist]
        return int(np.random.choice(closest))


class ConnectFourGame:
    def __init__(self):
        self.board = self.create_board()
        self.players = [Player("Player 1", 1), Agent("Agent", 2, opponent_piece=1)]
        self.current_player = 0
        self.game_over = False

    def create_board(self):
        """Create an empty Connect Four board."""
        return np.zeros((6, 7), dtype=int)

    def print_board(self):
        """Print the Connect Four board with labeled headers and improved formatting."""
        print("  0   1   2   3   4   5   6")  # Column headers
        print("+---+---+---+---+---+---+---+")  # Top border

        flipped_board = np.flip(self.board, 0)
        for row in flipped_board:
            print("|", end="")
            for cell in row:
                if cell == 0:
                    print("   |", end="")  # Empty cell
                elif cell == 1:
                    print(" O |", end="")  # Player 1's piece
                else:
                    print(" X |", end="")  # Player 2's piece
            print("\n+---+---+---+---+---+---+---+")  # Row separator

    def is_valid_location(self, col):
        """Check if a move is valid."""
        return self.board[5][col] == 0

    def get_next_open_row(self, col):
        """Get the next open row in a column."""
        for r in range(6):
            if self.board[r][col] == 0:
                return r

    def drop_piece(self, row, col, piece):
        """Drop a piece into the board."""
        self.board[row][col] = piece

    def winning_move(self, piece):
        """Check if the last move resulted in a win."""
        # Check horizontal locations
        for c in range(4):
            for r in range(6):
                if (self.board[r][c] == piece and
                    self.board[r][c+1] == piece and
                    self.board[r][c+2] == piece and
                    self.board[r][c+3] == piece):
                    return True

        # Check vertical locations
        for c in range(7):
            for r in range(3):
                if (self.board[r][c] == piece and
                    self.board[r+1][c] == piece and
                    self.board[r+2][c] == piece and
                    self.board[r+3][c] == piece):
                    return True

        # Check positively sloped diagonals
        for c in range(4):
            for r in range(3):
                if (self.board[r][c] == piece and
                    self.board[r+1][c+1] == piece and
                    self.board[r+2][c+2] == piece and
                    self.board[r+3][c+3] == piece):
                    return True

        # Check negatively sloped diagonals
        for c in range(4):
            for r in range(3, 6):
                if (self.board[r][c] == piece and
                    self.board[r-1][c+1] == piece and
                    self.board[r-2][c+2] == piece and
                    self.board[r-3][c+3] == piece):
                    return True

        return False

    def play_turn(self):
        """Handle a single turn for the current player."""
        player = self.players[self.current_player]
        while True:
            col = player.get_move(self.board)

            if not isinstance(col, int):
                print("The column you entered is invalid. Please enter a column between 0-6")
                continue

            if col < 0 or col >= self.board.shape[1]:
                print("The column you entered is invalid. Please enter a column between 0-6")
                continue

            if not self.is_valid_location(col):
                print("The column is full! Please try another column")
                continue

            #if the code gets to this point, then the value is valid
            break

        row = self.get_next_open_row(col)
        self.drop_piece(row, col, player.piece)

        if self.winning_move(player.piece):
                print(f"{player.name} wins!")
                self.game_over = True

    def switch_player(self):
        """Switch to the other player."""
        self.current_player = (self.current_player + 1) % 2 # assumes 0 or 1 

    def is_board_full(self):
        """Check if the board is full (tie)."""
        return np.all(self.board != 0)

    def play_game(self):
        """Main game loop."""
        self.print_board()

        while not self.game_over:
            self.play_turn()
            self.print_board()

            if self.is_board_full():
                print("It's a tie!")
                self.game_over = True

            self.switch_player()

if __name__ == "__main__":
    print("Welcome to Connect Four!")
    print("Player 1 is 'O' and Player 2 is 'X'.")
    print("Enter a column number (0-6) to drop your piece.\n")

    try:
        game = ConnectFourGame()
        game.play_game()
    except KeyboardInterrupt:
        print("\nGame interrupted. Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Thanks for playing!")