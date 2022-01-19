from http import server
import pytest
from .unit_tests.test_fixtures import client, mock_dbs, db_clubs, db_competitions, _login, _logout

import server

def test_saveCompetition(client, mock_dbs):
    """
    Save datas in competitions.json.
    """
    server.competitions.append({
            "name": "Strong crippled dwarf",
            "date": "2022-06-12 09:30:00",
            "numberOfPlaces": "40"
        })
    expected_value = [{
        "name": "Spring Festival",
        "date": "2022-03-27 10:00:00",
        "numberOfPlaces": "25"
    },{
        "name": "Fall Classic",
        "date": "2020-10-22 13:30:00",
        "numberOfPlaces": "13"
    },{
        "name": "Strong crippled dwarf",
        "date": "2022-06-12 09:30:00",
        "numberOfPlaces": "40"
    }]
    server.saveCompetitions(server.competitions)
    assert server.loadCompetitions() == expected_value

def test_saveClubs():
    """
    Save datas in clubs.json.
    """
    server.clubs.append({
        "name":"Bikini ropes",
        "email":"josianne@bikini-ropes.anu",
        "points":"8"
    })
    expected_value = [{
        "name":"Simply Lift",
        "email":"john@simplylift.co",
        "points":"4"
    },{
        "name":"Iron Temple",
        "email": "admin@irontemple.com",
        "points":"4"
    },{
        "name":"She Lifts",
        "email": "kate@shelifts.co.uk",
        "points":"12"
    },{
        "name":"Bikini ropes",
        "email":"josianne@bikini-ropes.anu",
        "points":"8"
    }]
    server.saveClubs(server.clubs)
    assert server.loadClubs() == expected_value

def test_show_summary_doesnt_display_past_contest_links(_login):
    """
    Check that the booking links for past contests
    are not displayed on the showSummary page.
    """
    assert '<p>Simply Lift - Points available : 8</p>' in _login.data.decode()
    assert _login.status_code == 200
    assert '<a href="/book/Fall%20Classic/She%20Lifts">' not in _login.data.decode()

def test_show_summary_display_futur_contest_links(_login):
    """
    Check that the booking links for futur contests
    are displayed of the showSummary page.
    """
    assert '<p>Simply Lift - Points available : 8</p>' in _login.data.decode()
    assert _login.status_code == 200
    assert '<a href="/book/Spring%20Festival/She%20Lifts">' in _login.data.decode()

def test_show_summary_display_futur_contest_links_not_loggin(client, _logout):
    """
    Check that the booking links for futur contests
    throws a 404 for a not logged user.
    """
    response = client.get('/showSummary')
    assert response.status_code == 404
