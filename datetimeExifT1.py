from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
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

# FIRST EXIF FUNCTION 
# def get_exif_data(filename):
#     ret = {}
#     i = Image.open(filename)  #--> filename must be a string of the file path
#     info = i._getexif()
#     # if info returns none = cannot access metadata with this method
#     # so check that info exists
    
#     for tag, value in info.items():
#         decoded = TAGS.get(tag, tag)
#         ret[decoded] = value
#     print ret




def get_exif_data(image):
    """Returns a dictionary from the exif data of a PIL Image item. Also converts the GPS Tags"""
    print "get_exif_data function"
    exif_data = {}
    print exif_data
    info = image._getexif()
    print "info"
    print info
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]
 
                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value
 
    return exif_data
 
def _get_if_exist(data, key):
    print "get if exist function"
    if key in data:
        print data[key]
        
    return None
    

 

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # return render_template("upload.html")
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print file_path
            file.save(file_path)
            

            image = Image.open(file_path)
            exif_data = get_exif_data(image)
            print exif_data


            # get_exif_data(file_path)
            print filename,file_path
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    
    return"""<!doctype html>
    <title>Upload</title>
    <h1>Upload a File</h1>
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
    # image = Image.open("file_path") # load an image through PIL's Image object
    # exif_data = get_exif_data(image)
    # print get_lat_lon(exif_data)
    