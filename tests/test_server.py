import pytest
from flask import request

import server


@pytest.fixture
def client():
    app = server.app
    with app.test_client() as client:
        yield client

@pytest.fixture
def db_clubs():
    return [{
        "name":"Simply Lift",
        "email":"john@simplylift.co",
        "points":"13"
    },{
        "name":"Iron Temple",
        "email": "admin@irontemple.com",
        "points":"4"
    },{
        "name":"She Lifts",
        "email": "kate@shelifts.co.uk",
        "points":"12"
    }]

@pytest.fixture
def db_competitions():
    return [{
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        },{
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        }]

@pytest.fixture
def mock_dbs(mocker, db_clubs, db_competitions):
    mocker.patch.object(server, 'clubs', db_clubs)
    mocker.patch.object(server, 'competitions', db_competitions)

@pytest.fixture
def _login(client, db_clubs, mocker):
    mocker.patch.object(server, 'clubs', db_clubs)
    response = client.post('/showSummary',
        data={'email': 'kate@shelifts.co.uk'})
    return response

@pytest.fixture
def _logout(client):
    return client.get('/logout')


def test_loadClubs_should_return_list_of_clubs(db_clubs):
    expected_value = [{
        "name":"Simply Lift",
        "email":"john@simplylift.co",
        "points":"13"
    },{
        "name":"Iron Temple",
        "email": "admin@irontemple.com",
        "points":"4"
    },{
        "name":"She Lifts",
        "email": "kate@shelifts.co.uk",
        "points":"12"
    }]
    assert db_clubs == expected_value

def test_showSummary_should_redirect_to_welcome(client, _login):
    """
    With an existing email, it should redirect to a new page.
    """
    assert _login.status_code == 200
    assert 'Welcome, ' in _login.data.decode()
    assert request.url == 'http://localhost/showSummary'

def test_showSummary_should_redirect_to_same_page(client):
    """
    If the email doesn't exist, the user stays on the same
    page, but with an error message.
    """
    # mocker.patch.object(server, 'clubs', db_clubs)
    response = client.post('/showSummary',
        data={'email': 'test@tast.com'})
    assert response.status_code == 200
    assert '<p>Your email doesn\'t exist.</p>' in response.data.decode()
    assert request.url == 'http://localhost/showSummary'

def test_purchasePlaces_correct_number(client, mock_dbs, _login):
    """
    Book a corret amount of places, should return the same page.
    With the new number of places.
    """
    places_available = int(server.competitions[0]['numberOfPlaces'])
    response = client.post('/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': '4'
        })
    places_left = int(server.competitions[0]['numberOfPlaces'])
    assert response.status_code == 200
    assert places_left == places_available-int(request.form['places'])
    assert request.url == 'http://localhost/purchasePlaces'

def test_purchasePlaces_too_high_number(client, mock_dbs, _login):
    """
    Book a highest number of places than available.
    Should return an error.
    """
    places_available = int(server.competitions[0]['numberOfPlaces'])
    response = client.post('/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': '100'
        })
    places_left = int(server.competitions[0]['numberOfPlaces'])
    assert response.status_code == 200
    assert places_left == places_available
    assert 'There is not enough places available.' in response.data.decode()
    assert request.url == 'http://localhost/purchasePlaces'

def test_purchasePlaces_negative_or_0_number(client, mock_dbs, _login):
    """
    Book a negative or null number of places.
    Should return an error.
    """
    places_available = int(server.competitions[0]['numberOfPlaces'])
    response = client.post('/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': '-10'
        })
    places_left = int(server.competitions[0]['numberOfPlaces'])
    assert response.status_code == 200
    assert places_left == places_available
    assert 'Please enter a valid number.' in response.data.decode()
    assert request.url == 'http://localhost/purchasePlaces'

def test_purchasePlaces_not_logged_in(client, mock_dbs, _logout):
    """
    The user is not logged in.
    Should return 404.
    """
    places_available = int(server.competitions[0]['numberOfPlaces'])
    response = client.post('/purchasePlaces',
        data={
            'places': '2'
        })
    places_left = int(server.competitions[0]['numberOfPlaces'])
    assert places_left == places_available
    assert response.status_code == 404

def test_purchasePlaces_more_than_12_places(client, mock_dbs, _logout):
    """
    Book more than 12 places.
    Should return an error.
    """
    places_available = int(server.competitions[0]['numberOfPlaces'])
    response = client.post('/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': '13'
        })
    places_left = int(server.competitions[0]['numberOfPlaces'])
    assert response.status_code == 200
    assert places_left == places_available
    assert 'Please book 12 or less places.' in response.data.decode()
    assert request.url == 'http://localhost/purchasePlaces'
