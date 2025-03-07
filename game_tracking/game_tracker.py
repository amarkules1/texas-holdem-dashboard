import logging
import math
import re

from texas_hold_em_utils.card import Card
from texas_hold_em_utils.preflop_stats_repository import PreflopStatsRepository
from texas_hold_em_utils.relative_ranking import get_hand_rank_details

from game_tracking.player_round_stats import PlayerRoundStats
from game_tracking.player_tracker import PlayerTracker

# TODO - After each game, save all player_round_summaries
class GameTracker:
    def __init__(self, logger=logging.getLogger(__name__), player_round_stats_repo=None):
        self.player_round_stats_repo = player_round_stats_repo
        self.logger = logger
        self.community_cards = []
        self.current_game = None  # maybe not needed?
        self.big_blind_amount = None
        self.small_blind_amount = None
        self.big_blind_seat = None
        self.small_blind_seat = None
        self.dealer_seat = None
        self.players = []
        self.user_player = None
        self.game_id = None
        self.table_name = None
        self.pot = 0.0
        self.round_bet = 0.0
        self.total_pot = 0.0
        self.rake = 0.0
        self.is_summary_phase = False
        self.line_count = 0
        self.preflop_stats_repo = PreflopStatsRepository()
        self.betting_round = 0 # 0= preflop, 1=flop, 2=turn, 3=river

    def reset(self):
        self.players = []
        self.game_id = None
        self.is_summary_phase = False
        self.betting_round = 0
        self.pot = 0
        self.round_bet = 0
        self.total_pot = 0
        self.rake = 0
        self.community_cards = []

    def parse_line(self, line):
        self.line_count += 1
        self.logger.debug(f"Line {self.line_count}: {line}")
        line = self.clean_line(line)
        if line.startswith("PokerStars Hand #"):
            self.save_player_round_summaries()
            self.reset()
            self.game_id = re.sub("[^0-9]", "", line.split(" ")[2])
            return
        if line.startswith("Table"):
            self.table_name = line.split("'")[1]
            player_count = int(line.split("' ")[1][0])
            self.players = [PlayerTracker() for _ in range(player_count)]
            return
        if line.startswith("Seat"):
            self.handle_seat_line(line)
            return
        if self.is_player_action_line(line):
            self.handle_player_action_line(line)
            return
        if (line == "*** HOLE CARDS ***" or line == "*** SHOW DOWN ***" or " collected " in line or line.strip() == ""
                or "is connected" in line or "has timed out" in line):
            return
        if "*** SUMMARY ***" in line:
            self.is_summary_phase = True
            return
        if line.startswith("Dealt to "):
            self.handle_deal_line(line)
            return
        if line.startswith("*** FLOP ***"):
            self.handle_flop_line(line)
            return
        if line.startswith("*** TURN ***"):
            self.handle_turn_line(line)
            return
        if line.startswith("*** RIVER ***"):
            self.handle_river_line(line)
            return
        if "leaves the table" in line:
            self.handle_leave_table_line(line)
            return
        if "joins the table" in line:
            self.handle_join_table_line(line)
            return
        if "is disconnected" in line:
            self.handle_disconnect_line(line)
            return
        if line.startswith("Total pot "):
            self.handle_total_line(line)
            return
        if line.startswith("Board ["):
            self.handle_board_line(line)
            return
        if line.startswith("Uncalled bet"):
            self.handle_uncalled_bet_line(line)
            return
        raise ValueError(f"Unknown line #{self.line_count}: {line}")

    def clean_line(self, line):
        line = line.replace("ï", "")
        line = line.replace("»", "")
        line = line.replace("¿", "")
        line = line.replace("\n", "")
        line = line.replace("\r", "")
        line = line.replace("﻿", "")
        return line

    def handle_seat_line(self, line):
        username = line.split(": ")[1].split(" (")[0]
        seat = int(line.split("Seat ")[1].split(":")[0])
        if not self.is_summary_phase:
            chips = line.split(" (")[1].split(" in chips")[0]
            chips = float(chips.replace("$", ""))
            sitting_out = "sitting out" in line
            player = PlayerTracker()
            player.username = username
            player.chips = chips
            player.round_start_chips = chips
            player.seat = seat
            player.sitting_out = sitting_out
            player.game_id = self.game_id
            # TODO 2/27/25 adjust everything below here to use new player tracker object, rip out anything that's not needed
            self.players[seat - 1] = player
            return
        player = self.get_player(username)
        if player is None:
            return
        player_round_summary = line.split(username)[1].strip()
        if " won ($" in player_round_summary:
            won = player_round_summary.split(" won ($")[1].split(")")[0]
            player.amount_won = float(won)
        else:
            player.amount_won = 0.0

    def is_player_action_line(self, line):
        # if there's no player in a seat, then we have a player with no username, indicates we need to filter
        players_need_filtering = False
        retval = False
        for player in self.players:
            if player.username is None:
                players_need_filtering = True
            elif line.startswith(player.username + ':'):
                retval = True
        if players_need_filtering:
            self.players = [player for player in self.players if player.username is not None]
        return retval

    def handle_player_action_line(self, line):
        username = line.split(":")[0]
        player = self.get_player(username)
        if player is None:
            raise ValueError(f"Unknown player: {line}")
        if "posts small blind" in line:
            self.small_blind_seat = player.seat
            self.big_blind_seat = self.find_bb_from_sb(self.small_blind_seat)
            self.dealer_seat = self.find_dealer_from_sb(self.small_blind_seat)
            sb = line.split("small blind ")[1]
            sb = sb.replace("$", "")
            self.small_blind_amount = float(sb)
            player.chips -= self.small_blind_amount
            player.amount_paid_in += self.small_blind_amount
            self.round_bet = self.small_blind_amount
            self.pot += self.small_blind_amount
            return
        if "posts big blind" in line:
            self.big_blind_seat = player.seat
            self.small_blind_seat = self.find_sb_from_bb(self.big_blind_seat)
            self.dealer_seat = self.find_dealer_from_bb(self.big_blind_seat)
            bb = line.split("big blind ")[1]
            bb = bb.replace("$", "")
            self.big_blind_amount = float(bb)
            player.chips -= self.big_blind_amount
            player.amount_paid_in += self.big_blind_amount
            self.round_bet = self.big_blind_amount
            self.pot += self.big_blind_amount
            return
        if "folds" in line:
            if self.betting_round < 1:
                player.folded_before_flop = True
            if self.betting_round < 2:
                player.folded_before_turn = True
            if self.betting_round < 3:
                player.folded_before_river = True
            player.folded_before_showdown = True
            player.sitting_out = False
            return
        if "calls" in line:
            player.sitting_out = False
            player.call_count += 1
            amount = line.split("calls ")[1].split(" ")[0]
            amount = amount.replace("$", "")
            amount = float(amount)
            player.amount_paid_in += amount
            player.chips -= amount
            self.pot += amount
            self.round_bet = amount
            return
        if "raises" in line:
            player.sitting_out = False
            player.raise_count += 1
            amount = line.split("raises ")[1].split("to ")[1].split(" ")[0]
            amount = amount.replace("$", "")
            amount = float(amount)
            player.amount_paid_in += amount
            player.chips -= amount
            self.pot += amount
            self.round_bet = amount
            return
        if "checks" in line:
            player.sitting_out = False
            player.check_count += 1
            return
        if "shows" in line:
            player.sitting_out = False
            return
        if "mucks" in line:
            return
        if "sits out" in line:
            player.sitting_out = True
            return
        if " bets " in line:
            player.sitting_out = False
            player.raise_count += 1
            amount = line.split(" bets ")[1].split(" ")[0]
            amount = amount.replace("$", "")
            amount = float(amount)
            player.amount_paid_in += amount
            player.chips -= amount
            self.pot += amount
            self.round_bet = amount
            return
        if "doesn't show hand" in line:
            player.sitting_out = False
            return
        if " is sitting out" in line:
            player.sitting_out = True
            return

        raise ValueError(f"Unknown player action line #{self.line_count}: {line}")

    def find_bb_from_sb(self, sb_seat):
        seat_nums = [player.seat for player in self.players]
        return seat_nums[(seat_nums.index(sb_seat) + 1) % len(seat_nums)]

    def find_sb_from_bb(self, bb_seat):
        seat_nums = [player.seat for player in self.players]
        return seat_nums[(seat_nums.index(bb_seat) - 1) % len(seat_nums)]

    def find_dealer_from_sb(self, sb_seat):
        seat_nums = [player.seat for player in self.players if not player.sitting_out]
        return seat_nums[(seat_nums.index(sb_seat) - 1) % len(seat_nums)]

    def find_dealer_from_bb(self, bb_seat):
        seat_nums = [player.seat for player in self.players]
        return seat_nums[(seat_nums.index(bb_seat) - 2) % len(seat_nums)]

    def handle_deal_line(self, line):
        username = line.split("Dealt to ")[1].split(" ")[0]
        player = self.get_player(username)
        player.is_player = True

    def get_player(self, username):
        for player in self.players:
            if player.username == username:
                return player
        return None

    def handle_flop_line(self, line):
        self.betting_round = 1

    def handle_leave_table_line(self, line):
        username = line.split(" leaves the table")[0]
        player = self.get_player(username)
        player.sitting_out = True

    def handle_river_line(self, line):
        self.betting_round = 3

    def handle_turn_line(self, line):
        self.betting_round = 2

    def add_player_statuses_to_summary(self, betting_round_summary):
        for player in self.players:
            if player.chips == 0 and not player.folded:
                betting_round_summary.add_player_all_in(player)
            elif player.current_hand_bet == self.round_bet:
                betting_round_summary.add_player_in_round(player)
            elif player.folded and not player.sitting_out:
                betting_round_summary.add_player_folded(player)
            elif not player.sitting_out:
                ValueError(f"not sure what's going on with this player")
        return betting_round_summary

    def handle_join_table_line(self, line):
        username = line.split(" joins the table")[0]
        seat = int(line.split("seat #")[1])
        player = PlayerTracker()
        player.username = username
        player.seat = seat
        player.sitting_out = True
        self.players.insert(seat - 1, player)

    def handle_disconnect_line(self, line):
        username = line.split(" is disconnected")[0]
        player = self.get_player(username)
        player.sitting_out = True

    def handle_total_line(self, line):
        self.total_pot = float(line.split("Total pot ")[1].split(" ")[0].replace("$", ""))
        self.rake = float(line.split("Rake $")[1].strip())
        self.pot = self.total_pot - self.rake

    def handle_board_line(self, line):
        # we should already have them at this point, doesn't hurt to be redundant
        cards = line.split("[")[1].split("]")[0].split(" ")
        self.community_cards = [Card().from_str(card[0], card[1]) for card in cards]

    def handle_uncalled_bet_line(self, line):
        player = line.split("returned to ")[-1]
        player = self.get_player(player)
        returned_amount = float(line.split("(")[1].split(")")[0].replace("$", ""))
        player.chips += returned_amount
        player.amount_paid_in -= returned_amount

    def save_player_round_summaries(self):
        if self.player_round_stats_repo is not None and len(self.players) > 0:
            existing_player_round_stats = self.player_round_stats_repo.get_records_for_game(self.game_id)
            if len(existing_player_round_stats) == 0:
                for player in self.players:
                    if player.username is not None and not player.sitting_out:
                        prs = PlayerRoundStats().from_player_tracker(player)
                        self.player_round_stats_repo.add(prs)
