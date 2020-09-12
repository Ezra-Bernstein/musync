from flask import Flask, request, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from storage_functions import upload_blob
from datastore_functions import *
import os
from dotenv import load_dotenv

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

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        addUser(username, password)
        session['username']


@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/upload', methods = ['POST', 'GET'])
def upload():
    if request.method == 'POST':
        print(request.files)
        if 'file' not in request.files:
            return "NO FILE"
        file = request.files['file']
        file.save('/tmp/username_instrument.mp3')
        upload_blob(STORAGE_BUCKET_NAME, "/tmp/username_instrument.mp3", "myclasscode/username_instrument.mp3")
        os.remove('/tmp/username_instrument.mp3')
        return("AWESOME!!")
    if request.method == 'GET':
        return render_template('login.html')
    


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='0.0.0.0', port=8080, debug=True)