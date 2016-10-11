import unittest
import tictactoe
from TTT_Game_class import TTT_Game


class tictactoeUnitTestCase(unittest.TestCase):
    """ tests for fuctions in tictactoe.py """

    def test_get_command(self):
        """ tests different inputs and the resulting command """
        # get_command returns "start new game" when given @username as the first word
        self.assertEqual(tictactoe.get_command("@username something"), "start new game")
        self.assertEqual(tictactoe.get_command("@username help"), "start new game")
        self.assertEqual(tictactoe.get_command("@ @ @ @ @ @"), "start new game")
        self.assertEqual(tictactoe.get_command("@username 3"), "start new game")
        self.assertEqual(tictactoe.get_command(" @username"), "start new game")
        self.assertEqual(tictactoe.get_command("@username3"), "start new game")
        self.assertEqual(tictactoe.get_command("@username"), "start new game")
        self.assertEqual(tictactoe.get_command(" @"), "start new game")
        # returns None because they don't have an @ as a first character
        self.assertIsNone(tictactoe.get_command("username@"))
        self.assertIsNone(tictactoe.get_command("username"))

        # get_command returns "endgame" when given endgame the first word
        self.assertEqual(tictactoe.get_command("endgame @username"), "endgame")
        self.assertEqual(tictactoe.get_command("  endgame"), "endgame")
        self.assertEqual(tictactoe.get_command("endgame 3"), "endgame")
        self.assertEqual(tictactoe.get_command("endgame"), "endgame")
        # returns None because they don't match "endgame"
        self.assertIsNone(tictactoe.get_command("end the game"))
        self.assertIsNone(tictactoe.get_command("end@username"))
        self.assertIsNone(tictactoe.get_command("end game"))
        self.assertIsNone(tictactoe.get_command("stopgame"))
        self.assertIsNone(tictactoe.get_command("end"))

        # get_command returns "help" when given help the first word
        self.assertEqual(tictactoe.get_command("help status"), "help")
        self.assertEqual(tictactoe.get_command("help None"), "help")
        self.assertEqual(tictactoe.get_command("  help"), "help")
        self.assertEqual(tictactoe.get_command("help"), "help")

        # get_command returns "status" when given status the first word
        self.assertEqual(tictactoe.get_command("status @username"), "status")
        self.assertEqual(tictactoe.get_command("  status"), "status")
        self.assertEqual(tictactoe.get_command("status 3"), "status")
        self.assertEqual(tictactoe.get_command("status"), "status")
        # returns None because they don't match "status"
        self.assertIsNone(tictactoe.get_command("status@username"))
        self.assertIsNone(tictactoe.get_command("game status"))
        self.assertIsNone(tictactoe.get_command("statuses"))
        self.assertIsNone(tictactoe.get_command("stat"))
        self.assertIsNone(tictactoe.get_command("game"))

        # get_command returns "procees to next move"
        # when given a string of all integers: "1", "34", etc
        self.assertEqual(tictactoe.get_command("3"), "proceed to next move")
        self.assertEqual(tictactoe.get_command("3 4 5"), "proceed to next move")
        self.assertEqual(tictactoe.get_command("0"), "proceed to next move")
        self.assertEqual(tictactoe.get_command("-100"), "proceed to next move")
        self.assertEqual(tictactoe.get_command("16354"), "proceed to next move")
        # returns None because they're not strings of all integers
        self.assertIsNone(tictactoe.get_command("-three"))
        self.assertIsNone(tictactoe.get_command("three"))
        self.assertIsNone(tictactoe.get_command("3@"))

        # get_command returns None with other types of input
        self.assertIsNone(tictactoe.get_command("X"))
        self.assertIsNone(tictactoe.get_command("O"))

    def test_get_valid_placement(self):
        """ tests different inputs and returns a place on the board
            or "error 10000" """
        # returns different locations on the board (indexed locations)
        self.assertEqual(tictactoe.get_valid_placement("1"), 0)
        self.assertEqual(tictactoe.get_valid_placement("5"), 4)
        self.assertEqual(tictactoe.get_valid_placement("9"), 8)
        self.assertEqual(tictactoe.get_valid_placement("3 4 5"), 2)

        # returns "error 10000", the location is NOT on the board
        self.assertEqual(tictactoe.get_valid_placement("0"), 10000)
        self.assertEqual(tictactoe.get_valid_placement("-1"), 10000)
        self.assertEqual(tictactoe.get_valid_placement("10000000000000000000000000000000000000000000"), 10000)
        self.assertEqual(tictactoe.get_valid_placement("10"), 10000)
        self.assertEqual(tictactoe.get_valid_placement("345"), 10000)

        # if input is not a string of int or int, returns None
        self.assertIsNone(tictactoe.get_valid_placement("three"))
        self.assertIsNone(tictactoe.get_valid_placement("-three"))
        self.assertIsNone(tictactoe.get_valid_placement("three four five"))
        self.assertIsNone(tictactoe.get_valid_placement("help"))
        self.assertIsNone(tictactoe.get_valid_placement("@username"))


