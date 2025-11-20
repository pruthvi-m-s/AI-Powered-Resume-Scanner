from flask import Flask, render_template, request, jsonify, send_from_directory
from resume_parser import parse_resume, extract_skills
from nlp_processor import rank_resumes
from models import db, Resume, JobDescription, Analysis
from config import Config
from werkzeug.utils import secure_filename
import os

# Flask app config
app = Flask(__name__, static_folder='statics')
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

# Initialize database
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

# Allow only PDF uploads
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Serve static files like CSS/JS
@app.route('/statics/<path:path>')
def send_static(path):
    return send_from_directory('statics', path)

# Upload and analyze resume
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['resume']
    job_desc = request.form.get('job_description', '')

    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": "Invalid or missing file. Only PDF allowed."}), 400

    # Save uploaded file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Parse resume and extract skills
    resume_data = parse_resume(file_path)
    resume_skills = resume_data.get('skills', [])
    required_skills = extract_skills(job_desc)

    # Compare skills
    matched_skills = list(set(resume_skills) & set(required_skills))
    missing_skills = list(set(required_skills) - set(resume_skills))
    match_score = round((len(matched_skills) / len(required_skills)) * 100, 2) if required_skills else 0

    # Save to database
    with app.app_context():
        resume = Resume(
            filename=filename,
            content=resume_data['text'],
            extracted_skills=resume_skills
        )
        db.session.add(resume)

        job = JobDescription(
            title="Job Position",  # Optional: replace with actual title field
            description=job_desc,
            required_skills=required_skills
        )
        db.session.add(job)

        analysis = Analysis(
            resume=resume,
            job_description=job,
            match_score=match_score / 100.0,
            skill_matches=matched_skills,
            missing_skills=missing_skills
        )
        db.session.add(analysis)
        db.session.commit()

    # Return JSON response
    return jsonify({
        "score": match_score,
        "skills": resume_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    })

# View analysis history
@app.route('/history', methods=['GET'])
def get_history():
    analyses = Analysis.query.order_by(Analysis.analysis_date.desc()).limit(10).all()
    history = []
    for analysis in analyses:
        history.append({
            'resume_name': analysis.resume.filename,
            'match_score': round(analysis.match_score * 100, 2),
            'analysis_date': analysis.analysis_date.strftime('%Y-%m-%d %H:%M:%S'),
            'skills_matched': analysis.skill_matches
        })
    return jsonify(history)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    print("Upload route called")  # This tells us the route was reached

    if 'resume' not in request.files:
        print("No resume file in request.files")
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['resume']
    print(f"Received file: {file.filename}")

    if file.filename == '':
        print("Filename is empty")
        return jsonify({"error": "No selected file"}), 400

    # Save the file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    print(f"Saving file to: {file_path}")

    try:
        file.save(file_path)
    except Exception as e:
        print(f"Error saving file: {e}")
        return jsonify({"error": "Could not save file"}), 500

    # If everything worked, respond success
    return jsonify({"message": "File uploaded successfully"})