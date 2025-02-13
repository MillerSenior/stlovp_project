import os
import json
import pytest
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


# Ensure correct import of fpdf
try:
    from fpdf import FPDF
except ImportError:
    raise ImportError("⚠️ 'fpdf' module not found! Install it using: pip install fpdf")

from app.extract_text import save_to_json, extract_text_from_pdf, DATASTORE_PATH
from app.models import Survey

@pytest.fixture
def mock_pdf(tmp_path):
    """Creates a valid mock PDF for testing."""
    pdf_path = tmp_path / "mock_survey.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="1. How interested are you in taking classes?", ln=True, align="L")
    pdf.cell(200, 10, txt="4 - Interested", ln=True, align="L")
    pdf.output(str(pdf_path))

    return str(pdf_path)



def test_extract_text_from_pdf(mock_pdf):
    """Test that text is correctly extracted from a sample PDF."""
    extracted_text = extract_text_from_pdf(mock_pdf)

    assert isinstance(extracted_text, list)
    assert len(extracted_text) > 0

    # Allow partial match to handle OCR number prefix variations
    found = any("How interested are you in taking classes" in line for line in extracted_text)
    assert found, f"Extracted text did not contain expected question. OCR output: {extracted_text}"



def test_save_to_json(mock_pdf, tmp_path):
    """Test extraction and saving process."""
    test_survey_type = "Resident"
    test_survey_folder = tmp_path / "resident"
    test_survey_folder.mkdir()

    # Copy mock PDF into the test folder
    pdf_copy = test_survey_folder / "mock_survey.pdf"
    with open(mock_pdf, "rb") as src, open(pdf_copy, "wb") as dest:
        dest.write(src.read())

    # Run the save_to_json function
    save_to_json(test_survey_type, str(test_survey_folder))

    # Ensure the JSON file was created
    assert os.path.exists(DATASTORE_PATH)

    with open(DATASTORE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert test_survey_type in data
    assert len(data[test_survey_type]) > 0
    assert "responses" in data[test_survey_type][0]
    assert len(data[test_survey_type][0]["responses"]) > 0


def test_survey_model():
    """Test that survey model correctly structures responses."""
    responses = [
        {"question_id": 1, "response": "4 - Interested"},
        {"question_id": 2, "response": "3 - Somewhat Important"}
    ]

    survey = Survey("Resident", "mock_survey.pdf", responses)
    survey_dict = survey.to_dict()

    assert survey_dict["survey_type"] == "Resident"
    assert survey_dict["survey_id"] == "mock_survey.pdf"
    assert isinstance(survey_dict["responses"], list)
    assert len(survey_dict["responses"]) == 2
