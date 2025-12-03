"""
Unit tests for the bias term analyser.
"""

import pytest
from pathlib import Path

from inclusive_job_ad_analyser.analyser import JobAdAnalyser
from inclusive_job_ad_analyser.models import MatchResult


@pytest.fixture
def analyser():
    """Create analyser instance for testing."""
    return JobAdAnalyser(use_spacy=False)  # Use regex only for consistent tests


class TestJobAdAnalyser:
    """Tests for JobAdAnalyser class."""
    
    def test_analyser_initializes(self, analyser):
        """Test that analyser initializes with bias terms."""
        assert analyser is not None
        assert len(analyser.terms) > 0
    
    def test_empty_text_returns_no_matches(self, analyser):
        """Test that empty text returns no matches."""
        result = analyser.analyse("")
        assert result == []
        
        result = analyser.analyse("   ")
        assert result == []
    
    def test_detects_single_biased_term(self, analyser):
        """Test detection of a single biased term."""
        text = "We need a rockstar developer for our team."
        results = analyser.analyse(text)
        
        assert len(results) > 0
        rockstar_match = next((r for r in results if r.term == "rockstar"), None)
        assert rockstar_match is not None
        assert rockstar_match.category == "gender-coded"
        assert rockstar_match.count == 1
    
    def test_detects_multiple_instances(self, analyser):
        """Test detection of multiple instances of same term."""
        text = "We need a rockstar developer. Be a rockstar!"
        results = analyser.analyse(text)
        
        rockstar_match = next((r for r in results if r.term == "rockstar"), None)
        assert rockstar_match is not None
        assert rockstar_match.count == 2
        assert len(rockstar_match.positions) == 2
    
    def test_detects_multiple_different_terms(self, analyser):
        """Test detection of multiple different biased terms."""
        text = "Looking for a rockstar ninja developer who is young and energetic."
        results = analyser.analyse(text)
        
        terms_found = {r.term for r in results}
        assert "rockstar" in terms_found
        assert "ninja" in terms_found
        assert "young and energetic" in terms_found
    
    def test_case_insensitive_detection(self, analyser):
        """Test that detection is case-insensitive."""
        text = "We need a ROCKSTAR Developer."
        results = analyser.analyse(text)
        
        rockstar_match = next((r for r in results if r.term == "rockstar"), None)
        assert rockstar_match is not None
    
    def test_word_boundary_detection(self, analyser):
        """Test that word boundaries are respected."""
        # "rock" in "rocket" should not match "rockstar"
        text = "We need a rocket scientist."
        results = analyser.analyse(text)
        
        rockstar_match = next((r for r in results if r.term == "rockstar"), None)
        assert rockstar_match is None
    
    def test_context_exceptions_respected(self, analyser):
        """Test that context exceptions prevent false positives."""
        # "competitive salary" should not be flagged
        text = "We offer a competitive salary and benefits."
        results = analyser.analyse(text)
        
        competitive_match = next((r for r in results if r.term == "competitive"), None)
        assert competitive_match is None
    
    def test_context_exceptions_not_triggered_outside_context(self, analyser):
        """Test that terms are flagged when not in exception context."""
        text = "We need a competitive person to join our team."
        results = analyser.analyse(text)
        
        competitive_match = next((r for r in results if r.term == "competitive"), None)
        assert competitive_match is not None
    
    def test_captures_sentence_context(self, analyser):
        """Test that sentence context is captured."""
        text = "We need a rockstar. Someone who excels at coding."
        results = analyser.analyse(text)
        
        rockstar_match = next((r for r in results if r.term == "rockstar"), None)
        assert rockstar_match is not None
        assert len(rockstar_match.contexts) > 0
        assert "rockstar" in rockstar_match.contexts[0].lower()
    
    def test_various_bias_categories(self, analyser):
        """Test detection across different bias categories."""
        text = """
        We need a rockstar developer (gender-coded)
        Must be a digital native (ageist)
        Must be able to stand for long periods (ableist)
        Join our bro culture (culture-fit)
        Ivy League preferred (socioeconomic)
        """
        results = analyser.analyse(text)
        
        categories = {r.category for r in results}
        assert "gender-coded" in categories
        assert "ageist" in categories
        assert "ableist" in categories
        assert "culture-fit" in categories
        assert "socioeconomic" in categories
    
    def test_get_statistics(self, analyser):
        """Test statistics method."""
        stats = analyser.get_statistics()
        
        assert "total_terms" in stats
        assert "by_category" in stats
        assert "by_severity" in stats
        assert stats["total_terms"] > 0
        assert len(stats["by_category"]) > 0


class TestMatchResult:
    """Tests for MatchResult data model."""
    
    def test_match_result_creation(self):
        """Test creating a MatchResult."""
        match = MatchResult(
            term="rockstar",
            category="gender-coded",
            severity="high",
            suggestion="skilled professional",
            explanation="Masculine-coded term",
            count=2,
            positions=[10, 50],
            contexts=["We need a rockstar", "Be a rockstar!"]
        )
        
        assert match.term == "rockstar"
        assert match.count == 2
        assert len(match.positions) == 2
        assert len(match.contexts) == 2
