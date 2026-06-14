"""Core game logic for the Number Guessing Game.

These functions are kept free of Streamlit so they can be unit-tested on
their own with pytest. The Streamlit UI in ``app.py`` imports and calls them.
"""

DEFAULT_HIGH_SCORE_PATH = "high_score.txt"


def get_range_for_difficulty(difficulty):
    """Return the inclusive ``(low, high)`` range for a difficulty.

    Args:
        difficulty: One of ``"Easy"``, ``"Normal"``, or ``"Hard"``.

    Returns:
        A ``(low, high)`` tuple. Unknown values fall back to ``(1, 100)``.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw, low=None, high=None):
    """Parse raw user input into an integer guess.

    When ``low`` and ``high`` are supplied, the guess must fall inside that
    inclusive range or it is rejected.

    Args:
        raw: The raw text entered by the player.
        low: Optional lower bound of the allowed range.
        high: Optional upper bound of the allowed range.

    Returns:
        A ``(ok, guess_int, error_message)`` tuple. On success ``ok`` is
        ``True`` and ``error_message`` is ``None``; on failure ``ok`` is
        ``False`` and ``guess_int`` is ``None``.
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    # FIX: reject guesses outside the allowed range so out-of-range numbers
    # like -5 or 0 are no longer treated as valid guesses (bug #1).
    if low is not None and high is not None and not (low <= value <= high):
        return False, None, f"Enter a number between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """Compare a guess to the secret and return the outcome.

    Args:
        guess: The player's guessed number.
        secret: The secret number to find.

    Returns:
        One of the strings ``"Win"``, ``"Too High"``, or ``"Too Low"``.
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score, outcome, attempt_number):
    """Return the new score after a guess.

    FIX (haywire score, bug #4): the old rules gave +5 for a "Too High"
    guess on even attempts and shrank the win bonus so fast that quick wins
    scored 0. Now a win is worth more the fewer attempts it took (floored at
    10), and every wrong guess costs a flat 5 points.

    Args:
        current_score: The score before this guess.
        outcome: The outcome from :func:`check_guess`.
        attempt_number: Which attempt this was (1 for the first guess).

    Returns:
        The updated score as an integer.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score


def get_proximity(guess, secret, low, high):
    """Return a hot/cold label describing how close a guess is.

    The distance is measured relative to the size of the range so the label
    means the same thing on Easy (1-20) as on Normal (1-100).

    Args:
        guess: The player's guessed number.
        secret: The secret number to find.
        low: Lower bound of the range.
        high: Upper bound of the range.

    Returns:
        A short labelled string such as ``"🔥 Hot"`` or ``"🧊 Cold"``.
    """
    distance = abs(guess - secret)
    if distance == 0:
        return "🎯 Bullseye!"

    span = high - low
    ratio = distance / span if span else 1
    if ratio <= 0.10:
        return "🔥 Hot"
    if ratio <= 0.25:
        return "🙂 Warm"
    return "🧊 Cold"


def load_high_score(path=DEFAULT_HIGH_SCORE_PATH):
    """Read the saved high score from disk.

    Args:
        path: File the high score is stored in.

    Returns:
        The stored high score, or ``0`` if the file is missing or unreadable.
    """
    try:
        with open(path) as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0


def save_high_score(score, path=DEFAULT_HIGH_SCORE_PATH):
    """Save ``score`` as the high score if it beats the stored one.

    Args:
        score: The score to consider saving.
        path: File the high score is stored in.

    Returns:
        The resulting high score (the larger of the new and stored values).
    """
    best = max(score, load_high_score(path))
    with open(path, "w") as f:
        f.write(str(best))
    return best
