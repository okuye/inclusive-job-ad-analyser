"""
Integration tests for the full analysis pipeline.
"""

import pytest
from pathlib import Path

from inclusive_job_ad_analyser.analyser import JobAdAnalyser
from inclusive_job_ad_analyser.cli import analyse_text
from inclusive_job_ad_analyser.loaders import ConfigLoader


@pytest.fixture
def analyser():
    """Create analyser for integration tests."""
    return JobAdAnalyser(use_spacy=False)


@pytest.fixture
def config():
    """Load configuration for tests."""
    return ConfigLoader()


class TestFullPipeline:
    """Integration tests for complete analysis pipeline."""
    
    def test_analyse_biased_text_full_pipeline(self, analyser, config, sample_biased_text):
        """Test full analysis of biased job ad."""
        result = analyse_text(sample_biased_text, analyser, config)
        
        # Should detect issues
        assert len(result.matches) > 0
        assert result.overall_score < 100
        
        # Should have category scores
        assert len(result.category_scores) > 0
        
        # Should have recommendations
        assert len(result.recommendations) > 0
        
        # Should be graded
        assert result.grade in ["Excellent", "Good", "Fair", "Poor"]
    
    def test_analyse_neutral_text_full_pipeline(self, analyser, config, sample_neutral_text):
        """Test full analysis of neutral job ad."""
        result = analyse_text(sample_neutral_text, analyser, config)
        
        # Should detect few or no issues
        assert len(result.matches) <= 2  # "competitive" in benefits context
        
        # Should have high score
        assert result.overall_score >= 85
        
        # Should detect positive indicators
        assert len(result.positive_aspects) > 0
        
        # Should be well graded
        assert result.grade in ["Excellent", "Good"]
    
    def test_multiple_categories_detected(self, analyser, config, sample_biased_text):
        """Test that multiple bias categories are detected."""
        result = analyse_text(sample_biased_text, analyser, config)
        
        categories = {match.category for match in result.matches}
        
        # Should detect at least 3 different categories
        assert len(categories) >= 3
        
        # Specific categories should be present
        assert "gender-coded" in categories
        assert "ageist" in categories
    
    def test_severity_levels_detected(self, analyser, config, sample_biased_text):
        """Test that different severity levels are detected."""
        result = analyse_text(sample_biased_text, analyser, config)
        
        severities = {match.severity for match in result.matches}
        
        # Should have multiple severity levels
        assert len(severities) >= 2
    
    def test_result_serialization(self, analyser, config, sample_biased_text):
        """Test that result can be serialized to dict."""
        result = analyse_text(sample_biased_text, analyser, config)
        
        data = result.to_dict()
        
        assert "overall_score" in data
        assert "grade" in data
        assert "issues" in data
        assert "category_scores" in data
        assert "recommendations" in data
        
        # Check structure
        assert isinstance(data["issues"], list)
        assert isinstance(data["category_scores"], dict)
    
    def test_empty_text_handling(self, analyser, config):
        """Test handling of empty text."""
        result = analyse_text("", analyser, config)
        
        assert result.overall_score == 100
        assert len(result.matches) == 0
    
    def test_short_text_handling(self, analyser, config):
        """Test handling of very short text."""
        text = "Join our team."
        result = analyse_text(text, analyser, config)
        
        assert result.overall_score > 0
        assert result.word_count > 0
    
    def test_long_text_handling(self, analyser, config):
        """Test handling of longer job ads."""
        # Create a longer text by repeating sections
        long_text = """
Senior Software Engineer

We're seeking skilled professionals to join our team.
        """ * 10
        
        result = analyse_text(long_text, analyser, config)
        
        assert result.word_count > 100
        assert result.overall_score >= 0
    
    def test_special_characters_handling(self, analyser, config):
        """Test handling of special characters and formatting."""
        text = """
        Senior Engineer 💻
        
        Requirements:
        • Strong skills
        • Team player
        
        Salary: $100,000-$150,000
        """
        
        result = analyse_text(text, analyser, config)
        
        # Should handle without errors
        assert result.overall_score >= 0
        assert isinstance(result.matches, list)
