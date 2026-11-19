# AI Resume & Job Matcher 📄

### An NLP-Powered Resume Screening and Job Compatibility Analysis System

AI Resume & Job Matcher is an intelligent resume analysis tool that evaluates how well a candidate's resume aligns with a given job description.

Built using **Python, NLP, and Sentence Transformers**, the system extracts relevant information from PDF resumes, identifies technical skills, and calculates a compatibility score using semantic similarity.

Rather than relying entirely on exact keyword matches, it uses transformer-based sentence embeddings to understand contextual similarities between resume content and job requirements.

## 🚀 Key Features

- **PDF Resume Parsing:** Extracts text and relevant information from uploaded PDF resumes.
- **Semantic Similarity Matching:** Uses Sentence Transformers to compare resumes with job descriptions based on contextual meaning.
- **Resume Compatibility Score:** Generates an overall similarity percentage to indicate how closely a resume matches a job description.
- **Skill Extraction:** Identifies technical skills from resumes and job descriptions.
- **Skill Gap Analysis:** Highlights matching and missing skills to help candidates identify areas for improvement.
- **Section-Based Analysis:** Identifies and analyzes important resume sections, including Skills, Experience, Projects, and Education.
- **Skill Normalization:** Handles variations in technical terminology, such as mapping PostgreSQL to SQL and PyTorch/TensorFlow to Deep Learning.

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| NLP & Embeddings | Sentence Transformers |
| Pre-trained Model | all-MiniLM-L6-v2 |
| Deep Learning Framework | PyTorch |
| Similarity Calculation | Cosine Similarity |
| PDF Processing | PyPDF |
| Text Processing | Regex |
| Frontend | Streamlit |

## 🧠 How It Works

The application follows a structured resume-matching pipeline.

### 1. Resume Upload & Text Extraction
- Accepts resumes in PDF format.
- Extracts text using PyPDF.
- Prepares extracted content for further processing.

### 2. Text Processing & Section Detection
- Processes resume and job description text.
- Identifies important sections such as Skills, Experience, Projects, and Education.
- Normalizes technical skill variations for more consistent matching.

### 3. Semantic Embedding Generation
- Uses the `all-MiniLM-L6-v2` Sentence Transformer model.
- Converts resume content and job descriptions into dense vector embeddings.
- Captures contextual relationships beyond exact keyword overlap.

### 4. Similarity Calculation
- Computes cosine similarity between the generated embeddings.
- Produces an overall resume-to-job compatibility score.

### 5. Skill Gap Analysis
- Extracts skills from both the resume and job description.
- Identifies matching skills.
- Highlights missing skills that may be relevant to the target role.

## 🏗️ System Architecture

```text
             PDF Resume
                  |
                  v
             PyPDF Parser
                  |
                  v
          Resume Text Extraction
                  |
                  |
Job Description --+
                  |
                  v
          Text Preprocessing
                  |
                  v
           Section Detection
                  |
                  v
         Skill Extraction &
          Normalization
                  |
                  v
       Sentence Transformer
          (all-MiniLM-L6-v2)
                  |
                  v
         Embedding Generation
                  |
                  v
          Cosine Similarity
                  |
          +-------+-------+
          |               |
          v               v
     Match Score      Skill Gap Analysis
          |               |
          +-------+-------+
                  |
                  v
          Streamlit Results
```

## 📊 Sample Evaluation

The following represents a sample matching run during development.

| Evaluation Component | Similarity |
|---|---:|
| Overall Similarity | 66.13% |
| Skills | 58.75% |
| Experience | 63.86% |
| Projects | 40.16% |
| Education | 48.43% |

These values represent an individual test result, not a benchmark across a large evaluation dataset.

## 📂 Project Structure

```text
AI-Resume-Job-Matcher/
│
├── app.py
├── matcher.py
├── skills.py
├── sections.py
├── pdf_reader.py
│
├── data/
│   └── skills.json
│
├── requirements.txt
├── .env.example
└── README.md
```

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd AI-Resume-Job-Matcher
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows**
```bash
venv\Scripts\activate
```

**macOS / Linux**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🔬 Technical Highlights

- Transformer-based semantic matching instead of relying exclusively on keyword overlap.
- Contextual text representations using Sentence Transformers.
- Cosine similarity for measuring resume-job compatibility.
- Rule-based skill extraction and normalization.
- Section-aware resume analysis.
- Modular implementation separating PDF extraction, skill processing, and matching logic.

## 🔮 Future Enhancements

- LLM-powered resume improvement suggestions using Groq.
- Personalized recommendations for missing skills.
- Resume rewriting suggestions tailored to specific job descriptions.
- Support for multiple resume formats.
- Batch resume screening for recruiters.
- Deployment with secure API-key management.

## 🎯 Project Objective

The goal of this project is to make resume screening more intelligent and accessible by combining semantic NLP techniques with structured skill analysis.

It demonstrates the practical application of **Sentence Transformers, semantic similarity, NLP-based information extraction, and text processing** to solve a real-world recruitment problem.

---

**Built with Python, Sentence Transformers, PyTorch, NLP, and Streamlit.**
