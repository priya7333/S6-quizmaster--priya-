import streamlit as st
import json
import os
from pathlib import Path
import hashlib
import os

user_file = 'users.txt'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def user_exists(username):
    if not os.path.exists(user_file):
        return False
    with open(user_file, 'r') as f:
        return any(line.startswith(f"{username}:") for line in f)

def register():
    st.subheader("Register")
    username = st.text_input("Enter a username", key="register_username")
    password = st.text_input("Enter a password", type="password", key="register_password")
    if st.button("Register"):
        if user_exists(username):
            st.error("Username already exists. Please choose a different username.")
        else:
            with open(user_file, 'a') as f:
                f.write(f"{username}:{hash_password(password)}\n")
            st.success("Registration successful! Please log in.")

def login():
    st.subheader("Login")
    username = st.text_input("Enter your username", key="login_username")
    password = st.text_input("Enter your password", type="password", key="login_password")
    if st.button("Login"):
        if not os.path.exists(user_file):
            st.error("No users registered yet. Please register first.")
            return
        hashed_password = hash_password(password)
        with open(user_file, 'r') as f:
            for line in f:
                if line.strip() == f"{username}:{hashed_password}":
                    st.success("Login successful!")
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    return
        st.error("Login failed. Please check your credentials.")

def main():
    st.title("User Authentication System")
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        st.success(f"Welcome, {st.session_state['username']}!")
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ""
            st.info("You have been logged out.")
    else:
        st.sidebar.title("Authentication")
        auth_option = st.sidebar.radio("Choose an option", ["Login", "Register"])
        if auth_option == "Login":
            login()
        elif auth_option == "Register":
            register()

if __name__ == "__main__":
    main()

# Page configuration
st.set_page_config(
    page_title="QuizMaster - Home",
    page_icon="🎯",
    layout="wide"
)

# Initialize session state variables
def initialize_session_state():
    """Initialize all session state variables if they don't exist"""
    if 'player_name' not in st.session_state:
        st.session_state.player_name = ''
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'game_active' not in st.session_state:
        st.session_state.game_active = False
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = None
    if 'answers_given' not in st.session_state:
        st.session_state.answers_given = []
    if 'correct_answers' not in st.session_state:
        st.session_state.correct_answers = 0
    if 'time_remaining' not in st.session_state:
        st.session_state.time_remaining = 30

def load_questions():
    """Load questions from JSON file"""
    questions_file = Path(__file__).parent / 'data' / 'questions.json'
    try:
        with open(questions_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('categories', {})
    except FileNotFoundError:
        st.error("⚠️ Questions file not found. Please create data/questions.json")
        return {}
    except json.JSONDecodeError:
        st.error("⚠️ Error reading questions file. Please check the JSON format.")
        return {}

# Initialize session state
initialize_session_state()

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .category-card {
        padding: 1.5rem;
        border-radius: 10px;
        background: #f8f9fa;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        transition: transform 0.2s;
    }
    .category-card:hover {
        transform: translateX(5px);
    }
    .stButton>button {
        width: 100%;
        background-color: #667eea;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #764ba2;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <h1>🎯 QuizMaster</h1>
        <p>Test Your Knowledge & Challenge Yourself!</p>
    </div>
""", unsafe_allow_html=True)

# Welcome section
st.markdown("### 👋 Welcome to QuizMaster!")
st.write("An interactive learning app to test your knowledge across multiple categories.")

# Load available categories
categories = load_questions()

if not categories:
    st.warning("📝 No quiz categories available yet. Please add questions to get started!")
    st.stop()

# Player name input
col1, col2 = st.columns([2, 1])
with col1:
    player_name = st.text_input(
        "Enter your name:",
        value=st.session_state.player_name,
        placeholder="Your Name",
        key="name_input"
    )
    
with col2:
    st.write("")  # Spacing
    st.write("")  # Spacing

if player_name:
    st.session_state.player_name = player_name
    
    # Category selection
    st.markdown("### 📚 Choose a Category")
    
    # Display categories in a grid
    cols = st.columns(2)
    
    for idx, (category_name, questions) in enumerate(categories.items()):
        with cols[idx % 2]:
            with st.container():
                st.markdown(f"""
                    <div class="category-card">
                        <h4>{category_name}</h4>
                        <p>📊 {len(questions)} questions available</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Start {category_name} Quiz", key=f"start_{category_name}"):
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
    
    # Stats section
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Categories", len(categories))
    with col2:
        total_questions = sum(len(qs) for qs in categories.values())
        st.metric("Total Questions", total_questions)
    with col3:
        st.metric("Your Name", player_name)

else:
    st.info("👆 Please enter your name to get SIGN UP!")
    
# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>💡 Navigate to different pages using the sidebar</p>
        <p>Good luck with your quiz! 🍀</p>
    </div>
""", unsafe_allow_html=True)
