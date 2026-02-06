import streamlit as st
import json
import random

st.title("🥇 Take a Quiz")

# Load questions
@st.cache_data
def load_questions():
    with open("data/questions.json", "r") as f:
        data = json.load(f)
    return data["questions"]

questions = load_questions()

if not questions:
    st.error("No questions available. Please add questions to data/questions.json")
    st.stop()

# Quiz state
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False

# Shuffle questions for variety
if not st.session_state.quiz_started:
    random.shuffle(questions)
    st.session_state.quiz_started = True

# Display current question
if st.session_state.current_question < len(questions):
    q = questions[st.session_state.current_question]
    st.subheader(f"Question {st.session_state.current_question + 1} of {len(questions)}")
    st.write(f"**{q['question']}**")
    st.write(f"*Category: {q['category']} | Difficulty: {q['difficulty']}*")

    # Options
    options = q["options"]
    choice = st.radio("Select your answer:", options, key=f"q_{st.session_state.current_question}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit Answer"):
            selected_index = options.index(choice)
            correct = selected_index == q["correctAnswer"]
            st.session_state.answers.append({
                "question": q["question"],
                "selected": choice,
                "correct": options[q["correctAnswer"]],
                "is_correct": correct
            })
            if correct:
                st.session_state.score += 1
                st.success("Correct! 🎉")
            else:
                st.error(f"Wrong! The correct answer is: {options[q['correctAnswer']]}")
            st.session_state.current_question += 1
            st.rerun()

    with col2:
        if st.button("Skip Question"):
            st.session_state.answers.append({
                "question": q["question"],
                "selected": "Skipped",
                "correct": options[q["correctAnswer"]],
                "is_correct": False
            })
            st.session_state.current_question += 1
            st.rerun()

else:
    # Quiz finished
    st.success(f"Quiz Complete! Your score: {st.session_state.score}/{len(questions)}")

    # Save highscore
    try:
        with open("data/highscores.json", "r") as f:
            highscores = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        highscores = []

    # Ask for name
    name = st.text_input("Enter your name for the highscore:")
    if st.button("Save Score") and name:
        highscores.append({
            "name": name,
            "score": st.session_state.score,
            "total": len(questions),
            "date": str(st.session_state)  # placeholder
        })
        # Sort and keep top 10
        highscores.sort(key=lambda x: x["score"], reverse=True)
        highscores = highscores[:10]

        with open("data/highscores.json", "w") as f:
            json.dump(highscores, f, indent=2)

        st.success("Score saved!")

    # Show answers
    with st.expander("Review Answers"):
        for i, ans in enumerate(st.session_state.answers):
            status = "✅" if ans["is_correct"] else "❌"
            st.write(f"{i+1}. {status} {ans['question']}")
            st.write(f"   Your answer: {ans['selected']}")
            st.write(f"   Correct: {ans['correct']}")
            st.write("---")

    if st.button("Take Another Quiz"):
        st.session_state.current_question = 0
        st.session_state.answers = []
        st.session_state.score = 0
        st.session_state.quiz_started = False
        st.rerun()
