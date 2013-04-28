from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
# importing all data types for columns
from sqlalchemy import Column, Integer, String, DateTime, Date, Float

from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref, session
from sqlalchemy.orm import relationship, backref, relation
from sqlalchemy.dialects import postgresql
from sqlalchemy import select, func, types, sql, update
import datetime

import psycopg2
from wtforms import Form, BooleanField, TextField, PasswordField, validators




engine = create_engine("postgres://lauren:@localhost/eyetravelv1", echo=False)

#db = postgresql.open("postgres://localhost/eyetravelv1")
session = scoped_session(sessionmaker(bind=engine, autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here




class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key = True)
	user_name = Column(String(64), nullable=True)
	email = Column(String(64), nullable=True)
	password = Column(String(64), nullable=True)

	photos = relationship("Photo", backref="users", lazy="joined")
	# users are the parents of the photo children

#increment function for up and down vote based on when a vote is cast - write this function
class Photo(Base):
	__tablename__ = "photos"

	id = Column(Integer, primary_key = True)
	user_id = Column(Integer, ForeignKey('users.id'))
	file_location = Column(String(100), nullable=True) 
	latitude = Column(Float, nullable=True) 
	longitude = Column(Float, nullable=True) 
	photo_location_id = Column(Integer, ForeignKey('locations.id'), nullable=True)
	timestamp = Column(DateTime)
	caption = Column(String(101), nullable=True)
	up_vote = Column(Integer, default=0)
	down_vote = Column(Integer, default=0)
	thumbnail = Column(String(101), nullable=True)
	# add upload_timestamp? for freshness algorithm?




# through table linking user and photo
class Vote(Base):
	__tablename__ = "votes"
	id = Column(Integer, primary_key = True)
	# change to single value column  1 == up -1 == down
	# Note: did not make nullable=False in postgres
	value = Column(Integer, nullable=False)
	photo_id = Column(Integer, ForeignKey('photos.id'))
	give_vote_user_id = Column(Integer, ForeignKey('users.id'))
	receive_vote_user_id = Column(Integer, ForeignKey('users.id'))
	timestamp = Column(DateTime, default=datetime.datetime.utcnow)

	give_vote_user = relationship("User", primaryjoin="User.id==Vote.give_vote_user_id", backref=backref("votes_given", order_by=id))
	receive_vote_user = relationship("User", primaryjoin="User.id==Vote.receive_vote_user_id", backref=backref("votes_received", order_by=id))
	photo = relationship("Photo", backref=backref("votes", order_by=id))


# if tag doesn't already exist - create a new tag and tag id --> add this logic
class Tag(Base):
	__tablename__ = "tags"
	id = Column(Integer, primary_key = True)
	tag_title = Column(String(64), nullable=True)



#links photos and tags
class Photo_Tag(Base):
	__tablename__ = "photo_tags"
	#id = Column(Integer, primary_key = True) don't need it because created composite key (two foreign keys)
	photo_id = Column(Integer, ForeignKey('photos.id'), primary_key = True)
	tag_id = Column(Integer, ForeignKey('tags.id'), primary_key = True)


class Location(Base):
	__tablename__ = "locations"
	id = Column(Integer, primary_key = True)
	country = Column(String(64), nullable=True)
	city = Column(String(64), nullable=True)
	neighborhood = Column(String(64), nullable=True)


### End class declarations


def create_db():
    Base.metadata.create_all(engine)


def connect(db_uri="postgres://lauren:@localhost/eyetravelv1"):
    global engine
    global session
    engine = create_engine(db_uri, echo=False) 
    # engine = create_engine("postgres://lauren:@localhost/eyetravelv1", echo=True)
    session = scoped_session(sessionmaker(bind=engine,
                             autocommit = False,
                             autoflush = False))


def main():
    """   """
    pass

if __name__ == "__main__":
    main()


