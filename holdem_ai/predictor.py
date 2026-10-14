"""
HoldemPredictor - High Level API for Texas Hold'em Strategy Prediction.
Provides move recommendations and probability distributions for any poker scenario.
Supports both pure NumPy inference (zero external runtime dependencies) and PyTorch.
"""

import os
import numpy as np
from texas_hold_em_utils.card import Card
from .feature_extractor import FeatureExtractor, parse_card
from .model import HoldemPolicyValueNumpy, HoldemPolicyValueNet, TORCH_AVAILABLE


class HoldemPredictor:
    """
    High-level interface to evaluate Texas Hold'em scenarios using the trained ML model.
    Seamlessly uses pure NumPy or PyTorch depending on environment availability.
    """

    def __init__(self, model_path=None):
        base_dir = os.path.dirname(__file__)
        default_npz = os.path.join(base_dir, "saved_models", "holdem_policy_net.npz")
        default_pt = os.path.join(base_dir, "saved_models", "holdem_policy_net.pt")

        if model_path is None:
            model_path = default_npz if os.path.exists(default_npz) else default_pt

        npz_path = model_path.replace(".pt", ".npz") if model_path.endswith(".pt") else model_path
        pt_path = model_path.replace(".npz", ".pt") if model_path.endswith(".npz") else model_path

        # 1. Prefer pure NumPy engine if .npz file is available or PyTorch is not available
        loaded = False
        if os.path.exists(npz_path):
            try:
                self.model = HoldemPolicyValueNumpy.from_checkpoint(npz_path)
                print(f"Loaded trained weights from {npz_path} via NumPy engine (input_dim={self.model.input_dim}, hidden_dim={self.model.hidden_dim})")
                loaded = True
            except Exception as e:
                print(f"NumPy engine load failed: {e}")

        # 2. Try PyTorch engine if NumPy wasn't loaded and PyTorch is available
        if not loaded and os.path.exists(pt_path) and TORCH_AVAILABLE and HoldemPolicyValueNet is not None:
            try:
                self.model = HoldemPolicyValueNet.from_checkpoint(pt_path)
                print(f"Loaded trained weights from {pt_path} via PyTorch engine (input_dim={self.model.input_dim}, hidden_dim={self.model.hidden_dim})")
                loaded = True
            except Exception as e:
                print(f"PyTorch engine load failed: {e}")

        # 3. Fallback to default NumPy initialization
        if not loaded:
            if os.path.exists(npz_path):
                self.model = HoldemPolicyValueNumpy.from_checkpoint(npz_path)
            elif os.path.exists(pt_path) and TORCH_AVAILABLE:
                self.model = HoldemPolicyValueNet.from_checkpoint(pt_path)
            else:
                raise FileNotFoundError(f"Neither {npz_path} nor {pt_path} could be loaded.")

        if hasattr(self.model, "eval"):
            self.model.eval()

    def predict_scenario(
        self,
        hole_cards,
        community_cards=None,
        pot=100,
        all_day=20,
        round_bet=0,
        stack=1000,
        position=0,
        player_ct=6,
        big_blind=20,
        temperature=1.0
    ):
        """
        Evaluates a game scenario and returns move recommendations and probabilities.

        :param hole_cards: List of 2 hole cards e.g. ["As", "Ks"] or ["A of Spades", "K of Spades"]
        :param community_cards: List of 0 to 5 community cards e.g. ["Qs", "Js", "2h"]
        :param pot: Current total pot size in chips (default 100)
        :param all_day: Highest bet in current hand across all rounds (default 20)
        :param round_bet: Player's existing bet in current round (default 0)
        :param stack: Player's remaining stack size in chips (default 1000)
        :param position: Player's seat position 0..player_ct-1 (default 0)
        :param player_ct: Total players at table (default 6)
        :param big_blind: Big blind chip size (default 20)
        :param temperature: Softmax temperature for probability smoothing
        :return: dict with action recommendation, probability distribution, and hand analysis
        """
        if community_cards is None:
            community_cards = []

        h_cards = [parse_card(c) for c in hole_cards]
        c_cards = [parse_card(c) for c in community_cards]

        round_num = 0
        if len(c_cards) == 3:
            round_num = 1
        elif len(c_cards) == 4:
            round_num = 2
        elif len(c_cards) == 5:
            round_num = 3

        to_call = max(0, all_day - round_bet)

        # 1. Extract features using texas_hold_em_utils
        features = FeatureExtractor.extract_features(
            hole_cards=h_cards,
            community_cards=c_cards,
            round_num=round_num,
            pot=pot,
            all_day=all_day,
            round_bet=round_bet,
            chips=stack,
            big_blind=big_blind,
            player_ct=player_ct
        )
        input_dim = getattr(self.model, "input_dim", len(features))
        state_tensor = np.array(features[:input_dim], dtype=np.float32)

        # 2. Build action mask
        mask = [1.0, 1.0, 1.0, 1.0, 1.0]
        if to_call == 0:
            mask[0] = 0.0  # Cannot fold if checking is free
        if stack <= to_call:
            mask[2] = 0.0  # Cannot raise small
            mask[3] = 0.0  # Cannot raise med
            mask[4] = 0.0  # Cannot raise all-in
        if stack == 0:
            mask = [0.0, 1.0, 0.0, 0.0, 0.0]
        action_mask = np.array(mask, dtype=np.float32)

        # 3. Network Prediction
        action_idx, action_name, prob_dict = self.model.predict_action(
            state_tensor,
            action_mask=action_mask,
            deterministic=True,
            temperature=temperature
        )

        _, value_est = self.model(state_tensor)
        if hasattr(value_est, "item"):
            state_val = float(value_est.item())
        elif hasattr(value_est, "__len__"):
            state_val = float(value_est[0])
        else:
            state_val = float(value_est)

        # 4. Determine bet amount and game action
        if action_idx == 0:
            action_type = "fold"
            bet_amt = 0
        elif action_idx == 1:
            if to_call == 0:
                action_type = "check"
                bet_amt = 0
            else:
                action_type = "call"
                bet_amt = min(to_call, stack)
        elif action_idx == 2:
            action_type = "raise"
            raise_inc = max(big_blind, pot // 2)
            target_total = all_day + raise_inc
            needed_chips = target_total - round_bet
            bet_amt = min(stack, needed_chips)
        elif action_idx == 3:
            action_type = "raise"
            raise_inc = max(big_blind * 2, pot)
            target_total = all_day + raise_inc
            needed_chips = target_total - round_bet
            bet_amt = min(stack, needed_chips)
        elif action_idx == 4:
            action_type = "raise"
            bet_amt = stack

        # 5. Hand Analysis Breakdown
        win_rate = float(features[0])
        win_rate_2p = float(features[1])
        percentile = float(features[2]) * 100.0
        ideal_kelly = float(features[3])

        # Pot odds calculation
        pot_odds = float(to_call / (pot + to_call)) if (pot + to_call) > 0 else 0.0

        # Sklansky group
        raw_sklansky = int(round(float(features[4]) * 8.0)) + 1
        sklansky_group = max(1, min(9, raw_sklansky))

        hand_analysis = {
            "expected_win_rate": round(win_rate, 4),
            "expected_2_player_win_rate": round(win_rate_2p, 4),
            "percentile_rank": round(percentile, 1),
            "ideal_kelly_max": round(ideal_kelly, 4),
            "sklansky_group": sklansky_group,
            "pot_odds": round(pot_odds, 4),
            "to_call": to_call,
            "pot": pot,
            "stack": stack,
            "round_num": round_num
        }

        return {
            "recommended_action": action_name,
            "recommended_bet_amount": bet_amt,
            "action_type": action_type,
            "action_probabilities": prob_dict,
            "state_value_estimate": round(state_val, 4),
            "hand_analysis": hand_analysis
        }
