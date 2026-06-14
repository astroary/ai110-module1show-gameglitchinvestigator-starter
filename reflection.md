# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

  The first time I ran it, the game looked normal. It was a number guessing game
  with a difficulty selector in the sidebar, a box to type my guess, and a
  "Developer Debug Info" panel that showed the secret number. The problems only
  showed up once I started playing: the hints pointed me the wrong way, and the
  game would not let me start over properly.

- List at least two concrete bugs you noticed at the start
  (for example: "the hints were backwards").

  The first two bugs I noticed while playing on my own were:
  1. **The higher/lower hints were backwards.** When my guess was too low, it
     told me to "Go LOWER," and when it was too high it told me to "Go HIGHER,"
     so following the hints actually moved me away from the answer.
  2. **Starting a new game was broken.** After I clicked "New Game" and typed a
     guess, clicking "Submit Guess" did nothing — the game would not accept my
     guess. While digging into these, I found more issues, listed in the table
     below.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| I guessed -5 | It should say my guess is out of the 1 to 100 range | It accepted the guess and said "Go LOWER" even though -5 is already too low | none |
| Secret was 70 and I guessed 30 | It should say "Go HIGHER" because my guess is too low | It said "Go LOWER", which is the wrong direction | none |
| I clicked New Game, typed a number, then clicked Submit Guess | It should start a new game and accept my guess | Nothing happened and my guess was never submitted | none |
| I typed a guess and clicked Submit Guess once | The guess should submit on the first click | I had to click Submit Guess twice before it would submit | none |
| I made several wrong guesses, then won | The score should make sense (lose points for wrong guesses, gain points for winning) | The score jumped around (a "Too High" guess sometimes added points) and a slow win ended at 0 | none |
| I checked the Developer Debug Info while playing | It should show my current score, attempts, and history | It showed numbers that were one guess behind (stale) | none |

**Code-level cause of each bug**

After investigating, here is the part of the code responsible for each bug:

1. **Backwards hint (rows 1–2):** in `check_guess`, the "Too High" outcome
   returned the message "Go HIGHER!" and "Too Low" returned "Go LOWER!" — the
   messages were swapped. `app.py` also turned the secret into a string on every
   even attempt, which broke the comparison and flipped the hint.
2. **Out-of-range guess (row 1):** `parse_guess` only checked that the input was
   a number, never that it was inside the 1–100 range, so -5 was accepted.
3. **New Game freeze (row 3):** the `if new_game:` block in `app.py` reset
   `attempts` and `secret` but forgot to reset `status`, `score`, and `history`,
   so a finished game stayed "won"/"lost" and `st.stop()` swallowed the next guess.
4. **Click Submit twice (row 4):** the guess box and Submit button were separate
   widgets, so clicking Submit first only made the text box lose focus (a
   Streamlit button quirk); it needed to be wrapped in a form.
5. **Haywire score (row 5):** `update_score` added +5 for a "Too High" guess on
   even attempts and shrank the win bonus with `100 - 10 * (attempt + 1)`, so a
   slow win ended near 0.
6. **Stale debug panel (row 6):** the debug expander was drawn near the top of
   `app.py`, before the guess handler ran, so it always showed last turn's values.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

  I used my AI coding assistant in VS Code. I attached app.py and logic_utils.py
  so it could see how the UI file and the logic file connect.

- Give one example of an AI suggestion that was correct (including what the AI
  suggested and how you verified the result).

  The AI suggested moving the game logic (check_guess, parse_guess, update_score,
  and get_range_for_difficulty) out of app.py and into logic_utils.py, then
  importing those functions back into app.py. This made the logic easy to test on
  its own. I verified it by running pytest, and all 5 tests passed, including the
  starter tests that import check_guess from logic_utils.

- Give one example of an AI suggestion that was incorrect or misleading (including
  what the AI suggested and how you verified the result).

  At first the AI explained the backwards hint as only a swapped message ("Too High" was printing "Go HIGHER"). If I had only swapped the message text, the hint would still have glitched, because there was a second hidden cause: the code turned the secret number into a string on every even attempt, which made the comparison break. I caught this by reading the code carefully and testing a guess on my second attempt, where the hint still came out wrong. The real fix was to remove the string conversion AND fix the message.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

  I decided a bug was fixed when the game behaved the way I expected during
  manual play AND the pytest tests passed. For example, after the hint fix, a
  guess that was too high finally told me to go lower. For the bugs that are
  about the screen and not pure logic (the double-click, the stale debug panel),
  I checked them by playing: the guess now submits on one click, and the debug
  panel shows my current score instead of being one guess behind.

- Describe at least one test you ran (manual or using pytest) and what it showed
  you about your code.

  I ran `pytest` and added tests for the bugs I fixed. test_out_of_range_guess_is_rejected
  checks that parse_guess("-5", 1, 100) returns ok=False with an error message,
  which before my fix would have passed -5 as a valid guess. I also added
  test_wrong_guess_always_loses_five_points and test_win_scores_more_for_fewer_attempts
  for the new scoring rules, which proved that a "Too High" guess no longer adds
  points and that a fast win is worth more than a slow one. All 7 tests passed.

- Did AI help you design or understand any tests? How?

  Yes. The AI helped me write the new pytest cases and explained that the
  existing starter tests expected check_guess to return just the outcome string
  (like "Win"), not a tuple. That told me how to shape the refactor so the old
  tests would still pass.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has
  never used Streamlit?

  Streamlit runs your whole script from top to bottom every time you click a
  button or type something. So normal variables get created fresh each time and
  forget their old values. To remember things between clicks (like the secret
  number, the score, and how many attempts you have left), you have to store them
  in `st.session_state`, which sticks around across reruns. This also explained
  two of my bugs: the debug panel showed old numbers because it was drawn before
  the new guess was processed, and I had to click Submit twice because a button
  is only "true" for the one rerun right after you click it.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future
  labs or projects?

  I want to keep writing pytest tests right after I fix something. Seeing a test
  fail and then pass gave me real proof that the bug was actually gone, instead of
  just hoping it was. I also liked keeping the logic in its own file so it was easy
  to test.

- What is one thing you would do differently next time you work with AI on a
  coding task?

  Next time I would ask the AI to explain the cause of a bug before I let it
  change anything, and I would read the whole function instead of just the one
  line. The backwards-hint bug had a second hidden cause, and I would have missed
  it if I had trusted the first quick answer.

- In one or two sentences, describe how this project changed the way you think
  about AI generated code.

  I learned that AI-generated code can look finished and still be full of quiet
  bugs. I now treat the AI as a helpful teammate whose work I always have to read,
  test, and verify myself before trusting it.
