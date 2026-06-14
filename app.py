import random
import streamlit as st

# FIX: core game logic was refactored out of app.py into logic_utils.py so the
# UI and the logic are separated and the logic can be unit-tested with pytest.
from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)

# FIX: hint text now lives in one place, mapped from the outcome. This fixes the
# backwards-hint bug (#2) where "Too High" used to say "Go HIGHER!".
HINT_MESSAGES = {
    "Win": "🎉 Correct!",
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
}

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    # FIX: start at 0 so "attempts left" is correct and matches the New Game reset.
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

st.info(
    # FIX: show the real range for the chosen difficulty instead of always "1 and 100".
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

# Show hint reacts right away, so it stays outside the form.
show_hint = st.checkbox("Show hint", value=True)

# FIX: the guess box and Submit button are wrapped in a form so one click (or
# pressing Enter) submits the typed value. Before this, clicking Submit while the
# cursor was still in the text box only committed the text on the first click, so
# you had to click a second time to actually submit (a Streamlit button quirk).
with st.form(key=f"guess_form_{difficulty}"):
    raw_guess = st.text_input("Enter your guess:")
    submit = st.form_submit_button("Submit Guess 🚀")

new_game = st.button("New Game 🔁")

if new_game:
    # FIX: a new game must reset EVERYTHING. The old version forgot status, score,
    # and history, so after winning/losing the next submit was silently ignored
    # (bug #3). It also now uses the difficulty range instead of hardcoded 1-100.
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    # FIX: pass the range so out-of-range guesses are rejected (bug #1).
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        # FIX: removed the code that turned the secret into a string on even
        # attempts. That caused a TypeError and made the hints flip randomly.
        outcome = check_guess(guess_int, st.session_state.secret)
        message = HINT_MESSAGES[outcome]

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()

# FIX: the debug panel is now drawn at the END of the script, after a guess is
# processed, so it shows the current score/attempts/history. Before, it was drawn
# before the guess handler ran, so it was always one step behind (stale).
with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

st.caption("Built by an AI that claims this code is production-ready.")
