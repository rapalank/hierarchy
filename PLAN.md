# Plan

Next steps for the hierarchy simulation, ordered by priority.

## Done

Steps 1–5 of the original plan are complete.

1. **The simulation is scriptable.** `organism_simulation.py` takes `--organisms`, `--battles`, `--seed` and `--export`, and prompts only for counts that are left out. With no `--seed`, it picks one at random and prints it. `requirements.txt` and `requirements-dev.txt` list the dependencies.
2. **There are tests.** `tests/test_organism_simulation.py` covers strength conservation, battle outcomes, pairing only living organisms, stopping at one survivor, win rates, same-seed reproducibility, bucket totals, export and the command-line options. Writing the reproducibility test showed that every simulation shared Python's global random generator, so creating a second one changed the first one's run. Each simulation now has its own generator, which still gives the same results as before for a given seed.
3. **Strength buckets count each organism once.** Each bucket in `STRENGTH_BUCKETS` excludes its lower bound and includes its upper bound, and "Dead" is no longer a special case.
4. **Python runs can be replayed in the browser.** `--export run.json` writes the seed, starting strengths and battle history. `organism_arena.html` loads the file from a file picker or by drag-and-drop, checks it, and replays every battle in order.
5. **The README is up to date.** It documents the options, tests and replay workflow, and explains that the mean strength never changes.

## Open questions

- Should the simulation support other battle rules, such as a partial strength transfer or a cost for fighting? If so, make the battle rule a pluggable function, and have the export record which rule was used so the visualization can replay it.
- Is IntelliJ the only editor in use? If so, keeping `.idea/` in the repo is fine. If not, consider ignoring the machine-specific files (`misc.xml`, `hierarchy.iml`).
