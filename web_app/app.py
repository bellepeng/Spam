from flask import Flask, make_response, request, abort, jsonify, render_template
from api import make_soft_prediction
from api import make_hard_prediction, open_email

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html', email_text=None)

@app.route('/spam_score', methods=['POST'])
def spam_or_ham():
    if not request.json or ('email' not in request.json):
        abort(400)

    email = request.json['email']
    prediction = make_hard_prediction(email)
    score = make_soft_prediction(email)

    response = {
        'email': email,
        'prediction': prediction,
        'score': score
    }

    return jsonify(response), 201

# Below is for uploading the files
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Users/bellepeng/Desktop/Metis/Work/Projects/P3_Spam/web_app/uploads/'
ALLOWED_EXTENSIONS = set(['eml'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(file):
    return '.' in file and \
           file.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'upload_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['upload_file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return redirect(url_for('post_file_upload',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def post_file_upload(filename):
    email_contents = open_email(filename)
    return render_template('index.html', email_text = email_contents)


if __name__ == '__main__':
    app.run(debug=True)
