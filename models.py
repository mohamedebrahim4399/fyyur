from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app = Flask(__name__)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

showing = db.Table('showing',
  db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id')),
  db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id')),
  db.Column('start_time', db.String(50))
)

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    seeking_venue = db.Column(db.String(10), default = "True")
    seeking_description = db.Column(db.String(300))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    def __repr__(self):
      return f"<Venue Id: {self.id}, Name: {self.name}, City: {self.city}, Address: {self.address}, Phone: {self.phone}>"

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    seeking_venue = db.Column(db.String(10), default = "True")
    seeking_description = db.Column(db.String(300))
    genres = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    show = db.relationship('Venue', secondary=showing, backref=db.backref('show', lazy='joined'))
