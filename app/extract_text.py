import os
import json
import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
from app.models import Response, Survey
from app.console_logger import log_stage

# Set Tesseract OCR and Poppler paths
TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
POPPLER_PATH = r"C:\poppler-24.08.0\poppler-24.08.0\Library\bin"

# JSON storage path
DATASTORE_PATH = os.path.join(os.getcwd(), "survey_data.json")

def preprocess_image(image):
    """
    Preprocesses image for better OCR accuracy.
    - Converts to grayscale
    - Applies adaptive thresholding for better contrast
    """
    log_stage("Preprocessing Image... 🖼️")
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

def extract_text_from_pdf(pdf_path: str) -> list:
    """
    Extracts text from a PDF file using OCR.
    - Converts PDF pages to images
    - Applies preprocessing
    - Runs OCR using Tesseract
    """
    log_stage(f"Extracting Text from {pdf_path}... 📄")
    images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
    extracted_text = []

    for page_num, image in enumerate(images):
        log_stage(f"Processing Page {page_num + 1}... 🔄")
        processed_image = preprocess_image(image)
        text = pytesseract.image_to_string(processed_image)
        extracted_text.extend(text.split("\n"))

    log_stage("✅ Text Extraction Complete!")
    return extracted_text

def parse_survey_responses(survey_type: str, survey_id: str, extracted_text: list) -> Survey:
    """
    Parses extracted text into a structured survey object.
    - Detects questions based on numbering (1., 2., etc.)
    - Associates responses with questions
    - Supports multiple choice and written responses
    """
    responses = []
    current_question_id = None
    response_buffer = []

    for line in extracted_text:
        line = line.strip()
        if not line:
            continue  # Skip empty lines

        # Detect question numbers (e.g., "1. How interested are you...?")
        if line.endswith("?") or any(line.startswith(f"{i}.") for i in range(1, 21)):
            if current_question_id is not None and response_buffer:
                responses.append(Response(current_question_id, response_buffer))

            current_question_id = len(responses) + 1
            response_buffer = []
        elif current_question_id:
            response_buffer.append(line)

    # Add last response if there is any remaining data
    if current_question_id and response_buffer:
        responses.append(Response(current_question_id, response_buffer))

    return Survey(survey_type, survey_id, responses)

def save_to_json(survey_type: str, survey_folder: str):
    """
    Extracts text from all PDFs in the given folder and saves structured survey responses to JSON.
    - Detects new surveys and appends data without overwriting
    - Ensures correct survey categorization ("Resident" or "Stakeholder")
    - Prevents duplicate survey entries
    """
    log_stage(f"Processing {survey_type} Surveys... 📊")

    # Load or initialize the data store
    if os.path.exists(DATASTORE_PATH):
        with open(DATASTORE_PATH, "r", encoding="utf-8") as f:
            try:
                data_store = json.load(f)
            except json.JSONDecodeError:
                data_store = {"Resident": [], "Stakeholder": []}
    else:
        data_store = {"Resident": [], "Stakeholder": []}

    existing_surveys = {(s["survey_id"], s["survey_type"]) for s in data_store[survey_type]}

    for filename in os.listdir(survey_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(survey_folder, filename)
            log_stage(f"Extracting text from {filename}... 📄")

            extracted_text = extract_text_from_pdf(pdf_path)
            if extracted_text:
                survey = parse_survey_responses(survey_type, filename, extracted_text)

                if (survey.survey_id, survey.survey_type) not in existing_surveys:
                    data_store[survey_type].append(survey.to_dict())

    # Save the updated data store
    with open(DATASTORE_PATH, "w", encoding="utf-8") as f:
        json.dump(data_store, f, indent=4)

    log_stage(f"✅ Survey Data Saved to {DATASTORE_PATH}")

