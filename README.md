# LurnZo – AI-Powered Learning Platform

A comprehensive, gamified learning platform built with Flask that provides AI assistance, structured courses, coding challenges, resume analysis, and interview preparation - all designed like Coursera.

## 🚀 Features

### Core Learning Platform
- **AI-Powered Q&A Assistant** - Get instant help with programming and learning questions
- **Structured Courses** - Curated learning paths with lessons, quizzes, and certificates
- **Gamification System** - Earn points, level up, unlock achievements, and compete on leaderboards
- **Progress Tracking** - Monitor your learning journey with detailed analytics

### Specialized Tools
- **Coding Challenges** - Practice with real programming problems and get instant feedback
- **Resume Analyzer** - AI-powered resume review with actionable improvement suggestions
- **Interview Preparation** - Practice technical interview questions with hints and explanations
- **Profile Dashboard** - Track achievements, streaks, and learning statistics

### Technical Features
- **TF-IDF Q&A Engine** - Smart question answering with subject-aware ranking
- **Code Execution** - Run and test code submissions in multiple languages
- **Responsive Design** - Modern, mobile-friendly UI with dark/light themes
- **Real-time Updates** - Live progress tracking and instant feedback

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **AI/NLP**: scikit-learn, TF-IDF, cosine similarity
- **Styling**: Custom CSS with CSS Grid/Flexbox
- **Database**: JSON-based storage (easily upgradable to SQL/NoSQL)

## 📁 Project Structure

```
lur/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── index.html       # Homepage with AI chat
│   ├── courses.html     # Course catalog
│   ├── coding.html      # Coding challenges
│   ├── resume.html      # Resume analyzer
│   ├── interview.html   # Interview prep
│   └── profile.html     # User profile & progress
├── static/              # Static assets
│   ├── css/
│   │   └── styles.css   # Main stylesheet
│   └── js/
│       └── app.js       # Frontend logic
├── services/            # Backend services
│   ├── __init__.py
│   ├── qa_engine.py     # AI Q&A engine
│   ├── gamification.py  # Points & achievements
│   ├── course_manager.py # Course management
│   ├── coding_challenges.py # Programming problems
│   ├── resume_analyzer.py # Resume analysis
│   └── interview_prep.py # Interview questions
└── data/               # Data files
    └── qa_dataset.json # Q&A knowledge base
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd lur
   ```

2. **Create virtual environment**
   ```bash
   # Windows
   python -m venv .venv
   .\.venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 🎯 Usage Guide

### Getting Started
1. **Homepage** - Explore features and chat with AI assistant
2. **Courses** - Browse and enroll in structured learning paths
3. **Coding** - Practice programming with real challenges
4. **Resume** - Get AI feedback on your resume
5. **Interview** - Prepare for technical interviews
6. **Profile** - Track your progress and achievements

### AI Assistant
- Ask any programming or learning question
- Get instant, contextual answers
- View source references and confidence scores

### Learning Paths
- **Beginner**: Python basics, web fundamentals
- **Intermediate**: Data science, algorithms, system design
- **Advanced**: Machine learning, advanced concepts

### Gamification
- **Points System**: Earn points for completing lessons
- **Leveling**: Progress through learning levels
- **Achievements**: Unlock badges for milestones
- **Streaks**: Maintain daily learning habits
- **Leaderboard**: Compete with other learners

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Set a secret key for production
export SECRET_KEY="your-secret-key-here"

# Optional: Set custom port
export PORT=5000
```

### Customizing Content
- **Courses**: Edit `services/course_manager.py`
- **Q&A Database**: Modify `data/qa_dataset.json`
- **Coding Challenges**: Update `services/coding_challenges.py`
- **Interview Questions**: Edit `services/interview_prep.py`

## 🚀 Deployment

### Production Setup
1. **Set environment variables**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY="your-secure-secret-key"
   ```

2. **Use Gunicorn**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

3. **Reverse Proxy** (Nginx example)
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🔮 Future Enhancements

### Planned Features
- **User Authentication** - Sign up, login, and personalized experiences
- **Database Integration** - PostgreSQL/MySQL for scalable data storage
- **Advanced AI** - Integration with OpenAI GPT or similar LLMs
- **Video Lessons** - Multimedia learning content
- **Peer Learning** - Study groups and collaborative features
- **Mobile App** - Native iOS/Android applications
- **API Access** - RESTful API for third-party integrations

### Technical Improvements
- **Caching Layer** - Redis for improved performance
- **Background Jobs** - Celery for async task processing
- **Real-time Features** - WebSocket support for live updates
- **Analytics Dashboard** - Detailed learning insights
- **A/B Testing** - Optimize learning experiences

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests (when implemented)
python -m pytest

# Code formatting
black .
flake8 .
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Flask Community** - For the excellent web framework
- **scikit-learn** - For powerful machine learning capabilities
- **Inter Font** - For beautiful typography
- **Open Source Community** - For inspiration and tools

## 📞 Support

- **Documentation**: Check this README and inline code comments
- **Issues**: Report bugs and feature requests via GitHub Issues
- **Discussions**: Join community discussions on GitHub
- **Email**: Contact the development team

---

**Built with ❤️ for students and lifelong learners**

*Transform your learning journey with AI-powered assistance and gamified experiences.*


