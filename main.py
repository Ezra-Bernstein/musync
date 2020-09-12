from flask import Flask, request, render_template, redirect, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from storage_functions import upload_blob
from datastore_functions import *
import os
import subprocess
from dotenv import load_dotenv
from mp4merger import mp4merger

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
load_dotenv()
app.secret_key=os.environ.get("SECRET_KEY")

STORAGE_BUCKET_NAME = os.environ.get("STORAGE_BUCKET_NAME")



@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        print("LOGIN")
        if verifyLogin(username, password):
            session['username'] = username
            return render_template('classes.html')
        else:
            return "ERROR LOGGING IN"
    elif request.method == 'GET':
        return render_template('login.html')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        okName = addUser(username, password)
        if okName:
            session['username'] = username
            return render_template('classes.html')
        else:
            return "NO DOTS IN YOUR NAME"
    elif request.method == 'GET':
        return render_template('signup.html')

@app.route('/logout', methods=['POST'])
def logout():
    if request.method == 'POST':
        session.pop('username', None)
        return render_template('')

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/classes', methods = ['GET'])
def classes():
    if request.method == 'GET':
        session.pop('classcode')
        session.pop('instrument')
        return render_template('classes.html', classes = getClasses(session['username']))

@app.route('/upload', methods = ['POST', 'GET'])
def upload():
    if request.method == 'POST':
        print(request.files)
        if 'file' not in request.files:
            return "NO FILE"
        file = request.files['file']

        instrument = getInstrument(classcode, session['username'])

        file.save('/tmp/' + session['username'] + "_" + )
        # file.save('/tmp/username_instrument.mp3')
        # command = "ffmpeg -i " + "/tmp/username_instrument.mp3" + " " + "/tmp/out.wav"
        # subprocess.call(command, shell=True)
        # upload_blob(STORAGE_BUCKET_NAME, "/tmp/out.wav", "myclasscode/out.wav")
        # os.remove('/tmp/username_instrument.mp3')
        # os.remove('/tmp/out.wav')
        # return render_template('displayAudio.html')
    if request.method == 'GET':
        return render_template('login.html')
    

@app.route('/showClass', methods = ['POST'])
def showClass():
    if request.method == 'POST':
        session['classcode'] = request.args['classcode']
        session['instrument'] = getInstrument(session['classcode'], session['username'])
        return redirect(url_for('classPage', classcode = session['classcode']))

@app.route('/classPage')
def classPage():
    return render_template('class.html', classcode = session['classcode'], username = session['username'])


@app.route('/merge', methods=['POST'])
def merge():
    if request.method == 'POST':
        #pull from gcs into tmp

        

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='0.0.0.0', port=8080, debug=True)