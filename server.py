import json
from flask import Flask,render_template,request,redirect,flash,url_for, abort
from datetime import datetime

def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions

def saveClubs(clubs):
    with open('clubs.json', 'w') as clubs_db:
        db = {'clubs': clubs}
        json.dump(db, clubs_db, indent=4)

def saveCompetitions(competitions):
    with open('competitions.json', 'w') as comps:
        db = {'competitions': competitions}
        json.dump(db, comps, indent=4)

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/board')
def board():
    return render_template('board.html', clubs=clubs)

@app.route('/showSummary',methods=['GET', 'POST'])
def showSummary():
    now = datetime.now()
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        for compet in competitions:
            if datetime.strptime(compet['date'], '%Y-%m-%d %H:%M:%S') <= now:
                compet['numberOfPlaces'] = 0

        return render_template('welcome.html', clubs=clubs,
            club=club, competitions=competitions, now=now)
    except IndexError:
        return render_template('email_unknown.html')
    except Exception as e:
        print('ERROR summary :::::::', e)
        abort(404)

@app.route('/book/<competition>/<club>')
def book(competition,club):
    try:
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        if foundCompetition['numberOfPlaces'] != 0 and foundCompetition['numberOfPlaces'] != '0':
            return render_template(
                'booking.html',
                club=foundClub,
                competition=foundCompetition,
                places_available=int(foundCompetition['numberOfPlaces']))
        else:
            abort(404)
    except Exception as e:
        print('ERROR book :::::::', e)
        abort(404)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    now = datetime.now()
    try:
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
    except:
        abort(404)
        
    if datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S') <= now:
            abort(400)

    try:
        placesRequired = int(request.form['places'])
    except:
        abort(400)
        
    clubPoints = int(club['points'])

    try:
        placesAvailable = int(competition['numberOfPlaces'])
    except:
        placesAvailable = 0

    if placesRequired <= 0:
        return render_template('booking.html', club=club,
            competition=competition , 
            message='Please enter a valid number.',
            places_available=placesAvailable)
    elif placesRequired <= placesAvailable and placesRequired <= 12 and clubPoints >= placesRequired:
        club['points'] = str(clubPoints-placesRequired)
        competition['numberOfPlaces'] = str(placesAvailable-placesRequired)
        saveCompetitions(competitions)
        saveClubs(clubs)
        flash('Great-booking complete!')
        return render_template('welcome.html',
            club=club, clubs=clubs, competitions=competitions)
    elif placesRequired > placesAvailable:
        return render_template('booking.html', club=club,
            competition=competition , 
            message='There is not enough places available.',
            places_available=placesAvailable)
    elif placesRequired > 12:
        return render_template('booking.html', club=club,
            competition=competition , 
            message='Please book 12 or less places.',
            places_available=placesAvailable)
    elif clubPoints < placesRequired:
        return render_template('booking.html', club=club,
            competition=competition , 
            message='You don\'t have enough points',
            places_available=placesAvailable)

# TODO: Add route for points display

@app.route('/logout')
def logout():
    return redirect(url_for('index'))
