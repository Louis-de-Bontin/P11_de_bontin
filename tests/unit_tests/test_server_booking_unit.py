import pytest
from flask import request

import server
from .test_fixtures import client, _logout, _login


def test_get_booking_page_futur_contest(client):
    """
    Get the booking page for a futur contest.
    Should return 200 and the booking page.
    """
    response = client.get('/book/Spring%20Festival/Simply%20Lift')
    assert response.status_code == 200
    assert request.url == 'http://localhost/book/Spring%20Festival/Simply%20Lift'
    assert 'You can book between 1 and 12 places.' in response.data.decode()

def test_get_booking_page_past_contest(client):
    """
    Get the booking page for a past contest.
    Should return 404.
    """
    response = client.get('/book/Fall%20Classic/Simply%20Lift')
    assert response.status_code == 404

def test_get_booking_page_futur_contest_not_loggin(client, _logout):
    """
    Get the booking page for a futur contest.
    But the user isn't logged.
    Should return 404.
    """
    response = client.get('/book/Spring%20Festival/')
    assert response.status_code == 404

def test_get_booking_page_competition_not_found(client):
    """
    Get a fake competition.
    Should return 404.
    """
    response = client.get('/book/fake_competition/Simply%20Lift')
    assert response.status_code == 404
