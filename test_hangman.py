import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from hangman import (
    evaluate_guess,
    load_leaderboard,
    main,
    show_leaderboard,
    update_leaderboard,
)


class HangmanLeaderboardTests(unittest.TestCase):
    def test_update_leaderboard_sorts_high_scores(self):
        with tempfile.NamedTemporaryFile("w+", delete=False) as temp_file:
            path = temp_file.name

        update_leaderboard("Alice", 30, "animals", "easy", file_path=path)
        update_leaderboard("Bob", 50, "countries", "medium", file_path=path)
        update_leaderboard("Charlie", 40, "fruits", "hard", file_path=path)

        leaderboard = load_leaderboard(file_path=path)

        self.assertEqual(leaderboard[0]["name"], "Bob")
        self.assertEqual(leaderboard[0]["score"], 50)
        self.assertEqual(leaderboard[1]["name"], "Charlie")
        self.assertEqual(leaderboard[2]["name"], "Alice")

    def test_load_leaderboard_handles_missing_file(self):
        self.assertEqual(load_leaderboard(file_path="missing_leaderboard.txt"), [])

    def test_evaluate_guess_returns_feedback(self):
        self.assertEqual(evaluate_guess(25, 10), "Too low")
        self.assertEqual(evaluate_guess(25, 40), "Too high")
        self.assertEqual(evaluate_guess(25, 25), "Correct")

    def test_show_leaderboard_displays_top_score(self):
        with tempfile.NamedTemporaryFile("w+", delete=False) as temp_file:
            path = temp_file.name
        update_leaderboard("Alice", 30, "animals", "easy", file_path=path)

        output = StringIO()
        with redirect_stdout(output):
            show_leaderboard(file_path=path)

        self.assertIn("Alice - 30 points (animals, easy)", output.getvalue())

    @patch("builtins.input", side_effect=["Akshay", "x", "3"])
    def test_main_shows_menu_and_handles_invalid_choice(self, _mock_input):
        output = StringIO()
        with redirect_stdout(output):
            main()

        self.assertIn("1. Play game", output.getvalue())
        self.assertIn("2. View leaderboard", output.getvalue())
        self.assertIn("Invalid option", output.getvalue())
        self.assertIn("Thanks for playing!", output.getvalue())


if __name__ == "__main__":
    unittest.main()
