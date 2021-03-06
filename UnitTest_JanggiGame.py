# Author:           Chi Hang Leung
# Date:             03/09/2021
# Description:      Unit tests for the Janggi class and for all game pieces.

import unittest
from JanggiGame import *


class TestJanggiGame(unittest.TestCase):
	"""Testing the JanggiGame class"""

	def test_init(self):
		"""Testing the instantiation of the board."""

		game = JanggiGame()

		# Test dimension
		self.assertEqual(game._rows, 10)
		self.assertEqual(game._columns, 9)

		# Test status and turn
		self.assertEqual(game._turn, "BLUE")
		self.assertEqual(game._status, "UNFINISHED")

		test_positions = [[None for _ in range(game._columns)] for _ in range(game._rows)]

		# Test starting position of all game pieces
		for i in range(game._rows):
			for j in range(game._columns):
				if game._board[(i, j)]:
					test_positions[i][j] = game._board[(i, j)].get_name()

					if i < 4:
						self.assertEqual(game._board[(i, j)].get_player(), "RED")
					elif i > 5:
						self.assertEqual(game._board[(i, j)].get_player(), "BLUE")

		correct_positions = [["Chariot", "Elephant", "Horse", "Guard", None, "Guard", "Elephant", "Horse", "Chariot"],
							 [None, None, None, None, "General", None, None, None, None],
							 [None, "Cannon", None, None, None, None, None, "Cannon", None],
							 ["Soldier", None, "Soldier", None, "Soldier", None, "Soldier", None, "Soldier"],
							 [None, None, None, None, None, None, None, None, None],
							 [None, None, None, None, None, None, None, None, None],
							 ["Soldier", None, "Soldier", None, "Soldier", None, "Soldier", None, "Soldier"],
							 [None, "Cannon", None, None, None, None, None, "Cannon", None],
							 [None, None, None, None, "General", None, None, None, None],
							 ["Chariot", "Elephant", "Horse", "Guard", None, "Guard", "Elephant", "Horse", "Chariot"]]

		self.assertEqual(test_positions, correct_positions)

		# Test inventory of the players
		self.assertIn("BLUE", game._players)
		self.assertIn("RED", game._players)

		# Test if each player has the correct number and type of game pieces
		test_blue_player = [game_piece.get_name() for game_piece in game._players["BLUE"]]
		test_red_player = [game_piece.get_name() for game_piece in game._players["RED"]]
		correct_player = ["General"] + ["Guard"] * 2 + ["Horse"] * 2 + ["Elephant"] * 2 + \
		                 ["Chariot"] * 2 + ["Cannon"] * 2 + ["Soldier"] * 5
		self.assertEqual(test_blue_player, correct_player)
		self.assertEqual(test_red_player, correct_player)

	def test_get_rows(self):
		"""Testing the get_rows method"""

		game = JanggiGame()
		self.assertEqual(game.get_rows(), 10)

	def test_get_columns(self):
		"""Testing the get_rows method"""

		game = JanggiGame()
		self.assertEqual(game.get_columns(), 9)

	def test_get_board(self):
		"""Testing the get_board method"""

		game = JanggiGame()
		self.assertEqual(game.get_board(), game._board)
		self.assertEqual(len(game.get_board()), 90)

	def test_players(self):
		"""Testing the get_players"""

		game = JanggiGame()
		self.assertEqual(game.get_players(), game._players)
		self.assertEqual(len(game.get_players()), 2)
		self.assertIn("BLUE", game.get_players())
		self.assertIn("RED", game.get_players())
		self.assertEqual(len(game.get_players()["BLUE"]), 16)
		self.assertEqual(len(game.get_players()["RED"]), 16)

	def test_get_game_state(self):
		"""Testing the get_game_state method"""

		game = JanggiGame()
		self.assertEqual(game.get_game_state(), "UNFINISHED")

		game._status = "RED_WON"
		self.assertEqual(game.get_game_state(), "RED_WON")

		game._status = "BLUE_WON"
		self.assertEqual(game.get_game_state(), "BLUE_WON")

	def test_get_position(self):
		"""Testing the get_position method"""

		game = JanggiGame()
		for player in game.get_players():
			for gamePiece in game.get_players()[player]:
				position = game.get_position(gamePiece)
				self.assertIs(game.get_board()[position], gamePiece)

	def test_convert_position(self):
		"""Testing the convert_position_to_tuple and convert_position_to_string method"""

		game = JanggiGame()

		with self.assertRaises(InvalidPositionError):
			game.convert_position("A11")

		with self.assertRaises(InvalidPositionError):
			game.convert_position("A")

		with self.assertRaises(InvalidPositionError):
			game.convert_position("Z1")

		with self.assertRaises(InvalidPositionError):
			game.convert_position("AA")

		with self.assertRaises(InvalidPositionError):
			game.convert_position("11")

		with self.assertRaises(InvalidPositionError):
			game.convert_position("B11")

		self.assertEqual(game.convert_position("A1"), (0, 0))
		self.assertEqual(game.convert_position("E5"), (4, 4))
		self.assertEqual(game.convert_position("e6"), (5, 4))
		self.assertEqual(game.convert_position("I10"), (9, 8))

	def test_get_opponent(self):
		"""Testing the get_opponent method."""

		game = JanggiGame()
		self.assertEqual(game.get_opponent("BLUE"), "RED")
		self.assertEqual(game.get_opponent("RED"), "BLUE")

	def test_try_restore_move(self):
		"""Testing the try_move and restore method."""

		game = JanggiGame()

		# Moving Red General to (2, 4)
		before_attempt = (game.get_board(), set(game.get_players()))
		captured = game.try_move((1, 4), (2, 4))
		game.restore_move((2, 4), (1, 4), captured)
		after_attempt = (game.get_board(), set(game.get_players()))
		self.assertEqual(before_attempt, after_attempt)

		# Moving Blue Soldier 3 to (3, 4)
		before_attempt = (game.get_board(), set(game.get_players()))
		captured = game.try_move((6, 4), (3, 4))
		game.restore_move((6, 4), (3, 4), captured)
		after_attempt = (game.get_board(), set(game.get_players()))
		self.assertEqual(before_attempt, after_attempt)

	def test_is_in_check(self):
		"""Testing the is_in_check method."""

		game = JanggiGame()

		self.assertFalse(game.is_in_check("RED"))
		self.assertFalse(game.is_in_check("BLUE"))

		# Move Blue Cannon 1 to (4, 4)
		game._board[(4, 4)] = game._board[(7, 1)]
		game._board[(7, 1)] = None
		self.assertTrue(game.is_in_check("RED"))
		self.assertFalse(game.is_in_check("BLUE"))

		# # Move Red General to (1, 3)
		game._board[(1, 3)] = game._board[(1, 4)]
		game._board[(1, 4)] = None
		self.assertFalse(game.is_in_check("RED"))
		self.assertFalse(game.is_in_check("BLUE"))

		# # Move Blue horse 2 to (2, 5)
		game._board[(2, 5)] = game._board[(9, 7)]
		game._board[(9, 7)] = None
		self.assertTrue(game.is_in_check("RED"))
		self.assertFalse(game.is_in_check("BLUE"))

		# # Move Red Guard 2 to (2, 4)
		game._board[(2, 4)] = game._board[(0, 5)]
		game._board[(0, 5)] = None
		self.assertFalse(game.is_in_check("RED"))
		self.assertFalse(game.is_in_check("BLUE"))

		# Move red soldier 5 to (7, 5)
		game._board[(7, 5)] = game._board[(3, 8)]
		game._board[(3, 8)] = None
		self.assertFalse(game.is_in_check("RED"))
		self.assertTrue(game.is_in_check("BLUE"))

	def test_is_checkmate(self):
		"""Testing the is_checkmate method."""

		game = JanggiGame()

		self.assertFalse(game.is_checkmate("RED"))
		self.assertFalse(game.is_checkmate("BLUE"))

		# Move two Blue soldier to (2, 3) and (2, 5) and
		# Move Blue Chariot 1 to (2, 4)
		game._board[(2, 3)] = game._board[(6, 2)]
		game._board[(6, 2)] = None
		game._board[(2, 5)] = game._board[(6, 6)]
		game._board[(6, 6)] = None
		game._board[(2, 4)] = game._board[(9, 0)]
		game._board[(9, 0)] = None
		self.assertTrue(game.is_in_check("RED"))
		self.assertTrue(game.is_checkmate("RED"))
		self.assertFalse(game.is_in_check("BLUE"))
		self.assertFalse(game.is_checkmate("BLUE"))

		# Move Red Cannon 2 to (5, 4)
		game._board[(5, 4)] = game._board[(2, 7)]
		game._board[(2, 7)] = None
		self.assertTrue(game.is_in_check("BLUE"))
		self.assertFalse(game.is_checkmate("BLUE"))

		# Move Red Chariot 1 to (7, 2)
		game._board[(7, 2)] = game._board[(0, 0)]
		game._board[(0, 0)] = None
		self.assertTrue(game.is_in_check("BLUE"))
		self.assertFalse(game.is_checkmate("BLUE"))

		# Move Red Chariot 2 to (8, 6)
		game._board[(8, 6)] = game._board[(0, 8)]
		game._board[(0, 8)] = None
		self.assertTrue(game.is_in_check("BLUE"))
		self.assertTrue(game.is_checkmate("BLUE"))

	def test_make_move(self):
		"""Testing the make_move method."""

		game = JanggiGame()

		# Test incorrect game status
		game._status = "RED_WON"
		self.assertFalse(game.make_move("A1", "A2"))
		game._status = "UNFINISHED"

		# Test incorrect to and from Square
		self.assertFalse(game.make_move("A1", "A0"))
		self.assertFalse(game.make_move("I10", "I11"))
		self.assertFalse(game.make_move("IDK", "WTF"))

		# Test moving an non-existing game piece
		self.assertFalse(game.make_move("D3", "D4"))

		# Test moving a game piece out of turn
		self.assertFalse(game.make_move("E2", "E3"))

		# Test illegal moves
		self.assertFalse(game.make_move("E2", "D4"))
		self.assertFalse(game.make_move("H3", "H9"))
		self.assertFalse(game.make_move("B3", "I3"))
		self.assertFalse(game.make_move("A4", "A3"))

		# Test making a turn that put oneself in check
		# Moving Blue Chariot 2 to H2
		game._board[(1, 7)] = game._board[(9, 8)]
		game._board[(9, 8)] = None
		game._turn = "RED"
		self.assertFalse(game.make_move("E2", "E2"))
		self.assertFalse(game.make_move("E2", "D2"))
		self.assertTrue(game.make_move("E2", "E1"))
		self.assertEqual(game.get_turn(), "BLUE")

		# Test passing a turn
		self.assertTrue(game.make_move("E9", "E9"))
		self.assertEqual(game.get_turn(), "RED")

		# Test checkmate
		game._turn = "BLUE"
		game._board[(1, 3)] = game._board[(9, 7)]
		game._board[(9, 7)] = None
		game._board[(5, 4)] = game._board[(7, 1)]
		game._board[(7, 1)] = None
		self.assertTrue(game.make_move("D2", "F3"))
		self.assertEqual(game.get_game_state(), "BLUE_WON")


