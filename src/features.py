# src/features.py

from .type_chart import get_type_multiplier
import pandas as pd

def add_features(df):
    df = df.copy()

    for stat in ["hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]:
        df[f"diff_{stat}"] = df[f"p1_{stat}"] - df[f"p2_{stat}"]

    advantages = []
    for _, row in df.iterrows():
        p1_types = [row["p1_type1"]]
        if row["p1_type2"] != "None":
            p1_types.append(row["p1_type2"])
        p2_types = [row["p2_type1"]]
        if row["p2_type2"] != "None":
            p2_types.append(row["p2_type2"])
        adv = get_type_multiplier(p1_types, p2_types) - get_type_multiplier(p2_types, p1_types)
        advantages.append(adv)
    
    df["type_advantage"] = advantages
    return df
