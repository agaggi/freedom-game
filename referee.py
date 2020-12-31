# Used to easily obtain diagonals
import numpy as np

class Referee:

    def __init__(self):

        '''Class implements methods to enforce rules and manage the game.'''

        self.current = 'Player 1'
        self.p1_score = 0
        self.p2_score = 0

        self.move = 0
        self.last_placed = ()


    def valid_move(self, board, x, y):

        '''Determines whether a move is valid or not.

        The function will check for various input errors, such as entering a non-integer
        value, if the length of the board is exceeded, if the selected coordinate is
        occupied etc. Whether `freedom` will be granted will also be determined.

        :param board: The passed in board state
        :param x: The x-coordinate (aka the row)
        :param y: The y-coordinate (aka the column)
        :return: True/False, whether the move is valid or not
        '''

        if not x.isdigit() or not y.isdigit():

            return False

        x, y = int(x), int(y)

        if x < 0 or y < 0 or \
           x >= len(board) or y >= len(board) or \
           board[x][y] != '*':

            return False

        if self.move == 0:

            self.last_placed = (x, y)
            return True

        last_x, last_y = self.last_placed

        # Top left corner, no need to check above or left
        if last_x == 0 and last_y == 0:

            # Freedom mechanic
            if board[last_x][last_y+1] != '*' and board[last_x+1][last_y] != '*':

                self.last_placed = (x, y)
                return True

            if (x, y) == (last_x, last_y+1) or (x, y) == (last_x+1, last_y):

                self.last_placed = (x, y)
                return True

        # Top right corner, no need to check above or right
        if last_x == 0 and last_y == len(board) - 1:

            # Freedom mechanic
            if board[last_x][last_y-1] != '*' and board[last_x+1][last_y] != '*':

                self.last_placed = (x, y)
                return True

            if (x, y) == (last_x, last_y-1) or (x, y) == (last_x+1, last_y):

                self.last_placed = (x, y)
                return True

        # Bottom left corner, no need to check below or left
        if last_x == len(board) - 1 and last_y == 0:

            # Freedom mechanic
            if board[last_x][last_y+1] != '*' and board[last_x-1][last_y] != '*':

                self.last_placed = (x, y)
                return True

            if (x, y) == (last_x, last_y+1) or (x, y) == (last_x-1, last_y):

                self.last_placed = (x, y)
                return True

        # Bottom right corner, no need to check above or right
        if last_x == len(board) - 1 and last_y == len(board) - 1:

            # Freedom mechanic
            if board[last_x][last_y-1] != '*' and board[last_x-1][last_y] != '*':

                self.last_placed = (x, y)
                return True

            if (x, y) == (last_x, last_y-1) or (x, y) == (last_x-1, last_y):

                self.last_placed = (x, y)
                return True

        # If we're in the first row, no need to check above
        if last_x == 0:

            # Freedom mechanic
            if board[last_x][last_y+1] != '*' and board[last_x][last_y-1] != '*' and \
               board[last_x+1][last_y] != '*':

                self.last_placed = (x, y)
                return True

            if (x, y) == (last_x, last_y+1) or (x, y) == (last_x, last_y-1) or \
               (x, y) == (last_x+1, last_y):

                self.last_placed = (x, y)
                return True

        # If we're in the first column, no need to check left
        if last_y == 0:

            # Freedom mechanic
            if board[last_x+1][last_y] != '*' and board[last_x-1][last_y] != '*' and \
               board[last_x][last_y+1] != '*':

                self.last_placed = (x, y)
                return True

            if (x, y) == (last_x+1, last_y) or (x, y) == (last_x-1, last_y) or \
               (x, y) == (last_x, last_y+1):

                self.last_placed = (x, y)
                return True

        # If we're in the last row, no need to check down
        if last_x == len(board) - 1:

            # Freedom mechanic
            if board[last_x][last_y+1] != '*' and board[last_x][last_y-1] != '*' and \
               board[last_x-1][last_y] != '*':

                self.last_placed = (x, y)
                return True

            if (x, y) == (last_x, last_y+1) or (x, y) == (last_x, last_y-1) or \
               (x, y) == (last_x-1, last_y):

                self.last_placed = (x, y)
                return True

        # If we're in the last column, no need to check right
        if last_y == len(board) - 1:

            # Freedom mechanic
            if board[last_x+1][last_y] != '*' and board[last_x-1][last_y] != '*' and \
               board[last_x][last_y-1] != '*':

                self.last_placed = (x, y)
                return True

            if (x, y) == (last_x+1, last_y) or (x, y) == (last_x-1, last_y) or \
               (x, y) == (last_x, last_y-1):

                self.last_placed = (x, y)
                return True

        # If we're in the center region of the board
        if 0 < last_x < len(board) - 1 and 0 < last_y < len(board) - 1:

            # Freedom mechanic
            if board[last_x+1][last_y] != '*' and board[last_x-1][last_y] != '*' and \
               board[last_x][last_y+1] != '*' and board[last_x][last_y-1] != '*':

                self.last_placed = (x, y)
                return True

            if (x, y) == (last_x+1, last_y) or (x, y) == (last_x-1, last_y) or \
               (x, y) == (last_x, last_y+1) or (x, y) == (last_x, last_y-1):

                self.last_placed = (x, y)
                return True

        return False


    def player_swap(self):

        '''Swaps the players, allowing for players to take turns.'''

        if self.current == 'Player 1':

            self.current = 'Player 2'

        else:

            self.current = 'Player 1'

        self.move += 1


    def assign_scores(self, board):

        '''Assigns scores to players by checking horizontal and diagonal directions.

        This function makes use of `Referee.get_scores()` in order to assign scores.
        The board will be split up into directions that need to be checked. `numpy` is
        used to easily obtain diagonals. The following is an example of how a board would
        look like when points need to be assigned:

        ```
        ------ Scoreboard ------
        ● Player 1: 2
        ○ Player 2: 2
        ------------------------

        Move: 16
        Last Placed: (2, 4)

        ● ● ● ● * *
        ○ ○ ○ ○ * *
        * * * * ○ ●
        * * * ○ ● *
        * * ○ ● * *
        * ○ ● * * *
        ```

        :param board: The current board state to be checked
        '''

        self.p1_score = 0
        self.p2_score = 0

        # Horizontal check
        for horizontal in board:

            self.get_scores(horizontal)

        # Diagonal check

        # Code retreived from first response - https://bit.ly/3ojEgi5
        b_array = np.array(board)
        diagonals = [b_array[::-1, :].diagonal(i) for i in range(-b_array.shape[0] + 1, \
                                                                 b_array.shape[1])]
        diagonals.extend(b_array.diagonal(i) for i in range(b_array.shape[1]-1, \
                                                            -b_array.shape[0],-1))

        diagonals = [n.tolist() for n in diagonals]
        # End of retreived code

        for diagonal in diagonals:

            self.get_scores(diagonal)


    def get_scores(self, direction):

        '''Assigns / deducts points to players depending on the board's status.

        Players will receive a point if they have exactly four stones of their color in
        either a horizontal or diagonal manner. If there are more than four stones of the
        same color in a horizontal or diagonal manner, a point is deducted from the
        player.

        :param direction: The direction to be checked
        '''

        white = '●'
        black = '○'

        white_count = 0
        black_count = 0

        # Counter for each color increases until interupted
        for char in direction:

            if char == white:

                white_count += 1
                black_count = 0

                # Add a point
                if white_count == 4:

                    self.p1_score += 1

                # Deduct a point
                if white_count == 5:

                    self.p1_score -= 1

            elif char == black:

                black_count += 1
                white_count = 0

                if black_count == 4:

                    self.p2_score += 1

                if black_count == 5:

                    self.p2_score -= 1

            # If an empty spot (i.e. *) interupts the sequence
            else:

                white_count = 0
                black_count = 0


    def print_scoreboard(self):

        '''Prints the current score of each player.'''

        print(f'''------ Scoreboard ------
● Player 1: {self.p1_score}
○ Player 2: {self.p2_score}
------------------------
''')


    def completion_check(self, board):

        '''Checks if all spaces on the board are filled.

        :param board: A board state to be checked for completion
        :return: True/False, whether the board is full or not
        '''

        vacant_spaces = 0

        for i in range(len(board)):

            vacant_spaces += board[i].count('*')

        if vacant_spaces == 0:

            return True

        return False


    def declare_winner(self, board):

        '''Declares the winner if the board is full or if a player does not want to
        place their last stone on the board.
        '''

        self.assign_scores(board)

        if self.p1_score > self.p2_score:

            print('\nPlayer 1 wins the game!\n')

        elif self.p2_score > self.p1_score:

            print('\nPlayer 2 wins the game!\n')

        else:

            print("\nIt's a draw!\n")

        exit()
