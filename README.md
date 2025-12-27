# AI‑Powered Resume Scanner

An AI-driven resume screening tool that uses Natural Language Processing (NLP) to parse, analyze, and match resumes against job descriptions. This helps recruiters and job seekers understand compatibility, missing keywords, and strengths.

Features

- Extracts text from resumes (`.pdf`, `.docx`, `.txt`)  
- Parses job descriptions  
- Computes semantic similarity between resume and job description using transformer‑based embeddings  
- Identifies missing or underrepresented skills / keywords in the resume  
- Generates a matching score / report  
- (Optional) Provides a UI (Streamlit / Flask) for easy upload & analysis  

##Technologies & Libraries Used

- **Python**  
- **spaCy** or **NLTK** (for NLP preprocessing)  
- **Transformers** (Sentence-BERT or other embedding models)  
- **PyPDF2 / python-docx** (for resume text extraction)  
- **scikit-learn** (for similarity or scoring logic)  
- **Streamlit** or **Flask** (if you build a UI)  

##Project Structure (example)

```text
AI‑Powered‑Resume‑Scanner/
├── data/  
│   ├── sample_resumes/  
│   └── sample_job_descriptions/  
├── notebooks/  
│   └── analysis.ipynb  
├── src/  
│   ├── resume_parser.py  
│   ├── job_parser.py  
│   ├── similarity.py  
│   └── report_generator.py  
├── app.py (if using Streamlit / Flask)  
├── requirements.txt  
└── README.md  
