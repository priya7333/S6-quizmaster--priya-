import streamlit as st
import json
from collections import defaultdict

st.title("🥉 Quiz Categories")

# Load questions
@st.cache_data
def load_questions():
    with open("data/questions.json", "r") as f:
        data = json.load(f)
    return data["questions"]

questions = load_questions()

if not questions:
    st.error("No questions available.")
    st.stop()

# Group by category
categories = defaultdict(list)
for q in questions:
    categories[q["category"]].append(q)

st.subheader("Available Categories")
for cat, qs in categories.items():
    with st.expander(f"{cat} ({len(qs)} questions)"):
        st.write("**Difficulties:**")
        difficulties = defaultdict(int)
        for q in qs:
            difficulties[q["difficulty"]] += 1
        for diff, count in difficulties.items():
            st.write(f"- {diff.capitalize()}: {count} questions")

        st.write("**Sample Questions:**")
        for q in qs[:3]:  # Show first 3
            st.write(f"- {q['question']}")

st.info("Head to the Quiz page to start playing!")
