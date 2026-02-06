import streamlit as st

st.set_page_config(
    page_title="QuizMaster",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Welcome to QuizMaster!")
st.markdown("""
A fun quiz application to test your knowledge.

**Navigate using the sidebar:**
- 🥇 Quiz: Take a quiz
- 🥈 Highscores: View top scores
- 🥉 Categories: Browse quiz categories

Get ready to challenge yourself!
""")

# Optional: Add some stats or welcome message
st.info("💡 Tip: Start with the Quiz page to begin!")