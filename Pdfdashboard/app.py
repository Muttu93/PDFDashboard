from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.endswith('.pdf'):
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            upload_time = datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S')
            files.append({'name': filename, 'upload_time': upload_time})
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete', methods=['POST'])
def delete_files():
    files_to_delete = request.form.getlist('files')
    for file_name in files_to_delete:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search_files():
    query = request.args.get('query', '').lower()
    matched_files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.endswith('.pdf') and query in filename.lower():
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            upload_time = datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S')
            matched_files.append({'name': filename, 'upload_time': upload_time})
    return jsonify(matched_files)

if __name__ == '__main__':
    app.run(debug=True)
