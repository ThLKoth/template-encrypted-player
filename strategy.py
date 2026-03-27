#!/usr/bin/env python3
"""Your encrypted strategy - edit this file, then encrypt it with setup_encryption.py"""

from typing import Any, Dict

import numpy as np


def strategy(state: Dict[str, Any]) -> Dict[str, Dict[str, int]]:
    """
    Your strategy function.
    
    Args:
        state: Game state dictionary containing:
            - playerIds: list of all player IDs
            - myPlayerId: your player ID
            - opponentsIds: list of opponent IDs
            - state: list of completed turns (history)
            - turnId: current turn number
    
    Returns:
        Dictionary with 'shoot' and 'keep' maps:
        {
            "shoot": {opponent_id: direction (0-2), ...},
            "keep": {opponent_id: direction (0-2), ...}
        }
        
    Directions:
        - 0 = left
        - 1 = center
        - 2 = right
    """
    my_id = state.get("myPlayerId")
    opponents = state.get("opponentsIds") or []
    history = state.get("state") or []
    
    if not my_id or not opponents:
        return {"shoot": {}, "keep": {}}
    
    recent_history = history[-10:]

    for opp_id in opponents:
        opp_shoot_counts = {0: 0, 1: 0, 2: 0}
        opp_keep_counts = {0: 0, 1: 0, 2: 0}

    for turn in recent_history:
            opp_actions = turn.get(opp_id, {})

            opp_shoot = opp_actions.get("shoot", {}).get(my_id)
            if opp_shoot is not None:
                opp_shoot_counts[opp_shoot] += 1

            opp_keep = opp_actions.get("keep", {}).get(my_id)
            if opp_keep is not None:
                opp_keep_counts[opp_keep] += 1
                if total_opp_shoots > 0:
                    keep_probs = [opp_shoot_counts[i] / total_opp_shoots for i in range(3)]
                    keep_actions[opp_id] = int(np.random.choice([0, 1, 2], p=keep_probs))
                    
        total_opp_shoots = sum(opp_shoot_counts.values())
        if total_opp_shoots > 0:
            keep_probs = [opp_shoot_counts[i] / total_opp_shoots for i in range(3)]
            keep_actions[opp_id] = int(np.random.choice([0, 1, 2], p=keep_probs))
        else:
            keep_actions[opp_id] = int(np.random.randint(0, 3))

        total_opp_keeps = sum(opp_keep_counts.values())
        if total_opp_keeps > 0:
            inverse_weights = [total_opp_keeps - opp_keep_counts[i] for i in range(3)]
            total_inverse = sum(inverse_weights)
            
            if total_inverse > 0:
                shoot_probs = [w / total_inverse for w in inverse_weights]
                shoot_actions[opp_id] = int(np.random.choice([0, 1, 2], p=shoot_probs))
            else:
                shoot_actions[opp_id] = int(np.random.randint(0, 3))
        else:
            # Fallback to random if no history exists yet
            shoot_actions[opp_id] = int(np.random.randint(0, 3))
        
    return {"shoot": shoot_actions,
        "keep": keep_actions,}
