from flask import request
from .test_fixtures import client, _login, _logout, db_clubs


def test_view_index_get(client):
    """
    Should return 200, and check the url and content.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert 'Welcome to the GUDLFT Registration Portal!' in response.data.decode()

def test_view_index_forbiden_methods(client):
    """
    Tests the view index with firbiden methods.
    Should return 405.
    """
    responses = [
        client.post('/'),
        client.put('/'),
        client.patch('/'),
        client.delete('/')
    ]
    for response in responses:
        assert response.status_code == 405

def test_view_board_get(client):
    """
    Should return 200, and check the template and content.
    """
    response = client.get('/board')
    assert response.status_code == 200
    assert request.url == 'http://localhost/board'
    assert '<p>Iron Temple - Points available : 4</p>' in response.data.decode()

# Faire un multiple test avec post/put/delete...
def test_view_board_forbiden_methods(client):
    """
    Should return 405.
    """
    url = '/board'
    responses = [
        client.post(url),
        client.put(url),
        client.patch(url),
        client.delete(url)
    ]
    for response in responses:
        assert response.status_code == 405

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

def test_logout(_logout):
    """
    Should redirect (302) index page.
    """
    assert _logout.status_code == 302
    assert request.url == 'http://localhost/logout'
