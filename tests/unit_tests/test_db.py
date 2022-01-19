import server
from .test_fixtures import mock_dbs, db_competitions, db_clubs


def test_loadClubs_should_return_list_of_clubs(mock_dbs):
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
    assert server.clubs == expected_value

def test_loadCompetition_should_return_list_of_competitions(mock_dbs):
    expected_value = [{
            "name": "Spring Festival",
            "date": "2022-03-27 10:00:00",
            "numberOfPlaces": "25"
        },{
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        }]
    assert server.competitions == expected_value