class TestGeneral(unittest.TestCase):
	"""Testing the General class."""

	def test_get_player(self):
		"""Testing the get_player method for the General"""

		test_red_player_0 = General("RED", 0)
		test_blue_player_0 = General("BLUE", 0)

		self.assertEqual(test_red_player_0.get_player(), "RED")
		self.assertEqual(test_blue_player_0.get_player(), "BLUE")

	def test_get_identifier(self):
		"""Testing the get_identifier method for the General"""
		test_blue_player_0 = General("BLUE", 0)
		self.assertEqual(test_blue_player_0.get_identifier(), 0)

	def test_get_name(self):
		"""Testing the get_name method for the General"""

		test_red_player_0 = General("RED", 0)
		test_blue_player_0 = General("BLUE", 0)

		self.assertEqual(test_red_player_0.get_name(), "General")
		self.assertEqual(test_blue_player_0.get_name(), "General")

	def test_get_starting_position(self):
		"""Testing the get_starting position method for the General"""

		test_red_player_0 = General("RED", 0)
		test_blue_player_0 = General("BLUE", 0)

		self.assertEqual(test_blue_player_0.get_starting_position(), (8, 4))
		self.assertEqual(test_red_player_0.get_starting_position(), (1, 4))

	def test_get_fortress(self):
		"""Testing the get_fortress method."""

		test_red_player_0 = General("RED", 0)
		test_blue_player_0 = General("BLUE", 0)

		red_fortress = {(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)}
		blue_fortress = {(7, 3), (7, 4), (7, 5), (8, 3), (8, 4), (8, 5), (9, 3), (9, 4), (9, 5)}
		test_red_fortress = test_red_player_0.get_fortress()
		test_blue_fortress = test_blue_player_0.get_fortress()

		self.assertEqual(test_red_fortress, red_fortress)
		self.assertEqual(test_blue_fortress, blue_fortress)

	def test_get_diagonalMoves(self):
		"""Testing the get_diagonalMoves method."""

		test_red_player_0 = General("RED", 0)
		test_blue_player_0 = General("BLUE", 0)

		self.assertEqual(test_red_player_0.get_diagonalMoves((1, 4)), {(0, 3), (0, 5), (2, 3), (2, 5)})
		self.assertEqual(test_blue_player_0.get_diagonalMoves((7, 5)), {(8, 4)})

	def test_legal_moves(self):
		"""Testing the legal_moves method for the General"""

		game = JanggiGame()
		red_general = game.get_players()["RED"][0]
		blue_general = game.get_players()["BLUE"][0]

		test_red_general_moves = red_general.legal_moves(game.get_board(), game.get_position(red_general))
		test_blue_general_moves = blue_general.legal_moves(game.get_board(), game.get_position(blue_general))
		self.assertEqual(test_red_general_moves, {(1, 4), (0, 4), (1, 3), (1, 5), (2, 3), (2, 4), (2, 5)})
		self.assertEqual(test_blue_general_moves, {(8, 4), (9, 4), (8, 3), (8, 5), (7, 3), (7, 4), (7, 5)})

		# Move Red General to (2, 5)
		game._board[(2, 5)] = game._board[(1, 4)]
		game._board[(1, 4)] = None
		test_red_general_moves = red_general.legal_moves(game.get_board(), game.get_position(red_general))
		self.assertEqual(test_red_general_moves, {(2, 5), (1, 4), (1, 5), (2, 4)})

		# Move Blue General to (9, 4)
		game._board[(9, 4)] = game._board[(8, 4)]
		game._board[(8, 4)] = None
		test_blue_general_moves = blue_general.legal_moves(game.get_board(), game.get_position(blue_general))
		self.assertEqual(test_blue_general_moves, {(9, 4), (8, 4)})

		# Move Blue Soldier to (1, 4), Red General is still in (2, 5)
		game._board[(1, 4)] = game._board[(6, 4)]
		game._board[(6, 4)] = None
		test_red_general_moves = red_general.legal_moves(game.get_board(), game.get_position(red_general))
		self.assertEqual(test_red_general_moves, {(2, 5), (1, 4), (1, 5), (2, 4)})

		# Move Red General to (1, 5), Blue Soldier is still at (1, 4)
		game._board[(1, 5)] = game._board[(2, 5)]
		game._board[(2, 5)] = None
		test_red_general_moves = red_general.legal_moves(game.get_board(), game.get_position(red_general))
		self.assertEqual(test_red_general_moves, {(1, 5), (1, 4), (2, 5)})


