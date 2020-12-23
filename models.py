from flask import render_template, jsonify
from app import db
from sqlalchemy import text
import sqlalchemy
import datetime
from datetime import *

from sqlalchemy import (Column,Integer,String,ForeignKey,Sequence,)



# Venue Model

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer,Sequence('venue_id'), primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = Column(String(120))
    seeking_venue = Column(String(10), default = True)
    seeking_description = Column(String(300))
    website = Column(String(120))

    def createVenue(self):
        data=sqlalchemy.text(f''' insert into "Venue"(name,city,state,address,phone,image_link,facebook_link,genres,seeking_venue,seeking_description,website)
            values
            ('{self('name')}','{self('city')}','{self('state')}','{self('address')}','{self('phone')}','{self('image_link')}','{self('facebook_link')}','{self('genres')}','{self('seeking_venue')}','{self('description')}','{self('website')}' ) ''')

        db.engine.execute(data)

    def allVenues():
        return Venue.query.all()

    def showVenue(self):
        venueData= Venue.query.get(self)
        selectedData=sqlalchemy.text(f'select artist_id, start_time from "Showing" where venue_id = {self}')
        selectedDataResult=db.engine.execute(selectedData)
        fetchData=selectedDataResult.fetchall()
        arr=[]
        for i in fetchData:
            arr.append(i)

        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pastCount=0
        upcommingCount=0
        pastArtist=[]
        upcommingArtist=[]
        past=[]
        upcomming=[]
        for i in range(0,len(arr)):
            if date<arr[i][1]:
                upcommingCount+=1
                upcomming.append(arr[i])
                upcommingArtist.append(Artist.query.get(arr[i][0]))
            else:
                pastCount+=1
                past.append(arr[i])
                pastArtist.append(Artist.query.get(arr[i][0]))

        data={"venue": venueData,
            "upcomming_artist" :  upcommingArtist,
            "upcomming_date" :  upcomming,
            "upcomming_count" :  upcommingCount,
            "past_artist" :  pastArtist,
            "past_date" :  past,
            "past_count" :  pastCount}
        return data

    def deleteVenue(self):
        try:
            Venue.query.filter_by(id = self).delete()
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()
            return jsonify({'sucess':True})

    def editVenue(self,id):
        data=Venue.query.get(id)
        data.name = self('name')
        data.city = self('city')
        data.state = self('state')
        data.address=self('address')
        data.phone = self('phone')
        data.image_link = self('image_link')
        data.facebook_link = self('facebook_link')
        data.genres  = self('genres')
        data.seeking_venue = self('seeking_venue')
        data.seeking_description = self('description')
        data.website = self('website')

        db.session.commit()


# Artist Model

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer,Sequence('artist_id'), primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = Column(String(10), default = True)
    seeking_description = Column(String(300))
    website = Column(String(120))


    def createِArtists(self):
        data=sqlalchemy.text(f'''insert into "Artist"(
            name,city,state,phone,image_link,facebook_link,genres,seeking_venue,seeking_description,website)
            values
            ('{self('name')}','{self('city')}','{self('state')}','{self('phone')}','{self('image_link')}','{self('facebook_link')}','{self('genres')}','{self('seeking_venue')}','{self('description')}','{self('website')}')''')

        db.engine.execute(data)

    def allArtists():
        return Artist.query.all()

    def showArtist(self):
        artistData= Artist.query.get(self)
        selectedData=sqlalchemy.text(f'select venue_id, start_time from "Showing" where artist_id = {self}')


        selectedDataResult=db.engine.execute(selectedData)
        fetchData=selectedDataResult.fetchall()
        arr=[]
        for i in fetchData:
            arr.append(i)

        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pastCount=0
        upcommingCount=0
        pastArtist=[]
        upcommingArtist=[]
        past=[]
        upcomming=[]
        for i in range(0,len(arr)):
            if date<arr[i][1]:
                upcommingCount+=1
                upcomming.append(arr[i])
                upcommingArtist.append(Venue.query.get(arr[i][0]))
            else:
                pastCount+=1
                past.append(arr[i])
                pastArtist.append(Venue.query.get(arr[i][0]))

        data={"artist": artistData,
            "upcomming_venue" :  upcommingArtist,
            "upcomming_date" :  upcomming,
            "upcomming_count" :  upcommingCount,
            "past_venue" :  pastArtist,
            "past_date" :  past,
            "past_count" :  pastCount}
        return data

    def editArtist(self,id):
        data=Artist.query.get(id)
        data.name = self('name')
        data.city = self('city')
        data.state = self('state')
        data.phone = self('phone')
        data.genres  = self('genres')
        data.image_link = self('image_link')
        data.facebook_link = self('facebook_link')
        data.seeking_venue = self('seeking_venue')
        data.seeking_description = self('description')
        data.website = self('website')

        db.session.commit()


# showing model for relation

class Showing(db.Model):
    __tablename__ = 'Showing'
    id = Column(Integer,Sequence('map_seq'),primary_key=True)
    start_time = Column(String(50))
    artist_id = Column(Integer,ForeignKey('Artist.id'))
    venue_id = Column(Integer,ForeignKey('Venue.id'))

    def createShow(self):
        venue=Venue.query.get(self('venue_id'))
        artist=Artist.query.get(self('artist_id'))
        if venue and artist:
            data=sqlalchemy.text(f''' insert into "Showing"(start_time,artist_id,venue_id) values ('{self('start_time')}', '{self('artist_id')}', '{self('venue_id')}')''')
            db.engine.execute(data)
        else:
            return 'error'


    def dataInShow():
        data = sqlalchemy.text(f'''select "Venue".id, "Venue".name, "Artist".id, "Artist".name,"Artist".image_link, "Showing".start_time from "Showing" join "Artist" on "Artist".id = "Showing".artist_id join "Venue" on "Venue".id = "Showing".venue_id''')
        dataExecute = db.engine.execute(data)
        fetchData = dataExecute.fetchall()
        arr=[]
        for i in range(0,len(fetchData)):
            dataSet = {
            'venue_id': fetchData[i][0],
            'venue_name': fetchData[i][1],
            'artist_id': fetchData[i][2],
            'artist_name': fetchData[i][3],
            'artist_image_link': fetchData[i][4],
            'start_time': fetchData[i][5]
            }
            arr.append(dataSet)
        return arr