class GameClassUnitTestCase(unittest.TestCase):
    """ tests for Class methods in TTT_Game_class.py """

    def test_get_formatted_board(self):
        """ Making sure the board is displayed corrently with numbers and
            symbols with the decorations"""
        TestGame = TTT_Game("John", "Jane")
        self.assertEqual(TestGame.get_formatted_board(),
                        (":one::two::three:\n" +
                         ":four::five::six:\n" +
                         ":seven::eight::nine:"))

        TestGame.board = [1, 2, "O", 4, "X", 6, 7, 8, 9]
        self.assertEqual(TestGame.get_formatted_board(),
                        (":one::two::o:\n" +
                         ":four::heavy_multiplication_x::six:\n" +
                         ":seven::eight::nine:"))

        TestGame.board = ["O", "O", "O", "O", "O", "O", "O", "O", "O"]
        self.assertEqual(TestGame.get_formatted_board(),
                        (":o::o::o:\n" +
                         ":o::o::o:\n" +
                         ":o::o::o:"))

    def test_current_symbol(self):
        """ Making sure the correct symbols are returned
            for alternating turns"""
        TestGame = TTT_Game("John", "Jane")

        # if odd, returns  "X"
        TestGame.turn_count = 1
        self.assertEqual(TestGame.current_symbol(), "X")
        TestGame.turn_count = 3
        self.assertEqual(TestGame.current_symbol(), "X")

        # if even, returns  "O"
        TestGame.turn_count = 4
        self.assertEqual(TestGame.current_symbol(), "O")

    def test_current_player(self):
        """ Making sure the correct player names are returned
            for alternating turns"""
        TestGame = TTT_Game("John", "Jane")

        # if odd, returns  "John"
        TestGame.turn_count = 1
        self.assertEqual(TestGame.current_player(), "John")
        TestGame.turn_count = 5
        self.assertEqual(TestGame.current_player(), "John")

        # if even, returns  "O"
        TestGame.turn_count = 8
        self.assertEqual(TestGame.current_player(), "Jane")

    def test_is_winner(self):
        """ Checks if the current combination is a winner """
        TestGame = TTT_Game("John", "Jane")

        # Check verticals
        TestGame.board = [1, 2, "X", 4, 5, "X", 7, 8, "X"]
        self.assertTrue(TestGame.is_winner("X"))
        TestGame.board = ["O", 2, 3, "O", 5, "X", "O", 8, "X"]
        self.assertTrue(TestGame.is_winner("O"))
        TestGame.board = [1, "X", "O", "O", "X", 6, 7, "X", "X"]
        self.assertTrue(TestGame.is_winner("X"))

        # Check horizontals
        TestGame.board = ["O", "O", "O", "O", 5, "X", 7, 8, 9]
        self.assertTrue(TestGame.is_winner("O"))
        TestGame.board = [1, 2, 3, "X", "X", "X", 7, 8, 9]
        self.assertTrue(TestGame.is_winner("X"))
        TestGame.board = [1, 2, 3, "O", 5, 6, "O", "O", "O"]
        self.assertTrue(TestGame.is_winner("O"))

        # Check diagonals
        TestGame.board = ["O", "X", 3, 4, "O", "X", "X", "O", "O"]
        self.assertTrue(TestGame.is_winner("O"))
        TestGame.board = [1, 2, "X", 4, "X", 6, "X", 8, 9]
        self.assertTrue(TestGame.is_winner("X"))


if __name__ == "__main__":
    unittest.main()
