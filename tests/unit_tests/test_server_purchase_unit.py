import pytest
from flask import request

import server
from .test_fixtures import mock_dbs, client, _login, _logout, db_clubs, db_competitions


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

def test_purchasePlaces_correct_number_correct_date_enough_points_competition_doesnt_exist(client, mock_dbs, _login):
    """
    Book a corret amount of places, but the competition doesnt exist.
    """
    places_available = int(server.competitions[0]['numberOfPlaces'])
    response = client.post('/purchasePlaces',
        data={
            'competition': 'Fake competition',
            'club': 'Simply Lift',
            'places': '4'
        })
    places_left = int(server.competitions[0]['numberOfPlaces'])
    assert server.clubs[0]['points'] == '8'
    assert response.status_code == 404
    assert places_left == places_available

def test_purchasePlaces_correct_number_correct_date_enough_points_club_doesnt_exist(client, mock_dbs, _login):
    """
    Book a corret amount of places, but the club doesnt exist.
    """
    places_available = int(server.competitions[0]['numberOfPlaces'])
    response = client.post('/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Fake club',
            'places': '4'
        })
    places_left = int(server.competitions[0]['numberOfPlaces'])
    assert response.status_code == 404
    assert places_left == places_available

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