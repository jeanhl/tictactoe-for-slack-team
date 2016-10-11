class TTT_Game(object):
    """ Stores information of an ongoing game such as the players involved,
        whose turn it is, and the current state of the board. Has methods to
        format the board, get the current player and their symbol and check
        for a winner. """

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.turn_count = 1  # keep track of game progress
        self.max_turns = 10  # to check for a draw
        self.board = [1, 2, 3,
                      4, 5, 6,
                      7, 8, 9]

    def get_formatted_board(self):
        """ Returns the board in the tictactoe format """
        return ("``` {} | {} | {}\n".format(self.prettify(self.board[0]),
                                            self.prettify(self.board[1]),
                                            self.prettify(self.board[2])) +
                "-----+-----+-----\n" +
                " {} | {} | {}\n".format(self.prettify(self.board[3]),
                                         self.prettify(self.board[4]),
                                         self.prettify(self.board[5])) +
                "-----+-----+-----\n" +
                " {} | {} | {}```".format(self.prettify(self.board[6]),
                                          self.prettify(self.board[7]),
                                          self.prettify(self.board[8]))
                )

    def prettify(self, content):
        """ Returns nicer board placements """
        # this helps players distinguish between the numbers,
        # Xs and Os on the board.
        if isinstance(content, int):
            return " {} ".format(content)
        elif content == "X":
            return "<X>"
        elif content == "O":
            return "(O)"
        else:
            return content

    def current_player(self):
        """ Switches turn. If move_count is odd, user1's turn.
            If move_count is even, user2's turn. """
        if self.turn_count % 2 != 0:
            return self.player1
        else:
            return self.player2

    def current_symbol(self):
        """ Keeps track of the current symbol to be placed on the board """
        if self.turn_count % 2 != 0:
            return "X"
        else:
            return "O"

    def is_winner(self, symbol):
        """ Checks if the new entry on the board is a winner """
        wins = [[0, 1, 2],
                [3, 4, 5],
                [6, 7, 8],
                [0, 3, 6],
                [1, 4, 7],
                [2, 5, 8],
                [0, 4, 8],
                [2, 4, 6]]
        for win in wins:
            if (self.board[win[0]] == symbol and
                self.board[win[1]] == symbol and
                self.board[win[2]] == symbol):
                return True
        return False
