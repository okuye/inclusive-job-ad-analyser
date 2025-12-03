"""
Shared test fixtures and configuration.
"""

import pytest
from pathlib import Path


@pytest.fixture
def sample_biased_text():
    """Sample job ad with multiple biased terms."""
    return """
Senior Software Engineer

We're looking for a rockstar developer to join our young and energetic team!
Must be a digital native who can work in a fast-paced environment.

Requirements:
- Recent graduate or 2-5 years experience
- Aggressive problem solver who can dominate technical challenges
- Must be able to stand for long periods
- Join our bro culture and work hard, play hard mentality
- Beer o'clock every Friday!
- Ivy League preferred

We need someone who's crazy good at coding and can crush it under pressure.
"""


@pytest.fixture
def sample_neutral_text():
    """Sample job ad with inclusive language."""
    return """
Senior Software Engineer

We're seeking a skilled professional to join our collaborative team.

Requirements:
- 2+ years of experience or equivalent skills
- Proactive problem solver
- Strong technical abilities
- Thrive in a dynamic, evolving environment

We offer:
- Flexible working arrangements
- Comprehensive parental leave
- Equal opportunity employer
- Accommodations available
- All backgrounds welcome
- Competitive salary and benefits
"""


@pytest.fixture
def temp_job_ad_file(tmp_path, sample_biased_text):
    """Create a temporary file with a job ad."""
    file_path = tmp_path / "job_ad.txt"
    file_path.write_text(sample_biased_text)
    return file_path


@pytest.fixture
def temp_neutral_file(tmp_path, sample_neutral_text):
    """Create a temporary file with a neutral job ad."""
    file_path = tmp_path / "neutral_ad.txt"
    file_path.write_text(sample_neutral_text)
    return file_path
