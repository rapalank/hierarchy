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
pip install numpy

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

## Project Structure

```
hierarchy/
├── README.md
├── organism_simulation.py    # Main simulation script
├── .git/                     # Git repository
└── .idea/                    # IDE configuration
```

## Example Results

Sample output from a simulation with 30 organisms and 25 iterations:

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

## Mathematical Model

The battle system uses probability-based competition:
- Win probability: `P(win) = strength / (strength1 + strength2)`
- Strength transfer: `winner.strength = strength1 + strength2`
- Elimination: `loser.strength = 0`

This creates a positive feedback loop where initial advantages compound over time, leading to natural hierarchy formation.

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
