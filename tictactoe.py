def tictactoe():
    board = new_board()
    count = 1 
    while count < 10:
        input1 = (user_input() - 1)
        if isinstance(board[input1], int):
            board[input1] = current_user(count)
            board_template(board)
            if is_winner(count, board) is True:
                break
            count += 1 
        elif isinstance(board[input1], str):
            print "That spot is already taken"
            board_template(board)
        else:
            continue
   
    if count == 10:        
        print "This is a draw."
    play_again()


def new_board():
    """ Sets up a new board for 1 game """
    return  [1, 2, 3,
             4, 5, 6,
             7, 8, 9]

def current_user(count):
    """ Switches turn. If count is odd, user1's turn. If count is 
        even, user2's turn. """

    if count % 2 != 0:
        return "X"
    else: 
        return "O"

def is_winner(count, board):
    wins = [[0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]]
    for win in wins:
        if ( board[win[0]] == current_user(count) and
             board[win[1]] == current_user(count) and
             board[win[2]] == current_user(count) ):
            print "You win!!"
            return True
        else:
            continue


def board_template(board):
    """ This prints the board """
    print "     |     |     "
    print " ", board[0], " | ", board[1], " | ", board[2], " "
    print "-----+-----+-----" 
    print " ", board[3], " | ", board[4], " | ", board[5], " "
    print "-----+-----+-----"  
    print " ", board[6], " | ", board[7], " | ", board[8], " "
    print "     |     |     "


def user_input():
    # need to add in a check for strings 
    input = int(raw_input("Pick a spot: "))
    if 1 <= input <= 9:
        return input
    else:
        print "That spot is not on the board."
        return user_input()

def play_again():
    """Asks players if they want to play again"""
    answer = raw_input("Would you like to play again? \n Y for yes > ")
    if (answer == "Y" or answer == "Yes" or
        answer == "y" or answer == "yes"):
        tictactoe()
    else:
        print "Thank you for playing!" 




tictactoe()