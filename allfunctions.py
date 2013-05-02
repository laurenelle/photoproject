
from datetime import datetime, timedelta
import re
from PIL.ExifTags import TAGS, GPSTAGS


UPLOAD_PHOTO_FOLDER = '/Users/lauren/Desktop/PHOTOS'
ALLOWED_EXTENSIONS = set(['PNG', 'png', 'jpg', 'JPG', 'jpeg','JPEG', 'gif', 'GIF'])
UPLOAD_CAPTION_FOLDER = '/Users/lauren/Desktop/PHOTOS/CAPTIONS'

# for voting logic
from datetime import datetime, timedelta
from math import log


import os, sys
from PIL import Image

def create_thumbnail(filename, photo_file_path, thumbnail_file_path):

    size = 100, 100

    if filename != thumbnail_file_path:

        try:
            im = Image.open(photo_file_path)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(thumbnail_file_path, "JPEG")

        except IOError:

            print "cannot create thumbnail for '%s'" % filename


def allowed_file(filename):

    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



def get_exif_data(image):
    """Returns a dictionary from the exif data of a PIL Image item. Also converts the GPS Tags"""
    # there may be a less nested way to do this function. Since you don't have an else after your
    # first if, you probably don't need it; you can use an exception there to return early.
    # try for tag...
    # except SomeError:
    # return some_data

    exif_data = {}
    info = image._getexif()

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

# is there a particular reason you're starting these variable names with _?
# usually reserved and may not be imported when the file is imported

def _get_if_exist(data, key):
    # you can just do return data[key] and return a default value if the key
    # doesn't exist (ie default to None). No need for a conditional here.
    if key in data:
        return data[key]
    return None

def _convert_to_degress(value):

    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    # it would be easier to understand what this code does at a glance
    # if the variables are named differently. Suggest naming value to what
    # it is (ie gps_value) and rename dn, mn, and sn.
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

    lat = None
    lon = None

    if "GPSInfo" in exif_data:

        gps_info = exif_data["GPSInfo"]

        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)

            if gps_latitude_ref != "N":
                lat = 0 - lat

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

    return lat, lon

def latlong(latlon):

    l = str(latlon)

# since you have variables named lat and long, name these something more
# descriptive - exp check_lat and check_lon since it looks like you're
# verifying the data format.
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

def get_time(exif_data):

    if "DateTime" in exif_data:
        photo_timestamp = exif_data['DateTime']
        return photo_timestamp

    else:
        # should be a return here - calling this function and expecting
        # a return may produce an error
        print "No timestamp available."
#__________________________________________________

def lat2(l2):

    match = re.search(r"[^A-Z], .* .(.*),(.*)\d.*", l2)
    if match:
        latitude = match.group(1)
        return latitude

def lon2(l2):
    match = re.search(r"[^A-Z], .* .(.*),(.*)\d.*", l2)
    if match:
        longitude = match.group(2)
        return longitude

#____________________________________________________
#original voting logic

epoch = datetime(1970, 1, 1)

def epoch_seconds(timestamp):
    """Returns the number of seconds from the epoch to date."""
    td = date - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

def score(upvote, downvote):
    return upvote - downvote

def hot(upvote, downvote, timestamp):
    """The hot formula. Should match the equivalent function in postgres."""
    s = score(ups, downs)
    order = log(max(abs(s), 1), 10)
    sign = 1 if s > 0 else -1 if s < 0 else 0
    seconds = epoch_seconds(date) - 1134028003
    return round(order + sign * seconds / 45000, 7)

