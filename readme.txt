~.~`~.~`~.~`~.~` EMOJI TIC-TAC-TOE FOR SLACK README `~.~`~.~`~.~`~.~

This is a tic-tac-toe game that can be played in Slack channels using the slash command /ttt.

Users can challenge anyone in the team to play a game of tic-tac-toe on any public Slack channel. There can be simultaneous games ongoing but only 1 game per channel. Players make a move by specifying which number on the board they'd like to place their symbol on. If the same symbol appears 3-in-a-row horizontally, vertically, or diagonally, that player is the winner. If the board is full with no winner, there is a draw. Anyone in the team can end an ongoing game. A new game can only begin after the previous one ends. At any time in a channel, any user can ask for the current game status and a help message.

How to play the game in Slack:
All commands are preceded by "/ttt ". Only the first whole word is taken into account. The valid commands are listed below:
/ttt @username : If the username is in the team, a new game starts between  
                 the user who called the slash command and username.
/ttt # : Players (whose turn it is), can place their symbols ( X or O ) on
         on an open spot on the board by specifying the number
/ttt endgame : Anyone on the Slack team can end an ongoing game including 
               the two current players.
/ttt status : Anyone on the Slack team can get a status of an ongoing game
              including the two current players.
/ttt help : Anyone on the Slack team can get a help message detailing how to 
            play the game including the two current players.
            
When starting a game, you should get this:

![Alt text](https://dl.dropboxusercontent.com/u/4440990/TTT/Welcome%20TTT.png)


For more information about tic-tac-toe, please visit:
https://en.wikipedia.org/wiki/Tic-tac-toe
