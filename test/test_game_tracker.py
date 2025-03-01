import os

from game_tracking.game_tracker import GameTracker
from game_tracking.player_round_stats_repository import PlayerRoundStatsRepository

# test.env in same directory pointing to an sqlite db
TEST_ENV_PATH = os.path.abspath(__file__).replace("test_game_tracker.py", "test.env")

def test_single_file():
    test_file = os.path.join("data", "mid_game_sample_1.txt")
    game_tracker = GameTracker()
    with open(test_file) as f:
        for line in f:
            game_tracker.parse_line(line)

    assert len(game_tracker.players) == 6

def test_full_file():
    test_file = os.path.join("data", "HH20241031 Hekate - $0.01-$0.02 - USD No Limit Hold'em.txt")
    prsr = PlayerRoundStatsRepository(TEST_ENV_PATH)
    game_tracker = GameTracker(player_round_stats_repo=prsr)
    with open(test_file) as f:
        for line in f:
            game_tracker.parse_line(line)

    assert len(prsr.get_all()) == 542
    #cleanup
    prsr.delete_all()
