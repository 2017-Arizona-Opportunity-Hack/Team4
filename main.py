from flask import Flask, render_template, request, redirect, url_for
import json, os, time

import load_and_filter, checkingFileType

global ATTEMPTS
global MISSING
global API_KEY

with open("NCMEC.cfg") as cfg:
    config = json.load(cfg)
    API_KEY = config['GOOGLE_API_KEY']
    MISSING = config['MISSING_CSV_FILE']
    ATTEMPTS = config['ATTEMPTS_CSV_FILE']
cfg.close()

UPLOAD_FOLDER = 'data/'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
@app.route('/')
def render_static():
    return render_template('index.html', key=API_KEY, mis=MISSING, att=ATTEMPTS)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/opencsv/', methods=['GET', 'POST'])
def index():
    global ATTEMPTS
    global MISSING
    global API_KEY
    if request.method == 'POST':
        file = request.files['file']
        tim = os.path.join(app.config['UPLOAD_FOLDER'], str(int(time.time())) + '_' + file.filename)
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(tim)
            x = checkingFileType.readFILE(tim)
            if x != -1:
                if request.form['type'] == 'A' and x == 0:
                    ATTEMPTS = tim
                elif request.form['type'] == 'M' and x == 1:
                    MISSING = tim
                config['MISSING_CSV_FILE'] = MISSING
                config['ATTEMPTS_CSV_FILE'] = ATTEMPTS
                config['GOOGLE_API_KEY'] = API_KEY
                with open("NCMEC.cfg", "w") as cfg:
                    json.dump(config, cfg)
                cfg.close()  
            return redirect(url_for('index'))
    return render_template('ref.html')

@app.route('/requests/', methods=['GET', 'POST'])
def requestData():
    global ATTEMPTS
    global MISSING
    result = json.loads(request.data);
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

    return json.dumps(load_and_filter.load_filtered_data(easy, ATTEMPTS, MISSING))

if __name__ == '__main__':
    app.run()
    config['MISSING_CSV_FILE'] = MISSING
    config['ATTEMPTS_CSV_FILE'] = ATTEMPTS
    with open("NCMEC.cfg", "w") as cfg:
        json.dump(config, cfg)
    cfg.close()
