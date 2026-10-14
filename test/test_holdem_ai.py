import pytest
from holdem_ai.predictor import HoldemPredictor


def test_holdem_ai_prediction():
    predictor = HoldemPredictor("holdem_ai/saved_models/holdem_policy_net.pt")
    result = predictor.predict_scenario(
        hole_cards=["As", "Ks"],
        community_cards=["Qs", "Js", "2h"],
        pot=150,
        all_day=40,
        round_bet=0,
        stack=980,
        position=2,
        player_ct=4,
        big_blind=20
    )
    assert "recommended_action" in result
    assert "action_probabilities" in result
    assert "hand_analysis" in result
    assert len(result["action_probabilities"]) == 5
    assert result["action_type"] in ["fold", "call", "check", "raise"]
