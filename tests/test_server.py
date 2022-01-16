import server


class TestLoadFunctions:
    print('I made some changes in branch #1')
    pass

def test_loadClubs_should_return_list_of_clubs():
    expected_value = [{
        "name":"Simply Lift",
        "email":"john@simplylift.co",
        "points":"13"
    },{
        "name":"Iron Temple",
        "email": "admin@irontemple.com",
        "points":"4"
    },{   "name":"She Lifts",
        "email": "kate@shelifts.co.uk",
        "points":"12"
    }]
    assert server.loadClubs() == expected_value