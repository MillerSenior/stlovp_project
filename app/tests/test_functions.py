import pytest
from app.functions import my_function

def test_my_function():
    """Test the `my_function` to ensure it returns the expected message."""
    response = my_function()
    assert response == {"message": "Hello from my_function!"}
