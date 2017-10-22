from flask import Flask, render_template, request, redirect, url_for
import json, os, time

import load_and_filter

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
    result = json.loads(request.data);
    print result
    easy = dict();
    if 'location' in result:
        if result['location'] != "":
            easy['location'] = result['location']
            easy['location_range'] = result['loc_range']
    if 'gender' in result:
        easy['gender'] = result['gender']
    if 'state' in result:
        if result['state'] != "ANY":
            easy['state'] = result['state']
    if 'age_max' in result:
        easy['age_max'] = int(result['age_max'])
    if 'age_min' in result:
        easy['age_min'] = int(result['age_min'])
    if 'methods' in result:
        if 'AN' in result['methods']:
            easy['animal'] = True;
        if 'CA' in result['methods']:
            easy['candy'] = True;
        if 'MO' in result['methods']:
            easy['money'] = True;
        if 'RD' in result['methods']:
            easy['ride'] = True;
        if 'OT' in result['methods']:
            easy['other'] = True;
    if 'date_max' in result:
        easy['date_max'] = result['date_max']
    if 'date_min' in result:
        easy['date_min'] = result['date_min']
    
    print load_and_filter.load_filtered_data(easy)

    if request.form:
        return 'That Looks Like Data to Me Boyo'
    else:
        return 'WOO'

if __name__ == '__main__':
    app.run()