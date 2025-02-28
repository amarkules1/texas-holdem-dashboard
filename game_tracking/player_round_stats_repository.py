import os

import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy import Table, select, MetaData
from sqlalchemy.orm import sessionmaker

from game_tracking.player_round_stats import PlayerRoundStats, PlayerRoundStatsTable


class PlayerRoundStatsRepository:
    def __init__(self, env_file=None):
        if env_file is not None:
            _ = load_dotenv(env_file)
        else:
            _ = load_dotenv()
        con_str = os.getenv("DATABASE_CONN_STRING")
        self.db_engine = sqlalchemy.create_engine(con_str)
        self.db_engine.raw_connection().execute("CREATE TABLE IF NOT EXISTS player_round_stats ("
                                                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
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
                                                "amount_won FLOAT NOT NULL default 0,"
                                                "seat INT NOT NULL default 0, "
                                                "big_blind FLOAT NOT NULL default 0, "
                                                "dealer_seat INT NOT NULL default 0, "
                                                "timestamp DATETIME NOT NULL default CURRENT_TIMESTAMP)")
        Session = sessionmaker(bind=self.db_engine)
        self.session = Session()
        self.table = Table("player_round_stats", MetaData(), autoload_with=self.db_engine)

    def add(self, betting_round_summary: PlayerRoundStats):
        self.session.add(PlayerRoundStatsTable(betting_round_summary))
        self.session.commit()

    def get_all(self) -> list[PlayerRoundStats]:
        stmt = select(self.table)
        # map result to PlayerRoundStats
        return self.session.query(PlayerRoundStatsTable).all()

    def delete_all(self):
        self.session.query(PlayerRoundStatsTable).delete()
        self.session.commit()