class TestGuard(unittest.TestCase):
	"""Testing the Guard class."""

	def test_get_starting_position(self):
		"""Testing the get_starting position method for the Guards."""

		test_red_guard_0 = Guard("RED", 0)
		test_red_guard_1 = Guard("RED", 1)
		test_blue_guard_0 = Guard("BLUE", 0)
		test_blue_guard_1 = Guard("BLUE", 1)

		self.assertEqual(test_red_guard_0.get_starting_position(), (0, 3))
		self.assertEqual(test_red_guard_1.get_starting_position(), (0, 5))
		self.assertEqual(test_blue_guard_0.get_starting_position(), (9, 3))
		self.assertEqual(test_blue_guard_1.get_starting_position(), (9, 5))

	def test_legal_moves(self):
		"""Testing the legal_moves method for the Guards."""

		game = JanggiGame()
		test_red_guard_0 = game.get_players()["RED"][1]
		test_red_guard_1 = game.get_players()["RED"][2]
		test_blue_guard_0 = game.get_players()["BLUE"][1]
		test_blue_guard_1 = game.get_players()["BLUE"][2]

		self.assertEqual(test_red_guard_0.legal_moves(game.get_board(), game.get_position(test_red_guard_0)),
		                 {(0, 3), (0, 4), (1, 3)})
		self.assertEqual(test_red_guard_1.legal_moves(game.get_board(), game.get_position(test_red_guard_1)),
		                 {(0, 5), (0, 4), (1, 5)})
		self.assertEqual(test_blue_guard_0.legal_moves(game.get_board(), game.get_position(test_blue_guard_0)),
		                 {(9, 3), (8, 3), (9, 4)})
		self.assertEqual(test_blue_guard_1.legal_moves(game.get_board(), game.get_position(test_blue_guard_1)),
		                 {(9, 5), (8, 5), (9, 4)})

		# Moving the Red General to (2, 4)
		game._board[(2, 4)] = game._board[(1, 4)]
		game._board[(1, 4)] = None
		self.assertEqual(test_red_guard_0.legal_moves(game.get_board(), game.get_position(test_red_guard_0)),
		                 {(0, 3), (0, 4), (1, 3), (1, 4)})

		# Moving the Guard 0 to (1, 4). Red General is still at (2, 4)
		game._board[(1, 4)] = game._board[(0, 3)]
		game._board[(0, 3)] = None
		self.assertEqual(test_red_guard_0.legal_moves(game.get_board(), game.get_position(test_red_guard_0)),
		                 {(1, 4), (0, 3), (0, 4), (1, 3), (1, 5), (2, 3), (2, 5)})


