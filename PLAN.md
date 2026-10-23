# Plan

Next steps for the hierarchy simulation, ordered by priority.

## Current state

- `organism_simulation.py` runs an interactive simulation: N organisms with uniform random strength in [0, 1), M random battles, and the winner absorbs the loser's strength.
- `organism_arena.html` replays the same rules in the browser, but it uses its own random generator, so it can't reproduce a Python run.
- There are no tests, no dependency file and no command-line options. The seed is hardcoded to 42 in `main()`.

## 1. Make the simulation scriptable

- Add `argparse` options for `--organisms`, `--battles` and `--seed`, and keep the interactive prompts as the fallback when no options are given.
- Stop hardcoding `seed=42`. Default to a random seed and print it so a run can be reproduced.
- Add a `requirements.txt` with `numpy`.

## 2. Add tests

Use `pytest`, with fixed seeds so the results are deterministic.

- Total strength is the same before and after any number of battles.
- After a battle, the loser has strength 0 and the winner has the combined strength.
- Battles only pair living organisms, and the run stops when fewer than two are alive.
- Over many trials, an organism's win rate approaches `s1 / (s1 + s2)`.
- The final-analysis buckets add up to N. This guards the "Very Weak" double-count fixed in PR #1.

## 3. Fix the strength bucket boundaries

`filter_by_strength` includes both ends of each range, so a strength exactly at 0.2, 0.4, 0.6 or 0.8 is counted in two buckets. Change the ranges so each one includes its upper bound and excludes its lower bound, then drop the special case for dead organisms. This is unlikely to happen with random floats, but it's a one-line fix once the tests from step 2 exist.

## 4. Export runs and replay them in the visualization

- Add a `--export run.json` option that writes the starting strengths and `battle_history`.
- Let `organism_arena.html` load that file, through a file picker or drag-and-drop, and replay the exact Python run. This removes the gap where a seed gives different draws in Python and in the browser.

## 5. Tidy up the README

- The "Example Results" section shows a final mean strength of 0.424. The mean never changes during a run because total strength is conserved, so say that this is also the starting mean.
- Document the new command-line options and the export and replay workflow once they exist.

## Open questions

- Should the simulation support other battle rules, such as a partial strength transfer or a cost for fighting? If so, the battle rule should become a pluggable function before steps 2 and 4 are built on it.
- Is IntelliJ the only editor in use? If so, keeping `.idea/` in the repo is fine. If not, consider ignoring the machine-specific files (`misc.xml`, `hierarchy.iml`).
