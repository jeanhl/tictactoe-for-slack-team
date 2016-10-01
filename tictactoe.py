def play_tictactoe():
    board = get_new_board()
    move_count = 1 
    max_turns = 10
    print "~~~ WELCOME TO TIC TAC TOE!!! ~~~"
    show_board(board)
    while move_count < max_turns:
        print current_user(move_count), "it's your turn."
        input1 = get_user_input()
        if isinstance(board[input1], int):
            board[input1] = current_symbol(move_count)
            show_board(board)
            if is_winner(move_count, board) is True:
                break
            move_count += 1 
        elif isinstance(board[input1], str):
            print "That spot is already taken"
            show_board(board)
        else:
            continue
   
    if move_count == max_turns:        
        print "This is a draw."
    play_again()


def get_new_board():
    """ Sets up a new board for 1 game """
    return  [1, 2, 3,
             4, 5, 6,
             7, 8, 9]


def show_board(board):
    """ This prints the board """
    print "\n\n     |     |     "
    print " ", board[0], " | ", board[1], " | ", board[2], " "
    print "-----+-----+-----" 
    print " ", board[3], " | ", board[4], " | ", board[5], " "
    print "-----+-----+-----"  
    print " ", board[6], " | ", board[7], " | ", board[8], " "
    print "     |     |     "


def get_user_input():
    input = raw_input("Pick a spot: ")
    try:
        int(input)
    except ValueError:
        print "Please type in a number"
        return get_user_input()
    if 1 <= int(input) <= 9:
        return (int(input)-1)
    else:
        print "That spot is not on the board."
        return get_user_input()


def current_symbol(move_count):
    """ Switches turn. If move_count is odd, user1's turn. If move_count is 
        even, user2's turn. """

    if move_count % 2 != 0:
        return "X"
    else: 
        return "O"


def current_user(move_count):
    """ Keeps track of current player. """

    return "Player " + current_symbol(move_count)


def is_winner(move_count, board):
    wins = [[0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]]
    for win in wins:
        if (board[win[0]] == current_symbol(move_count) and
            board[win[1]] == current_symbol(move_count) and
            board[win[2]] == current_symbol(move_count)):
            print "~`~`~`~`~",current_user(move_count), " winsss!!~`~`~`~`~"
            return True
        else:
            continue


def play_again():
    """Asks players if they want to play again"""
    answer = raw_input("Would you like to play again? \n Y for yes > ")
    if (answer.lower() == "y" or answer.lower() == "yes"):
        play_tictactoe()
    else:
        print "Thank you for playing!" 




play_tictactoe()