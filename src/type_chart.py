# src/type_chart.py

ALL_TYPES = [
    "Normal", "Fire", "Water", "Electric", "Grass", "Ice",
    "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug",
    "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy"
]

TYPE_EFFECT = {
    # your full type chart here — paste from notebook
}

def single_type_multiplier(attacking_type, defending_type):
    if defending_type == "None":
        return 1.0
    info = TYPE_EFFECT.get(attacking_type, None)
    if info is None:
        return 1.0
    if defending_type in info["no_effect"]:
        return 0.0
    if defending_type in info["not_very_effective"]:
        return 0.5
    if defending_type in info["super_effective"]:
        return 2.0
    return 1.0

def get_type_multiplier(attacking_types, defending_types):
    mult = 1.0
    for atk in attacking_types:
        if atk == "None":
            continue
        for dfn in defending_types:
            mult *= single_type_multiplier(atk, dfn)
    return mult
