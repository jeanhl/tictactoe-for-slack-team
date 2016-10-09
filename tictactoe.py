import os
import requests
import json
from flask import Flask, request, Response, jsonify
from slackclient import SlackClient
from TT_Game_class import TTT_Game
app = Flask(__name__)

SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')
SLACK_TEST_TOKEN = os.environ.get('SLACK_TEST_TOKEN')
SLACK_SLASH_TOKEN = os.environ.get('SLACK_SLASH_TOKEN')
SC = SlackClient(SLACK_TEST_TOKEN)

ALL_CHANNELS = {} #dictionary to keep track of all the game objects

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
    chunk = {
                "response_type": "in_channel",
                "text": msg,
                "attachments": [{"text": attachment}]
            }
    requests.request("POST", response_url, data=json.dumps(chunk), headers=files)


def checks_text_content(text, player1, channel, response_url):
    """ Checks the text of the slash command for:
        If valid user: Make a new game
        If integer: Make next move """
    if len(text) == 0:
        msg = "Doesn't seem like there is anything here :/"
        post_game_msg(msg, response_url)
    else:
        player2 = get_second_player(text)
        placement_num = check_if_valid_move(text, response_url)
        if player2 is None and placement_num is None:
            msg = "I don't understand. Please check your request for typos."
            post_game_msg(msg, response_url)
        else:
            if check_for_game_in_channel(channel) is True:
                if isinstance(placement_num, int) and player1 == ALL_CHANNELS[channel].current_player():
                    print "make a move"
                    continue_game(ALL_CHANNELS[channel], placement_num, response_url, channel)
                else:
                    msg = "Your decision to make, this move is not"
                    post_game_msg(msg, response_url)
                    msg = (ALL_CHANNELS[channel].current_player() +
                           ", it's your turn. Your symbol is " +
                           ALL_CHANNELS[channel].current_symbol())
                    post_game_msg(msg, response_url)
                if isinstance(player2, str):
                    msg = "There is already a game ongoing in this channel."
                    post_game_msg(msg, response_url)
            else:
                if isinstance(placement_num, int):
                    "tried to make amove"
                    msg = "You are not currently in a game in this channel."
                    post_game_msg(msg, response_url)
                if isinstance(player2, str):
                    "starting new game"
                    start_new_game(channel, player1, player2, response_url)


def get_all_users():
    """ Gets all the users in the team, including Slackbot. """
    list_of_users = []
    dict_users = SC.api_call("users.list")
    dict_members = dict_users["members"]
    for each in dict_members:
        list_of_users.append(each["name"])
    return list_of_users

def get_second_player(text):
    """ Checks if the user requested in the team """
    text = text.split()
    if text[0][1:] in get_all_users():
        return text[0][1:]
    else:
        return None

def check_if_valid_move(text, response_url=None):
    """ Checks to see if text is an integer, if yes, turns it into a board location """
    text = text.split()
    try:
        placement_num = int(text[0])
    except ValueError:
        return None
    if 1 <= int(placement_num) <= 9:
            return (int(placement_num)-1)
    else:
        msg = "There is no such spot on the board here, sport."
        post_game_msg(msg, response_url)
        return True


def check_for_game_in_channel(channel):
    """ Checks to see if there is an ongoing game in the channel. """
    print "channel", channel
    print "ALL_CHANNELS", ALL_CHANNELS
    if channel in ALL_CHANNELS:
        return True


def start_new_game(channel, player1, player2, response_url):
    """ Initiates a new game oject and announces a new game in the channel """
    ALL_CHANNELS[channel] = TTT_Game(channel, player1, player2)
    msg = ("~~~ WELCOME TO TIC TAC TOE!!! ~~~\n" + player1 + " has challenged " 
            + player2 + " to a game of tictactoe in channel: " + channel + "!\n" 
            + ALL_CHANNELS[channel].get_formatted_board())
    post_game_msg(msg, response_url)
    msg = (ALL_CHANNELS[channel].current_player() + 
           ", it's your turn. Your symbol is " +
           ALL_CHANNELS[channel].current_symbol())
    post_game_msg(msg, response_url)


def continue_game(Current_Game, placement_num, response_url, channel):
    """ Continues a game and states the next player's turn if needed """
    play_tictactoe(Current_Game, placement_num, response_url, channel)
    

def play_tictactoe(Current_Game, placement_num, response_url, channel):
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
        msg = (Current_Game.current_player() +
               ", it's your turn. Your symbol is " +
               Current_Game.current_symbol())
        post_game_msg(msg, response_url)
    elif isinstance(Current_Game.board[placement_num], str):
        msg = "That spot is already taken"
        post_game_msg(msg, response_url)
        msg = (Current_Game.current_player() +
               ", it's your turn. Your symbol is " +
               Current_Game.current_symbol())
        post_game_msg(msg, response_url)
    else:
        msg = "Error in the input"
        post_game_msg(msg, response_url)

def game_draw(response_url, channel):
    """ Game ended in a draw. """
    msg = "This is a draw."
    post_game_msg(msg, response_url)
    end_game(channel)


def end_game(channel):
    """ Deletes the game after it ends """
    ALL_CHANNELS.pop(channel)



if __name__ == "__main__":
    app.run(debug=False)