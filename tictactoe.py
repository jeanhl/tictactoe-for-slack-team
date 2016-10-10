import os
import requests
import json
from flask import Flask, request
from slackclient import SlackClient
from TT_Game_class import TTT_Game
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "SLACKCODINGEXERCISE")

SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')
SLACK_TEST_TOKEN = os.environ.get('SLACK_TEST_TOKEN')
SLACK_SLASH_TOKEN = os.environ.get('SLACK_SLASH_TOKEN')
SC = SlackClient(SLACK_TEST_TOKEN)

ALL_GAMES = {}  # dictionary to keep track of all the game objects


@app.route('/')
def homepage():
    """ Shows a homepage on Heroku for debugging purposes"""
    return "TicTacToe is running."  # displayed on the homepage


@app.route('/slack', methods=['POST'])
def inbound():
    """ Manages requests from the Slack channel"""
    if request.form.get('token') == SLACK_SLASH_TOKEN:
        channel = str(request.form.get('channel_name'))
        username = str(request.form.get('user_name'))
        text = str(request.form.get('text'))
        response_url = str(request.form.get('response_url'))
        process_text_content(text, username, channel, response_url)
        return " "


def post_to_slack(msg, response_url, attachment=None):
    """ Posts game msgs to Slack """
    files = {"content-type": "application/json"}
    chunk = {"response_type": "in_channel",
             "text": msg,
             "attachments": [{"text": attachment}]}
    requests.request("POST", response_url, data=json.dumps(chunk), headers=files)


def process_text_content(text, username, channel, response_url):
    """ Processed the text input for different commands or just invalid inputs and
        calls the appropriate functions """
    # checks to see if the text is empty
    if len(text) == 0:
        msg = "Doesn't seem like there is anything there :/"
        post_to_slack(msg, response_url)

    # text is not empty. Take the first word in the text and process it
    else:
        # checks if the first word is a valid user in the team. If yes, get it
        # If none, gets None
        target_username = get_target_username(text)
        # checks if the first word is a number on the board. If yes, get it
        # If none, gets None
        placement_num = get_valid_placement(text)

        # if the word is none of the above, check to see if it is a command
        text = text.split()
        # a username is a command to start a new game
        if text[0].startswith("@"):
            start_new_game(channel, username, target_username, response_url)
        # command to end a game that anyone can do
        elif text[0] == "endgame":
            manual_end(username, channel, response_url)
        # command to show the help info that anyone can do
        elif text[0] == "help":
            display_help(response_url)
        # command to show the game status that anyone can do
        elif text[0] == "status":
            determine_game_status(channel, response_url)
        # an integer is a command to start a new game
        elif is_text_integer(text[0]):
            validate_and_make_move(username, channel, placement_num, response_url)
        # the text entered isn't a command or username or move
        else:
            msg = "I don't understand. Please enter */ttt help* for more info."
            post_to_slack(msg, response_url)


def start_new_game(channel, player1, player2, response_url):
    """ Initiates a new game oject if possible and
        announces a new game in the channel """

    # checks if there is already an existing game in the channel
    if is_game_in_channel(channel):
        msg = "There is already a game ongoing in this channel."
        post_to_slack(msg, response_url)

    # checks to see if player2 is a valid game partner
    elif player2 is None:
        msg = "That person is not part of this team."
        post_to_slack(msg, response_url)

    # there is no game in the channel, a new one can start
    else:
        ALL_GAMES[channel] = TTT_Game(player1, player2)  # adding a new game object
        msg = ("*~~~ WELCOME TO TIC TAC TOE!!! ~~~*\n" + player1 + " has challenged "
               + player2 + " to a game of tictactoe in channel: " + channel + "!\n"
               + ALL_GAMES[channel].get_formatted_board())
        post_to_slack(msg, response_url)
        display_current_player(ALL_GAMES[channel], response_url)


def validate_and_make_move(username, channel, placement_num, response_url):
    """ Checks all the requirements for there to be a valid move and makes it
        if possible. """
    # Check 1: making sure that the game exists
    if is_game_in_channel(channel):

        # Check 2: making sure that only the current player whose turn it is can make a move
        if username == ALL_GAMES[channel].current_player():

            # Check 3: when current player tries to play a location not on the board
            if placement_num == 10000:
                msg = "There is no such spot on the board here, sport."
                post_to_slack(msg, response_url)
                display_current_player(ALL_GAMES[channel], response_url)

            # all requirements are fulfilled, the game can proceed
            else:
                make_move(ALL_GAMES[channel], placement_num, response_url, channel)

        # someone not current player tried to make a move
        else:
            msg = "Your move to make, this is not."
            post_to_slack(msg, response_url)
            display_current_player(ALL_GAMES[channel], response_url)

    # there is no game currently in the channel
    else:
        display_no_game(response_url)


