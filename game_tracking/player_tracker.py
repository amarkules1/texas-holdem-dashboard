from texas_hold_em_utils.hands import HandOfTwo


class PlayerTracker:
    def __init__(self):
        self.username = None
        self.chips = None
        self.seat = None
        self.sitting_out = False
        self.folded = False
        self.current_hand_bet = 0.0
        self.is_player = False
        self.cards = HandOfTwo([])
        self.player_round_summary = None
        self.round_winnings = 0.0
