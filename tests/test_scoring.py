"""
Unit tests for scoring logic.
"""

import pytest
from inclusive_job_ad_analyser.scoring import (
    compute_bias_score,
    get_grade,
    compute_category_scores,
    detect_positive_indicators,
    generate_recommendations,
    get_severity_weight,
    get_category_weight,
)
from inclusive_job_ad_analyser.models import MatchResult


@pytest.fixture
def sample_matches():
    """Create sample match results for testing."""
    return [
        MatchResult(
            term="rockstar",
            category="gender-coded",
            severity="high",
            suggestion="skilled professional",
            explanation="Masculine-coded",
            count=1,
            positions=[10],
            contexts=["We need a rockstar developer"]
        ),
        MatchResult(
            term="digital native",
            category="ageist",
            severity="high",
            suggestion="tech-proficient",
            explanation="Age discrimination",
            count=1,
            positions=[50],
            contexts=["Must be a digital native"]
        ),
    ]


class TestScoring:
    """Tests for scoring functions."""
    
    def test_get_severity_weight(self):
        """Test severity weight retrieval."""
        assert get_severity_weight("critical") == 2.0
        assert get_severity_weight("high") == 1.5
        assert get_severity_weight("medium") == 1.0
        assert get_severity_weight("low") == 0.5
        assert get_severity_weight("unknown") == 1.0  # default
    
    def test_get_category_weight(self):
        """Test category weight retrieval."""
        assert get_category_weight("gender-coded") > 0
        assert get_category_weight("ageist") > 0
        assert get_category_weight("ableist") > 0
    
    def test_compute_bias_score_no_matches(self):
        """Test score computation with no matches."""
        score = compute_bias_score([], "This is a test text with about fifty words.")
        assert score == 100.0
    
    def test_compute_bias_score_with_matches(self, sample_matches):
        """Test score computation with matches."""
        text = "We need a rockstar developer. Must be a digital native."
        score = compute_bias_score(sample_matches, text)
        
        assert 0 <= score <= 100
        assert score < 100  # Should be penalized
    
    def test_compute_bias_score_multiple_severe_issues(self):
        """Test score with multiple severe issues."""
        matches = [
            MatchResult(
                term="bro culture",
                category="culture-fit",
                severity="critical",
                suggestion="inclusive culture",
                explanation="Exclusionary",
                count=1,
                positions=[0],
                contexts=["Join our bro culture"]
            ),
            MatchResult(
                term="young and energetic",
                category="ageist",
                severity="critical",
                suggestion="enthusiastic",
                explanation="Age discrimination",
                count=1,
                positions=[50],
                contexts=["young and energetic team"]
            ),
        ]
        
        text = "Join our bro culture. We're a young and energetic team."
        score = compute_bias_score(matches, text)
        
        # Should have lower score due to multiple critical issues
        assert score < 70
    
    def test_get_grade(self):
        """Test grade assignment."""
        assert get_grade(95) == "Excellent"
        assert get_grade(90) == "Excellent"
        assert get_grade(80) == "Good"
        assert get_grade(75) == "Good"
        assert get_grade(65) == "Fair"
        assert get_grade(60) == "Fair"
        assert get_grade(50) == "Poor"
        assert get_grade(0) == "Poor"
    
    def test_compute_category_scores(self, sample_matches):
        """Test category score computation."""
        scores = compute_category_scores(sample_matches)
        
        assert "gender-coded" in scores
        assert "ageist" in scores
        
        for category, score in scores.items():
            assert 0 <= score.score <= 100
            assert score.issues_count > 0
            assert score.max_severity in ["low", "medium", "high", "critical"]


class TestPositiveIndicators:
    """Tests for positive indicator detection."""
    
    def test_detect_positive_indicators(self):
        """Test detection of positive inclusive language."""
        text = """
        We are an equal opportunity employer committed to diversity.
        Flexible working arrangements available.
        All backgrounds welcome.
        """
        
        indicators = detect_positive_indicators(text)
        
        assert len(indicators) > 0
        assert any("equal opportunity" in i.lower() for i in indicators)
        assert any("diverse" in i.lower() or "diversity" in i.lower() for i in indicators)
        assert any("flexible working" in i.lower() for i in indicators)
    
    def test_no_positive_indicators(self):
        """Test text with no positive indicators."""
        text = "We need a developer to write code."
        indicators = detect_positive_indicators(text)
        
        assert len(indicators) == 0
    
    def test_case_insensitive_detection(self):
        """Test that detection is case-insensitive."""
        text = "We are an EQUAL OPPORTUNITY EMPLOYER."
        indicators = detect_positive_indicators(text)
        
        assert len(indicators) > 0


class TestRecommendations:
    """Tests for recommendation generation."""
    
    def test_generate_recommendations_no_issues(self):
        """Test recommendations with no issues."""
        recommendations = generate_recommendations([], {})
        
        assert len(recommendations) > 0
        assert any("no biased language" in r.lower() for r in recommendations)
    
    def test_generate_recommendations_with_critical(self):
        """Test recommendations with critical issues."""
        matches = [
            MatchResult(
                term="bro culture",
                category="culture-fit",
                severity="critical",
                suggestion="inclusive culture",
                explanation="Exclusionary",
                count=1,
                positions=[0],
                contexts=["bro culture"]
            )
        ]
        
        scores = compute_category_scores(matches)
        recommendations = generate_recommendations(matches, scores)
        
        assert len(recommendations) > 0
        assert any("critical" in r.lower() for r in recommendations)
    
    def test_generate_recommendations_with_high_severity(self):
        """Test recommendations with high severity issues."""
        matches = [
            MatchResult(
                term="rockstar",
                category="gender-coded",
                severity="high",
                suggestion="skilled professional",
                explanation="Masculine-coded",
                count=2,
                positions=[0, 50],
                contexts=["rockstar dev", "rockstar team"]
            )
        ]
        
        scores = compute_category_scores(matches)
        recommendations = generate_recommendations(matches, scores)
        
        assert len(recommendations) > 0
        assert any("high priority" in r.lower() or "priority" in r.lower() for r in recommendations)
    
    def test_recommendations_include_category_advice(self, sample_matches):
        """Test that recommendations include category-specific advice."""
        scores = compute_category_scores(sample_matches)
        recommendations = generate_recommendations(sample_matches, scores)
        
        assert len(recommendations) > 0
        # Should mention reviewing specific categories
        rec_text = " ".join(recommendations).lower()
        assert any(cat in rec_text for cat in ["gender", "age"])
