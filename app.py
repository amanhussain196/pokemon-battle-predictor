import streamlit as st
import sys
import os

# Ensure package path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.predictor import predict_and_simulate

st.set_page_config(page_title="Pokémon Battle Predictor", page_icon="⚔️")

st.title("⚔️ Pokémon Battle Predictor")
st.write("Select two Pokémon to simulate who will win!")

# Input Fields
p1 = st.text_input("Pokémon 1:", "Pikachu")
p2 = st.text_input("Pokémon 2:", "Charizard")

if st.button("Battle!"):
    try:
        result = predict_and_simulate(p1, p2)

        st.success(f"🥇 Predicted Winner: **{result['ML Winner']}**")
        st.write(f"Win Probability: **{result['Win Prob']}**")

        st.info(f"Simulated Winner: {result['Simulated Winner']}")
    except:
        st.error("Invalid Pokémon name! Try again.")
