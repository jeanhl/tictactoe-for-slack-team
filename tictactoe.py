import os
from flask import Flask, request, Response
from slackclient import SlackClient
from pprint import pprint
app = Flask(__name__)

SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')
SLACK_TEST_TOKEN = os.environ.get('SLACK_TEST_TOKEN')
SLACK_SLASH_TOKEN = os.environ.get('SLACK_SLASH_TOKEN')
SC = SlackClient(SLACK_TEST_TOKEN)

# to do to get 1 game going in 1 channel:
# figure out how to make a game object with the following attributes:
    
# make a function to parse the incoming text to find the first username and return it
# make a function to manage the dictionary to remember the game's history
# edit the code so that it adds to the history, loads the current board and checks for winner 

@app.route('/slack', methods=['POST'])
def inbound():
    """ Manages requests from the Slack channel"""
    if request.form.get('token') == SLACK_SLASH_TOKEN:
        channel = request.form.get('channel_name')
        username = request.form.get('user_name')
        text = request.form.get('text')
        player2 = get_second_player(text, channel)
        if player2 == None:
            msg = "There is an error. Please check your request for typos. :/"
            SC.api_call("chat.postMessage", as_user='false', channel=channel, text=msg)
        test_chatmsg(channel)
    return text + " and " + username + " are playing tictactoe in " + channel

    # if I call a bunch of functions here, will there be an error? Synchronous processes?

def test_chatmsg(channel):
    """ testing to see if board shows up on Slack channel """
    msg = show_board(get_new_board())
    return SC.api_call("chat.postMessage", as_user='false', channel=channel, text=msg)

def get_all_users():
    """ Gets all the users in the team, including Slackbot. """
    list_of_users = []
    dict_users = SC.api_call("users.list") # 
    dict_members = dict_users["members"]
    for each in dict_members:
        list_of_users.append(each["name"])
    return list_of_users


def get_second_player(text, channel):
    text = text.split()
    for word in text:
        if word in get_all_users():
            return word
        else:
             return None


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
    # play_again() #uncomment this line if want the option of asking to play again


def get_new_board():
    """ Sets up a new board for 1 game """
    return  [1, 2, 3,
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

# if want to play again, uncomment the section below
# def play_again():
#     """Asks players if they want to play again"""
#     answer = raw_input("Would you like to play again? \n Y for yes > ")
#     if (answer.lower() == "y" or answer.lower() == "yes"):
#         play_tictactoe()
#     else:
#         print "Thank you for playing!" 



if __name__ == "__main__":
    app.run(debug=True)