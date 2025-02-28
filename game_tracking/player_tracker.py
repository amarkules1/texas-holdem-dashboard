from texas_hold_em_utils.hands import HandOfTwo


class PlayerTracker:
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
    round_start_chips: float = 0
    chips = 0
    seat = 0
    sitting_out = False
