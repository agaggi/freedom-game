import os
import copy

from referee import Referee

class Board:

    def __init__(self, difficulty):

        '''Class implements methods to generate and determine the next best possible move.

        :param difficulty: beginner/novice/experienced. Determines board size
        '''

        self.difficulty = difficulty
        self.board = []

        self.p1_stone = '●'
        self.p2_stone = '○'

        self.ref = Referee()


    def generate_board(self):

        '''Generates the board based on the difficulty the user selected.

            - Beginner: 6x6
            - Novice: 8x8
            - Experienced: 10x10
        '''

        if self.difficulty == 'beginner':

            board_size = 6

        elif self.difficulty == 'novice':

            board_size = 8

        elif self.difficulty == 'experienced':

            board_size = 10

        else:

            exit('\n-- Invalid argument entered, see README file for instructions --\n')

        self.board = [['*' for j in range(board_size)] for i in range(board_size)]

        while not self.ref.completion_check(self.board):

            self.prompt()

        self.ref.declare_winner(self.board)


    def refresh_screen(self):

        '''Clears the terminal window for nicer UI/UX.'''

        # For Windows
        if os.name == 'nt':

            _ = os.system('cls')

        # For MacOS and Linux
        else:

            _ = os.system('clear')

        self.ref.print_scoreboard()
        print(f'Move: {self.ref.move}')
        print(f'Last Placed: {self.ref.last_placed}\n')
        self.print_board()


    def print_board(self):

        '''Prints the current board state.'''

        for i in range(len(self.board)):

            print(' '.join(self.board[i]))


    def error_message(self):

        '''Lets the user know that they made an error inputting their coordinates.'''

        input('''\n :: Something is wrong with your input. Ensure that:

    1. You entered integer values that do not exceed board size
    2. You enter coordinates that have a stone adjacent to it unless you have freedom

[Press ENTER to continue]
''')


    def place_stone(self, x, y):

        '''Places a stone on the board with respect to who's turn it is.

        :param x: The entered x-coordinate
        :param y: The entered y-coordinate
        '''

        if self.ref.current == 'Player 1':

            self.board[x][y] = self.p1_stone

        else:

            self.board[x][y] = self.p2_stone


    def prompt(self):

        '''Prompts the human player, Player 1, to enter coordinates to where they want to
        place their next piece. If it is the AI's turn, Player 2, `Board.minimax()` is
        called to make the next move.

        Input for Player 1 is checked for whether it is valid or not. Invalid input
        includes:

        1. If anything other than an integer is entered (i.e. a a)
        2. If the piece is not adjacent to the last placed piece (unless you have freedom)
        3. If your integer values exceed board dimensions or are less than 0
        '''

        self.refresh_screen()

        if self.ref.current == 'Player 1':

            x, y = input(f'\n{self.ref.current}, where would you like to place a stone? ').split()

            # Loop until a valid choice is made
            while not self.ref.valid_move(self.board, x, y):

                self.error_message()
                self.refresh_screen()

                x, y = input(f'\n{self.ref.current}, where would you like to place a stone? ').split()

        # If it is the AI's turn
        else:

            last_x, last_y = self.ref.last_placed
            value, x, y = self.minimax([self.board, (last_x, last_y)], 6,
                                       float('-inf'), float('inf'), True)

            self.ref.valid_move(self.board, str(x), str(y))

        x, y = int(x), int(y)
        self.place_stone(x, y)

        # Check for any change in scores after the last move, then swap
        self.ref.assign_scores(self.board)
        self.ref.player_swap()


    def make_possible_moves(self, board, stone, coordinates):

        '''Uses coordinates passed in to generate possible board states.

        :param board: The current board state
        :param stone: The current player's stone
        :param coordinates: The list of coordinates for possible moves
        :return: The list of possible board states with the coords of the moved piece
        '''

        moves = []

        # Create a board state for each coordinate (i.e. possibility)
        for coordinate in coordinates:

            x, y = coordinate

            if board[x][y] == '*':

                board_copy = copy.deepcopy(board)
                board_copy[x][y] = stone
                moves.append([board_copy, (x, y)])

        return moves


    def generate_moves(self, board, stone):

        '''Generates the possible moves that can be made from a board state.

        :param board: The board state to have its next moves generated
        :param stone: The current player's stone
        :return: The possible moves that can be made from the current state
        '''

        possible_moves = []
        coords = []

        # List format: [board state, coordinates of last placed piece]
        x, y = board[1]

        # We don't want to enter the seperate cases if both are true
        both_cases = False

        # Top left corner
        if x == 0 and y == 0:

            coords.append((x+1, y))
            coords.append((x, y+1))

            both_cases = True

        # Top right corner
        if x == 0 and y == len(board[0]) - 1:

            coords.append((x+1, y))
            coords.append((x, y-1))

            both_cases = True

        # Bottom left corner
        if x == len(board[0]) - 1 and y == 0:

            coords.append((x-1, y))
            coords.append((x, y+1))

            both_cases = True

        # Bottom right corner
        if x == len(board[0]) - 1 and y == len(board[0]) - 1:

            coords.append((x-1, y))
            coords.append((x, y-1))

            both_cases = True

        # First row
        if x == 0 and not both_cases:

            coords.append((x+1, y))
            coords.append((x, y+1))
            coords.append((x, y-1))

        # First column
        if y == 0 and not both_cases:

            coords.append((x+1, y))
            coords.append((x-1, y))
            coords.append((x, y+1))

        # Last row
        if x == len(board[0]) - 1 and not both_cases:

            coords.append((x-1, y))
            coords.append((x, y+1))
            coords.append((x, y-1))

        # Last column
        if y == len(board[0]) - 1 and not both_cases:

            coords.append((x+1, y))
            coords.append((x-1, y))
            coords.append((x, y-1))

        # Center region of the board
        if 0 < x < len(board[0]) - 1 and 0 < y < len(board[0]) - 1:

            coords.append((x+1, y))
            coords.append((x-1, y))
            coords.append((x, y+1))
            coords.append((x, y-1))

        # Generate possible board states using the list of coordinates
        possible_moves = self.make_possible_moves(board[0], stone, coords)

        # Freedom rule
        # If no possible moves, get all empty spaces & consider them possible moves
        if len(possible_moves) == 0:

            for i in range(len(board[0])):

                for j in range(len(board[0])):

                    if board[0][i][j] == '*':

                        coords.append((i, j))

            possible_moves = self.make_possible_moves(board[0], stone, coords)

        return possible_moves


    def board_value(self, board):

        '''Computes the value of the board state passed in.

        :param board: [board state, (last_x, last_y)]
        :return: A list in the form [value, x_coord, y_coord]
        '''

        self.ref.assign_scores(board[0])
        return self.ref.p2_score - self.ref.p1_score, board[1][0], board[1][1]


    def minimax(self, position, depth, alpha, beta, is_ai):

        '''The Minimax algorithm.

        This function uses the minimax algorithm in order to determine the best possible
        move from a current state. Alpha-Beta pruning is also used in order to increase
        performance of the program.

        :param position: [board state, (last_x, last_y)]
        :param depth: How many moves we want to look ahead
        :param alpha: The alpha value of a node (initially -Infinity)
        :param beta: The beta value of a node (initially Infinity)
        :param AI: True/False, whether it's the AI's turn to move
        :return: (value of node, x_coord, y_coord)
        '''

        # If the depth is 0 or the game is finished
        if depth == 0 or self.ref.completion_check(position[0]):

            return self.board_value(position)

        x_pos = None
        y_pos = None

        if is_ai:

            max_value = float('-inf')
            possible_moves = self.generate_moves(position, self.p2_stone)

            for child in possible_moves:

                state_value, x, y = self.minimax(child, depth-1, alpha, beta, False)

                if state_value > max_value:

                    max_value = state_value
                    x_pos = child[1][0]
                    y_pos = child[1][1]

                alpha = max(alpha, state_value)

                if beta <= alpha:

                    break

            return max_value, x_pos, y_pos

        # If the algorithm is calculating the player's possible turn
        min_value = float('inf')
        possible_moves = self.generate_moves(position, self.p1_stone)

        for child in possible_moves:

            state_value, x, y = self.minimax(child, depth-1, alpha, beta, True)

            if state_value < min_value:

                min_value = state_value
                x_pos = child[1][0]
                y_pos = child[1][1]

            beta = min(beta, state_value)

            if beta <= alpha:

                break

        return min_value, x_pos, y_pos
