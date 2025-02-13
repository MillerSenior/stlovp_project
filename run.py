# import sys
# import pytest
# from app import create_app
# from app.functions import get_resident_survey_info, get_stakeholder_survey_info
# from app.console_logger import log_stage
# from app.extract_text import save_to_json

# def run_tests():
#     """Run tests and exit if any fail."""
#     exit_code = pytest.main(["-q", "--disable-warnings"])
#     if exit_code != 0:
#         log_stage("❌ Tests Failed!", "Fix the issues before running the app.")
#         sys.exit(1)

# if __name__ == '__main__':
#     run_tests()  # Run tests first

#     log_stage("Initializing Application... ⚙️")
#     app = create_app()

#     log_stage("Gathering Resident Survey Data... 📂")
#     resident_data = get_resident_survey_info()

#     log_stage("Gathering Stakeholder Survey Data... 📂")
#     stakeholder_data = get_stakeholder_survey_info()

#     # Extract text from all Resident survey PDFs and save them
#     log_stage("Extracting Resident Survey Responses... 📝")
#     save_to_json("Resident", "surveys/resident")

#     # Extract text from all Stakeholder survey PDFs and save them
#     log_stage("Extracting Stakeholder Survey Responses... 📝")
#     save_to_json("Stakeholder", "surveys/stakeholder")

#     log_stage("Finalizing Initialization... ✅", "All data loaded and saved successfully.")

#     print("\n🚀 STLOVP app is running...\n")
#     app.run(debug=True)
import sys
import time  # Import time module
import pytest
from app import create_app
from app.functions import get_resident_survey_info, get_stakeholder_survey_info
from app.console_logger import log_stage
from app.extract_text import save_to_json

def run_tests():
    """Run tests and exit if any fail."""
    start_time = time.time()  # Start test timing
    exit_code = pytest.main(["-q", "--disable-warnings"])
    end_time = time.time()  # End test timing
    duration = end_time - start_time

    if exit_code != 0:
        log_stage("❌ Tests Failed!", f"Fix the issues before running the app. (⏳ {duration:.2f} seconds)")
        sys.exit(1)
    log_stage("✅ Tests Passed!", f"All tests ran successfully. (⏳ {duration:.2f} seconds)")

if __name__ == '__main__':
    overall_start_time = time.time()  # Start full script timing

    run_tests()  # Run tests first

    log_stage("Initializing Application... ⚙️")
    app = create_app()

    log_stage("Gathering Resident Survey Data... 📂")
    resident_data = get_resident_survey_info()

    log_stage("Gathering Stakeholder Survey Data... 📂")
    stakeholder_data = get_stakeholder_survey_info()

    # Extract text from all Resident survey PDFs and save them
    log_stage("Extracting Resident Survey Responses... 📝")
    resident_start_time = time.time()
    save_to_json("Resident", "surveys/resident")
    resident_end_time = time.time()
    log_stage("Resident Survey Extraction Complete ✅", f"Time taken: ⏳ {resident_end_time - resident_start_time:.2f} seconds")

    # Extract text from all Stakeholder survey PDFs and save them
    log_stage("Extracting Stakeholder Survey Responses... 📝")
    stakeholder_start_time = time.time()
    save_to_json("Stakeholder", "surveys/stakeholder")
    stakeholder_end_time = time.time()
    log_stage("Stakeholder Survey Extraction Complete ✅", f"Time taken: ⏳ {stakeholder_end_time - stakeholder_start_time:.2f} seconds")

    log_stage("Finalizing Initialization... ✅", "All data loaded and saved successfully.")

    overall_end_time = time.time()  # End full script timing
    log_stage("Total Execution Time", f"⏳ {overall_end_time - overall_start_time:.2f} seconds")

    print("\n🚀 STLOVP app is running...\n")
    app.run(debug=True)
