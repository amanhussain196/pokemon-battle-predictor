# src/predictor.py# src/predictor.py

import os
import pandas as pd
import joblib
from .features import add_features
from .battle_sim import simulate_battle

# Auto-detect project root for both local & Streamlit deployments
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(PROJECT_ROOT, "data", "pokemon_clean.csv")
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "battle_model.pkl")

# Load Data and Model
df_clean = pd.read_csv(DATA_PATH)
df_clean["name_lower"] = df_clean["name"].str.lower()

model = joblib.load(MODEL_PATH)


def get_pokemon(name):
    row = df_clean[df_clean["name_lower"] == name.lower()]
    if row.empty:
        raise ValueError(f"Pokémon '{name}' not found!")
    return row.iloc[0]


def build_feature_row(p1, p2):
    row = {
        "p1_hp": p1["hp"], "p1_attack": p1["attack"], "p1_defense": p1["defense"],
        "p1_sp_attack": p1["sp_attack"], "p1_sp_defense": p1["sp_defense"], "p1_speed": p1["speed"],
        "p2_hp": p2["hp"], "p2_attack": p2["attack"], "p2_defense": p2["defense"],
        "p2_sp_attack": p2["sp_attack"], "p2_sp_defense": p2["sp_defense"], "p2_speed": p2["speed"],
        "p1_type1": p1["type1"], "p1_type2": p1["type2"],
        "p2_type1": p2["type1"], "p2_type2": p2["type2"]
    }

    df_row = pd.DataFrame([row])
    df_row = add_features(df_row)

    # Only diff_stats + type advantage needed
    feature_cols = [c for c in df_row.columns if c.startswith("diff_")] + ["type_advantage"]
    return df_row[feature_cols]


def predict_battle_ml(name1, name2):
    p1, p2 = get_pokemon(name1), get_pokemon(name2)
    row = build_feature_row(p1, p2)
    prob = model.predict_proba(row)[0][1]
    return (name1, prob) if prob >= 0.5 else (name2, 1 - prob)


def predict_and_simulate(name1, name2):
    ml_winner, ml_prob = predict_battle_ml(name1, name2)

    # Convert simulator numeric result to Pokémon name
    sim_result = simulate_battle(get_pokemon(name1), get_pokemon(name2))
    sim_winner = name1 if sim_result == 1 else name2

    return {
        "ML Winner": ml_winner,
        "Win Prob": f"{ml_prob:.2%}",
        "Simulated Winner": sim_winner
    }


