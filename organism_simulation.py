import argparse
import json
import random
import numpy as np
from typing import List, Optional, Tuple

# Strength buckets for the final analysis. Each bucket excludes its lower bound
# and includes its upper bound, so every organism lands in exactly one bucket.
STRENGTH_BUCKETS = [
    (float('-inf'), 0.0, "Dead"),
    (0.0, 0.2, "Very Weak"),
    (0.2, 0.4, "Weak"),
    (0.4, 0.6, "Average"),
    (0.6, 0.8, "Strong"),
    (0.8, float('inf'), "Very Strong")
]

class Organism:
    """Represents an organism with a strength attribute."""
    
    def __init__(self, organism_id: int, strength: float):
        self.id = organism_id
        self.strength = strength
    
    def __repr__(self):
        return f"Organism(id={self.id}, strength={self.strength:.3f})"
    
    def __str__(self):
        return f"Organism #{self.id}: Strength = {self.strength:.3f}"

class OrganismSimulation:
    """Simulates a population of organisms with random strengths."""
    
    def __init__(self, num_organisms: int, time_iterations: int = 0, seed: Optional[int] = None):
        """
        Initialize the simulation with N organisms.
        
        Args:
            num_organisms: Number of organisms to create
            time_iterations: Number of time iterations to run battles
            seed: Random seed for reproducibility
        """
        # Each simulation owns its generator, so creating another simulation
        # can't disturb this one's sequence
        self.rng = random.Random(seed)

        self.num_organisms = num_organisms
        self.time_iterations = time_iterations
        self.seed = seed
        self.organisms = self._create_organisms()
        self.initial_strengths = [org.strength for org in self.organisms]
        self.battle_history = []
    
    def _create_organisms(self) -> List[Organism]:
        """Create N organisms with random strengths between 0 and 1."""
        organisms = []
        for i in range(self.num_organisms):
            strength = self.rng.random()  # Random float between 0 and 1
            organism = Organism(i + 1, strength)
            organisms.append(organism)
        return organisms
    
    def get_statistics(self) -> Tuple[float, float, float, float]:
        """
        Calculate basic statistics of the population.
        
        Returns:
            Tuple of (mean_strength, std_strength, min_strength, max_strength)
        """
        strengths = [org.strength for org in self.organisms]
        return (
            np.mean(strengths),
            np.std(strengths),
            min(strengths),
            max(strengths)
        )
    
    def get_strongest_organisms(self, count: int = 5) -> List[Organism]:
        """Get the top N strongest organisms."""
        return sorted(self.organisms, key=lambda x: x.strength, reverse=True)[:count]
    
    def get_weakest_organisms(self, count: int = 5) -> List[Organism]:
        """Get the bottom N weakest organisms."""
        return sorted(self.organisms, key=lambda x: x.strength)[:count]
    
    def filter_by_strength(self, min_strength: float, max_strength: float = 1.0) -> List[Organism]:
        """Filter organisms by strength range."""
        return [org for org in self.organisms if min_strength <= org.strength <= max_strength]

    def bucket_counts(self) -> List[Tuple[str, int]]:
        """Count organisms in each of STRENGTH_BUCKETS, as (label, count) pairs."""
        return [
            (label, sum(1 for org in self.organisms if low < org.strength <= high))
            for low, high, label in STRENGTH_BUCKETS
        ]

    def to_dict(self) -> dict:
        """Return the run's settings, starting strengths, and battle history."""
        return {
            'seed': self.seed,
            'num_organisms': self.num_organisms,
            'time_iterations': self.time_iterations,
            'initial_strengths': self.initial_strengths,
            'battle_history': self.battle_history
        }

    def export_json(self, path: str):
        """Write the run to a JSON file that organism_arena.html can replay."""
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    def display_population(self, max_display: int = 20):
        """Display the population information."""
        print(f"\n=== Population of {self.num_organisms} Organisms ===")
        
        if self.num_organisms <= max_display:
            for organism in self.organisms:
                print(f"  {organism}")
        else:
            print(f"  Showing first {max_display} of {self.num_organisms} organisms:")
            for organism in self.organisms[:max_display]:
                print(f"  {organism}")
            print(f"  ... and {self.num_organisms - max_display} more")
    
    def display_statistics(self):
        """Display population statistics."""
        mean_strength, std_strength, min_strength, max_strength = self.get_statistics()
        
        print(f"\n=== Population Statistics ===")
        print(f"  Mean Strength:     {mean_strength:.3f}")
        print(f"  Std Deviation:     {std_strength:.3f}")
        print(f"  Minimum Strength:  {min_strength:.3f}")
        print(f"  Maximum Strength:  {max_strength:.3f}")
    
    def battle(self, org1: Organism, org2: Organism) -> Tuple[Organism, Organism]:
        """
        Have two organisms battle. Winner takes loser's strength, loser gets 0.
        
        Args:
            org1: First organism
            org2: Second organism
            
        Returns:
            Tuple of (winner, loser)
        """
        total_strength = org1.strength + org2.strength
        
        # Probability of org1 winning is proportional to its strength
        prob_org1_wins = org1.strength / total_strength if total_strength > 0 else 0.5
        
        if self.rng.random() < prob_org1_wins:
            winner, loser = org1, org2
        else:
            winner, loser = org2, org1
        
        # Transfer strength
        winner_strength_before = winner.strength
        loser_strength_before = loser.strength
        
        winner.strength = total_strength
        loser.strength = 0.0
        
        # Record battle
        self.battle_history.append({
            'iteration': len(self.battle_history) + 1,
            'winner_id': winner.id,
            'loser_id': loser.id,
            'winner_strength_before': winner_strength_before,
            'loser_strength_before': loser_strength_before,
            'winner_strength_after': winner.strength,
            'loser_strength_after': loser.strength,
            'total_transferred': loser_strength_before
        })
        
        return winner, loser
    
    def run_time_iterations(self):
        """Run M time iterations of random battles."""
        if self.time_iterations <= 0:
            return
        
        print(f"\n=== Running {self.time_iterations} Time Iterations ===")
        
        for iteration in range(self.time_iterations):
            # Pick two random organisms (excluding dead ones with strength 0)
            alive_organisms = [org for org in self.organisms if org.strength > 0]
            
            if len(alive_organisms) < 2:
                print(f"  Iteration {iteration + 1}: Not enough alive organisms to battle. Stopping.")
                break
            
            org1, org2 = self.rng.sample(alive_organisms, 2)
            winner, loser = self.battle(org1, org2)
            
            if (iteration + 1) % max(1, self.time_iterations // 10) == 0 or iteration < 5:
                battle_data = self.battle_history[-1]
                print(f"  Iteration {iteration + 1}: Organism #{winner.id} ({battle_data['winner_strength_before']:.3f}) defeated Organism #{loser.id} ({battle_data['loser_strength_before']:.3f})")
    
    def display_battle_summary(self):
        """Display summary of battles."""
        if not self.battle_history:
            return
        
        print(f"\n=== Battle Summary ===")
        print(f"  Total battles: {len(self.battle_history)}")
        
        # Find organisms with most wins
        wins = {}
        for battle in self.battle_history:
            winner_id = battle['winner_id']
            wins[winner_id] = wins.get(winner_id, 0) + 1
        
        if wins:
            top_winners = sorted(wins.items(), key=lambda x: x[1], reverse=True)[:5]
            print(f"  Top winners:")
            for org_id, win_count in top_winners:
                print(f"    Organism #{org_id}: {win_count} wins")
        
        # Count dead organisms
        dead_count = sum(1 for org in self.organisms if org.strength == 0)
        alive_count = self.num_organisms - dead_count
        print(f"  Organisms alive: {alive_count}")
        print(f"  Organisms dead: {dead_count}")
    
    def display_top_bottom(self, count: int = 5):
        """Display the strongest and weakest organisms."""
        strongest = self.get_strongest_organisms(count)
        weakest = self.get_weakest_organisms(count)
        
        print(f"\n=== Top {count} Strongest Organisms ===")
        for i, organism in enumerate(strongest, 1):
            print(f"  {i}. {organism}")
        
        print(f"\n=== Bottom {count} Weakest Organisms ===")
        for i, organism in enumerate(weakest, 1):
            print(f"  {i}. {organism}")

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line options. Counts that are left out are prompted for."""
    parser = argparse.ArgumentParser(
        description="Simulate organism battles and the strength hierarchy they produce."
    )
    parser.add_argument("-n", "--organisms", type=int,
                        help="number of organisms (prompted for if omitted)")
    parser.add_argument("-m", "--battles", type=int,
                        help="number of battles to run (prompted for if omitted)")
    parser.add_argument("--seed", type=int,
                        help="random seed (if omitted, one is chosen at random and printed)")
    parser.add_argument("--export", metavar="PATH",
                        help="write the run to a JSON file that organism_arena.html can replay")
    args = parser.parse_args(argv)

    if args.organisms is not None and args.organisms <= 0:
        parser.error("--organisms must be positive")
    if args.battles is not None and args.battles < 0:
        parser.error("--battles cannot be negative")
    return args

def main(argv: Optional[List[str]] = None):
    """Main function to run the simulation."""
    args = parse_args(argv)

    print("Organism Strength Simulation with Battles")
    print("=" * 45)

    # Get user input for number of organisms
    n = args.organisms
    if n is None:
        try:
            n = int(input("Enter the number of organisms to simulate (default 100): ") or "100")
            if n <= 0:
                print("Number of organisms must be positive. Using 100.")
                n = 100
        except ValueError:
            print("Invalid input. Using 100 organisms.")
            n = 100

    # Get user input for time iterations
    m = args.battles
    if m is None:
        try:
            m = int(input("Enter the number of time iterations (default 20): ") or "20")
            if m < 0:
                print("Time iterations cannot be negative. Using 20.")
                m = 20
        except ValueError:
            print("Invalid input. Using 20 time iterations.")
            m = 20

    # Pick a random seed if none was given, and print it so the run can be repeated
    seed = args.seed if args.seed is not None else random.randrange(1_000_000)
    print(f"Seed: {seed} (rerun with --seed {seed})")

    # Create simulation
    sim = OrganismSimulation(n, m, seed=seed)
    
    # Display initial state
    print("\n" + "=" * 45)
    print("INITIAL STATE")
    print("=" * 45)
    sim.display_population()
    sim.display_statistics()
    sim.display_top_bottom(5)
    
    # Run time iterations
    sim.run_time_iterations()
    
    # Display final state
    print("\n" + "=" * 45)
    print("FINAL STATE")
    print("=" * 45)
    sim.display_statistics()
    sim.display_top_bottom(5)
    sim.display_battle_summary()
    
    # Additional analysis
    print(f"\n=== Final Analysis ===")
    
    # Count organisms in different strength ranges
    for label, count in sim.bucket_counts():
        percentage = (count / n) * 100
        print(f"  {label}: {count} organisms ({percentage:.1f}%)")

    if args.export:
        sim.export_json(args.export)
        print(f"\nRun exported to {args.export}")

if __name__ == "__main__":
    main()
