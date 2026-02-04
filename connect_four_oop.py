import numpy as np

class Player: # class 
    def __init__(self, name:str, piece:int): 
        self.name = name #attributes
        self.piece = piece # attributes

    def get_move(self, board):
        """Prompt the player for a move."""
        col = int(input(f"{self.name}, choose a column (0-6): "))
        return col

#class Agent:
    # code goes here 

class ConnectFourGame:
    def __init__(self):
        self.board = self.create_board()
        self.players = [Player("Player 1", 1), Player("Player 2", 2)] # update 
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
        col = player.get_move(self.board)

        if self.is_valid_location(col):
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