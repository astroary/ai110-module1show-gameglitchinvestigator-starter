# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the agent to add a persistent "High Score" feature: save the best
score to a file so it survives across games and new browser sessions, and show
it in the sidebar. I also asked it to enhance the UI with a hot/cold proximity
hint and a session summary table.

**What did the agent do?**

- Added `load_high_score()` and `save_high_score()` to `logic_utils.py`
  (they read/write a `high_score.txt` file and keep only the larger score).
- Added `get_proximity()` to `logic_utils.py` for the hot/cold hint.
- Updated `app.py` to show the high score in the sidebar with `st.metric`,
  save the high score on a win, show the proximity caption after each guess,
  and render a "Session Summary" table from a new `rounds` session-state list.
- Added `high_score.txt` to `.gitignore` so the runtime file is not committed.
- Wrote pytest cases for all of the above.

**What did you have to verify or fix manually?**

- I made the high-score functions take a `path` argument so the tests could
  use a temporary file (`tmp_path`) instead of writing the real one.
- I checked that the "New high score" message only appears when the new score
  actually ties or beats the stored best.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

**Prompt used:** "Look at parse_guess and get_proximity in logic_utils.py.
Suggest three edge-case inputs that might still break the game and write pytest
cases that verify each one is handled gracefully."

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Decimal input like `3.7` | (prompt above) | `test_decimal_guess_is_truncated_to_int` | Yes | Decimals shouldn't crash; they truncate to an int. |
| Extremely large number `999999999999` | (prompt above) | `test_extremely_large_guess_is_rejected` | Yes | Huge values are out of range and must be rejected cleanly. |
| Non-numeric text `abc` | (prompt above) | `test_non_numeric_guess_is_rejected` | Yes | Letters should give a friendly error, not an exception. |

Empty input was also added (`test_empty_guess_is_rejected`) for completeness.

Terminal output (all tests passing) is pasted in `README.md`.

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
Add professional docstrings to every function in logic_utils.py, then run
pycodestyle on app.py, logic_utils.py, and the tests and fix any PEP 8 issues.
```

**Linting output before:**

```
$ pycodestyle app.py logic_utils.py tests/test_game_logic.py
tests/test_game_logic.py:10:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:15:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:20:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:35:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:42:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:48:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:65:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:72:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:79:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:92:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:96:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:109:1: E302 expected 2 blank lines, found 1
```

**Linting output after:**

```
$ pycodestyle app.py logic_utils.py tests/test_game_logic.py
(no output - all files pass)
```

**Changes applied:**

- Added Google-style docstrings (Args/Returns) to every function in
  `logic_utils.py`, plus a module-level docstring.
- Added a second blank line between the test functions to satisfy `E302`.
- While adding the new features I kept all comment and code lines within the
  79-character limit so `app.py` and `logic_utils.py` stayed clean from the
  start.

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:** I gave each model the buggy starter code and asked
what was wrong and how to fix it. I focused on the backwards higher/lower hint as
the specific logic bug.

| | Model A: Google Gemini | Model B: Claude (Opus 4.8, in VS Code) |
|-|------------------------|----------------------------------------|
| **Model name** | Google Gemini | Claude Opus 4.8 |
| **Response summary** | Gave general debugging advice: "test the inputs and see the expected outputs" and "test the button functionalities to make sure they work correctly." It did not name a specific bug or give a code fix. | Pinpointed specific bugs — the swapped messages in `check_guess`, the secret being turned into a string on even attempts, the missing range check in `parse_guess`, and the New Game button not resetting state — and gave concrete corrected code. |
| **More Pythonic fix?** | No actual code was provided, so there was nothing to judge. | Yes — it provided the corrected functions directly. |
| **Clearer explanation?** | Clear and simple, but generic; it never explained the *cause* of the bug. | Clearer for this task — it explained the exact line-level cause of each bug. |

**Which did you prefer and why?**

For this task I preferred Claude, because it found the exact buggy lines and gave
working fixes that I could verify with pytest, while Gemini only gave high-level
advice. That said, Gemini's instinct to "write tests for the inputs and buttons"
was genuinely good practice — it is basically the testing-first habit that later
helped me catch the edge cases. So Claude was the better debugger here, but
Gemini's advice was a reminder to verify everything with tests rather than trust
a fix on sight.