class TestHorse(unittest.TestCase):
	"""Testing the Horse class."""

	def test_get_starting_position(self):
		"""Testing the get_starting position method for the Horse."""

		test_red_horse_0 = Horse("RED", 0)
		test_red_horse_1 = Horse("RED", 1)
		test_blue_horse_0 = Horse("BLUE", 0)
		test_blue_horse_1 = Horse("BLUE", 1)

		self.assertEqual(test_red_horse_0.get_starting_position(), (0, 2))
		self.assertEqual(test_red_horse_1.get_starting_position(), (0, 7))
		self.assertEqual(test_blue_horse_0.get_starting_position(), (9, 2))
		self.assertEqual(test_blue_horse_1.get_starting_position(), (9, 7))

	def test_legal_moves(self):
		"""Testing the legal_moves method for the Horses."""

		game = JanggiGame()
		test_red_horse_0 = game.get_players()["RED"][3]
		test_red_horse_1 = game.get_players()["RED"][4]
		test_blue_horse_0 = game.get_players()["BLUE"][3]
		test_blue_horse_1 = game.get_players()["BLUE"][4]

		self.assertEqual(test_red_horse_0.legal_moves(game.get_board(),
		                                              game.get_position(test_red_horse_0)), {(0, 2), (2, 3)})
		self.assertEqual(test_red_horse_1.legal_moves(game.get_board(),
		                                              game.get_position(test_red_horse_1)), {(0, 7), (2, 6), (2, 8)})
		self.assertEqual(test_blue_horse_0.legal_moves(game.get_board(),
		                                               game.get_position(test_blue_horse_0)), {(9, 2), (7, 3)})
		self.assertEqual(test_blue_horse_1.legal_moves(game.get_board(),
		                                               game.get_position(test_blue_horse_1)), {(9, 7), (7, 6), (7, 8)})

		# Moving Red Horse 1 to (2, 3)
		game._board[(2, 3)] = game._board[(0, 2)]
		game._board[(0, 2)] = None
		self.assertEqual(test_red_horse_0.legal_moves(game.get_board(), game.get_position(test_red_horse_0)),
		                 {(2, 3), (0, 2), (1, 1), (3, 1), (4, 2), (4, 4), (3, 5), (1, 5), (0, 4)})

		# Moving Blue Horse 1 to (3, 3) and Blue Horse 2 to (3, 1)
		game._board[(3, 3)] = game._board[(9, 2)]
		game._board[(9, 2)] = None
		game._board[(3, 1)] = game._board[(9, 7)]
		game._board[(9, 7)] = None
		self.assertEqual(test_red_horse_0.legal_moves(game.get_board(), game.get_position(test_red_horse_0)),
		                 {(2, 3), (0, 2), (1, 1), (3, 1), (3, 5), (1, 5), (0, 4)})

