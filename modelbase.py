from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


engine = create_engine("sqlite:///ratings.db", echo=False)
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


#increment function for up and down vote based on when a vote is cast - write this function
class Photo(Base):
	__tablename__ = "photos"

	id = Column(Integer, primary_key = True)
	file_location = (String(100), nullable=True)  #????????????? a pointer to..?
	photo_location_id = Column(Integer, ForeignKey('locations.id'), nullable=True)
	timestamp = Column(DateTime)
	caption = Column(String(101), nullable=True)
	up_vote(int)
	down_vote(int)

# through table linking user and photo
# use trigger with up and down to automatically update counts  - update that increments by 1
class Vote(Base):
	__tablename__ = "votes"
	id = Column(Integer, primary_key = True)
	# use enum for up/down vote? 
	up = Column(Integer, nullable = True)
	down = Column(Integer, nullable = True)
	photo_id = Column(Integer, ForeignKey('photos.id'))
	give_vote_user_id = Column(Integer, ForeignKey('users.id'))
	receive_vote_user_id = Column(Integer, ForeignKey('users.id'))
	timestamp = Date.datetime.now() # doublecheck syntax

	user = relationship("User", backref=backref("votes", order_by=id))
	photo = relationship("Photo", backref=backref("votes", order_by=id))

# if tag doesn't already exist - creat a new tag and tag id
class Tag(Base):
	__tablename__ = "tags"
	id = Column(Integer, primary_key = True)
	tag_title = Column(String(64), nullable=True)

#links photos and tags
class Photo_Tag(Base):
	__tablename__ = "photo_tags"
	photo_id = Column(Integer, ForeignKey('photos.id'))
	tag_id = Column(Integer, ForeignKey('tags.id'))


class Location(Base):
	__tablename__ = "locations"
	id = Column(Integer, primary_key = True)
	country = Column(String(64), nullable=True)
	city = Column(String(64), nullable=True)
	neighborhood = Column(String(64), nullable=True)



### End class declarations

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()


