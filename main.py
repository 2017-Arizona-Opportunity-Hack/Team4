from flask import Flask, render_template, request, redirect, url_for
import json, os, time

with open("NCMEC.cfg") as cfg:
    config = json.load(cfg)
    API_KEY = config['GOOGLE_API_KEY']

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
@app.route('/')
def render_static():
    return render_template('index.html', key=API_KEY)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/opencsv/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(int(time.time())) + '.csv'))
            return redirect(url_for('index'))
    return render_template('ref.html')

@app.route('/requests/', methods=['GET', 'POST'])
def requestData():
    result = request.form
    for key, value in result.iteritems():
        print key
        print value
    if request.form:
        return 'That Looks Like Data to Me Boyo'
    else:
        return 'WOO'

if __name__ == '__main__':
    app.run()