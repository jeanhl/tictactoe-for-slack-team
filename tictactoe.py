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

ALL_CHANNELS = {}  # dictionary to keep track of all the game objects


@app.route('/')
def homepage():
    """ Shows a homepage on Heroku for debugging purposes"""
    return "TicTacToe is running."  # displayed on the homepage


@app.route('/slack', methods=['POST'])
def inbound():
    """ Manages requests from the Slack channel"""
    if request.form.get('token') == SLACK_SLASH_TOKEN:
        channel = str(request.form.get('channel_name'))
        player1 = str(request.form.get('user_name'))
        text = str(request.form.get('text'))
        response_url = str(request.form.get('response_url'))
        checks_text_content(text, player1, channel, response_url)
        return " "


def post_game_msg(msg, response_url, attachment=None):
    """ Posts game msgs to Slack """
    files = {"content-type": "application/json"}
    chunk = {"response_type": "in_channel",
             "text": msg,
             "attachments": [{"text": attachment}]}
    requests.request("POST", response_url, data=json.dumps(chunk), headers=files)


def checks_text_content(text, player1, channel, response_url):
    """ Checks the text of the slash command for:
        If valid user: Make a new game
        If integer: Make next move """
    if len(text) == 0:  # checks to see if the text is empty
        msg = "Doesn't seem like there is anything there :/"
        post_game_msg(msg, response_url)
    else:
        argument = get_argument(text)
        placement_num = check_if_valid_move(text, response_url)
        if argument is None and placement_num is None:
        # checks to see if we have a second player or a valid move
            msg = "I don't understand. Please enter /ttt help for more info."
            post_game_msg(msg, response_url)
        else:
            if is_game_in_channel(channel) is True:
            # if there is an ongoing game in the channel, the following can happen
                if isinstance(placement_num, int):
                    if player1 == ALL_CHANNELS[channel].current_player():
                    # making sure that only the current player whose turn it is can make a move
                        continue_game(ALL_CHANNELS[channel], placement_num, response_url, channel)
                    else:
                        msg = "Your move to make, this is not."
                        post_game_msg(msg, response_url)
                        display_current_player(ALL_CHANNELS[channel], response_url)
                elif argument == "endtttgame":
                    # any user can end a current game
                    end_game(channel)
                    msg = player1 + " has ended the current game."
                    post_game_msg(msg, response_url)
                elif argument == "ttthelp":
                    display_help(response_url)
                elif argument == "tttstatus":
                    display_game_status(ALL_CHANNELS[channel], response_url)
                else:
                    # if someone tries to start a new game
                    msg = "There is already a game ongoing in this channel."
                    post_game_msg(msg, response_url)

            else:  # if there isn't a game currently ongoing in the channel
                if argument == "ttthelp":
                    display_help(response_url)
                elif (isinstance(placement_num, int) or argument == "tttstatus"
                      or argument == "endtttgame"):
                    msg = ("No game in this channel.\n" +
                           " Start a new game with */ttt @username*")
                    post_game_msg(msg, response_url)
                else:
                    player2 = argument
                    start_new_game(channel, player1, player2, response_url)


def get_all_users():
    """ Gets all the users in the team, including Slackbot. """
    list_of_users = []
    dict_users = SC.api_call("users.list")
    dict_members = dict_users["members"]
    for each in dict_members:
        list_of_users.append(each["name"])
    return list_of_users


def get_argument(text):
    """ Refine user inputs into one of five possible arguments """
    text = text.split()
    if text[0].startswith("@") and text[0][1:] in get_all_users():
        return text[0][1:]
    elif text[0] == "endgame":
        return "endtttgame"
    elif text[0] == "help":
        return "ttthelp"
    elif text[0] == "status":
        return "tttstatus"
    else:
        return None


def check_if_valid_move(text, response_url=None):
    """ Checks to see if text is an integer, if yes, turns it into a board location """
    text = text.split()
    try:
        placement_num = int(text[0])
    except ValueError:
        return None
    else:
        if 1 > placement_num or 9 < placement_num:
            msg = "There is no such spot on the board here, sport."
            post_game_msg(msg, response_url)
            return "Nothing"
        else:
            return placement_num-1


def is_game_in_channel(channel):
    """ Checks to see if there is an ongoing game in the channel. """
    if channel in ALL_CHANNELS:
        return True


def start_new_game(channel, player1, player2, response_url):
    """ Initiates a new game oject and announces a new game in the channel """
    ALL_CHANNELS[channel] = TTT_Game(channel, player1, player2)
    msg = ("*~~~ WELCOME TO TIC TAC TOE!!! ~~~*\n" + player1 + " has challenged "
           + player2 + " to a game of tictactoe in channel: " + channel + "!\n"
           + ALL_CHANNELS[channel].get_formatted_board())
    post_game_msg(msg, response_url)
    display_current_player(ALL_CHANNELS[channel], response_url)


def continue_game(Current_Game, placement_num, response_url, channel):
    """ Runs the tic tac toe game specific to the channel """
    if isinstance(Current_Game.board[placement_num], int):
        Current_Game.board[placement_num] = Current_Game.current_symbol()
        post_game_msg(Current_Game.get_formatted_board(), response_url)
        if Current_Game.is_winner(Current_Game.current_symbol()) is True:
            msg = ("~~~~~~~ We have a winner!! Tic Tac Toe champion is: "
                   + Current_Game.current_player() + "~~~~~~~")
            post_game_msg(msg, response_url)
            return end_game(channel)
        Current_Game.turn_count += 1
        if Current_Game.turn_count == Current_Game.max_turns:
            return game_draw(response_url, channel)
        display_current_player(Current_Game, response_url)
    elif isinstance(Current_Game.board[placement_num], str):
        msg = "That spot is already taken"
        post_game_msg(msg, response_url)
        display_current_player(Current_Game, response_url)
    else:
        msg = "Error in the input"
        post_game_msg(msg, response_url)


def game_draw(response_url, channel):
    """ Game ended in a draw. """
    msg = (ALL_CHANNELS[channel].player1 +
           " and " + ALL_CHANNELS[channel].player2 +
           "draw on this game.")
    post_game_msg(msg, response_url)
    end_game(channel)


def end_game(channel):
    """ Deletes the game after it ends """
    ALL_CHANNELS.pop(channel)


def display_current_player(Current_Game, response_url):
    """ Posts to channel the current player and symbol. """
    msg = (Current_Game.current_player() +
           ", it's your turn. Your symbol is *" +
           Current_Game.current_symbol()) + "*"
    post_game_msg(msg, response_url)


def display_help(response_url):
    """ Posts to the channel helpful information about the game """
    msg = "*-XOXO- TicTacToe Help -XOXO-* \n"
    attch = ("Slash commands:\n /ttt help: displays this help session" +
             "\n /ttt status: displays the current board and players" +
             "\n /ttt @username: starts a new game in this channel" +
             "\n /ttt endgame: ends the current game" +
             "\n /ttt #: # = number on the board. Current player whose turn " +
             "it is, makes a move")
    post_game_msg(msg, response_url, attch)


def display_game_status(Current_Game, response_url):
    """ Posts to the channel the status of current game """
    msg = ("There is an ongoing game between " +
           Current_Game.player1 + " and " + Current_Game.player2 +
           " in this channel. \n" + Current_Game.get_formatted_board() +
           "\n It is " + Current_Game.current_player() + "'s turn.")
    post_game_msg(msg, response_url)


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)
