#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import datetime
from datetime import *
from sqlalchemy import text
import sqlalchemy
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

from models import showing, Artist, Venue

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#



    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  data = Venue.query.all()

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  input_value = request.form.get('search_term')
  input_value_lower = input_value.lower()

  desired_data = []
  count_of_result = 0
  venue_data = Venue.query.all()
  for i in venue_data:
    venue_name = i.name
    if venue_name.lower().find(input_value_lower) >= 0:
      desired_data.append(i)
      count_of_result += 1


  return render_template('pages/search_venues.html', results=desired_data, search_term=request.form.get('search_term', ''), count_of_result = count_of_result)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  data = Venue.query.get(venue_id)

  today_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  venue_data = []
  query = sqlalchemy.text(f"select artist_id, start_time from showing where venue_id = {venue_id}")
  query_result = db.engine.execute(query)
  fetch_all_data = query_result.fetchall()
  for row in fetch_all_data:
    venue_data.append(row)

  upcomming_show_count = 0
  past_show_count = 0

  upcomming_show_arr = []
  past_show_arr = []

  upcomming_show_artist_arr = []
  past_show_artist_arr = []

  for i in range(0, len(venue_data)):
    if today_date > venue_data[i][1]:
      past_show_count += 1
      past_show_arr.append(venue_data[i])
      past_show_artist_arr.append(Artist.query.get(venue_data[i][0]))
    else:
      upcomming_show_count += 1
      upcomming_show_arr.append(venue_data[i])
      upcomming_show_artist_arr.append(Artist.query.get(venue_data[i][0]))

  return render_template('pages/show_venue.html',
    venue=data,
    upcomming_artist = upcomming_show_artist_arr,
    upcomming_date = upcomming_show_arr,
    upcomming_count = upcomming_show_count,

    past_artist = past_show_artist_arr,
    past_date = past_show_arr,
    past_count = past_show_count

  )

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success

    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    address = request.form.get('address')
    phone = request.form.get('phone')
    genres = request.form.get('genres')
    seeking_venue = request.form.get('seeking_venue')
    seeking_description = request.form.get('description')
    website = request.form.get('website')
    facebook_link = request.form.get('facebook_link')
    image_link = request.form.get('image_link')

    venue_data = Venue(name = name, city = city, state = state, address = address, phone = phone, seeking_venue = seeking_venue, seeking_description = seeking_description, website = website ,facebook_link = facebook_link, image_link = image_link)

    #return f"<h1>{genres}</h1>"
    db.session.add(venue_data)
    db.session.commit()

    flash('Venue ' + request.form['name'] + ' was successfully listed!')

    return render_template('pages/home.html')

  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')

  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

  try:
    Venue.query.filter_by(id = venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.rollback()
  return jsonify({'success': True})


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  data = Artist.query.all()

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  input_value = request.form.get('search_term')
  input_value_lower = input_value.lower()

  desired_data = []
  count_of_result = 0
  artist_data = Artist.query.all()
  for i in artist_data:
    venue_name = i.name
    if venue_name.lower().find(input_value_lower) >= 0:
      desired_data.append(i)
      count_of_result += 1

  return render_template('pages/search_artists.html', results=desired_data, search_term=request.form.get('search_term', ''), count_of_result = count_of_result)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  data = Artist.query.get(artist_id)

  today_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  artist_data = []
  query = sqlalchemy.text(f"select venue_id, start_time from showing where artist_id = {artist_id}")
  query_result = db.engine.execute(query)
  fetch_all_data = query_result.fetchall()
  for row in fetch_all_data:
    artist_data.append(row)

  upcomming_show_count = 0
  past_show_count = 0

  upcomming_show_arr = []
  past_show_arr = []

  upcomming_show_venue_arr = []
  past_show_venue_arr = []

  for i in range(0, len(artist_data)):
    if today_date > artist_data[i][1]:
      past_show_count += 1
      past_show_arr.append(artist_data[i])
      past_show_venue_arr.append(Venue.query.get(artist_data[i][0]))
    else:
      upcomming_show_count += 1
      upcomming_show_arr.append(artist_data[i])
      upcomming_show_venue_arr.append(Venue.query.get(artist_data[i][0]))


  return render_template('pages/show_artist.html',
    artist=data,
    upcomming_venue = upcomming_show_venue_arr,
    upcomming_date = upcomming_show_arr,
    upcomming_count = upcomming_show_count,

    past_venue = past_show_venue_arr,
    past_date = past_show_arr,
    past_count = past_show_count
  )

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  data = Artist.query.get(artist_id)
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  data = Artist.query.get(artist_id)
  data.name = request.form.get('name')
  data.city = request.form.get('city')
  data.state = request.form.get('state')
  data.phone = request.form.get('phone')
  data.genres = request.form.get('genres')
  data.seeking_venue = request.form.get('seeking_venue')
  data.seeking_description = request.form.get('description')
  data.website = request.form.get('website')
  data.facebook_linke = request.form.get('facebook_link')
  data.image_link = request.form.get('image_link')

  db.session.commit()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()

  data = Venue.query.get(venue_id)

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  data = Venue.query.get(venue_id)
  data.name = request.form.get('name')
  data.city = request.form.get('city')
  data.state = request.form.get('state')
  data.phone = request.form.get('phone')
  data.genres = request.form.get('geners')
  data.seeking_venue = request.form.get('seeking_venue')
  data.seeking_description = request.form.get('description')
  data.website = request.form.get('website')
  data.facebook_link = request.form.get('facebook_link')
  data.image_link = request.form.get('image_link')

  db.session.commit()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  name = request.form.get('name')
  city = request.form.get('city')
  state = request.form.get('state')
  phone = request.form.get('phone')
  genres = request.form.get('genres')
  seeking_venue = request.form.get('seeking_venue')
  seeking_description = request.form.get('description')
  website = request.form.get('website')
  facebook_link = request.form.get('facebook_link')
  image_link = request.form.get('image_link')


  artist_data = Artist(name = name, city = city, state = state, phone = phone, genres = genres, seeking_venue = seeking_venue, seeking_description = seeking_description, website = website, facebook_link = facebook_link, image_link = image_link)
  db.session.add(artist_data)
  db.session.commit()

  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')

#  Delete Artist
#  ----------------------------------------------------------------

@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):

  try:
    Artist.query.filter_by(id = artist_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.rollback()
  return jsonify({'success': True})

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  showing_artists = Artist.query.join(showing).join(Venue).filter((showing.c.artist_id == Artist.id) & (showing.c.venue_id == Venue.id)).all()

  showing_venues = Venue.query.join(showing).join(Artist).filter((showing.c.artist_id == Artist.id) & (showing.c.venue_id == Venue.id)).all()

  result = db.session.query(Venue.id, Venue.name, Artist.id, Artist.name, Artist.image_link).filter(showing.c.artist_id == Artist.id).filter(showing.c.venue_id == Venue.id).all()

  start_time_arr = []
  for i in range(0, len(result)):
    query = sqlalchemy.text(f"SELECT start_time from showing WHERE (venue_id = {result[i][0]} AND artist_id = {result[i][2]})")
    query_result = db.engine.execute(query)
    fetch_all_data = query_result.fetchall()
    for row in fetch_all_data:
      for data in row:
        start_time_arr.append(data)

  data = []
  for i in range(0, len(result)):

    test_data = {
      'venue_id': result[i][0],
      'venue_name': result[i][1],
      'artist_id': result[i][2],
      'artist_name': result[i][3],
      'artist_image_link': result[i][4],
      'start_time': start_time_arr[i]
    }
    data.append(test_data)


  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  artist_id = request.form.get('artist_id')
  venue_id = request.form.get('venue_id')
  start_time = request.form.get('start_time')

  artist = Artist.query.get(artist_id)
  venue = Venue.query.get(venue_id)


  if artist and venue:
    venue.show.append(artist)
    db.session.commit()

    # inser start date into association table
    sql_query = sqlalchemy.text(f"UPDATE showing SET start_time='{start_time}' WHERE (artist_id={artist_id} AND venue_id={venue_id})")
    db.engine.execute(sql_query)
  else:
    return "The ID of this element is wrong"

  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
