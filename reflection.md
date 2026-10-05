# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
The game loaded as a simple Streamlit page with a difficulty setting, a box to enter a guess, and Submit, New Game, and Show hint controls. At first glance it looked like it worked, but the hints quickly stopped making sense and the game got stuck after a round ended.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
1. The hints were backwards: guessing too high told me to "Go HIGHER!" and guessing too low told me to "Go LOWER!"
2. On some attempts the hints were wrong even for the right direction, because the secret was compared as a string (so "9" counted as bigger than "50").
3. After winning or losing, clicking New Game did not let me keep playing; guesses were blocked.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess 60 when the secret is 50 | "Too High" with the hint "Go LOWER!" | Hint said "Go HIGHER!" | No error, wrong message |
| Guess 9 when the secret is 50 (on an even attempt) | "Too Low" with the hint "Go HIGHER!" | Said "Too High", because "9" > "50" as strings | No error, wrong outcome |
| Finish a game, then click New Game and submit a guess | Fresh game starts and guesses are accepted | New secret was picked, but status stayed "won"/"lost", so guesses were blocked | No error, app stopped at `st.stop()` |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used Claude for this project.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
AI found and fixed the new-game button bug correctly reseting the user attempts and allowed the user to input new guesses. AI noted that ending a game sets status to "won"/"lost", but New Game never resets it to "playing," so the st.stop() guard keeps blocking guesses after rerun. I verified the results by mkaing and running pytests and also testing it in the UI.

- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
Initially when I asked AI to generate pytests for the first bug (too high, too low hints), it created pytests that compare the whole return value to a single word. After thorugh testing, I checked manually and mentioned the error to AI and we updated the test cases accordingly.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I ran pytests and rebooted the streamlit system to check via the UI too.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
A manual test I ran was finishing one game and using the new-game button to start a new game session. I repeated this a few times to ensure it was working as expected.

- Did AI help you design or understand any tests? How?
Yes, AI helped me design my pytests for the bugs fixed. When I ran into an error about how the pytests were failing... it fixed the test value to function as expected.

---

## 4. What did you learn about Streamlit and state?

Every time you click a button or type something, Streamlit reruns the whole script from top to bottom, so normal variables get wiped and start over. Session state is like a notebook that survives those reruns, so it's where you keep things like the secret number, attempts, and whether the game is won. That's why the New Game bug happened: the old "won" status was still saved in session state, so the game stayed stuck until we reset it.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
Having an AI-agent open readily to break down complex problems instead of spending too much time confused.

- What is one thing you would do differently next time you work with AI on a coding task?
Provide a clean system architetecture and test the code heavily before pushing to production.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
It is never all wrong or all right. Just like humans, AI makes mistakes. But working with it will make code that supercedes both human-only and AI-only code production. 
