from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy

nlp = spacy.load('en_core_web_sm')

def preprocess_text(text):
    doc = nlp(text.lower())
    tokens = [token.text for token in doc if not token.is_stop and not token.is_punct and token.is_alpha]
    return ' '.join(tokens)

def rank_resumes(job_description, resumes):
    # Preprocess job description and resumes
    processed_jd = preprocess_text(job_description)
    processed_resumes = [preprocess_text(resume) for resume in resumes]
    
    # Create TF-IDF vectors
    vectorizer = TfidfVectorizer()
    all_documents = [processed_jd] + processed_resumes
    tfidf_matrix = vectorizer.fit_transform(all_documents)
    
    # Calculate similarity scores
    jd_vector = tfidf_matrix[0:1]
    resume_vectors = tfidf_matrix[1:]
    similarity_scores = cosine_similarity(jd_vector, resume_vectors)[0]
    
    return similarity_scores.tolist()