from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# Regression tests for the "Go HIGHER / Go LOWER" bug:
# 1. The hint messages were swapped (a too-high guess said "Go HIGHER!").
# 2. On even attempts the secret was compared as a string, so "9" > "50".

def test_too_high_guess_tells_player_to_go_lower():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_too_low_guess_tells_player_to_go_higher():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_guesses_are_compared_numerically_not_as_strings():
    # As strings, "9" > "50" and "100" < "50"; numerically it's the opposite.
    assert check_guess(9, 50) == ("Too Low", "📈 Go HIGHER!")
    assert check_guess(100, 50) == ("Too High", "📉 Go LOWER!")


# Regression test for the "New Game" bug: after a game ended, New Game picked a
# new secret but left status as "won"/"lost", so st.stop() blocked every guess.

from pathlib import Path
from streamlit.testing.v1 import AppTest

APP_PATH = str(Path(__file__).resolve().parent.parent / "app.py")

def test_new_game_after_game_over_allows_guessing_again():
    at = AppTest.from_file(APP_PATH).run()

    # Simulate a finished game.
    at.session_state.status = "lost"
    at.session_state.history = [10, 20, 30]
    at.run()

    new_game = next(b for b in at.button if "New Game" in b.label)
    new_game.click().run()

    assert at.session_state.status == "playing"
    assert at.session_state.history == []

    # The player must actually be able to submit a guess now.
    secret = at.session_state.secret
    guess = 1 if secret != 1 else 2
    at.text_input(key="guess_input_Normal").input(str(guess))
    submit = next(b for b in at.button if "Submit" in b.label)
    submit.click().run()

    assert at.session_state.history == [guess]
    assert not any("Game over" in e.value for e in at.error)
