from app import create_app

def test_app_creation():
    """Ensure Flask app initializes correctly."""
    app = create_app()
    assert app is not None
    assert app.config["TESTING"] is False  # Default should be False
