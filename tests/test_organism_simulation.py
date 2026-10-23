import json

import pytest

from organism_simulation import OrganismSimulation, STRENGTH_BUCKETS, main, parse_args


def total_strength(sim):
    return sum(org.strength for org in sim.organisms)


def test_total_strength_is_conserved():
    sim = OrganismSimulation(50, 200, seed=1)
    before = total_strength(sim)
    sim.run_time_iterations()
    assert total_strength(sim) == pytest.approx(before)


def test_battle_moves_loser_strength_to_winner():
    sim = OrganismSimulation(2, seed=7)
    a, b = sim.organisms
    a.strength, b.strength = 0.3, 0.5

    winner, loser = sim.battle(a, b)

    assert {winner, loser} == {a, b}
    assert winner.strength == pytest.approx(0.8)
    assert loser.strength == 0.0
    record = sim.battle_history[-1]
    assert record['winner_id'] == winner.id
    assert record['loser_id'] == loser.id
    assert record['total_transferred'] == record['loser_strength_before']


def test_battles_only_pair_living_organisms():
    sim = OrganismSimulation(30, 25, seed=3)
    sim.run_time_iterations()
    for record in sim.battle_history:
        assert record['winner_strength_before'] > 0
        assert record['loser_strength_before'] > 0


def test_run_stops_when_one_organism_is_left():
    sim = OrganismSimulation(5, 100, seed=11)
    sim.run_time_iterations()
    # Each battle eliminates one organism, so 5 organisms allow exactly 4 battles
    assert len(sim.battle_history) == 4
    assert sum(1 for org in sim.organisms if org.strength > 0) == 1


def test_win_rate_matches_strength_ratio():
    sim = OrganismSimulation(2, seed=0)
    a, b = sim.organisms
    trials = 4000
    wins = 0
    for _ in range(trials):
        a.strength, b.strength = 0.3, 0.1
        winner, _ = sim.battle(a, b)
        wins += winner is a
    # Expected 0.3 / (0.3 + 0.1) = 0.75; standard error is about 0.007
    assert wins / trials == pytest.approx(0.75, abs=0.03)


def test_same_seed_gives_same_run():
    # Create both before running either: they must not share random state
    first = OrganismSimulation(20, 15, seed=5)
    second = OrganismSimulation(20, 15, seed=5)
    first.run_time_iterations()
    second.run_time_iterations()
    assert first.initial_strengths == second.initial_strengths
    assert first.battle_history == second.battle_history


@pytest.mark.parametrize("seed", range(5))
def test_bucket_counts_add_up_to_population(seed):
    sim = OrganismSimulation(40, 30, seed=seed)
    sim.run_time_iterations()
    assert sum(count for _, count in sim.bucket_counts()) == 40


def test_bucket_boundaries_are_counted_once():
    sim = OrganismSimulation(6, seed=0)
    for org, strength in zip(sim.organisms, [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]):
        org.strength = strength
    counts = dict(sim.bucket_counts())
    assert list(counts) == [label for _, _, label in STRENGTH_BUCKETS]
    assert all(count == 1 for count in counts.values())


def test_export_json_round_trips(tmp_path):
    sim = OrganismSimulation(10, 6, seed=2)
    sim.run_time_iterations()
    path = tmp_path / "run.json"
    sim.export_json(str(path))

    data = json.loads(path.read_text())
    assert data['seed'] == 2
    assert data['num_organisms'] == 10
    assert data['time_iterations'] == 6
    assert len(data['initial_strengths']) == 10
    assert data['battle_history'] == sim.battle_history


def test_export_json_creates_missing_folder(tmp_path):
    sim = OrganismSimulation(4, 2, seed=1)
    path = tmp_path / "runs" / "run.json"
    sim.export_json(str(path))
    assert json.loads(path.read_text())['num_organisms'] == 4


def test_parse_args_rejects_invalid_counts():
    with pytest.raises(SystemExit):
        parse_args(["--organisms", "0"])
    with pytest.raises(SystemExit):
        parse_args(["--battles", "-1"])


def test_main_runs_without_prompts_when_options_given(tmp_path, capsys, monkeypatch):
    def no_input(prompt=""):
        raise AssertionError("main() should not prompt when counts are given")
    monkeypatch.setattr("builtins.input", no_input)
    path = tmp_path / "run.json"

    main(["-n", "12", "-m", "8", "--seed", "4", "--export", str(path)])

    out = capsys.readouterr().out
    assert "Seed: 4" in out
    assert json.loads(path.read_text())['seed'] == 4
