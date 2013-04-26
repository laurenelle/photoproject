from PIL import Image

import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, flash, session, request, g
from werkzeug import secure_filename
from model import session as db_session, User, Photo, Vote, Tag, Photo_Tag, Location
import model
import re
import time

from sqlalchemy import select, func, types, sql, update

from allfunctions import *
# fix keys file
from K import *

from geopy import geocoders


#from flask_heroku import Heroku

UPLOAD_PHOTO_FOLDER = '/Users/lauren/Desktop/PHOTOS'
ALLOWED_EXTENSIONS = set(['PNG', 'png', 'jpg', 'JPG', 'jpeg','JPEG', 'gif', 'GIF'])

#allowed extensions are case sensitive and many other things are as well

app = Flask(__name__)
app.secret_key = 'balloonicorn'
app.config['UPLOAD_PHOTO_FOLDER'] = UPLOAD_PHOTO_FOLDER
app.config.from_object(__name__) #???



@app.before_request
def load_user_id():
    g.user_id = session.get('user_id')
    if g.user_id != None:
        g.user = db_session.query(User).filter_by(id=g.user_id)
        g.photos = db_session.query(Photo).filter_by(user_id=g.user_id).all()



@app.teardown_request
def shutdown_session(exception = None):
    db_session.remove()

@app.route('/')
def home_page():
    if g.user_id:
        return redirect(url_for("userpage"))
    return render_template("index.html")

# breaks when user doesn't exist or submits wrong password
@app.route("/login", methods=["POST"])
def login():
    email = request.form['email']
    password = request.form['password']
    
    try:
        u = db_session.query(User).filter_by(email=email, password=password).one()
        

    except:
        flash("Invalid email or password", "error")
        return redirect(url_for("index"))

    print "this is a u.id", u.id
    session['user_id'] = u.id
    print "session user_id is", session.get('user_id')
    return redirect(url_for("userpage"))


# breaks when user already exists
@app.route("/signup", methods=['POST'])
def register():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    existing = db_session.query(User).filter_by(email=email).first()
    if existing:
        flash("Email already in use", "error")
        return redirect(url_for("index"))
    u = User(email=email, password=password, user_name=username)
    print u
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    session['user_id'] = u.id 
    return redirect(url_for("userpage"))

@app.route("/popular", methods=['GET', 'POST'])
def popular():

    sql = "select v.photo_id, p.file_location, sum( 1 / ( (extract(epoch from now()) - extract(epoch from v.timestamp))/60/60/24 ) * value ) as POPULAR from votes v inner join photos p on p.id = v.photo_id group by v.photo_id, p.file_location;"
    photos = db_session.execute(sql)

    return render_template("popular.html", u=g.user, photos=photos)






@app.route("/map", methods=['GET', 'POST'])
def map():

    return render_template("map.html", u=g.user, photos=g.photos)



@app.route("/vote", methods=['GET', 'POST'])
def vote():

    allphotos=db_session.query(Photo).all()
    if request.form:
        vote = request.form['vote']
        print "VOTE"
        photoid = request.form['photoid']
        photoowner = request.form['photoowner']
        if vote == "upvote":
            v = Vote(value=1, give_vote_user_id=g.user_id, photo_id=photoid, receive_vote_user_id=photoowner)
            db_session.add(v)

            p = db_session.query(Photo).filter_by(id=1).one()
            p.up_vote = Photo.up_vote + 1
            db_session.add(p)
            db_session.commit()

            return redirect(url_for("vote"))

        elif vote == "downvote":
            print "downvote"
            v = Vote(value=-1, give_vote_user_id=g.user_id, photo_id=photoid, receive_vote_user_id=photoowner)
            db_session.add(v)

            p = db_session.query(Photo).filter_by(id=1).one()
            p.down_vote = Photo.down_vote + 1
            db_session.add(p)
            db_session.commit()

            return redirect(url_for("vote"))

    return render_template("vote.html", u=g.user, photos=allphotos)


@app.route("/userpage")
def userpage():
    if not g.user_id:
        flash("Please log in", "warning")
        return redirect(url_for("index"))

    return render_template("userpage.html", u=g.user, photos=g.photos)



@app.route("/logout")
def logout():
    del session['user_id']
    return render_template("logout.html")

@app.route('/upload', methods=['GET', 'POST'])
# this function corresponds to the jinja {{url_for("uploadfile")}} ACTION in upload.html
def uploadfile():

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            
            filename = secure_filename(file.filename)
            photo_location = "uploads/"+filename
            photo_file_path = os.path.join(app.config['UPLOAD_PHOTO_FOLDER'], filename)
            file.save(photo_file_path)
            
            thumbnail_file_path = os.path.splitext(photo_file_path)[0] + ".thumbnail"
            create_thumbnail(filename, photo_file_path, thumbnail_file_path)
            thumbnail_location = "uploads/"+ os.path.splitext(filename)[0] + ".thumbnail"
            
            image = Image.open(photo_file_path)
            exif_data = get_exif_data(image)
            latlon = get_lat_lon(exif_data)

            l = str(latlon)

            latitude = lat(l)
            longitude = lon(l)

            timestamp = get_time(exif_data)

            if timestamp != None:
                timestamp = datetime.strptime(str(timestamp), "%Y:%m:%d %H:%M:%S")

            caption = request.form['caption']
            city = request.form['city']

            if latitude == None:
                goo = geocoders.GoogleV3()
                geocodes = goo.geocode(city, exactly_one=False)
                l2 = str(geocodes)
                latitude = lat2(l2)
                longitude = lon2(l2)


            p = Photo(file_location=photo_location, caption=caption, latitude=latitude, longitude=longitude, timestamp=timestamp, user_id=g.user_id, thumbnail=thumbnail_location)

            db_session.add(p)
            db_session.commit()
            db_session.refresh(p)

            user = db_session.query(User).filter_by(id=g.user_id).one()


            
            # create a template that shows the view of an uploaded photo and then the user's other photos
            

            return redirect(url_for('uploaded_file',filename=filename))      
    
    return render_template("upload.html") 


@app.route('/uploads/<filename>')
def uploaded_file(filename):


    # create a template for this
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

    