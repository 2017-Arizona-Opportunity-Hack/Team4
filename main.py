from flask import Flask, render_template
import json, os

with open("NCMEC.cfg") as cfg:
    config = json.load(cfg)
    API_KEY = config['GOOGLE_API_KEY']

app = Flask(__name__)
 
@app.route('/')
def render_static():
    return render_template('index.html', key=API_KEY)

@app.route('/opencsv', methods=['POST'])
def opencsv():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
 
if __name__ == '__main__':
    app.run()