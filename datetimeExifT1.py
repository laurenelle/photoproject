from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import time, datetime, pprint

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

# def get_exif(filename):
#     ret = {}
#     i = Image.open(filename)
#     info = i._getexif()
#     # if info returns none = cannot access metadata with this method
#     # so check that info exists
    
#     for tag, value in info.items():
#         decoded = TAGS.get(tag, tag)
#         ret[decoded] = value
#     print ret

def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    print "get_exif_data function"
    exif_data = {}
    print exif_data
    info = image._getexif()
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
        return data[key]
        
    return None
    
def _convert_to_degress(value):
    print "convert to degrees function"
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)
 
    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)
 
    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)
 
    return d + (m / 60.0) + (s / 3600.0)
 
def get_lat_lon(exif_data):
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    print "get_lat_lon function"
    lat = None
    lon = None
 
    if "GPSInfo" in exif_data:  
        print "GPSInfo If"    
        gps_info = exif_data["GPSInfo"]
 
        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')
 
        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            print "gps_latitude if"
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":                     
                lat = 0 - lat
 
            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon
 
    return lat, lon

# def get_date_time(exif_data):
#     """WIP: return datetime if available, from the provided exif_data (obtained through get_exif_data)"""
#     print "get_date_time"
#     datetime = None

#     if "Datetime" in exif_data:
#         print "Dateime IF"

#     else: print "Datetime Unavailable"


def get_time(exif_data):
    print "get_time function"
    if "DateTime" in exif_data:
        photo_timestamp = exif_data['DateTime']
        print photo_timestamp
    else:
        print "No timestamp available."


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
            print get_lat_lon(exif_data)
            print get_time(exif_data)

            # get_exif_data(file_path)
            print filename,file_path
            return redirect(url_for('uploaded_file',
                                    filename=filename))
            print "hello"
            
    
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
    