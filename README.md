# AI-Powered Smart Resume Analyzer & Career Assistant

A full-stack AI platform that analyzes resumes, scores ATS compatibility, detects skill gaps, matches job descriptions, analyzes GitHub/LinkedIn profiles, and generates personalized career roadmaps.

---

## Project Structure

```
AI-Resume-Analyzer/
├── .env                          ← API keys & config (ROOT)
├── requirements.txt              ← Python dependencies (ROOT)
├── README.md
│
├── backend/
│   ├── app.py                    ← Flask entry point
│   ├── dataset/
│   │   ├── occupations.csv
│   │   ├── skills.csv
│   │   ├── role_skill_mapping.csv
│   │   └── certifications.xlsx
│   ├── uploads/
│   │   ├── resumes/              ← uploaded resume files
│   │   └── reports/              ← generated PDF reports
│   ├── parsers/
│   │   ├── pdf_parser.py
│   │   ├── docx_parser.py
│   │   ├── text_cleaner.py
│   │   └── resume_parser.py      ← master parser
│   ├── nlp/
│   │   ├── skill_extractor.py
│   │   ├── keyword_extractor.py
│   │   ├── education_extractor.py
│   │   ├── experience_extractor.py
│   │   ├── project_extractor.py
│   │   └── certification_extractor.py
│   ├── ml/
│   │   ├── ats_score.py
│   │   ├── job_matcher.py
│   │   ├── jd_matcher.py
│   │   ├── resume_ranker.py
│   │   └── missing_skill_detector.py
│   ├── ai/
│   │   ├── suggestion_engine.py
│   │   ├── resume_rewriter.py
│   │   ├── project_analyzer.py
│   │   └── career_advisor.py
│   ├── integrations/
│   │   ├── github_analyzer.py
│   │   └── linkedin_analyzer.py
│   ├── reports/
│   │   └── report_generator.py
│   ├── routes/
│   │   ├── upload_routes.py
│   │   ├── ats_routes.py
│   │   ├── job_routes.py
│   │   ├── github_routes.py
│   │   ├── linkedin_routes.py
│   │   └── report_routes.py
│   └── utils/
│       ├── constants.py
│       ├── helpers.py
│       └── validators.py
│
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── index.css
        ├── services/
        │   └── api.js
        ├── pages/
        │   ├── Home.jsx
        │   ├── ResumeUpload.jsx
        │   ├── Dashboard.jsx
        │   ├── JobMatcher.jsx
        │   ├── GithubAnalysis.jsx
        │   ├── LinkedinAnalysis.jsx
        │   └── Report.jsx
        ├── components/
        │   ├── Navbar.jsx
        │   ├── Footer.jsx
        │   ├── UploadCard.jsx
        │   ├── ATSCard.jsx
        │   ├── SkillsCard.jsx
        │   ├── MissingSkills.jsx
        │   ├── Suggestions.jsx
        │   ├── ResumeRank.jsx
        │   └── DownloadReport.jsx
        └── charts/
            ├── ATSRadarChart.jsx
            ├── SkillPieChart.jsx
            ├── MatchScoreChart.jsx
            ├── SectionAnalysisChart.jsx
            └── KeywordChart.jsx
```

---

## Setup & Installation

### 1. Configure Environment
Copy `.env.example` as `.env` and then Edit `.env` folder:
```
GEMINI_API_KEY=your-gemini-api-key
OPENAI_API_KEY=your-openai-api-key
GITHUB_TOKEN=your-github-personal-access-token
```

### 2. Backend Setup
```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate           # Windows
# source venv/bin/activate      # Mac

# Install dependencies
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm

# Run backend
cd backend
python app.py
# Backend runs at http://localhost:5000
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
# Frontend runs at http://localhost:5173
```

---

## API Endpoints

| Method | Endpoint                    | Description                        |
|--------|-----------------------------|------------------------------------|
| GET    | `/api/health`               | Health check                       |
| POST   | `/api/upload`               | Upload & analyze resume            |
| GET    | `/api/analyze/<file_id>`    | Re-analyze uploaded resume         |
| GET    | `/api/ats/<file_id>`        | Get ATS score                      |
| GET    | `/api/roles`                | List all target roles              |
| POST   | `/api/missing-skills`       | Detect missing skills for role     |
| POST   | `/api/jd-match`             | Match resume vs job description    |
| POST   | `/api/career-analysis`      | Full career readiness analysis     |
| POST   | `/api/career-readiness`     | Career readiness score only        |
| POST   | `/api/rewrite-bullets`      | AI rewrite bullet points (batch)   |
| POST   | `/api/rewrite-bullet`       | AI rewrite single bullet           |
| POST   | `/api/analyze-projects`     | Analyze project quality            |
| POST   | `/api/github`               | Analyze GitHub profile             |
| POST   | `/api/linkedin`             | Analyze LinkedIn profile           |
| POST   | `/api/report/generate`      | Generate PDF report                |
| GET    | `/api/report/download/<id>` | Download generated PDF             |

---

## Tech Stack

### Backend
- **Flask** — REST API
- **PyMuPDF + pdfplumber** — PDF parsing
- **python-docx** — DOCX parsing
- **spaCy + NLTK** — NLP processing
- **scikit-learn** — TF-IDF, cosine similarity
- **sentence-transformers** — semantic similarity
- **Gemini AI** — suggestions, rewriting, roadmap
- **ReportLab** — PDF report generation
- **pandas** — dataset management

### Frontend
- **React 18** — UI framework
- **Tailwind CSS** — styling
- **Recharts** — data visualization
- **Framer Motion** — animations
- **React Dropzone** — file upload
- **Vite** — build tool

---

## Features

1. **Resume Upload** — PDF & DOCX support
2. **Smart Parsing** — extracts name, email, phone, skills, education, experience, projects, certifications
3. **ATS Score (0-100)** — weighted across 6 dimensions
4. **Missing Skills Detection** — gap analysis for 200+ roles
5. **JD Matcher** — TF-IDF + semantic similarity
6. **AI Suggestions** — Gemini-powered improvement tips
7. **Resume Rewriter** — transforms weak bullets into impactful ones
8. **Project Analyzer** — quality scoring with feedback
9. **Career Readiness Score** — composite score across 5 dimensions
10. **Career Gap Analysis** — identifies what's missing
11. **Learning Roadmap** — step-by-step personalized path
12. **GitHub Analyzer** — profile strength scoring
13. **LinkedIn Analyzer** — completeness audit
14. **PDF Report** — full career report with charts
