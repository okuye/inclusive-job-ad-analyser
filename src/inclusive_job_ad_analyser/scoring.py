"""
Scoring logic for bias analysis.
"""

import math
from typing import List, Dict, Optional
from collections import defaultdict

from .models import MatchResult, CategoryScore
from .loaders import ConfigLoader


def get_severity_weight(severity: str, config: Optional[ConfigLoader] = None) -> float:
    """
    Get the numeric weight for a severity level.
    
    Args:
        severity: Severity level (critical, high, medium, low).
        config: Optional config loader. Uses defaults if None.
        
    Returns:
        Numeric weight for the severity.
    """
    if config:
        weight = config.get(f'severity_multipliers.{severity}')
        if weight is not None:
            return float(weight)
    
    # Default weights
    default_weights = {
        'critical': 2.0,
        'high': 1.5,
        'medium': 1.0,
        'low': 0.5,
    }
    return default_weights.get(severity, 1.0)


def get_category_weight(category: str, config: Optional[ConfigLoader] = None) -> float:
    """
    Get the numeric weight for a category.
    
    Args:
        category: Bias category.
        config: Optional config loader. Uses defaults if None.
        
    Returns:
        Numeric weight for the category.
    """
    if config:
        weight = config.get(f'category_weights.{category}')
        if weight is not None:
            return float(weight)
    
    # Default weights
    default_weights = {
        'gender-coded': 0.25,
        'ageist': 0.25,
        'ableist': 0.25,
        'culture-fit': 0.15,
        'socioeconomic': 0.05,
        'racial': 0.05,
    }
    return default_weights.get(category, 0.10)


def compute_category_scores(
    matches: List[MatchResult],
    config: Optional[ConfigLoader] = None
) -> Dict[str, CategoryScore]:
    """
    Compute per-category scores.
    
    Args:
        matches: List of bias term matches.
        config: Optional config loader.
        
    Returns:
        Dictionary mapping category names to CategoryScore objects.
    """
    category_data = defaultdict(lambda: {
        'issues': 0,
        'raw_score': 0.0,
        'max_severity': 'low'
    })
    
    severity_order = {'low': 0, 'medium': 1, 'high': 2, 'critical': 3}
    
    for match in matches:
        cat_data = category_data[match.category]
        cat_data['issues'] += match.count
        
        # Accumulate raw score
        sev_weight = get_severity_weight(match.severity, config)
        cat_data['raw_score'] += match.count * sev_weight
        
        # Track maximum severity
        if severity_order.get(match.severity, 0) > severity_order.get(cat_data['max_severity'], 0):
            cat_data['max_severity'] = match.severity
    
    # Convert to CategoryScore objects with normalized scores
    result = {}
    for category, data in category_data.items():
        # Normalize to 0-100 scale (lower is worse)
        # More issues = lower score
        raw = data['raw_score']
        # Use log scaling to prevent extreme penalties
        penalty = min(50, raw * 10)
        score = max(0, 100 - penalty)
        
        result[category] = CategoryScore(
            category=category,
            score=round(score, 1),
            issues_count=data['issues'],
            max_severity=data['max_severity']
        )
    
    return result


def compute_bias_score(
    matches: List[MatchResult],
    text: str,
    config: Optional[ConfigLoader] = None
) -> float:
    """
    Compute overall bias score (0-100, higher is better).
    
    The score considers:
    - Number and severity of biased terms
    - Categories represented
    - Text length normalization
    
    Args:
        matches: List of bias term matches.
        text: Full analysed text. Used for length normalization.
        config: Optional config loader for custom weights.
        
    Returns:
        Bias score from 0-100 (100 = no bias detected).
    """
    if not matches:
        return 100.0
    
    # Calculate word count (approximate)
    word_count = max(1, len(text.split()))
    
    # Get normalization factor from config
    norm_factor = 100  # default: 100 words = standard job ad
    if config:
        norm_factor = config.get('scoring.normalization_factor', norm_factor)
    
    # Calculate raw penalty points
    total_penalty = 0.0
    base_points = 10 if not config else config.get('scoring.base_points_per_issue', 10)
    
    for match in matches:
        cat_weight = get_category_weight(match.category, config)
        sev_weight = get_severity_weight(match.severity, config)
        match_penalty = match.count * base_points * cat_weight * sev_weight
        total_penalty += match_penalty
    
    # Normalize by text length
    if config and config.get('scoring.length_normalization', True):
        length_factor = max(0.5, min(2.0, word_count / norm_factor))
        total_penalty = total_penalty / length_factor
    
    # Convert penalty to 0-100 score (lower penalty = higher score)
    # Use logarithmic scaling to avoid extreme scores
    if total_penalty > 0:
        scaled_penalty = min(100, 20 * math.log(total_penalty + 1))
    else:
        scaled_penalty = 0
    
    score = max(0, 100 - scaled_penalty)
    return round(score, 1)


