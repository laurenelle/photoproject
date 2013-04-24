import model
import csv
from datetime import date, datetime
import time

def load_users(session):






import model

db = model.connect_db()
user_id = model.new_user(db, "chriszf@gmail.com", "securepassword", "Christian")
