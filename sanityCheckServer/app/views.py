import os
from app import app
from flask import render_template, request, redirect, url_for, flash
from .forms import LoginForm
from werkzeug.utils import secure_filename

import imageManager

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Bla'}  # fake user
    return render_template('index.html',
                           title='Home',
                           user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html',
                           title='Sign In',
                           form=form)


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
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
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            fullPath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(fullPath)

            if imageManager.hasShaderError(fullPath):
                print "Potential shader error on: " + fullPath


            print "Uploaded: " + filename

            #return redirect(url_for('uploaded_file',
            #                      filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''



@app.route('/images')
def showImages():

    im = imageManager.ImageManager(app.config['UPLOAD_FOLDER'])
    data = im.getRenderData(10, "TestScene1")
    print data
    return render_template('images.html',
                           data=data)