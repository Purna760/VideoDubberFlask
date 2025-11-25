import os
import uuid
import json
from flask import Flask, render_template, request, jsonify, send_file, url_for
from werkzeug.utils import secure_filename
import threading
from video_processor import VideoProcessor

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov', 'mkv'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

jobs = {}

SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'hi': 'Hindi',
    'ta': 'Tamil',
    'ar': 'Arabic',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh-cn': 'Chinese (Simplified)',
    'pt': 'Portuguese',
    'it': 'Italian',
    'ru': 'Russian',
    'nl': 'Dutch',
    'tr': 'Turkish',
    'pl': 'Polish'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html', languages=SUPPORTED_LANGUAGES)

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    video = request.files['video']
    source_lang = request.form.get('source_language', 'en')
    target_lang = request.form.get('target_language', 'hi')
    
    if video.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(video.filename):
        return jsonify({'error': 'Invalid file format. Please upload MP4, AVI, MOV, or MKV'}), 400
    
    job_id = str(uuid.uuid4())
    filename = secure_filename(video.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{job_id}_{filename}")
    video.save(input_path)
    
    jobs[job_id] = {
        'status': 'queued',
        'progress': 0,
        'step': 'Initializing...',
        'input_file': input_path,
        'output_file': None,
        'source_language': source_lang,
        'target_language': target_lang,
        'error': None
    }
    
    thread = threading.Thread(target=process_video_async, args=(job_id, input_path, source_lang, target_lang))
    thread.daemon = True
    thread.start()
    
    return jsonify({'job_id': job_id})

def process_video_async(job_id, input_path, source_lang, target_lang):
    try:
        processor = VideoProcessor(job_id, jobs)
        output_path = processor.process(input_path, source_lang, target_lang)
        
        jobs[job_id]['status'] = 'completed'
        jobs[job_id]['progress'] = 100
        jobs[job_id]['step'] = 'Completed!'
        jobs[job_id]['output_file'] = output_path
        
    except Exception as e:
        jobs[job_id]['status'] = 'failed'
        jobs[job_id]['error'] = str(e)
        jobs[job_id]['step'] = f'Error: {str(e)}'

@app.route('/status/<job_id>')
def get_status(job_id):
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = jobs[job_id]
    return jsonify({
        'status': job['status'],
        'progress': job['progress'],
        'step': job['step'],
        'error': job.get('error'),
        'download_url': url_for('download_video', job_id=job_id) if job['status'] == 'completed' else None
    })

@app.route('/download/<job_id>')
def download_video(job_id):
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = jobs[job_id]
    if job['status'] != 'completed' or not job['output_file']:
        return jsonify({'error': 'Video not ready'}), 400
    
    return send_file(job['output_file'], as_attachment=True, download_name=f'dubbed_{job_id}.mp4')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
