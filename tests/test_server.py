import pytest

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

def test_loadClubs_should_return_list_of_clubs():
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
    assert server.loadClubs() == expected_value

def test_showSummary_should_redirect_to_welcome(client, db_clubs, mocker):
    """
    With an existing email, it should redirect to a new page.
    """
    mocker.patch.object(server, 'clubs', db_clubs)
    request = client.post('/showSummary',
        data={'email': 'kate@shelifts.co.uk'})
    assert request.status_code == 200
    assert 'Welcome, ' in request.data.decode()

def test_showSummary_should_redirect_to_same_page(client, db_clubs, mocker):
    """
    If the email doesn't exist, the user stays on the same
    page, but with an error message.
    """
    mocker.patch.object(server, 'clubs', db_clubs)
    request = client.post('/showSummary',
        data={'email': 'test@tast.com'})
    assert request.status_code == 200
    assert '<p>Your email doesn&#39;t exist.</p>' in request.data.decode()
