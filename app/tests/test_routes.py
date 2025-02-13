import pytest
from app import create_app

@pytest.fixture
def client():
    """Creates a test client for Flask app."""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_hello_world(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Hello from my_function!"}
