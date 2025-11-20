from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    extracted_skills = db.Column(db.JSON)
    analyses = db.relationship('Analysis', backref='resume', lazy=True)

class JobDescription(db.Model):
    __tablename__ = 'job_descriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    required_skills = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    analyses = db.relationship('Analysis', backref='job_description', lazy=True)

class Analysis(db.Model):
    __tablename__ = 'analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    job_description_id = db.Column(db.Integer, db.ForeignKey('job_descriptions.id'), nullable=False)
    match_score = db.Column(db.Float, nullable=False)
    skill_matches = db.Column(db.JSON)
    missing_skills = db.Column(db.JSON)
    analysis_date = db.Column(db.DateTime, default=datetime.utcnow) 