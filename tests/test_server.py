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
        "points":"8"
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
            "date": "2022-03-27 10:00:00",
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
        "points":"8"
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

def test_showSummary_should_redirect_to_email_not_found(client):
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

def test_showSummary_get(client, _logout):
    """
    Try to access showSummary view without connexion.
    Should return 404.
    """
    response = client.get('/showSummary')
    assert response.status_code == 404

def test_purchasePlaces_correct_number_correct_date_enough_points(client, mock_dbs, _login):
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
    assert server.clubs[0]['points'] == '4'
    assert response.status_code == 200
    assert places_left == places_available-int(request.form['places'])
    assert request.url == 'http://localhost/purchasePlaces'

def test_purchasePlaces_not_integer_date_enough_points(client, mock_dbs, _login):
    """
    Book a corret amount of places, should return the same page.
    With the new number of places.
    """
    places_available = int(server.competitions[0]['numberOfPlaces'])
    response = client.post('/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': 'g'
        })
    places_left = int(server.competitions[0]['numberOfPlaces'])
    assert server.clubs[0]['points'] == '8'
    assert response.status_code == 400
    assert places_left == places_available
    assert request.url == 'http://localhost/purchasePlaces'

def test_purchasePlaces_correct_number_correct_date_not_enough_points(client, mock_dbs, _login):
    """
    Book a corret amount of places, should return the same page.
    With the new number of places.
    """
    places_available = int(server.competitions[0]['numberOfPlaces'])
    response = client.post('/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': '9'
        })
    places_left = int(server.competitions[0]['numberOfPlaces'])
    assert server.clubs[0]['points'] == '8'
    assert response.status_code == 200
    assert places_left == places_available
    assert request.url == 'http://localhost/purchasePlaces'

def test_purchasePlaces_correct_number_wrong_date(client, mock_dbs, _login):
    """
    Book a corret amount of places, but the contest is past.
    Should return 404.
    """
    places_available = int(server.competitions[0]['numberOfPlaces'])
    response = client.post('/purchasePlaces',
        data={
            'competition': 'Fall Classic',
            'club': 'Simply Lift',
            'places': '4'
        })
    places_left = int(server.competitions[0]['numberOfPlaces'])
    assert server.clubs[0]['points'] == '8'
    assert response.status_code == 400
    assert places_left == places_available

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
    assert server.clubs[0]['points'] == '8'
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
    assert server.clubs[0]['points'] == '8'
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

def test_purchasePlaces_more_than_12_places(client, mock_dbs):
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

def test_get_booking_page_past_contest(client):
    """
    Get the booking page for a past contest.
    Should return 404.
    """
    response = client.get('/book/Fall%20Classic/Simply%20Lift')
    assert response.status_code == 404

def test_get_booking_page_futur_contest(client):
    """
    Get the booking page for a futur contest.
    Should return 200 and the booking page.
    """
    response = client.get('/book/Spring%20Festival/Simply%20Lift')
    assert response.status_code == 200

def test_get_booking_page_futur_contest_not_loggin(client, _logout):
    """
    Get the booking page for a futur contest.
    But the user isn't logged.
    Should return 404.
    """
    response = client.get('/book/Spring%20Festival/')
    assert response.status_code == 404

def test_show_summary_doesnt_display_past_contest_links(_login):
    """
    Check that the booking links for past contests
    are not displayed on the showSummary page.
    """
    assert _login.status_code == 200
    assert '<a href="/book/Fall%20Classic/She%20Lifts">' not in _login.data.decode()

def test_show_summary_display_futur_contest_links(_login):
    """
    Check that the booking links for futur contests
    are displayed of the showSummary page.
    """
    assert _login.status_code == 200
    assert '<a href="/book/Spring%20Festival/She%20Lifts">' in _login.data.decode()

def test_show_summary_display_futur_contest_links_not_loggin(client, _logout):
    """
    Check that the booking links for futur contests
    throws a 404 for a not logged user.
    """
    response = client.get('/showSummary')
    assert response.status_code == 404
