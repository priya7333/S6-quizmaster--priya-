import streamlit as st
import json
import time
from pathlib import Path
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="QuizMaster - Quiz",
    page_icon="📝",
    layout="wide"
)

def load_questions():
    """Load questions from JSON file"""
    questions_file = Path(__file__).parent.parent / 'data' / 'questions.json'
    try:
        with open(questions_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('categories', {})
    except FileNotFoundError:
        st.error("⚠️ Questions file not found.")
        return {}

def save_highscore(player_name, category, score, correct_answers, total_questions):
    """Save highscore to JSON file"""
    highscores_file = Path(__file__).parent.parent / 'data' / 'highscores.json'
    
    # Load existing highscores
    try:
        with open(highscores_file, 'r', encoding='utf-8') as f:
            highscores = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        highscores = []
    
    # Add new score
    new_score = {
        'player_name': player_name,
        'category': category,
        'score': score,
        'correct_answers': correct_answers,
        'total_questions': total_questions,
        'percentage': round((correct_answers / total_questions) * 100, 1),
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    highscores.append(new_score)
    
    # Sort by score (descending)
    highscores.sort(key=lambda x: x['score'], reverse=True)
    
    # Keep only top 50
    highscores = highscores[:50]
    
    # Save back to file
    with open(highscores_file, 'w', encoding='utf-8') as f:
        json.dump(highscores, f, indent=2, ensure_ascii=False)

# Custom CSS
st.markdown("""
    <style>
    .quiz-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .question-card {
        padding: 2rem;
        border-radius: 10px;
        background: #f8f9fa;
        border: 2px solid #667eea;
        margin: 1rem 0;
    }
    .option-button {
        margin: 0.5rem 0;
    }
    .correct-answer {
        background-color: #d4edda !important;
        border-color: #28a745 !important;
    }
    .wrong-answer {
        background-color: #f8d7da !important;
        border-color: #dc3545 !important;
    }
    .timer {
        font-size: 2rem;
        font-weight: bold;
        color: #dc3545;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Check if game is active
if not st.session_state.get('game_active', False):
    st.warning("⚠️ No active quiz! Please go to Home page and select a category.")
    if st.button("🏠 Go to Home"):
        st.switch_page("Home.py")
    st.stop()

# Check if player name exists
if not st.session_state.get('player_name', ''):
    st.error("⚠️ Please enter your name on the Home page first!")
    if st.button("🏠 Go to Home"):
        st.switch_page("Home.py")
    st.stop()

# Load questions
categories = load_questions()
selected_category = st.session_state.selected_category

if selected_category not in categories:
    st.error(f"⚠️ Category '{selected_category}' not found!")
    st.stop()

questions = categories[selected_category]
current_q_index = st.session_state.current_question

# Check if quiz is complete
if current_q_index >= len(questions):
    st.markdown("""
        <div class="quiz-header">
            <h1>🎉 Quiz Complete!</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Display results
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Final Score", f"{st.session_state.score} points")
    with col2:
        st.metric("Correct Answers", f"{st.session_state.correct_answers}/{len(questions)}")
    with col3:
        percentage = (st.session_state.correct_answers / len(questions)) * 100
        st.metric("Percentage", f"{percentage:.1f}%")
    
    # Performance message
    if percentage >= 90:
        st.success("🌟 Outstanding! You're a true master!")
    elif percentage >= 70:
        st.success("👏 Great job! You really know your stuff!")
    elif percentage >= 50:
        st.info("👍 Good effort! Keep practicing!")
    else:
        st.warning("💪 Don't give up! Practice makes perfect!")
    
    # Save highscore
    save_highscore(
        st.session_state.player_name,
        selected_category,
        st.session_state.score,
        st.session_state.correct_answers,
        len(questions)
    )
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.game_active = False
            st.switch_page("Home.py")
    with col2:
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.answers_given = []
            st.session_state.correct_answers = 0
            st.rerun()
    with col3:
        if st.button("🏆 View Highscores", use_container_width=True):
            st.switch_page("pages/2_Highscores.py")
    
    st.stop()

# Display current question
current_question = questions[current_q_index]

# Header
st.markdown(f"""
    <div class="quiz-header">
        <h1>📝 {selected_category} Quiz</h1>
        <p>Question {current_q_index + 1} of {len(questions)}</p>
    </div>
""", unsafe_allow_html=True)

# Progress bar
progress = (current_q_index) / len(questions)
st.progress(progress)

# Display score and stats
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Score", st.session_state.score)
with col2:
    st.metric("Correct", st.session_state.correct_answers)
with col3:
    st.metric("Player", st.session_state.player_name)

st.markdown("---")

# Question display
st.markdown(f"""
    <div class="question-card">
        <h3>Question {current_q_index + 1}</h3>
        <h2>{current_question['question']}</h2>
    </div>
""", unsafe_allow_html=True)

# Difficulty badge
difficulty = current_question.get('difficulty', 'medium')
difficulty_colors = {
    'easy': '🟢',
    'medium': '🟡',
    'hard': '🔴'
}
st.markdown(f"**Difficulty:** {difficulty_colors.get(difficulty, '⚪')} {difficulty.capitalize()}")
st.markdown(f"**Points:** {current_question.get('points', 10)}")

st.markdown("---")

# Answer options
st.markdown("### Choose your answer:")

# Check if answer has been given for this question
answer_given_key = f"answer_given_{current_q_index}"
if answer_given_key not in st.session_state:
    st.session_state[answer_given_key] = False

# Display options
options = current_question['options']
correct_index = current_question['correct']

for idx, option in enumerate(options):
    col1, col2 = st.columns([4, 1])
    
    with col1:
        # Create button for each option
        button_key = f"option_{current_q_index}_{idx}"
        
        if st.button(
            f"{chr(65 + idx)}) {option}",
            key=button_key,
            use_container_width=True,
            disabled=st.session_state[answer_given_key]
        ):
            # Record answer
            st.session_state[answer_given_key] = True
            st.session_state.answers_given.append(idx)
            
            # Check if correct
            if idx == correct_index:
                st.session_state.correct_answers += 1
                st.session_state.score += current_question.get('points', 10)
                st.session_state[f"feedback_{current_q_index}"] = "correct"
            else:
                st.session_state[f"feedback_{current_q_index}"] = "wrong"
            
            st.rerun()

# Show feedback if answer given
if st.session_state[answer_given_key]:
    st.markdown("---")
    feedback = st.session_state.get(f"feedback_{current_q_index}", "")
    
    if feedback == "correct":
        st.success("✅ Correct! Well done!")
        st.balloons()
    else:
        st.error(f"❌ Wrong! The correct answer was: {options[correct_index]}")
    
    # Next question button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("➡️ Next Question", use_container_width=True, type="primary"):
            st.session_state.current_question += 1
            st.rerun()

# Sidebar with quiz info
with st.sidebar:
    st.markdown("### 📊 Quiz Progress")
    st.write(f"**Category:** {selected_category}")
    st.write(f"**Progress:** {current_q_index + 1}/{len(questions)}")
    st.write(f"**Score:** {st.session_state.score}")
    st.write(f"**Accuracy:** {st.session_state.correct_answers}/{current_q_index + 1 if st.session_state[answer_given_key] else current_q_index}")
    
    st.markdown("---")
    
    if st.button("🚪 Exit Quiz", use_container_width=True):
        st.session_state.game_active = False
        st.switch_page("Home.py")
