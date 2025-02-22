from dataclasses import dataclass


@dataclass
class PlayerRoundStats:
    username = None
    game_id = None
    round_number = None
    folded_before_flop = False
    folded_before_turn = False
    folded_before_river = False
    folded_before_showdown = False
    raise_count = 0
    call_count = 0
    check_count = 0
    amount_paid_in = 0
    amount_won = 0
