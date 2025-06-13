from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'myfirstproject'  # Local use only

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

SECTIONS = ['Store', 'Material', 'Employee']

def get_files(section):
    folder = os.path.join(DATA_DIR, section)
    if not os.path.exists(folder):
        os.makedirs(folder)
    files = []
    for filename in os.listdir(folder):
        if filename.endswith('.pdf'):
            filepath = os.path.join(folder, filename)
            upload_time = datetime.fromtimestamp(os.path.getctime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
            files.append({'name': filename, 'path': filepath, 'time': upload_time})
    return files

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_section = request.form.get('section', 'Store')
    search_query = request.form.get('search', '').lower()
    files = get_files(selected_section)
    if search_query:
        files = [f for f in files if search_query in f['name'].lower() or search_query in f['time']]
    return render_template('index1.html', sections=SECTIONS, files=files, selected=selected_section)

@app.route('/upload', methods=['POST'])
def upload_file():
    section = request.form['section']
    file = request.files['file']
    if file and file.filename.endswith('.pdf'):
        save_path = os.path.join(DATA_DIR, section, file.filename)
        file.save(save_path)
        flash('File uploaded successfully!', 'success')
    else:
        flash('Only PDF files allowed!', 'danger')
    return redirect(url_for('index'))

@app.route('/view/<section>/<filename>')
def view_file(section, filename):
    return send_from_directory(os.path.join(DATA_DIR, section), filename)

@app.route('/delete', methods=['POST'])
def delete_files():
    section = request.form['section']
    files_to_delete = request.form.getlist('delete_files')
    for filename in files_to_delete:
        file_path = os.path.join(DATA_DIR, section, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    flash('File(s) deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
