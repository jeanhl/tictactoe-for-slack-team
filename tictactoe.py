def tictactoe():
    board = [1,2,3,
            4,5,6,
            7,8,9]

    while True:
        input1 = (user_input() - 1)
        if board[input1] != "X" and board[input1] != "O":
            board[input1] = "X"
            board_template(board)
        elif board[input1] == "X" or board[input1] == "O":
            print "That spot is already taken"
            board_template(board)
        else:
            continue



def board_template(board):
    print "     |     |     "
    print " ", board[0], " | ", board[1], " | ", board[2], " "
    print "-----+-----+-----"   
    print " ", board[3], " | ", board[4], " | ", board[5], " "
    print "-----+-----+-----"  
    print " ", board[6], " | ", board[7], " | ", board[8], " "
    print "     |     |     "



def user_input():
    # need to add in a check for strings 
    input = int(raw_input("Pick a spot:"))
    if 1<=input<=9:
        return input
    else:
        print "That spot is not on the board."
        user_input()

tictactoe()