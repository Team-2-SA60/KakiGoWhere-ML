import pytest
from app.flaskapp import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello from Flask on DigitalOcean!" in response.data