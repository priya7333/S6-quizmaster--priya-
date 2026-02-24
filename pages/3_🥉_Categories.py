import streamlit as st
import json
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="QuizMaster - Categories",
    page_icon="📚",
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
    except json.JSONDecodeError:
        st.error("⚠️ Error reading questions file.")
        return {}

# Custom CSS
st.markdown("""
    <style>
    .categories-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .category-box {
        padding: 1.5rem;
        border-radius: 10px;
        background: #f8f9fa;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .difficulty-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: bold;
        margin: 0.25rem;
    }
    .easy {
        background-color: #d4edda;
        color: #155724;
    }
    .medium {
        background-color: #fff3cd;
        color: #856404;
    }
    .hard {
        background-color: #f8d7da;
        color: #721c24;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="categories-header">
        <h1>📚 Quiz Categories</h1>
        <p>Explore all available quiz topics and questions</p>
    </div>
""", unsafe_allow_html=True)

# Load categories
categories = load_questions()

if not categories:
    st.warning("📝 No categories available yet!")
    if st.button("🏠 Go to Home"):
        st.switch_page("Home.py")
    st.stop()

# Overview statistics
st.markdown("### 📊 Overview")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Categories", len(categories))

with col2:
    total_questions = sum(len(qs) for qs in categories.values())
    st.metric("Total Questions", total_questions)

with col3:
    avg_questions = total_questions / len(categories) if categories else 0
    st.metric("Avg Questions/Category", f"{avg_questions:.1f}")

st.markdown("---")

# Display each category
for category_name, questions in categories.items():
    with st.expander(f"📖 {category_name} ({len(questions)} questions)", expanded=False):
        
        # Category statistics
        col1, col2, col3, col4 = st.columns(4)
        
        # Count difficulties
        difficulty_counts = {'easy': 0, 'medium': 0, 'hard': 0}
        total_points = 0
        
        for q in questions:
            diff = q.get('difficulty', 'medium')
            difficulty_counts[diff] = difficulty_counts.get(diff, 0) + 1
            total_points += q.get('points', 10)
        
        with col1:
            st.metric("Questions", len(questions))
        with col2:
            st.metric("🟢 Easy", difficulty_counts['easy'])
        with col3:
            st.metric("🟡 Medium", difficulty_counts['medium'])
        with col4:
            st.metric("🔴 Hard", difficulty_counts['hard'])
        
        st.write(f"**Total Points Available:** {total_points}")
        
        st.markdown("---")
        
        # Display questions
        st.markdown("#### Questions Preview")
        
        for idx, question in enumerate(questions):
            with st.container():
                st.markdown(f"**Question {idx + 1}**")
                st.write(question['question'])
                
                # Difficulty and points
                difficulty = question.get('difficulty', 'medium')
                points = question.get('points', 10)
                st.markdown(f"<span class='difficulty-badge {difficulty}'>{difficulty.upper()}</span> <span style='color: #666;'>• {points} points</span>", unsafe_allow_html=True)
                
                # Show options
                options = question['options']
                correct_idx = question['correct']
                
                for opt_idx, option in enumerate(options):
                    if opt_idx == correct_idx:
                        st.success(f"✅ {chr(65 + opt_idx)}) {option} (Correct)")
                    else:
                        st.write(f"{chr(65 + opt_idx)}) {option}")
                
                if idx < len(questions) - 1:
                    st.markdown("---")
        
        # Start quiz button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(f"🚀 Start {category_name} Quiz", key=f"start_{category_name}", use_container_width=True):
                # Check if player name exists
                if not st.session_state.get('player_name', ''):
                    st.error("⚠️ Please enter your name on the Home page first!")
                else:
                    # Reset game state
                    st.session_state.selected_category = category_name
                    st.session_state.current_question = 0
                    st.session_state.score = 0
                    st.session_state.game_active = True
                    st.session_state.answers_given = []
                    st.session_state.correct_answers = 0
                    st.session_state.time_remaining = 30
                    
                    # Navigate to quiz page
                    st.switch_page("pages/1_Quiz.py")

st.markdown("---")

# Difficulty distribution chart
st.markdown("### 📊 Difficulty Distribution")

all_difficulties = []
for questions in categories.values():
    for q in questions:
        all_difficulties.append(q.get('difficulty', 'medium'))

diff_counts = {
    'Easy': all_difficulties.count('easy'),
    'Medium': all_difficulties.count('medium'),
    'Hard': all_difficulties.count('hard')
}

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🟢 Easy Questions", diff_counts['Easy'])
with col2:
    st.metric("🟡 Medium Questions", diff_counts['Medium'])
with col3:
    st.metric("🔴 Hard Questions", diff_counts['Hard'])

# Points distribution
st.markdown("---")
st.markdown("### 💰 Points Information")

st.info("""
**Points are awarded based on difficulty:**
- 🟢 Easy questions: 10 points
- 🟡 Medium questions: 15 points  
- 🔴 Hard questions: 20 points

Complete all questions correctly to maximize your score!
""")

# Action buttons
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("Home.py")

with col2:
    if st.button("🏆 View Highscores", use_container_width=True):
        st.switch_page("pages/2_Highscores.py")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>💡 Tip: Start with easier categories to build confidence!</p>
    </div>
""", unsafe_allow_html=True)
