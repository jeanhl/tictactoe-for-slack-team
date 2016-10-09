class TTT_Game(object):

    def __init__(self, channel, player1, player2):
        self.channel = channel
        self.player1 = player1
        self.player2 = player2
        self.turn_count = 1
        self.max_turns = 10
        self.board = [1, 2, 3,
                      4, 5, 6,
                      7, 8, 9]

    def get_formatted_board(self):
        """ Returns the board in the tictactoe format """
        return ("```  {}  |  {}  |  {}\n".format(self.prettify(self.board[0]), self.prettify(self.board[1]), self.prettify(self.board[2])) +
                "-----+-----+-----\n" +
                "  {}  |  {}  |  {}\n".format(self.prettify(self.board[3]), self.prettify(self.board[4]), self.prettify(self.board[5])) +
                "-----+-----+-----\n" +
                "  {}  |  {}  |  {}```".format(self.prettify(self.board[6]), self.prettify(self.board[7]), self.prettify(self.board[8]))
                )

    def prettify(self, content):
        """ Returns nicer board placements """
        if isinstance(content, int):
            return " " + content + " "
        elif content == "X":
            return "<X>"
        elif content == "O":
            return "(O)"
        else:
            return content

    def current_symbol(self):
        """ Switches turn. If move_count is odd, user1's turn. If move_count is
            even, user2's turn. """
        if self.turn_count % 2 != 0:
            return "X"
        else:
            return "O"

    def current_player(self):
        """ Keeps track of current player. """
        if self.turn_count % 2 != 0:
            return self.player1
        else:
            return self.player2

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
                print "Game ends with a winner"
                return True
            else:
                continue
