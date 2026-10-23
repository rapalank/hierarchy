# Hierarchy

A project for simulating organism populations with competitive battles and strength-based hierarchies.

## Description

This project simulates the evolution of hierarchical structures through competitive organism battles. It demonstrates how natural selection and competition lead to the emergence of dominance hierarchies, where stronger organisms accumulate strength through victories while weaker organisms are eliminated.

## Features

- **Organism Simulation**: Create N organisms with random strength values (0-1)
- **Competitive Battles**: Time-iterated battles with probability-based winning
- **Strength Transfer**: Winners absorb losers' strength, creating power accumulation
- **Statistical Analysis**: Track population dynamics, survival rates, and dominance patterns
- **Battle History**: Comprehensive logging of all battles and outcomes
- **Hierarchical Evolution**: Observe emergence of dominance hierarchies over time

## Installation

```bash
# Clone the repository
git clone https://github.com/rapalank/hierarchy.git
cd hierarchy

# Install dependencies
pip install -r requirements.txt

# Run the simulation
python3 organism_simulation.py
```

## Usage

The organism simulation allows you to model competitive evolution and hierarchy formation:

```bash
# Run with interactive prompts
python3 organism_simulation.py

# Example output:
# Enter the number of organisms to simulate (default 100): 50
# Enter the number of time iterations (default 20): 25
```

### Command-line options

Pass the counts as options to skip the prompts. Any count you leave out is still prompted for.

| Option | Meaning |
|---|---|
| `-n`, `--organisms` | Number of organisms (must be positive) |
| `-m`, `--battles` | Number of battles to run (0 or more) |
| `--seed` | Random seed. If omitted, one is chosen at random and printed so you can rerun the same simulation |
| `--export PATH` | Write the run (seed, starting strengths, and every battle) to a JSON file |

```bash
# 30 organisms, 25 battles, reproducible
python3 organism_simulation.py -n 30 -m 25 --seed 42

# Save the run so the visualization can replay it
python3 organism_simulation.py -n 30 -m 25 --seed 42 --export runs/run.json
```

The export creates the folder if needed. `runs/` is in `.gitignore`, so exported runs saved there never show up as changes.

The run stops early if fewer than two organisms are left alive, so `N` organisms allow at most `N - 1` battles.

### Running the tests

```bash
pip install -r requirements-dev.txt
python3 -m pytest
```

### Key Components

- **Organism Class**: Represents individual organisms with unique IDs and strength values
- **Battle System**: Probability-based combat where stronger organisms have higher win chances
- **Time Iterations**: Sequential rounds of random pairings and battles
- **Statistical Tracking**: Real-time analysis of population dynamics

### Simulation Output

The simulation provides comprehensive analysis including:
- Initial population statistics
- Battle-by-battle progression
- Final hierarchy structure
- Survival and dominance metrics
- Strength distribution analysis

### Visualization

`organism_arena.html` is an interactive, browser-based replay of the same battle rules. Open it directly in a browser (no build step or server needed):

```bash
open organism_arena.html
```

It shows organisms in a petri dish sized by strength, a leaderboard, a battle log, and a chart of how many organisms are alive versus how much of the total strength the strongest one holds. You can set the number of organisms, battles, seed, and playback speed.

Random runs in the page use its own generator, so a seed gives different draws than the same seed in Python. To watch an exact Python run, export it with `--export runs/run.json`, then choose the file under **Python run** or drop it anywhere on the page. The page checks the file and replays every battle in order.

## Project Structure

```
hierarchy/
├── README.md
├── PLAN.md                   # Roadmap
├── organism_simulation.py    # Main simulation script
├── organism_arena.html       # Interactive battle visualization
├── requirements.txt          # Runtime dependencies
├── requirements-dev.txt      # Test dependencies
├── pytest.ini                # Test configuration
├── tests/                    # pytest suite
├── runs/                     # Exported runs (git-ignored)
├── .git/                     # Git repository
└── .idea/                    # IDE configuration
```

## Example Results

Sample output from `python3 organism_simulation.py -n 30 -m 25 --seed 42`:

```
=== Final State ===
Mean Strength:     0.424
Maximum Strength:  5.030
Organisms alive: 5
Organisms dead: 25

=== Top Winners ===
Organism #25: 4 wins, Strength = 5.030
Organism #5: 4 wins, Strength = 2.500
Organism #6: 3 wins, Strength = 2.020
```

The final mean strength (0.424) is the same as the starting mean. Battles move strength from loser to winner without creating or destroying any, so total strength, and therefore the mean, never changes. What changes is how it's spread: here 5 organisms hold all of it.

## Mathematical Model

The battle system uses probability-based competition:
- Win probability: `P(win) = strength / (strength1 + strength2)`
- Strength transfer: `winner.strength = strength1 + strength2`
- Elimination: `loser.strength = 0`

This creates a positive feedback loop where initial advantages compound over time, leading to natural hierarchy formation.

Final strengths are grouped into buckets: Dead (0), Very Weak (0–0.2], Weak (0.2–0.4], Average (0.4–0.6], Strong (0.6–0.8], and Very Strong (above 0.8). Each bucket includes its upper bound only, so every organism is counted exactly once.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

[Your Name] - [Your Email]

## Acknowledgments

- Inspired by evolutionary biology and game theory principles
- Demonstrates emergence of hierarchical structures in competitive systems