class TestElephant(unittest.TestCase):
	"""Testing the Elephant class."""

	def test_get_starting_position(self):
		"""Testing the get_starting position method for the Elephant."""

		test_red_Elephant_0 = Elephant("RED", 0)
		test_red_Elephant_1 = Elephant("RED", 1)
		test_blue_Elephant_0 = Elephant("BLUE", 0)
		test_blue_Elephant_1 = Elephant("BLUE", 1)

		self.assertEqual(test_red_Elephant_0.get_starting_position(), (0, 1))
		self.assertEqual(test_red_Elephant_1.get_starting_position(), (0, 6))
		self.assertEqual(test_blue_Elephant_0.get_starting_position(), (9, 1))
		self.assertEqual(test_blue_Elephant_1.get_starting_position(), (9, 6))

	def test_legal_moves(self):
		"""Testing the legal_moves method for the Elephant."""

		game = JanggiGame()
		test_red_Elephant_0 = game.get_players()["RED"][5]
		test_red_Elephant_1 = game.get_players()["RED"][6]
		test_blue_Elephant_0 = game.get_players()["BLUE"][5]
		test_blue_Elephant_1 = game.get_players()["BLUE"][6]

		self.assertEqual(test_red_Elephant_0.legal_moves(game.get_board(), game.get_position(test_red_Elephant_0)),
		                 {(0, 1), (3, 3)})
		self.assertEqual(test_red_Elephant_1.legal_moves(game.get_board(), game.get_position(test_red_Elephant_1)),
		                 {(0, 6)})
		self.assertEqual(test_blue_Elephant_0.legal_moves(game.get_board(), game.get_position(test_blue_Elephant_0)),
		                 {(9, 1), (6, 3)})
		self.assertEqual(test_blue_Elephant_1.legal_moves(game.get_board(), game.get_position(test_blue_Elephant_1)),
		                 {(9, 6)})

		# Moving the Red Elephant 1 to (3, 3)
		game._board[(3, 3)] = game._board[(0, 1)]
		game._board[(0, 1)] = None
		self.assertEqual(test_red_Elephant_0.legal_moves(game.get_board(), game.get_position(test_red_Elephant_0)),
		                 {(3, 3), (0, 1), (6, 1), (6, 5)})

		# Red Element Remain at (3, 3)
		# Moving Blue Elephant 2 to (6, 5)
		game._board[(6, 5)] = game._board[(9, 6)]
		game._board[(9, 6)] = None

		self.assertEqual(test_red_Elephant_0.legal_moves(game.get_board(), game.get_position(test_red_Elephant_0)),
		                 {(3, 3), (0, 1), (6, 1), (6, 5)})
		self.assertEqual(test_blue_Elephant_1.legal_moves(game.get_board(), game.get_position(test_blue_Elephant_1)),
		                 {(6, 5), (3, 3), (3, 7)})


