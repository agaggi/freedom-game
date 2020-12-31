import sys

from board import Board

def main():

    '''Main function for the Freedom AI program.'''

    difficulty = sys.argv[1].lower()
    board = Board(difficulty)

    board.generate_board()


if __name__ == '__main__':

    main()
