from logic_utils import (
    check_guess,
    parse_guess,
    update_score,
    get_proximity,
    load_high_score,
    save_high_score,
)


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# --- New tests for the bugs fixed in Phase 2 ---

def test_out_of_range_guess_is_rejected():
    # Bug #1: a guess below the range should be rejected, not accepted.
    ok, value, error = parse_guess("-5", 1, 100)
    assert ok is False
    assert value is None
    assert "between 1 and 100" in error


def test_in_range_guess_is_accepted():
    # A normal guess inside the range still works.
    ok, value, error = parse_guess("42", 1, 100)
    assert ok is True
    assert value == 42
    assert error is None


def test_wrong_guess_always_loses_five_points():
    # Bug #4: every wrong guess should cost 5 points, including "Too High".
    # The old code gave +5 for "Too High" on even attempts.
    assert update_score(50, "Too High", 2) == 45
    assert update_score(50, "Too Low", 3) == 45


def test_win_scores_more_for_fewer_attempts():
    # Winning on the first attempt is worth the most, and the bonus never
    # drops below 10 even after many attempts.
    assert update_score(0, "Win", 1) == 100
    assert update_score(0, "Win", 3) == 80
    assert update_score(0, "Win", 20) == 10


# --- Challenge 1: edge-case inputs that might still break the game ---

def test_decimal_guess_is_truncated_to_int():
    # Edge case: a decimal like "3.7" should not crash; it parses to an int.
    ok, value, error = parse_guess("3.7", 1, 100)
    assert ok is True
    assert value == 3
    assert error is None


def test_extremely_large_guess_is_rejected():
    # Edge case: a huge number is out of range and should be rejected cleanly.
    ok, value, error = parse_guess("999999999999", 1, 100)
    assert ok is False
    assert value is None
    assert "between 1 and 100" in error


def test_non_numeric_guess_is_rejected():
    # Edge case: letters should be handled gracefully, not crash.
    ok, value, error = parse_guess("abc", 1, 100)
    assert ok is False
    assert value is None
    assert error == "That is not a number."


def test_empty_guess_is_rejected():
    # Edge case: an empty submission asks the player to enter a guess.
    ok, value, error = parse_guess("", 1, 100)
    assert ok is False
    assert value is None
    assert error == "Enter a guess."


# --- Challenge 4: hot/cold proximity hint ---

def test_proximity_exact_match_is_bullseye():
    assert get_proximity(50, 50, 1, 100) == "🎯 Bullseye!"


def test_proximity_close_guess_is_hot():
    # Within 10% of the range (10 on a 1-100 board) reads as Hot.
    assert get_proximity(45, 50, 1, 100) == "🔥 Hot"


def test_proximity_far_guess_is_cold():
    assert get_proximity(5, 90, 1, 100) == "🧊 Cold"


# --- Challenge 2: persistent high score ---

def test_high_score_saves_and_loads(tmp_path):
    # Use a temp file so the test never touches the real high_score.txt.
    path = tmp_path / "high_score.txt"
    assert load_high_score(str(path)) == 0      # missing file -> 0
    assert save_high_score(120, str(path)) == 120
    assert load_high_score(str(path)) == 120


def test_high_score_keeps_the_best(tmp_path):
    path = tmp_path / "high_score.txt"
    save_high_score(80, str(path))
    # A lower score should not overwrite the existing best.
    assert save_high_score(50, str(path)) == 80
    assert load_high_score(str(path)) == 80
