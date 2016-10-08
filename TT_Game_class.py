class TTT_Game(object):

    def __init__(self, channel):
        self.channel = channel
        self.player1 = player1
        self.player2 = player2
        self.count = 1
        self.board = [1, 2, 3,
                      4, 5, 6,
                      7, 8, 9]


    def get_formatted_board(self):
        """ Returns the board in the tictactoe format """
        return ("```  {}  |  {}  |  {}\n".format(self.board[0], self.board[1], self.board[2]) +
            "-----+-----+-----\n" +
            "  {}  |  {}  |  {}\n".format(self.board[3], self.board[4], self.board[5]) +
            "-----+-----+-----\n" +
            "  {}  |  {}  |  {}```".format(self.board[6], self.board[7], self.board[8])
            )


    def current_symbol(self):
        """ Switches turn. If move_count is odd, user1's turn. If move_count is 
            even, user2's turn. """
        if self.count % 2 != 0:
            return "X"
        else: 
            return "O"

    def current_user(self):
        """ Keeps track of current player. """
        if self.count % 2 != 0:
            return self.player1
        else: 
            return self.player2


    def is_winner(symbol, self):
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
                print "~`~`~`~`~ Player", symbol, " winsss!!~`~`~`~`~"
                return True
            else:
                continue


