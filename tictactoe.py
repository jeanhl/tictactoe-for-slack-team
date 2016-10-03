import os
from flask import Flask, request, Response
from slackclient import SlackClient
app = Flask(__name__)

SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')
SLACK_TEST_TOKEN = os.environ.get('SLACK_TEST_TOKEN')
SLACK_SLASH_TOKEN = os.environ.get('SLACK_SLASH_TOKEN')


@app.route('/slack', methods=['POST'])
def inbound():
    """ Manages requests from the Slack channel"""
    if request.form.get('token') == SLACK_SLASH_TOKEN:
        channel = request.form.get('channel_name')
        username = request.form.get('user_name')
        text = request.form.get('text')
        inbound_message = username + " in " + channel + " says: " + text
        print(inbound_message)
        test_chatmsg(channel, username)
    return show_board(get_new_board())


@app.route('/', methods=['GET'])
def test():
    return Response('It works!')


def test_chatmsg(channel, username):
    sc = SlackClient(SLACK_TEST_TOKEN)
    msg = show_board(get_new_board())
    return sc.api_call("chat.postMessage", as_user='false', channel=channel, text=msg)



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
            if is_winner(current_symbol(move_count), board) is True:
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
    return  [1, "X", 3,
             4, 5, 6,
             7, 8, 9]


def show_board(board):
    """ This prints the board """
    return ("```  {}  |  {}  |  {}\n".format(board[0], board[1], board[2]) +
            "-----+-----+-----\n" +
            "  {}  |  {}  |  {}\n".format(board[3], board[4], board[5]) +
            "-----+-----+-----\n" +
            "  {}  |  {}  |  {}```".format(board[6], board[7], board[8])
            )
    # print "\n\n     |     |     "
    # print " ", board[0], " | ", board[1], " | ", board[2], " "
    # print "-----+-----+-----" 
    # print " ", board[3], " | ", board[4], " | ", board[5], " "
    # print "-----+-----+-----"  
    # print " ", board[6], " | ", board[7], " | ", board[8], " "
    # print "     |     |     "


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


def is_winner(symbol, board):
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
        if (board[win[0]] == symbol and
            board[win[1]] == symbol and
            board[win[2]] == symbol):
            print "~`~`~`~`~ Player", symbol, " winsss!!~`~`~`~`~"
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



if __name__ == "__main__":
    app.run(debug=True)