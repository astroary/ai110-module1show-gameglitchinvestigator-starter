from logic_utils import check_guess, parse_guess, update_score

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
    # Winning on the first attempt is worth the most, and the bonus never drops
    # below 10 even after many attempts.
    assert update_score(0, "Win", 1) == 100
    assert update_score(0, "Win", 3) == 80
    assert update_score(0, "Win", 20) == 10
