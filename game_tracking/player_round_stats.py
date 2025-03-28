from dataclasses import dataclass
from sqlalchemy import Column, Integer, Float, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from game_tracking.player_tracker import PlayerTracker

Base = declarative_base()

@dataclass
class PlayerRoundStats:
    username: str = None
    game_id: str = None
    folded_before_flop: bool = False
    folded_before_turn: bool = False
    folded_before_river: bool = False
    folded_before_showdown: bool = False
    raise_count: int = 0
    call_count: int = 0
    check_count: int = 0
    amount_paid_in: float = 0
    amount_won: float = 0
    seat: int = 0
    big_blind: float = 0
    dealer_seat: int = 0

    def from_player_tracker(self, player_tracker: PlayerTracker):
        self.username = player_tracker.username
        self.game_id = player_tracker.game_id
        self.folded_before_flop = player_tracker.folded_before_flop
        self.folded_before_turn = player_tracker.folded_before_turn
        self.folded_before_river = player_tracker.folded_before_river
        self.folded_before_showdown = player_tracker.folded_before_showdown
        self.raise_count = player_tracker.raise_count
        self.call_count = player_tracker.call_count
        self.check_count = player_tracker.check_count
        self.amount_paid_in = player_tracker.amount_paid_in
        self.amount_won = player_tracker.amount_won
        self.seat = player_tracker.seat
        return self

class PlayerRoundStatsTable(Base):

    __tablename__ = 'player_round_stats'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    game_id = Column(String)
    folded_before_flop = Column(Boolean)
    folded_before_turn = Column(Boolean)
    folded_before_river = Column(Boolean)
    folded_before_showdown = Column(Boolean)
    raise_count = Column(Integer)
    call_count = Column(Integer)
    check_count = Column(Integer)
    amount_paid_in = Column(Float)
    amount_won = Column(Float)
    seat = Column(Integer)
    big_blind = Column(Float)
    dealer_seat = Column(Integer)

    def __init__(self, player_round_stats: PlayerRoundStats):
        self.username = player_round_stats.username
        self.game_id = player_round_stats.game_id
        self.folded_before_flop = player_round_stats.folded_before_flop
        self.folded_before_turn = player_round_stats.folded_before_turn
        self.folded_before_river = player_round_stats.folded_before_river
        self.folded_before_showdown = player_round_stats.folded_before_showdown
        self.raise_count = player_round_stats.raise_count
        self.call_count = player_round_stats.call_count
        self.check_count = player_round_stats.check_count
        self.amount_paid_in = player_round_stats.amount_paid_in
        self.amount_won = player_round_stats.amount_won
        self.seat = player_round_stats.seat
        self.big_blind = player_round_stats.big_blind
        self.dealer_seat = player_round_stats.dealer_seat
