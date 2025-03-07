import os

import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy import Table, select, MetaData, text
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
        with self.db_engine.connect() as conn:
            if con_str.startswith('postgresql'):
                conn.commit()
            conn.execute(text(f"CREATE TABLE IF NOT EXISTS player_round_stats ("
                         f"id {'serial PRIMARY KEY' if con_str.startswith('postgresql') else 'INTEGER PRIMARY KEY AUTOINCREMENT'}, "
                         f"username VARCHAR(255) NOT NULL, "
                         f"game_id VARCHAR(255) NOT NULL, "
                         f"folded_before_flop BOOLEAN NOT NULL DEFAULT FALSE, "
                         f"folded_before_turn BOOLEAN NOT NULL DEFAULT FALSE, "
                         f"folded_before_river BOOLEAN NOT NULL DEFAULT FALSE, "
                         f"folded_before_showdown BOOLEAN NOT NULL DEFAULT FALSE, "
                         f"raise_count INT NOT NULL default 0, "
                         f"call_count INT NOT NULL default 0, "
                         f"check_count INT NOT NULL default 0, "
                         f"amount_paid_in FLOAT NOT NULL default 0, "
                         f"amount_won FLOAT NOT NULL default 0,"
                         f"seat INT NOT NULL default 0, "
                         f"big_blind FLOAT NOT NULL default 0, "
                         f"dealer_seat INT NOT NULL default 0, "
                         f"timestamp {'TIMESTAMP' if con_str.startswith('postgresql') else 'DATETIME'} NOT NULL default CURRENT_TIMESTAMP)"))
            conn.commit()
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

    def get_records_for_game(self, game_id: str) -> list[PlayerRoundStats]:
        stmt = select(PlayerRoundStatsTable).where(PlayerRoundStatsTable.game_id == game_id)
        # map result to PlayerRoundStats
        return self.session.execute(stmt).scalars(PlayerRoundStatsTable).all()
