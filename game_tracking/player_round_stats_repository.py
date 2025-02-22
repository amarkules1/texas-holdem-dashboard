import os

import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

from game_tracking.player_round_stats import PlayerRoundStats


class PlayerRoundStatsRepository:
    def __init__(self, env_file=None):
        if env_file is not None:
            _ = load_dotenv(env_file)
        else:
            _ = load_dotenv()
        con_str = os.getenv("DATABASE_CONN_STRING")
        self.db_engine = sqlalchemy.create_engine(con_str)
        self.db_engine.raw_connection().execute("CREATE TABLE IF NOT EXISTS player_round_stats ("
                                                "username VARCHAR(255) NOT NULL, "
                                                "game_id VARCHAR(255) NOT NULL, "
                                                "folded_before_flop BOOLEAN NOT NULL DEFAULT FALSE, "
                                                "folded_before_turn BOOLEAN NOT NULL DEFAULT FALSE, "
                                                "folded_before_river BOOLEAN NOT NULL DEFAULT FALSE, "
                                                "folded_before_showdown BOOLEAN NOT NULL DEFAULT FALSE, "
                                                "raise_count INT NOT NULL default 0, "
                                                "call_count INT NOT NULL default 0, "
                                                "check_count INT NOT NULL default 0, "
                                                "amount_paid_in FLOAT NOT NULL default 0, "
                                                "amount_won FLOAT NOT NULL default 0)")
        Session = sessionmaker(bind=self.db_engine)
        self.session = Session()

    def add(self, betting_round_summary: PlayerRoundStats):
        stmt = (f"INSERT INTO player_round_stats (username, game_id, folded_before_flop, folded_before_turn, "
                f"folded_before_river, folded_before_showdown, raise_count, call_count, check_count, "
                f"amount_paid_in, amount_won) "
                f"VALUES ('{betting_round_summary.username}', '{betting_round_summary.game_id}', "
                f"{betting_round_summary.folded_before_flop}, {betting_round_summary.folded_before_turn}, "
                f"{betting_round_summary.folded_before_river}, {betting_round_summary.folded_before_showdown}, "
                f"{betting_round_summary.raise_count}, {betting_round_summary.call_count}, "
                f"{betting_round_summary.check_count}, {betting_round_summary.amount_paid_in}, "
                f"{betting_round_summary.amount_won})")
        self.db_engine.raw_connection().execute(stmt)

    def get_all(self):
        return self.session.query(PlayerRoundStats).all()
