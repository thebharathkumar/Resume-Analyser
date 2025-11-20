# 🎯 Resume ATS Analyzer - Blackbox Edition

> **The ultimate tool to understand how Applicant Tracking Systems (ATS) read your resume**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18.0+-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)

## ✨ Features

### 🔍 **ATS Blackbox Simulation**
See exactly how Applicant Tracking Systems parse and interpret your resume.

### 📊 **Keyword Scoring**
- Intelligent keyword extraction
- Industry-specific keyword matching
- Relevance scoring with AI
- Missing keyword recommendations

### 🎯 **Desired Role Matching**
- Match your resume against target job roles
- Get percentage compatibility scores
- Identify skill gaps
- Tailored improvement suggestions

### 🌡️ **Grammar & Strength Heatmap**
- Visual heatmap showing strong/weak sections
- Grammar checking and corrections
- Impact word identification
- Action verb strength analysis

### 👔 **Hiring Manager Readability Score**
- Flesch Reading Ease Score
- ATS-friendly formatting check
- Layout and structure analysis
- White space optimization

### 🆚 **Job Description Comparison**
- Upload target job descriptions
- Side-by-side comparison
- Gap analysis
- Tailoring recommendations

### 📈 **Export & Share**
- Export detailed reports as PDF
- JSON data export for further analysis
- Shareable LinkedIn-ready insights

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/thebharathkumar/Resume-Analyser.git
   cd Resume-Analyser
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   ```

4. **Start the application**

   Terminal 1 (Backend):
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```

   Terminal 2 (Frontend):
   ```bash
   cd frontend
   npm start
   ```

5. **Open your browser**
   Navigate to `http://localhost:3000`

## 🏗️ Architecture

```
Resume-Analyser/
├── backend/               # FastAPI Backend
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Core functionality
│   │   ├── models/       # Data models
│   │   ├── services/     # Business logic
│   │   └── utils/        # Utility functions
│   ├── uploads/          # Temporary file storage
│   └── main.py           # Application entry point
│
├── frontend/             # React Frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   ├── utils/        # Utility functions
│   │   └── App.tsx       # Main application
│   └── public/           # Static assets
│
└── docs/                 # Documentation
```

## 🎨 Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework
- **Python 3.9+** - Core language
- **spaCy** - NLP and text analysis
- **PyPDF2 / python-docx** - Document parsing
- **NLTK** - Natural language processing
- **textstat** - Readability scoring

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **shadcn/ui** - Component library
- **Recharts** - Data visualization
- **Axios** - HTTP client

## 📖 Usage

1. **Upload Resume**: Drag and drop or select your resume (PDF/DOCX)
2. **Add Job Description** (Optional): Paste the job description for comparison
3. **Analyze**: Click analyze and watch the magic happen
4. **Review Results**: Explore the comprehensive analysis
5. **Export**: Download your detailed report

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🌟 Show Your Support

If this tool helped you land your dream job, give it a ⭐️ and share it on LinkedIn!

## 📬 Contact

Created by [@thebharathkumar](https://github.com/thebharathkumar)

---

**Built with ❤️ to help job seekers succeed**