def get_grade(score: float) -> str:
    """
    Convert numeric score to letter grade.
    
    Args:
        score: Bias score (0-100).
        
    Returns:
        Grade string (Excellent, Good, Fair, Poor).
    """
    if score >= 90:
        return "Excellent"
    elif score >= 75:
        return "Good"
    elif score >= 60:
        return "Fair"
    else:
        return "Poor"


def detect_positive_indicators(text: str, config: Optional[ConfigLoader] = None) -> List[str]:
    """
    Detect positive inclusive language indicators in text.
    
    Args:
        text: Job ad text.
        config: Optional config loader.
        
    Returns:
        List of detected positive indicators.
    """
    # Get indicators from config or use defaults
    indicators = [
        "equal opportunity employer",
        "diverse",
        "diversity",
        "inclusive",
        "accommodations available",
        "flexible working",
        "parental leave",
        "accessibility",
        "underrepresented",
        "all backgrounds",
        "equivalent experience",
    ]
    
    if config:
        config_indicators = config.get('positive_indicators')
        if config_indicators:
            indicators = config_indicators
    
    text_lower = text.lower()
    found = []
    
    for indicator in indicators:
        if indicator.lower() in text_lower:
            found.append(indicator)
    
    return found


def generate_recommendations(
    matches: List[MatchResult],
    category_scores: Dict[str, CategoryScore]
) -> List[str]:
    """
    Generate actionable recommendations based on analysis.
    
    Args:
        matches: List of bias term matches.
        category_scores: Per-category scores.
        
    Returns:
        List of recommendation strings.
    """
    recommendations = []
    
    if not matches:
        recommendations.append("✓ No biased language detected - great job!")
        return recommendations
    
    # Priority recommendations by severity
    critical_matches = [m for m in matches if m.severity == 'critical']
    high_matches = [m for m in matches if m.severity == 'high']
    
    if critical_matches:
        count = sum(m.count for m in critical_matches)
        recommendations.append(
            f"🔴 CRITICAL: Remove {count} critically biased term(s) immediately - "
            "these may violate employment law"
        )
    
    if high_matches:
        count = sum(m.count for m in high_matches)
        recommendations.append(
            f"⚠️  HIGH PRIORITY: Replace {count} strongly biased term(s) with "
            "neutral alternatives"
        )
    
    # Category-specific recommendations
    problem_categories = [
        (cat, score) for cat, score in category_scores.items()
        if score.score < 90
    ]
    
    if problem_categories:
        # Sort by score (worst first)
        problem_categories.sort(key=lambda x: x[1].score)
        
        for category, score in problem_categories[:3]:  # Top 3 issues
            cat_name = category.replace('-', ' ').title()
            recommendations.append(
                f"📝 Review {cat_name} language: {score.issues_count} issue(s) detected"
            )
    
    # General advice
    total_issues = sum(m.count for m in matches)
    if total_issues <= 3:
        recommendations.append(
            "💡 You're close! Fix these few issues for an excellent score"
        )
    elif total_issues <= 7:
        recommendations.append(
            "💡 Consider using more neutral, inclusive language throughout"
        )
    else:
        recommendations.append(
            "💡 Significant revision recommended - focus on removing gendered, "
            "age-specific, and exclusionary terms"
        )
    
    return recommendations
