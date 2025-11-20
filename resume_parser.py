import pdfplumber
import spacy
from pathlib import Path

nlp = spacy.load('en_core_web_sm')

# Common technical skills and keywords
SKILL_PATTERNS = [
    'python', 'java', 'javascript', 'html', 'css', 'sql', 'react', 'angular', 'vue',
    'node.js', 'express', 'django', 'flask', 'spring', 'docker', 'kubernetes',
    'aws', 'azure', 'gcp', 'machine learning', 'data science', 'ai', 'devops',
    'ci/cd', 'git', 'agile', 'scrum', 'rest api', 'graphql', 'microservices'
]

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_skills(text):
    doc = nlp(text.lower())
    skills = set()
    
    # Extract skills based on patterns
    for skill in SKILL_PATTERNS:
        if skill in text.lower():
            skills.add(skill)
    
    # Extract potential skills based on noun phrases
    for chunk in doc.noun_chunks:
        if chunk.text.lower() in SKILL_PATTERNS:
            skills.add(chunk.text.lower())
    
    return list(skills)

def parse_resume(file_path):
    if not Path(file_path).exists():
        raise FileNotFoundError(f"Resume file not found: {file_path}")
    
    text = extract_text_from_pdf(file_path)
    skills = extract_skills(text)
    
    return {
        'text': text,
        'skills': skills
    }