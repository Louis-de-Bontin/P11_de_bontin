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