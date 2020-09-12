from flask import Flask, request, render_template
from storage_functions import upload_blob

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/upload', methods = ['POST'])
def upload():
    if request.method == 'POST':
        file = "GET FILE HERE"
        #upload_blob(file)
    



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)