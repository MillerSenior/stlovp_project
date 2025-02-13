import os
import pytest
from app.functions import get_survey_info, get_resident_survey_info, get_stakeholder_survey_info

@pytest.fixture
def mock_survey_directory(tmp_path):
    """
    Create temporary mock survey directories for testing.
    """
    resident_dir = tmp_path / "surveys" / "resident"
    stakeholder_dir = tmp_path / "surveys" / "stakeholder"
    
    resident_dir.mkdir(parents=True, exist_ok=True)
    stakeholder_dir.mkdir(parents=True, exist_ok=True)

    # Create mock files in resident
    (resident_dir / "survey1.json").touch()
    (resident_dir / "survey2.json").touch()

    # Create mock file in stakeholder
    (stakeholder_dir / "stakeholder_survey.csv").touch()

    return {"resident": str(resident_dir), "stakeholder": str(stakeholder_dir)}

def test_get_survey_info_no_files(tmp_path):
    """Test get_survey_info when directory exists but has no files."""
    empty_dir = tmp_path / "empty_surveys"
    empty_dir.mkdir()

    result = get_survey_info(str(empty_dir))
    assert result["exists"] is True
    assert result["file_count"] == 0
    assert result["file_names"] == []

def test_get_survey_info_with_files(mock_survey_directory):
    """Test get_survey_info when files exist in the directory."""
    resident_info = get_survey_info(mock_survey_directory["resident"])
    stakeholder_info = get_survey_info(mock_survey_directory["stakeholder"])

    assert resident_info["exists"] is True
    assert resident_info["file_count"] == 2
    assert set(resident_info["file_names"]) == {"survey1.json", "survey2.json"}

    assert stakeholder_info["exists"] is True
    assert stakeholder_info["file_count"] == 1
    assert set(stakeholder_info["file_names"]) == {"stakeholder_survey.csv"}

def test_get_survey_info_directory_not_exist():
    """Test get_survey_info when directory does not exist."""
    result = get_survey_info("non_existent_dir")
    assert result["exists"] is False
    assert result["file_count"] == 0
    assert result["file_names"] == []
