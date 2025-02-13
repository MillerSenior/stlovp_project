from typing import List, Dict, Union
from app.console_logger import log_stage

class Response:
    """
    Represents a single response to a survey question.
    """
    def __init__(self, question_id: int, response: Union[str, int, List[str]]):
        """
        Initialize a response object.

        Args:
            question_id (int): The unique ID of the question.
            response (Union[str, int, List[str]]): The response value.
        """
        self.question_id = question_id
        self.response = response

    def to_dict(self) -> Dict:
        """Converts response data to a dictionary format."""
        return {
            "question_id": self.question_id,
            "response": self.response
        }

class Survey:
    """
    Represents a survey containing multiple questions and responses.
    """
    def __init__(self, survey_type: str, survey_id: str, responses: list):
        """
        Initialize a survey object.

        Args:
            survey_type (str): Either "Resident" or "Stakeholder".
            survey_id (str): Unique ID for the survey file.
            responses (list): List of response dictionaries.
        """
        if survey_type not in ["Resident", "Stakeholder"]:
            raise ValueError("Invalid survey type. Must be 'Resident' or 'Stakeholder'.")

        self.survey_type = survey_type
        self.survey_id = survey_id
        self.responses = responses

    def to_dict(self):
        """Converts survey data to dictionary."""
        return {
            "survey_type": self.survey_type,
            "survey_id": self.survey_id,
            "responses": [resp.to_dict() if hasattr(resp, "to_dict") else resp for resp in self.responses]
        }

