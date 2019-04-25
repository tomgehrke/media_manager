import string
import json
import random
import httplib2
import requests
from flask import (
    Flask,
    render_template,
    request,
    make_response,
    redirect,
    url_for,
    jsonify,
    flash
)
from flask import session as login_session
from sqlalchemy import (
    create_engine,
    func
)
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker
)
from database_setup import (
    Base,
    Media,
    MediaType,
    MediaFormat,
    User
)
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError


app = Flask(__name__)

# OAUTH Constants
CLIENT_ID = json.loads(open('client_secret.json', 'r')
                       .read())['web']['client_id']
APPLICATION_NAME = "Media Manager"

engine = create_engine('sqlite:///mediamanager.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = scoped_session(sessionmaker(bind=engine))
session = DBSession()

redirect_url = '/'


@app.route('/')
def showStart():
    mediatype_sql = """select mediatype.id, mediatype.name, fa_icon_class, count(*) as media_count
        from mediatype, media
        where mediatype.id = media.mediatype_id
        group by mediatype.name
        union all
        select mediatype.id, mediatype.name, fa_icon_class, 0 as media_count
        from mediatype
        where mediatype.id not in (select distinct mediatype_id from media)
        order by name"""
    mediaformat_sql = """select mediaformat.id, mediaformat.name, fa_icon_class, count(*) as media_count
        from mediaformat, media
        where mediaformat.id = media.mediaformat_id
        group by mediaformat.name
        union all
        select mediaformat.id, mediaformat.name, fa_icon_class, 0 as media_count
        from mediaformat
        where mediaformat.id not in (select distinct mediaformat_id from media)
        order by name"""

    mediatypes = session.execute(mediatype_sql)
    mediaformats = session.execute(mediaformat_sql)
    return render_template(
        'start.html',
        mediatypes=mediatypes,
        mediaformats=mediaformats
    )


@app.route('/media/new/', methods=['GET', 'POST'])
def createMedia():
    if 'user_id' not in login_session:
        return redirect('/login')
    else:
        global redirect_url
        mediatypes = session.query(MediaType).all()
        mediaformats = session.query(MediaFormat).all()
        if request.method == 'POST':
            if request.form['title'] and 'submitButton' in request.form:
                newMedia = Media(
                    title=request.form['title'],
                    year=request.form['year'],
                    rating=request.form['rating'],
                    mediatype_id=request.form['mediatype'],
                    mediaformat_id=request.form['mediaformat'],
                    created_user_id=login_session['user_id'],
                    poster_url=request.form['poster_url'],
                    imdb_id=request.form['imdb_id'],
                )
                session.add(newMedia)
                session.commit()
                flash('Added "{title}"!'.format(title=newMedia.title), 'info')
            return redirect(redirect_url)
        else:
            redirect_url = request.referrer
            return render_template(
                'createMedia.html',
                mediatypes=mediatypes,
                mediaformats=mediaformats)


@app.route('/media/<int:media_id>/edit/', methods=['GET', 'POST'])
def editMedia(media_id):
    if 'user_id' not in login_session:
        return redirect('/login')
    else:
        media = session.query(Media).filter_by(id=media_id).one()
        if login_session.get('user_id') != media.created_user_id:
            flash('You may not edit media that you did not add!', 'danger')
            return redirect('/')
        global redirect_url
        if request.method == 'POST':
            if request.form['title'] and 'submitButton' in request.form:
                media.title = request.form['title']
                media.year = request.form['year']
                media.rating = request.form['rating']
                media.mediatype_id = request.form['mediatype']
                media.mediaformat_id = request.form['mediaformat']
                media.poster_url = request.form['poster_url']
                media.imdb_id = request.form['imdb_id']

                session.add(media)
                session.commit()
            return redirect(redirect_url)
        else:
            redirect_url = request.referrer
            mediatypes = session.query(MediaType).all()
            mediaformats = session.query(MediaFormat).all()
            return render_template(
                'editMedia.html',
                media=media,
                mediatypes=mediatypes,
                mediaformats=mediaformats)


@app.route('/media/<int:media_id>/delete/', methods=['GET', 'POST'])
def deleteMedia(media_id):
    if 'user_id' not in login_session:
        return redirect('/login')
    else:
        mediaToDelete = session.query(Media).filter_by(id=media_id).one()
        if login_session.get('user_id') != mediaToDelete.created_user_id:
            flash('You may not delete media that you did not add!', 'danger')
            return redirect('/')
        global redirect_url
        if request.method == 'POST':
            if "submitButton" in request.form:
                session.delete(mediaToDelete)
                session.commit()
                flash('Deleted "{title}"'.format(
                    title=mediaToDelete.title), 'info')
            return redirect(redirect_url)
        else:
            return render_template('deleteMedia.html', media=mediaToDelete)


@app.route('/mediatype/<int:mediatype_id>/')
def listMediaByType(mediatype_id):
    mediatype = session.query(MediaType).filter_by(id=mediatype_id).one()
    media = session.query(Media).filter_by(
        mediatype_id=mediatype_id).order_by(Media.title, Media.year).all()
    return render_template(
        'media.html',
        media=media,
        mediatype=mediatype
    )


@app.route('/mediaformat/<int:mediaformat_id>/')
def listMediaByFormat(mediaformat_id):
    mediaformat = session.query(MediaFormat).filter_by(id=mediaformat_id).one()
    media = session.query(Media).filter_by(
        mediaformat_id=mediaformat_id).order_by(Media.title, Media.year).all()
    return render_template(
        'media.html',
        media=media,
        mediaformat=mediaformat
    )


@app.route('/media/json/')
@app.route('/mediaformat/<int:mediaformat_id>/json/')
@app.route('/mediatype/<int:mediatype_id>/json/')
def listMediaJSON(mediaformat_id=0, mediatype_id=0):
    mediaQuery = session.query(Media).order_by(Media.title, Media.year)
    if mediaformat_id > 0:
        mediaQuery = mediaQuery.filter_by(mediaformat_id=str(mediaformat_id))
    if mediatype_id > 0:
        mediaQuery = mediaQuery.filter_by(mediatype_id=str(mediatype_id))
    media = mediaQuery.all()
    return jsonify(media=[m.serialize for m in media])


# AUTHENTICATION

@app.route('/gauth', methods=['POST'])
def googleauth():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(
            json.dumps('Invalid state parameter.'),
            401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    authcode = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(authcode)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'),
            401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(
            json.dumps(result.get('error')),
            500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    google_id = credentials.id_token['sub']
    if result['user_id'] != google_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."),
            401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."),
            401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_google_id = login_session.get('google_id')
    if stored_access_token is not None and google_id == stored_google_id:
        response = make_response(
            json.dumps('Current user is already connected.'),
            200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['google_id'] = google_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    currentuser = session.query(User).filter_by(email=data['email']).first()
    if currentuser is None:
        currentuser = User(
            username=data['name'],
            picture_url=data['picture'],
            email=data['email'])
        session.add(currentuser)
        session.commit()

    login_session['user_id'] = currentuser.id
    login_session['username'] = currentuser.username
    login_session['picture'] = currentuser.picture_url
    login_session['email'] = currentuser.email

    output = "<h1>Welcome, {username}</h1>"
    return output.format(username=login_session['username'])


@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/logout')
def logout():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'),
            401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s' %
           login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['google_id']
        del login_session['user_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        return redirect("/", code=303)
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.'),
            400)
        response.headers['Content-Type'] = 'application/json'
        return response


if __name__ == "__main__":
    app.secret_key = "sm4Ra*Peb3XquIdRK%FNiwUZQhotHB@J"
    app.debug = True
    app.run(host="0.0.0.0", port=8000)
