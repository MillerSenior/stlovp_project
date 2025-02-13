import pytest
from app.models import Response, Survey

def test_response_creation():
    """Test that a response object is correctly created."""
    response = Response(1, "5 - Very Interested")
    assert response.question_id == 1  # Correct attribute
    assert response.response == "5 - Very Interested"


def test_response_to_dict():
    """Test that response objects convert properly to dictionaries."""
    response = Response(10, "Bachelor’s degree")
    assert response.to_dict() == {
        "question_id": 10,  # Fix: Ensure correct attribute reference
        "response": "Bachelor’s degree"
    }


def test_survey_creation():
    """Test survey creation with valid types."""
    responses = [
        Response(1, "3 - Somewhat Interested"),
        Response(2, "I want to learn job skills.")
    ]
    survey = Survey("Resident", "resident_survey1.pdf", responses)

    assert survey.survey_type == "Resident"
    assert survey.survey_id == "resident_survey1.pdf"
    assert len(survey.responses) == 2


def test_survey_invalid_type():
    """Test that an invalid survey type raises an error."""
    with pytest.raises(ValueError):
        Survey("InvalidType", "mock_survey.pdf", [])


def test_survey_to_dict():
    """Test conversion of survey data to dictionary format."""
    responses = [
        Response(1, 4),  # Corrected format
        Response(2, ["Job Skills", "Life Skills"])  # Corrected format
    ]
    survey = Survey("Resident", "mock_survey.pdf", responses)

    assert survey.to_dict() == {
        "survey_type": "Resident",
        "survey_id": "mock_survey.pdf",
        "responses": [
            {"question_id": 1, "response": 4},  # Ensure structure matches models.py
            {"question_id": 2, "response": ["Job Skills", "Life Skills"]}
        ]
    }

