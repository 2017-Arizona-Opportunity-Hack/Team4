from flask import Flask, render_template
import Tkinter, tkFileDialog


 
app = Flask(__name__)
 
@app.route('/')
def render_static():
    return render_template('index.html')

@app.route('/opencsv')
def opencsv():
    return render_template('ref.html')
 
if __name__ == '__main__':
    app.run()