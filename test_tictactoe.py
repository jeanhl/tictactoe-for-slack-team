import unittest
import tictactoe
from TTT_Game_class import TTT_Game


class tictactoeUnitTestCase(unittest.TestCase):

    def test_get_command(self):
        # get_command returns "start new game" when given @username as the first word
        self.assertEqual(tictactoe.get_command("@username"), "start new game")
        self.assertEqual(tictactoe.get_command(" @username"), "start new game")
        self.assertEqual(tictactoe.get_command(" @"), "start new game")
        self.assertEqual(tictactoe.get_command("@ @ @ @ @ @"), "start new game")
        self.assertEqual(tictactoe.get_command("@username something"), "start new game")
        self.assertEqual(tictactoe.get_command("@username help"), "start new game")
        self.assertEqual(tictactoe.get_command("@username 3"), "start new game")
        self.assertEqual(tictactoe.get_command("@username3"), "start new game")

        # get_command returns "endgame" when given endgame the first word
        self.assertEqual(tictactoe.get_command("endgame"), "endgame")
        self.assertEqual(tictactoe.get_command("  endgame"), "endgame")
        self.assertEqual(tictactoe.get_command("endgame @username"), "endgame")
        self.assertEqual(tictactoe.get_command("endgame 3"), "endgame")

        # get_command returns "help" when given help the first word
        self.assertEqual(tictactoe.get_command("help"), "help")
        self.assertEqual(tictactoe.get_command("  help"), "help")
        self.assertEqual(tictactoe.get_command("help status"), "help")
        self.assertEqual(tictactoe.get_command("help None"), "help")

        # get_command returns "status" when given status the first word
        self.assertEqual(tictactoe.get_command("status"), "status")
        self.assertEqual(tictactoe.get_command("  status"), "status")
        self.assertEqual(tictactoe.get_command("status @username"), "status")
        self.assertEqual(tictactoe.get_command("status 3"), "status")

        # get_command returns "procees to next move"
        # when given a string of integers: "1", "34", etc
        self.assertEqual(tictactoe.get_command("3"), "proceed to next move")
        self.assertEqual(tictactoe.get_command("0"), "proceed to next move")
        self.assertEqual(tictactoe.get_command("-100"), "proceed to next move")
        self.assertEqual(tictactoe.get_command("16354"), "proceed to next move")

        # get_command returns None with other types of input
        self.assertIsNone(tictactoe.get_command("username@"))
        self.assertIsNone(tictactoe.get_command("username"))
        self.assertIsNone(tictactoe.get_command("end the game"))
        self.assertIsNone(tictactoe.get_command("end"))
        self.assertIsNone(tictactoe.get_command("stopgame"))
        self.assertIsNone(tictactoe.get_command("three"))
        self.assertIsNone(tictactoe.get_command("-three"))
        self.assertIsNone(tictactoe.get_command("stat"))
        self.assertIsNone(tictactoe.get_command("statuses"))
        self.assertIsNone(tictactoe.get_command("status@username"))
        self.assertIsNone(tictactoe.get_command("end@username"))
        self.assertIsNone(tictactoe.get_command("game status"))
        self.assertIsNone(tictactoe.get_command("game"))
        self.assertIsNone(tictactoe.get_command("X"))
        self.assertIsNone(tictactoe.get_command("O"))
        self.assertIsNone(tictactoe.get_command("3@"))


if __name__ == "__main__":
    unittest.main()
