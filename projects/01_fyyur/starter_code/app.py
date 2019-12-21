# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from flask_migrate import Migrate
from forms import *
from flask_wtf import Form
from logging import Formatter, FileHandler
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
import json
from datetime import datetime
import dateutil.parser
import babel
from flask import Flask,render_template,request,Response,flash,redirect,url_for
# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#
# TODO: implement any missing fields, as a database migration using
# Flask-Migrate


class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'venue.id',
            ondelete="CASCADE"),
        nullable=False)
    artist_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'artist.id',
            ondelete="CASCADE"),
        nullable=False)
    show_time = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow)
    # venues = relationship("Venue", backref=backref("venue"))


class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.String(300))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    shows = db.relationship('Show', backref='venue', lazy=True)


class Artist(db.Model):
    __tablename__ = 'artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120), nullable=False)
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean(300))
    seeking_description = db.Column(db.String(300))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist', lazy=True)


# TODO: implement any missing fields, as a database migration using
# Flask-Migrate

# TODO Implement Show and Artist models, and complete all model
# relationships and properties, as a database migration.

# ---------------------------------------------------------------------------#
# Filters.
# --------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

# ---------------------------------------------------------------------------#
# Controllers.
# --------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    # num_shows should be aggregated based on number of upcoming shows per
    # venue.
    vstates = Venue.query.with_entities(
        Venue.state).group_by(
        Venue.state).all()
    resultList = []
    for st in vstates:
        fset = {}
        venstate = []
        venstate = Venue.query.filter(Venue.state == st).all()
        venues = []
        for ven in venstate:
            venue = {}
            show = Show.query.filter(
                Show.venue_id == ven.id,
                Show.show_time > datetime.today()).count()
            venue["id"] = ven.id
            venue["name"] = ven.name
            venue["num_upcoming_shows"] = show
            venues.append(venue)
        fset["city"] = venstate[0].city
        fset["state"] = venstate[0].state
        fset["venues"] = venues
        resultList.append(fset)

    return render_template('pages/venues.html', areas=resultList)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search.
    # Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square
    # Live Music & Coffee"

    response = {}
    data = []
    sch_term = request.form.get('search_term', '')
    if sch_term:
        venues = Venue.query.filter(Venue.name.ilike('%' + sch_term + '%'))
        venues = venues.order_by(Venue.name).all()
        cnt = len(venues)
        response["count"] = cnt

        for ven in venues:
            vens = {}
            vens["id"] = ven.id
            vens["name"] = ven.name
            vens["num_upcoming_shows"] = len(ven.shows)
            data.append(vens)
        response["data"] = data
    else:
        response["count"] = 0
    return render_template(
        'pages/search_venues.html',
        results=response,
        search_term=request.form.get(
            'search_term',
            ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using
    # venue_id

    vn = Venue.query.get(venue_id)
    pshowcnt = Show.query.filter(
        Show.venue_id == venue_id,
        Show.show_time < datetime.today()).count()
    upshowcnt = Show.query.filter(
        Show.venue_id == venue_id,
        Show.show_time > datetime.today()).count()
    pshowinfo = Show.query.with_entities(
        Show.show_time,
        Show.artist_id).filter(
        Show.venue_id == venue_id,
        Show.show_time < datetime.today())
    upshowinfo = Show.query.with_entities(
        Show.show_time,
        Show.artist_id).filter(
        Show.venue_id == venue_id,
        Show.show_time > datetime.today())

    past_show = []
    up_show = []
    venue = {}
    venue["id"] = vn.id
    venue["name"] = vn.name
    venue["city"] = vn.city
    venue["state"] = vn.state
    venue["genres"] = vn.genres.strip('}{}').split(', ')
    venue["address"] = vn.address
    venue["phone"] = vn.phone
    venue["website"] = vn.website_link
    venue["facebook_link"] = vn.facebook_link
    venue["seeking_talent"] = vn.seeking_talent
    venue["seeking_description"] = vn.seeking_description
    venue["image_link"] = vn.image_link
    for show in pshowinfo:
        pshow = {}
        artist = Artist.query.get(show[1])
        dtstr = show[0].strftime('%m/%d/%Y %H:%M:%S')
        if artist is not None:
            pshow["artist_id"] = artist.id
            pshow["artist_name"] = artist.name
            pshow["artist_image_link"] = artist.image_link
            pshow["start_time"] = dtstr
            past_show.append(pshow)
    for ush in upshowinfo:
        ushow = {}
        arinfo = Artist.query.get(ush[1])
        dt = ush[0].strftime('%m/%d/%Y %H:%M:%S')
        if arinfo is not None:
            ushow["artist_id"] = arinfo.id
            ushow["artist_name"] = arinfo.name
            ushow["artist_image_link"] = arinfo.image_link
            ushow["start_time"] = dt
            up_show.append(ushow)
    venue["past_shows"] = past_show
    venue["upcoming_shows"] = up_show
    venue["past_shows_count"] = pshowcnt
    venue["upcoming_shows_count"] = upshowcnt
    return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm()
    vname = request.form.get('name')
    vgenres = form.genres.data
    vcity = request.form.get('city')
    vstate = request.form.get('state')
    vphone = request.form.get('phone')
    vaddress = request.form.get('address')
    vfblink = request.form.get('facebook_link')

    venue = Venue(
        name=vname,
        city=vcity,
        state=vstate,
        phone=vphone,
        address=vaddress,
        genres=vgenres,
        facebook_link=vfblink)
    try:
        db.session.add(venue)
        db.session.commit()
        flash(
            'Venue ' +
            request.form['name'] +
            ' was successfully listed!')
    except Exception as e:
        flash(
            'Error Occured: Venue ' +
            request.form['name'] +
            ' could not be listed.')
    return render_template('pages/home.html')

    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success

    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + '
    # could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


@app.route('/venues/<venue_id>', methods=['GET', 'POST'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session
    # commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a
    # Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to
    # the homepage
    try:
        qry = db.session.query(Venue).filter(Venue.id == venue_id)
        qry.delete()
        db.session.commit()
        flash(
            'Venue with venue ID ' +
            venue_id +
            ' was successfully deleted!')
    except Exception as e:
        flash('Error Occured: Venue with venue ID ' +
              venue_id + ' could not be deleted.')
    return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    data = Artist.query.with_entities(Artist.id, Artist.name).all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search.
    # Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado",
    # and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    response = {}
    data = []
    sch_term = request.form.get('search_term', '')
    if sch_term:
        artists = Artist.query.filter(
            Artist.name.ilike('%' + sch_term + '%'))
        artists = artists.order_by(Artist.name).all()
        cnt = len(artists)
        response["count"] = cnt

        for artist in artists:
            arts = {}
            arts["id"] = artist.id
            arts["name"] = artist.name
            arts["num_upcoming_shows"] = len(artist.shows)
            data.append(arts)
        response["data"] = data
    else:
        response["count"] = 0

    return render_template(
        'pages/search_artists.html',
        results=response,
        search_term=request.form.get(
            'search_term',
            ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using
    # venue_id
    ar = Artist.query.get(artist_id)
    pshowcnt = Show.query.filter(
        Show.artist_id == artist_id,
        Show.show_time < datetime.today()).count()
    upshowcnt = Show.query.filter(
        Show.artist_id == artist_id,
        Show.show_time > datetime.today()).count()
    pshowinfo = Show.query.with_entities(
        Show.show_time,
        Show.venue_id).filter(
        Show.artist_id == artist_id,
        Show.show_time < datetime.today())
    upshowinfo = Show.query.with_entities(
        Show.show_time,
        Show.venue_id).filter(
        Show.artist_id == artist_id,
        Show.show_time > datetime.today())

    past_show = []
    up_show = []
    artist = {}
    artist["id"] = ar.id
    artist["genres"] = ar.genres.strip('}{}').split(', ')
    artist["name"] = ar.name
    artist["city"] = ar.city
    artist["state"] = ar.state
    artist["phone"] = ar.phone
    artist["website"] = ar.website_link
    artist["facebook_link"] = ar.facebook_link
    artist["seeking_venue"] = ar.seeking_venue
    artist["seeking_description"] = ar.seeking_description
    artist["image_link"] = ar.image_link
    for show in pshowinfo:
        pshow = {}
        venue = Venue.query.get(show[1])
        dtstr = show[0].strftime('%m/%d/%Y %H:%M:%S')
        if venue is not None:
            pshow["venue_id"] = venue.id
            pshow["venue_name"] = venue.name
            pshow["venue_image_link"] = venue.image_link
            pshow["start_time"] = dtstr
            past_show.append(pshow)
    for ush in upshowinfo:
        ushow = {}
        veninfo = Venue.query.get(ush[1])
        dt = ush[0].strftime('%m/%d/%Y %H:%M:%S')
        if veninfo is not None:
            ushow["venue_id"] = veninfo.id
            ushow["venue_name"] = veninfo.name
            ushow["venue_image_link"] = veninfo.image_link
            ushow["start_time"] = dt
            up_show.append(ushow)

    artist["past_shows"] = past_show
    artist["upcoming_shows"] = up_show
    artist["past_shows_count"] = pshowcnt
    artist["upcoming_shows_count"] = upshowcnt
    return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    if artist:
        gen = artist.genres.strip('}{').split(",")
        form = ArtistForm(formdata=request.form, obj=artist)
        form.genres.data = gen
    return render_template(
        'forms/edit_artist.html',
        form=form,
        artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    artist = Artist.query.get(artist_id)
    if artist:
        form = ArtistForm(obj=artist)
        form.populate_obj(artist)
        db.session.commit()
        flash("info updated", "success")

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    if venue:
        gen = venue.genres.strip('}{').split(",")
        form = VenueForm(formdata=request.form, obj=venue)
        form.genres.data = gen
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    venue = Venue.query.get(venue_id)
    if venue:
        form = VenueForm(obj=venue)
        form.populate_obj(venue)
        db.session.commit()
        flash("info updated", "success")
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm()
    agenres = []
    aname = request.form.get('name')
    acity = request.form.get('city')
    astate = request.form.get('state')
    aphone = request.form.get('phone')
    agenres = form.genres.data
    afblink = request.form.get('facebook_link')
    try:
        artist = Artist(
            name=aname,
            city=acity,
            state=astate,
            phone=aphone,
            genres=agenres,
            facebook_link=afblink)
        db.session.add(artist)
        db.session.commit()
        flash(
            'Artist ' +
            request.form['name'] +
            ' was successfully listed!')
    except BaseException:
        flash(
            'An error occurred. Artist ' +
            data.name +
            ' could not be listed.')

    return render_template('pages/home.html')

    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    # flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + '
    # could not be listed.')
    # return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    # num_shows should be aggregated based on number of upcoming shows per
    # venue.
    shows = Show.query.all()
    showinfo = {}
    vens = []
    for show in shows:
        ven = {}
        venue = Venue.query.get(show.venue_id)
        artist = Artist.query.get(show.artist_id)
        ven["venue_id"] = venue.id
        ven["venue_name"] = venue.name
        ven["artist_id"] = artist.id
        ven["artist_name"] = artist.name
        ven["artist_image_link"] = artist.image_link
        ven["start_time"] = (show.show_time).strftime('%m/%d/%Y %H:%M:%S')
        vens.append(ven)

    return render_template('pages/shows.html', shows=vens)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting
    # new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    aid = request.form.get('artist_id')
    vid = request.form.get('venue_id')
    start_time = request.form.get('start_time')
    show = Show(artist_id=aid, venue_id=vid, show_time=start_time)
    db.session.add(show)
    db.session.commit()

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
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# --------------------------------------------------------------------------#
# Launch.
# --------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
