import streamlit as st
import json

# Emoji helpers
RANK_EMOJI = {
    1: "🥇",
    2: "🥈",
    3: "🥉",
}

def get_rank_emoji(rank: int) -> str:
    return RANK_EMOJI.get(rank, str(rank))

st.title("🥈 Highscores")

# Load highscores
try:
    with open("data/highscores.json", "r") as f:
        highscores = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    highscores = []

if not highscores:
    st.info("No highscores yet. Take a quiz to set a record!")
else:
    st.subheader("Top Scores")
    for i, score in enumerate(highscores, 1):
        emoji = get_rank_emoji(i)
        percentage = (score["score"] / score["total"]) * 100 if score["total"] > 0 else 0
        st.write(f"{emoji} **{score['name']}**: {score['score']}/{score['total']} ({percentage:.1f}%)")
