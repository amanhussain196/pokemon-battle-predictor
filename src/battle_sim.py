# src/battle_sim.py

import numpy as np
from .type_chart import get_type_multiplier

def compute_damage(attacker, defender):
    atk_stat = max(attacker["attack"], attacker["sp_attack"])
    def_stat = max(defender["defense"], defender["sp_defense"])
    base = atk_stat / max(1, def_stat)

    atk_types = [attacker["type1"]]
    if attacker["type2"] != "None":
        atk_types.append(attacker["type2"])

    def_types = [defender["type1"]]
    if defender["type2"] != "None":
        def_types.append(defender["type2"])

    stab = 1.5
    type_mult = get_type_multiplier(atk_types, def_types)
    if type_mult == 0.0:
        type_mult = 0.1

    return max(1.0, base * stab * type_mult * 10.0)

def simulate_battle(p1, p2, max_turns=50):
    hp1, hp2 = float(p1["hp"]), float(p2["hp"])
    speed1, speed2 = p1["speed"], p2["speed"]

    dmg1 = compute_damage(p1, p2)
    dmg2 = compute_damage(p2, p1)

    for _ in range(max_turns):
        if speed1 > speed2:
            hp2 -= dmg1
            if hp2 <= 0: return 1
            hp1 -= dmg2
            if hp1 <= 0: return 0
        elif speed2 > speed1:
            hp1 -= dmg2
            if hp1 <= 0: return 0
            hp2 -= dmg1
            if hp2 <= 0: return 1
        else:
            hp2 -= dmg1
            hp1 -= dmg2
            if hp1 <= 0 and hp2 <= 0:
                return 1 if p1["total"] >= p2["total"] else 0
            elif hp2 <= 0: return 1
            elif hp1 <= 0: return 0
    return int(hp1 >= hp2)