def make_move(Current_Game, placement_num, response_url, channel):
    """ Runs the tic tac toe game specific to the channel """
    # if the spot is an interger, it is an available spot
    if isinstance(Current_Game.board[placement_num], int):
        Current_Game.board[placement_num] = Current_Game.current_symbol()
        Current_Game.turn_count += 1
        post_to_slack(Current_Game.get_formatted_board(), response_url)

        # checks if the move results in a winner
        if Current_Game.is_winner(Current_Game.current_symbol()) is True:
            game_win(response_url, channel)
            return None

        # checks if the game is at a draw
        if Current_Game.turn_count == Current_Game.max_turns:
            game_draw(response_url, channel)
            return None

        display_current_player(Current_Game, response_url)

    # if the spot is a string ( X or O ), it is not available
    elif isinstance(Current_Game.board[placement_num], str):
        msg = "That spot is already taken"
        post_to_slack(msg, response_url)
        display_current_player(Current_Game, response_url)

    # something went wrong
    else:
        msg = "Error in the input"
        post_to_slack(msg, response_url)


def get_all_users():
    """ Gets all the users in the team, including Slackbot. """
    list_of_users = []
    dict_members = SC.api_call("users.list")["members"]
    for each in dict_members:
        list_of_users.append(each["name"])
    return list_of_users


def get_target_username(text):
    """ Gets the username of player2 if any """
    text = text.split()
    if text[0].startswith("@") and text[0][1:] in get_all_users():
        return text[0][1:]
    else:
        return None


def get_valid_placement(text):
    """ Gets the location on the board for the next move, if any """
    text = text.split()
    if is_text_integer(text[0]):
        placement_num = int(text[0])
        if 1 <= placement_num <= 9:
            return placement_num-1
        else:
            return 10000 
    else:
        return None


def is_text_integer(text):
    """ Checks if a string can be converted to an interger """
    try:
        int(text[0])
    except ValueError:
        return False
    return True


def is_game_in_channel(channel):
    """ Checks to see if there is an ongoing game in the channel. """
    if channel in ALL_GAMES:
        return True


def game_win(response_url, channel):
    """ Game ended with a winner. """
    msg = ("~~~~~~~ We have a winner!! Tic Tac Toe champion is: "
           + ALL_GAMES[channel].current_player() + "~~~~~~~")
    post_to_slack(msg, response_url)
    end_game(channel)


def game_draw(response_url, channel):
    """ Game ended in a draw. """
    msg = (ALL_GAMES[channel].player1 +
           " and " + ALL_GAMES[channel].player2 +
           " draw on this game.")
    post_to_slack(msg, response_url)
    end_game(channel)


def manual_end(username, channel, response_url):
    """ checks to see if there is an ongoing game. If yes, ends it """
    # if there is a game ongoing, ends it and displays who ended it
    if is_game_in_channel(channel):
        msg = username + " has ended the current game."
        post_to_slack(msg, response_url)
        end_game(channel)

    # if no game, then there is no game to end
    else:
        display_no_game(response_url)


def end_game(channel):
    """ Deletes the game after it ends """
    ALL_GAMES.pop(channel)


def display_current_player(Current_Game, response_url):
    """ Posts to channel the current player and symbol. """
    msg = (Current_Game.current_player() +
           ", it's your turn. Your symbol is *" +
           Current_Game.current_symbol()) + "*"
    post_to_slack(msg, response_url)


def display_help(response_url):
    """ Posts to the channel helpful information about the game """
    msg = "*-XOXO- TicTacToe Help -XOXO-* \n"
    attch = ("Slash commands:\n /ttt help: displays this help session" +
             "\n /ttt status: displays the current board and players" +
             "\n /ttt @username: starts a new game in this channel" +
             "\n /ttt endgame: ends the current game" +
             "\n /ttt #: # = number on the board. Current player whose turn " +
             "it is, makes a move")
    post_to_slack(msg, response_url, attch)


def determine_game_status(channel, response_url):
    """ checks to see if there is an ongoing game. If yes, displays the current status """
    # if there is a game ongoing, displays the game status
    if is_game_in_channel(channel):
        msg = ("There is an ongoing game between " +
               ALL_GAMES[channel].player1 + " and " + ALL_GAMES[channel].player2 +
               " in this channel. \n" + ALL_GAMES[channel].get_formatted_board() +
               "\n It is " + ALL_GAMES[channel].current_player() + "'s turn.")
        post_to_slack(msg, response_url)

    # if no game, says so
    else:
        display_no_game(response_url)


def display_no_game(response_url):
    """ displays a message that there is no ongoing game in the Slack channel """
    msg = "No game in this channel.\n Start a new game with */ttt @username*"
    post_to_slack(msg, response_url)


if __name__ == "__main__":
    # PORT = int(os.environ.get("PORT", 5000))
    # app.run(host="0.0.0.0", port=PORT)
    app.run()