class TestChariot(unittest.TestCase):
	"""Testing the Chariot class."""

	def test_get_starting_position(self):
		"""Testing the get_starting position method for the Chariot."""

		test_red_Chariot_0 = Chariot("RED", 0)
		test_red_Chariot_1 = Chariot("RED", 1)
		test_blue_Chariot_0 = Chariot("BLUE", 0)
		test_blue_Chariot_1 = Chariot("BLUE", 1)

		self.assertEqual(test_red_Chariot_0.get_starting_position(), (0, 0))
		self.assertEqual(test_red_Chariot_1.get_starting_position(), (0, 8))
		self.assertEqual(test_blue_Chariot_0.get_starting_position(), (9, 0))
		self.assertEqual(test_blue_Chariot_1.get_starting_position(), (9, 8))

	def test_legal_moves(self):
		"""Testing the legal_moves method for the Chariot."""

		game = JanggiGame()
		test_red_Chariot_0 = game.get_players()["RED"][7]
		test_red_Chariot_1 = game.get_players()["RED"][8]
		test_blue_Chariot_0 = game.get_players()["BLUE"][7]
		test_blue_Chariot_1 = game.get_players()["BLUE"][8]

		self.assertEqual(test_red_Chariot_0.legal_moves(game.get_board(), game.get_position(test_red_Chariot_0)),
		                 {(0, 0), (1, 0), (2, 0)})
		self.assertEqual(test_red_Chariot_1.legal_moves(game.get_board(), game.get_position(test_red_Chariot_1)),
		                 {(0, 8), (1, 8), (2, 8)})
		self.assertEqual(test_blue_Chariot_0.legal_moves(game.get_board(), game.get_position(test_blue_Chariot_0)),
		                 {(9, 0), (7, 0), (8, 0)})
		self.assertEqual(test_blue_Chariot_1.legal_moves(game.get_board(), game.get_position(test_blue_Chariot_1)),
		                 {(9, 8), (7, 8), (8, 8)})

		# Move Red Chariot 1 to (7, 3) and Blue General to (9, 4)
		game._board[(7, 3)] = game._board[(0, 0)]
		game._board[(0, 0)] = None
		game._board[(9, 4)] = game._board[(8, 4)]
		game._board[(8, 4)] = None

		self.assertEqual(test_red_Chariot_0.legal_moves(game.get_board(), game.get_position(test_red_Chariot_0)),
		                 {(7, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (8, 3), (9, 3), (7, 2), (7, 1),
		                  (7, 4), (7, 5), (7, 6), (7, 7), (8, 4), (9, 5)})

		# Moving Red Chariot 2 to (9, 5)
		game._board[(9, 5)] = game._board[(0, 8)]
		game._board[(0, 8)] = None

		self.assertEqual(test_red_Chariot_0.legal_moves(game.get_board(), game.get_position(test_red_Chariot_0)),
		                 {(7, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (8, 3), (9, 3), (7, 2), (7, 1),
		                  (7, 4), (7, 5), (7, 6), (7, 7), (8, 4)})

		# Move Red Chariot 1 to (8, 4)
		game._board[(8, 4)] = game._board[(7, 3)]
		game._board[(7, 3)] = None
		self.assertEqual(test_red_Chariot_0.legal_moves(game.get_board(), game.get_position(test_red_Chariot_0)),
		                 {(8, 4), (8, 0), (8, 1), (8, 2), (8, 3), (8, 5), (8, 6), (8, 7), (8, 8), (7, 4), (6, 4),
		                  (7, 3), (7, 5), (9, 3), (9, 4)})


class TestCannon(unittest.TestCase):
	"""Testing the Cannon class."""

	def test_get_starting_position(self):
		"""Testing the get_starting position method for the Cannon."""

		test_red_cannon_0 = Cannon("RED", 0)
		test_red_cannon_1 = Cannon("RED", 1)
		test_blue_cannon_0 = Cannon("BLUE", 0)
		test_blue_cannon_1 = Cannon("BLUE", 1)

		self.assertEqual(test_red_cannon_0.get_starting_position(), (2, 1))
		self.assertEqual(test_red_cannon_1.get_starting_position(), (2, 7))
		self.assertEqual(test_blue_cannon_0.get_starting_position(), (7, 1))
		self.assertEqual(test_blue_cannon_1.get_starting_position(), (7, 7))

	def test_legal_moves(self):
		"""Testing the legal_moves method for the Cannons."""

		game = JanggiGame()
		test_red_cannon_0 = game.get_players()["RED"][9]
		test_red_cannon_1 = game.get_players()["RED"][10]
		test_blue_cannon_0 = game.get_players()["BLUE"][9]
		test_blue_cannon_1 = game.get_players()["BLUE"][10]

		self.assertEqual(test_red_cannon_0.legal_moves(game.get_board(), game.get_position(test_red_cannon_0)),
		                 {(2, 1)})
		self.assertEqual(test_red_cannon_1.legal_moves(game.get_board(), game.get_position(test_red_cannon_1)),
		                 {(2, 7)})
		self.assertEqual(test_blue_cannon_0.legal_moves(game.get_board(), game.get_position(test_blue_cannon_0)),
		                 {(7, 1)})
		self.assertEqual(test_blue_cannon_1.legal_moves(game.get_board(), game.get_position(test_blue_cannon_1)),
		                 {(7, 7)})

		# Moving Red Cannon 1 to (2, 4)
		game._board[(2, 4)] = game._board[(2, 1)]
		game._board[(2, 1)] = None
		self.assertEqual(test_red_cannon_0.legal_moves(game.get_board(), game.get_position(test_red_cannon_0)),
		                 {(2, 4), (0, 4), (4, 4), (5, 4), (6, 4)})

		# Moving Red Cannon 2 to (3, 7)
		game._board[(3, 7)] = game._board[(2, 7)]
		game._board[(2, 7)] = None
		self.assertEqual(test_red_cannon_1.legal_moves(game.get_board(), game.get_position(test_red_cannon_1)),
		                 {(3, 7), (3, 5)})

		# Moving Blue Cannon 2 to (7, 5)
		game._board[(7, 5)] = game._board[(7, 7)]
		game._board[(7, 7)] = None
		self.assertEqual(test_blue_cannon_1.legal_moves(game.get_board(), game.get_position(test_blue_cannon_1)),
		                 {(7, 5)})

		# Moving Blue Guard 1 to (9, 4)
		game._board[(9, 4)] = game._board[(9, 3)]
		game._board[(9, 3)] = None
		self.assertEqual(test_blue_cannon_1.legal_moves(game.get_board(), game.get_position(test_blue_cannon_1)),
		                 {(7, 5), (9, 3)})

		# Moving Blue General to (8, 5)
		game._board[(8, 5)] = game._board[(8, 4)]
		game._board[(8, 4)] = None
		self.assertEqual(test_blue_cannon_1.legal_moves(game.get_board(), game.get_position(test_blue_cannon_1)),
		                 {(7, 5)})

		# Moving Red Cannon 1 to (8, 4)
		game._board[(8, 4)] = game._board[(2, 4)]
		game._board[(2, 4)] = None
		self.assertEqual(test_blue_cannon_1.legal_moves(game.get_board(), game.get_position(test_blue_cannon_1)),
		                 {(7, 5)})

		# Moving Red Cannon 2 to (3, 5)
		game._board[(3, 5)] = game._board[(3, 7)]
		game._board[(3, 7)] = None
		self.assertEqual(test_red_cannon_1.legal_moves(game.get_board(), game.get_position(test_red_cannon_1)),
		                 {(3, 5), (3, 3), (3, 7)})
		self.assertEqual(test_blue_cannon_1.legal_moves(game.get_board(), game.get_position(test_blue_cannon_1)),
		                 {(7, 5)})

		# Moving Blue Guard 1 to (8, 4)
		game._board[(8, 4)] = game._board[(9, 4)]
		game._board[(9, 4)] = None

		# Moving Red Cannon 2 to (9, 3)
		game._board[(9, 3)] = game._board[(3, 5)]
		game._board[(3, 5)] = None
		self.assertEqual(test_blue_cannon_1.legal_moves(game.get_board(), game.get_position(test_blue_cannon_1)),
		                 {(7, 5)})


class TestSoldier(unittest.TestCase):
	"""Testing the Soldier class."""

	def test_get_starting_position(self):
		"""Testing the get_starting position method for the Soldier."""

		test_red_solider_0 = Soldier("RED", 0)
		test_red_solider_1 = Soldier("RED", 1)
		test_red_solider_2 = Soldier("RED", 2)
		test_red_solider_3 = Soldier("RED", 3)
		test_red_solider_4 = Soldier("RED", 4)
		test_blue_solider_0 = Soldier("BLUE", 0)
		test_blue_solider_1 = Soldier("BLUE", 1)
		test_blue_solider_2 = Soldier("BLUE", 2)
		test_blue_solider_3 = Soldier("BLUE", 3)
		test_blue_solider_4 = Soldier("BLUE", 4)

		self.assertEqual(test_red_solider_0.get_starting_position(), (3, 0))
		self.assertEqual(test_red_solider_1.get_starting_position(), (3, 2))
		self.assertEqual(test_red_solider_2.get_starting_position(), (3, 4))
		self.assertEqual(test_red_solider_3.get_starting_position(), (3, 6))
		self.assertEqual(test_red_solider_4.get_starting_position(), (3, 8))

		self.assertEqual(test_blue_solider_0.get_starting_position(), (6, 0))
		self.assertEqual(test_blue_solider_1.get_starting_position(), (6, 2))
		self.assertEqual(test_blue_solider_2.get_starting_position(), (6, 4))
		self.assertEqual(test_blue_solider_3.get_starting_position(), (6, 6))
		self.assertEqual(test_blue_solider_4.get_starting_position(), (6, 8))

	def test_legal_moves(self):
		"""Testing the legal_moves method for the Soldier."""

		game = JanggiGame()
		test_red_solider_0 = game.get_players()["RED"][11]
		test_red_solider_1 = game.get_players()["RED"][12]
		test_red_solider_2 = game.get_players()["RED"][13]
		test_red_solider_3 = game.get_players()["RED"][14]
		test_red_solider_4 = game.get_players()["RED"][15]

		test_blue_solider_0 = game.get_players()["BLUE"][11]
		test_blue_solider_1 = game.get_players()["BLUE"][12]
		test_blue_solider_2 = game.get_players()["BLUE"][13]
		test_blue_solider_3 = game.get_players()["BLUE"][14]
		test_blue_solider_4 = game.get_players()["BLUE"][15]

		self.assertEqual(test_red_solider_0.legal_moves(game.get_board(), game.get_position(test_red_solider_0)),
		                 {(3, 0), (3, 1), (4, 0)})
		self.assertEqual(test_red_solider_1.legal_moves(game.get_board(), game.get_position(test_red_solider_1)),
		                 {(3, 2), (3, 1), (3, 3), (4, 2)})
		self.assertEqual(test_red_solider_2.legal_moves(game.get_board(), game.get_position(test_red_solider_2)),
		                 {(3, 4), (3, 3), (3, 5), (4, 4)})
		self.assertEqual(test_red_solider_3.legal_moves(game.get_board(), game.get_position(test_red_solider_3)),
		                 {(3, 6), (3, 5), (3, 7), (4, 6)})
		self.assertEqual(test_red_solider_4.legal_moves(game.get_board(), game.get_position(test_red_solider_4)),
		                 {(3, 8), (3, 7), (4, 8)})

		self.assertEqual(test_blue_solider_0.legal_moves(game.get_board(), game.get_position(test_blue_solider_0)),
		                 {(6, 0), (6, 1), (5, 0)})
		self.assertEqual(test_blue_solider_1.legal_moves(game.get_board(), game.get_position(test_blue_solider_1)),
		                 {(6, 2), (6, 1), (6, 3), (5, 2)})
		self.assertEqual(test_blue_solider_2.legal_moves(game.get_board(), game.get_position(test_blue_solider_2)),
		                 {(6, 4), (6, 3), (6, 5), (5, 4)})
		self.assertEqual(test_blue_solider_3.legal_moves(game.get_board(), game.get_position(test_blue_solider_3)),
		                 {(6, 6), (6, 5), (6, 7), (5, 6)})
		self.assertEqual(test_blue_solider_4.legal_moves(game.get_board(), game.get_position(test_blue_solider_4)),
		                 {(6, 8), (6, 7), (5, 8)})

		# Move Red Soldier 2 to (5, 2)
		game._board[(5, 2)] = game._board[(3, 2)]
		game._board[(3, 2)] = None
		self.assertEqual(test_red_solider_1.legal_moves(game.get_board(), game.get_position(test_red_solider_1)),
		                 {(5, 2), (5, 1), (5, 3), (6, 2)})
		self.assertEqual(test_blue_solider_1.legal_moves(game.get_board(), game.get_position(test_blue_solider_1)),
		                 {(6, 2), (6, 1), (6, 3), (5, 2)})

		# Move Blue Soldier 3 to (2, 5)
		game._board[(2, 5)] = game._board[(6, 4)]
		game._board[(6, 4)] = None
		self.assertEqual(test_blue_solider_2.legal_moves(game.get_board(), game.get_position(test_blue_solider_2)),
		                 {(2, 5), (2, 4), (2, 6), (1, 5), (1, 4)})

		# Move Blue General to (9, 4)
		game._board[(9, 4)] = game._board[(8, 4)]
		game._board[(8, 4)] = None

		# Move Red Soldier 4 to (8, 4)
		game._board[(8, 4)] = game._board[(3, 6)]
		game._board[(3, 6)] = None

		# Move Red Soldier 5  to (9, 5)
		game._board[(9, 5)] = game._board[(3, 8)]
		game._board[(3, 8)] = None

		self.assertEqual(test_red_solider_3.legal_moves(game.get_board(), game.get_position(test_red_solider_3)),
		                 {(8, 4), (8, 3), (8, 5), (9, 3), (9, 4)})


if __name__ == "__main__":
	unittest.main()