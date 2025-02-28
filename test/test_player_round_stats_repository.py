import os

from game_tracking.player_round_stats import PlayerRoundStats
from game_tracking.player_round_stats_repository import PlayerRoundStatsRepository

# test.env in same directory pointing to an sqlite db
TEST_ENV_PATH = os.path.abspath(__file__).replace("test_player_round_stats_repository.py", "test.env")

def test_init_repository():
    repo = PlayerRoundStatsRepository(TEST_ENV_PATH)
    assert repo


def test_add_and_get_all():
    repo = PlayerRoundStatsRepository(TEST_ENV_PATH)
    p = PlayerRoundStats('test', 'test', True, True, True, True, 1, 1, 1, 1, 1)

    repo.add(p)
    all = repo.get_all()
    assert len(all) == 1
    assert all[0].username == 'test'
    assert all[0].game_id == 'test'
    #cleanup
    repo.delete_all()
