# QuizMaster - Interactive Learning App 🎯

An interactive quiz application built with Streamlit for studying and testing knowledge across multiple categories.

## 📋 Project Overview

QuizMaster is a web-based quiz application that allows users to:
- Choose from multiple quiz categories
- Answer questions and track scores
- View highscores and leaderboards
- Browse all available questions by category

## 🚀 Features

### Phase 1 Features (Complete)

- **Home Page**: Welcome screen with player name input and category selection
- **Quiz Page**: Interactive quiz with immediate feedback
- **Highscores Page**: Leaderboard displaying top performers
- **Categories Page**: Browse all available quiz topics and questions
- **Session State Management**: Maintains game state across page navigation
- **JSON Data Storage**: Questions and highscores stored in JSON format
- **Scoring System**: Points based on difficulty (Easy: 10, Medium: 15, Hard: 20)
- **Multi-page Navigation**: Easy navigation between different sections

## 📁 Project Structure

```
s6-quizmaster-demo/
├── streamlit/
│   └── config.toml          # Streamlit configuration
├── data/
│   ├── questions.json       # Quiz questions database
│   └── highscores.json      # Highscores storage
├── pages/
│   ├── 1_📝_Quiz.py        # Quiz gameplay page
│   ├── 2_🏆_Highscores.py  # Leaderboard page
│   └── 3_📚_Categories.py  # Categories overview
├── Home.py                  # Main entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone or download the project**
   ```bash
   cd s6-quizmaster-demo
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run Home.py
   ```

4. **Access the app**
   Open your browser and navigate to `http://localhost:8501`

## 📊 Data Structures

### Questions JSON Structure

```json
{
  "categories": {
    "Category Name": [
      {
        "id": 1,
        "question": "Your question here?",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct": 0,
        "difficulty": "easy",
        "points": 10
      }
    ]
  }
}
```

### Highscores JSON Structure

```json
[
  {
    "player_name": "John Doe",
    "category": "Mathematics",
    "score": 85,
    "correct_answers": 6,
    "total_questions": 7,
    "percentage": 85.7,
    "date": "2026-01-30 14:30:00"
  }
]
```

## 🎮 How to Use

1. **Start the App**: Run `streamlit run Home.py`
2. **Enter Your Name**: Type your name on the home page
3. **Choose a Category**: Select from available quiz categories
4. **Answer Questions**: Click on your answer choice
5. **View Results**: See your score and accuracy at the end
6. **Check Highscores**: Visit the Highscores page to see top performers

## 🎯 Session State Variables

The app uses Streamlit's session state to maintain game data:

- `player_name`: Current player's name
- `score`: Current quiz score
- `current_question`: Index of current question
- `game_active`: Whether a quiz is in progress
- `selected_category`: Currently selected quiz category
- `answers_given`: List of answers provided
- `correct_answers`: Number of correct answers

## 📚 Available Categories

The demo includes three categories:

1. **Mathematics** (7 questions)
   - Basic arithmetic, algebra, geometry
   - Difficulty: Easy to Hard
   - Points: 10-20 per question

2. **Computer Science** (7 questions)
   - Programming, data structures, algorithms
   - Difficulty: Easy to Hard
   - Points: 10-20 per question

3. **General Knowledge** (8 questions)
   - Geography, history, culture
   - Difficulty: Easy to Hard
   - Points: 10-20 per question

## ➕ Adding New Questions

To add new questions, edit `data/questions.json`:

```json
{
  "categories": {
    "New Category": [
      {
        "id": 1,
        "question": "Your new question?",
        "options": ["A", "B", "C", "D"],
        "correct": 0,
        "difficulty": "medium",
        "points": 15
      }
    ]
  }
}
```

## 🎨 Customization

### Changing Theme Colors

Edit `streamlit/config.toml`:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f8f9fa"
textColor = "#262730"
```

### Modifying Points System

In the quiz questions, adjust the `points` value:
- Easy: 10 points
- Medium: 15 points
- Hard: 20 points

## 🚀 Phase 2 Extensions (Future)

The following features are planned for Phase 2:

- **SQLite Database**: Replace JSON with proper database
- **User Authentication**: Login system with password hashing
- **Admin Panel**: CRUD interface for managing questions
- **User Statistics**: Personal performance tracking
- **Advanced Features**: Timer, sound effects, achievements

## 🐛 Troubleshooting

### Common Issues

**Problem**: `FileNotFoundError: questions.json`
- **Solution**: Ensure `data/questions.json` exists and is properly formatted

**Problem**: Session state not persisting
- **Solution**: Don't use browser back button; use app navigation buttons

**Problem**: Highscores not saving
- **Solution**: Check write permissions for `data/highscores.json`

## 📝 Development Notes

### Git Workflow

```bash
# Initial setup
git init
git add .
git commit -m "Initial commit: Phase 1 complete"

# Making changes
git add .
git commit -m "Add new question category"
git push
```

### Testing

- Test each page independently
- Verify session state persistence
- Check JSON file read/write operations
- Test with different user inputs

## 🏆 Grading Criteria Checklist

- ✅ **Functionality**: All features work correctly
- ✅ **Code Quality**: Clean, readable, well-commented code
- ✅ **UI/UX**: User-friendly interface with good design
- ✅ **Git Workflow**: Proper commits and documentation
- ✅ **Session State**: Correctly implemented state management
- ✅ **JSON Storage**: Proper data structure and file handling

## 🎓 Learning Objectives Achieved

- ✅ Understanding and applying `st.session_state`
- ✅ Working with JSON files (reading, writing, structuring)
- ✅ Implementing game logic (scoring, game states)
- ✅ Creating multi-page apps with Streamlit
- ✅ Proper project structure and organization

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Session State Guide](https://docs.streamlit.io/develop/concepts/architecture/session-state)
- [Python JSON Documentation](https://docs.python.org/3/library/json.html)
- [Streamlit Multi-page Apps](https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app)

## 👥 Contributing

To contribute:
1. Fork the project
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is created for educational purposes as part of the S6 Streamlit Project.

## 🙋 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review the code comments
3. Ask your classmates or teacher
4. Check Streamlit documentation

---

**Created by**: [Your Name]  
**Date**: January 31, 2026  
**Course**: S6 Streamlit Project  
**Version**: Phase 1 - Complete

Good luck with your coding! 🚀
