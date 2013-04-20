from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, flash, session, request, g
from werkzeug import secure_filename
from model import session as db_session, User, Photo, Vote, Tag, Photo_Tag, Location
import model
import re
import time

from allfunctions import *

# for voting logic
from datetime import datetime, timedelta
from math import log



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

@app.before_request
def load_user_id():
    g.user_id = session.get('user_id')

@app.teardown_request
def shutdown_session(exception = None):
    db_session.remove()



#_____________________________________________________

#currently only gets the user id, consider getting email, username etc later

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

    session['user_id'] = user.id
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
            
            p = Photo(file_location=photo_file_path, caption=caption, latitude=latitude, longitude=longitude, timestamp=timestamp, user_id=g.user_id)
            # add location stuff and connect to location table LATER
            l = Location()
            u = User()       


            db_session.add(p)
            db_session.commit()
            db_session.refresh(p)
            #u is not defined
            # session['user_id'] = u.id 


            g.user_id = session.get('user_id')
            user = db_session.query(User).filter_by(id=g.user_id).one()


            
            # create a template that shows the view of a uploaded photo and then the user's other photos
            return redirect(url_for('uploaded_file',filename=filename))      
    
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
    