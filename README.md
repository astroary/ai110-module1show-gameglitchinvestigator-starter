# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **The game's purpose:** It is a number guessing game built with Streamlit.
  The app picks a secret number inside a range that depends on the difficulty
  (Easy 1–20, Normal 1–100, Hard 1–50). You type a guess, the game tells you if
  it is too high or too low, and you try to find the secret before you run out of
  attempts. Your score goes up when you win and down for wrong guesses.

- [x] **Bugs I found:**
  1. The hints were backwards — a guess that was too high told me to "Go HIGHER".
  2. Guesses outside the range (like -5) were accepted as valid.
  3. The "New Game" button did not fully reset, so after a win/loss the next
     guess was silently ignored.
  4. The hint flipped randomly on even attempts (the code turned the secret into
     a string, which broke the comparison).
  5. I had to click "Submit Guess" twice for it to register.
  6. The score jumped around (a "Too High" guess sometimes added points) and a
     slow win still ended at 0. The debug panel also showed stale numbers.

- [x] **Fixes I applied:**
  - Moved the game logic (`check_guess`, `parse_guess`, `update_score`,
    `get_range_for_difficulty`) out of `app.py` into `logic_utils.py`.
  - Fixed the hint direction and removed the string conversion that flipped it.
  - Added range validation in `parse_guess` so out-of-range guesses are rejected.
  - Made "New Game" reset the status, score, and history (and use the right range).
  - Wrapped the guess box and Submit button in an `st.form` so one click submits.
  - Rewrote the scoring so wrong guesses cost a flat 5 points and faster wins are
    worth more, and moved the debug panel to the bottom so it shows live numbers.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Run `python -m streamlit run app.py` and open the app in the browser.
2. Leave the difficulty on "Normal" (range 1–100). Open "Developer Debug Info" at
   the bottom to see the secret number (for this example, say the secret is 44).
3. Enter a guess of `70` and click "Submit Guess" once → the hint says
   "📉 Go LOWER!" because 70 is too high, and the score drops by 5.
4. Enter a guess of `30` → the hint says "📈 Go HIGHER!" because 30 is too low,
   and the score drops by another 5.
5. Enter a guess of `44` → "🎉 Correct!", balloons appear, and the game shows the
   final score. Clicking "New Game 🔁" resets everything so you can play again.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ pytest tests/ -v
============================= test session starts ==============================
collected 7 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 14%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 28%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 42%]
tests/test_game_logic.py::test_out_of_range_guess_is_rejected PASSED     [ 57%]
tests/test_game_logic.py::test_in_range_guess_is_accepted PASSED         [ 71%]
tests/test_game_logic.py::test_wrong_guess_always_loses_five_points PASSED [ 85%]
tests/test_game_logic.py::test_win_scores_more_for_fewer_attempts PASSED [100%]

============================== 7 passed in 0.04s ===============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
