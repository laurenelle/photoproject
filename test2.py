from PIL import Image
from PIL.ExifTags import TAGS
import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug import secure_filename

UPLOAD_FOLDER = '/Users/lauren/Desktop/PHOTOS'
ALLOWED_EXTENSIONS = set(['PNG', 'png', 'jpg', 'JPG', 'jpeg','JPEG', 'gif', 'GIF'])
#allowed extensions are case sensitive and many other things are as well

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home_page():
    return render_template("home.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_exif(filename):
    ret = {}
    i = Image.open(filename)
    info = i._getexif()
    # if info returns none = cannot access metadata with this method
    # so check that info exists
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
        print ret

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # return render_template("upload.html")
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            get_exif(file_path)
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    
    return"""<!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
   
        <p></p>
             <input type="text" name="caption"></input>
                <input type="submit"></p>
    </form>"""



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run(debug=True)