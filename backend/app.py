from flask import Flask, request, send_from_directory, jsonify
import os
from werkzeug.utils import secure_filename

from video_processor import process_video
from anime_generator import generate_anime_style

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = './uploads'
PROCESSED_FOLDER = './processed'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_video():
    # Check if the post request has the file part
    if 'video' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(video_path)
        # Process video to extract frames
        frames = process_video(video_path)
        # Generate anime style frames
        anime_frames = generate_anime_style(frames)
        return jsonify({'message': 'File successfully uploaded and processed', 'frames': anime_frames}), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400

@app.route('/frames/<path:filename>')
def download_frame(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)
    app.run(debug=True)
