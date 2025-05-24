# 🎯 AI Recruitment Screener

A multi-agent AI system that automates resume screening and candidate evaluation using OpenAI GPT models.

## 🚀 Features

- **Multi-Agent Architecture**: 4 specialized AI agents working together
- **Resume Parsing**: Extracts structured data from PDF, DOCX, and TXT files
- **Skills Matching**: Intelligent matching of candidate skills with job requirements
- **Interview Questions**: Auto-generates relevant technical, behavioral, and experience questions
- **Candidate Ranking**: Comprehensive scoring with detailed breakdown
- **Interactive UI**: User-friendly Streamlit interface

## 🤖 AI Agents

1. **Resume Parser Agent**: Extracts structured information from resumes
2. **Skills Matcher Agent**: Compares candidate skills with job requirements
3. **Interview Generator Agent**: Creates personalized interview questions
4. **Candidate Ranker Agent**: Provides final scoring and recommendations

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Git (for cloning)

## 🛠️ Installation

1. **Clone or download this project**
2. **Navigate to project directory**
   ```bash
   cd recruitment-screener
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Open `.env` file
   - Replace `your_openai_api_key_here` with your actual OpenAI API key

## 🔑 Getting OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy and paste it into your `.env` file

## 🚀 Running the Application

1. **Start the application**
   ```bash
   streamlit run main.py
   ```

2. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL manually

## 📖 How to Use

1. **Upload Resume**: Choose a PDF, DOCX, or TXT resume file
2. **Enter Job Description**: Paste the job requirements and description
3. **Click Process**: Let the AI agents analyze the candidate
4. **Review Results**: Get comprehensive screening report with:
   - Skills match analysis
   - Interview questions
   - Final score and recommendation
   - Strengths and improvement areas

## 📁 Project Structure

```
recruitment-screener/
├── agents/                 # AI agent implementations
│   ├── resume_parser.py   # Resume parsing agent
│   ├── skills_matcher.py  # Skills matching agent
│   ├── interview_generator.py # Interview questions agent
│   └── candidate_ranker.py # Ranking and scoring agent
├── utils/                 # Utility functions
│   ├── openai_client.py  # OpenAI API client
│   └── file_handlers.py  # File processing utilities
├── main.py               # Main Streamlit application
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables
└── README.md            # This file
```

## 🔧 Configuration

### Scoring Weights (in candidate_ranker.py)
- Skills Match: 40%
- Experience: 30%
- Education: 15%
- Additional Factors: 15%

### Supported File Formats
- **PDF**: Standard PDF files
- **DOCX**: Microsoft Word documents
- **TXT**: Plain text files

## 📊 Scoring System

### Final Score Ranges
- **80-100**: Strong Hire (High confidence)
- **65-79**: Hire (Medium-High confidence)
- **50-64**: Maybe (Medium confidence)
- **0-49**: Pass (Low confidence)

### Component Scores
- **Skills Score**: Based on match with job requirements
- **Experience Score**: Years of experience and role diversity
- **Education Score**: Degree level and relevance
- **Additional Score**: Contact info, skills diversity, detailed descriptions

## 🚨 Troubleshooting

### Common Issues

1. **OpenAI API Error**
   - Check your API key in `.env` file
   - Ensure you have sufficient API credits
   - Verify internet connection

2. **File Upload Issues**
   - Ensure file size is under 10MB
   - Check file format (PDF, DOCX, TXT only)
   - Try a different file

3. **Installation Problems**
   - Use Python 3.8 or higher
   - Try installing dependencies one by one
   - Use virtual environment

### Getting Help

If you encounter issues:
1. Check the error message in the Streamlit interface
2. Look at the console/terminal for detailed error logs
3. Ensure all dependencies are properly installed
4. Verify your OpenAI API key is correct

## 🔮 Future Enhancements

- [ ] Batch processing for multiple candidates
- [ ] Integration with ATS systems
- [ ] Advanced bias detection
- [ ] Machine learning model training
- [ ] Email automation
- [ ] Advanced analytics dashboard

## 📝 License

This project is for educational and commercial use.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for improvements.

---

**Happy Recruiting! 🎯**