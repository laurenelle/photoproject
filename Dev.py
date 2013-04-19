from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, flash, session, request, g
from werkzeug import secure_filename
from model import session as db_session, User, Photo, Vote, Tag, Photo_Tag, Location
import model
import re
import time

# for voting logic
from datetime import datetime, timedelta
from math import log

# home of tested functions
import allfunctions


#from flask_heroku import Heroku

UPLOAD_PHOTO_FOLDER = '/Users/lauren/Desktop/PHOTOS'
ALLOWED_EXTENSIONS = set(['PNG', 'png', 'jpg', 'JPG', 'jpeg','JPEG', 'gif', 'GIF'])
#allowed extensions are case sensitive and many other things are as well
UPLOAD_CAPTION_FOLDER = '/Users/lauren/Desktop/PHOTOS/CAPTIONS'

app = Flask(__name__)
app.secret_key = 'balloonicorn' # temp
app.config['UPLOAD_PHOTO_FOLDER'] = UPLOAD_PHOTO_FOLDER
app.config.from_object(__name__) #???

#______________________________________________________
#OK
@app.teardown_request
def shutdown_session(exception = None):
    db_session.remove()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def get_exif_data(image):
    """Returns a dictionary from the exif data of a PIL Image item. Also converts the GPS Tags"""
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



def get_time(exif_data):
    print "get_time function"
    if "DateTime" in exif_data:
        photo_timestamp = exif_data['DateTime']
        return photo_timestamp
    else:
        print "No timestamp available."

# @app.route('/upload', methods=['GET'])
# def test():
#     render_template("test.html")


def latlong(latlon):
    l = str(latlon)    


def lat(l):
    match = re.search(r"[^)](.*),(.*)\d", l)
    if match:
        latitude = match.group(1)
        return latitude


def lon(l):
    match = re.search(r"[^)](.*),(.*)\d", l)
    if match:
        longitude = match.group(2)
        return longitude   

#____________________________________________________
#voting logic

epoch = datetime(1970, 1, 1)

def epoch_seconds(date):
    """Returns the number of seconds from the epoch to date."""
    td = date - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

def score(ups, downs):
    return ups - downs

def hot(ups, downs, date):
    """The hot formula. Should match the equivalent function in postgres."""
    s = score(ups, downs)
    order = log(max(abs(s), 1), 10)
    sign = 1 if s > 0 else -1 if s < 0 else 0
    seconds = epoch_seconds(date) - 1134028003
    return round(order + sign * seconds / 45000, 7)

#_____________________________________________________

#OK
@app.before_request
def load_user_id():
    g.user_id = session.get('user_id')

#ALTER LATER
@app.route('/')
def home_page():
    # if g.user_id:
    #     return redirect(url_for("user_page"))
    return render_template("index.html")

#OK
@app.route("/login", methods=["POST"])
def login():
    email = request.form['email']
    password = request.form['password']
    
    try:
        user = db_session.query(User).filter_by(email=email, password=password).one()
        print "THIS IS THE USER", user.email

    except:
        flash("Invalid email or password", "error")
        return redirect(url_for("index"))
    print "before session" 
    # breaks here
    print user.id
    session['user_id'] = user.id
    print "THIS IS THE SESSION", session
    print "after session"
    return redirect(url_for("user_page"))

#OK
@app.route("/signup", methods=['POST'])
def register():
    email = request.form['email']
    # user_name = request.form['user_name']
    password = request.form['password']
    existing = db_session.query(User).filter_by(email=email).first()
    if existing:
        flash("Email already in use", "error")
        return redirect(url_for("index"))
    # defines u
    u = User(email=email, password=password)
    print u
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    session['user_id'] = u.id 
    return redirect(url_for("user_page"))

#OK
@app.route("/logout")
def logout():
    del session['user_id']
    return redirect(url_for("index"))




@app.route('/vote', methods=['POST', 'GET'])
def vote():
    # if up:

    # elif down:


    # db_session.add(some_variable)
    # db_session.commit()
    # db_session.refresh(some_variable)
    return render_template("vote.html")



    # up = Column(Integer, nullable = True)
    # down = Column(Integer, nullable = True)
    # photo_id = Column(Integer, ForeignKey('photos.id'))
    # give_vote_user_id = Column(Integer, ForeignKey('users.id'))
    # receive_vote_user_id = Column(Integer, ForeignKey('users.id'))
    # timestamp = Column(TIMESTAMP, default=sql.text('CURRENT_TIMESTAMP'))

# TAGS --> implement later
# @app.route("/search", methods=["POST"])
# def search():
#     query = request.form['query']
#     movies = db_session.query(Tag).\
#             filter(Tag.tag_title.ilike("%" + query + "%")).\
#             limit(20).all()






@app.route("/userpage")
def user_page():
    g.user_id = session.get('user_id')
    user = db_session.query(User).filter_by(id=g.user_id).one()

    return render_template("userpage.html", u=user)


@app.route("/logout")
def logout():
    del session['user_id']
    return redirect(url_for("home_page"))


# ----------------------------------------------------------------------------------------
#





@app.route('/upload', methods=['GET', 'POST'])
# this function corresponds to the jinja {{url_for("uploadfile")}} ACTION in upload.html
def uploadfile():
    # return render_template("upload.html")
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            photo_file_path = os.path.join(app.config['UPLOAD_PHOTO_FOLDER'], filename)
            
            file.save(photo_file_path)
            
            image = Image.open(photo_file_path)
            exif_data = get_exif_data(image)
            latlon = get_lat_lon(exif_data)
            
            print latlon

            l = str(latlon)
            latitude = lat(l)
            longitude = lon(l)

            timestamp = get_time(exif_data)
            print timestamp

            if timestamp != None:
                timestamp = datetime.strptime(str(timestamp), "%Y:%m:%d %H:%M:%S")

            caption = request.form['caption']

            p = Photo(file_location=photo_file_path, caption=caption, latitude=latitude, longitude=longitude, timestamp=timestamp)
            #u = User()
            # add location stuff and connect to location table
            l = Location()            


            db_session.add(p)
            db_session.commit()
            db_session.refresh(p)
            session['user_id'] = u.id 
            
            
            return redirect(url_for('uploaded_file',
                                    filename=filename))      
    
    return render_template("upload.html") 


@app.route('/uploads/<filename>')
def uploaded_file(filename):


    return send_from_directory(app.config['UPLOAD_PHOTO_FOLDER'],
                               filename)






# @app.route('/uploads/<filename>', methods=["GET"])
# def uploaded_file(filename):
#     photo = db_session.query(Photo).get(filename)
#     voting = photo.votes
#     photo_nums = []
#     user_rating = None
#     for v in votes:
#         if r.user_id == session['user_id']:
#             user_rating = r
#         rating_nums.append(r.rating)
#     return send_from_directory(app.config['UPLOAD_PHOTO_FOLDER'],
#                                filename)

#above modeled after:
# @app.route("/movie/<int:id>", methods=["GET"])
# def view_movie(id):
#     movie = db_session.query(Movie).get(id)
#     ratings = movie.ratings
#     rating_nums = []
#     user_rating = None
#     for r in ratings:
#         if r.user_id == session['user_id']:
#             user_rating = r
#         rating_nums.append(r.rating)
#     avg_rating = float(sum(rating_nums))/len(rating_nums)


#__________________________________________________________________________________________


if __name__ == '__main__':
    app.run(debug=True)

    # image = Image.open("file_path") # load an image through PIL's Image object
    # exif_data = get_exif_data(image)
    # print get_lat_lon(exif_data)
    