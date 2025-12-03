"""
Inclusive Job Ad Analyser
==========================

An NLP-powered tool for detecting biased language in job descriptions
and suggesting inclusive alternatives.

This package provides:
- Rule-based bias detection across multiple categories
- Configurable scoring and severity weighting
- Multiple output formats (text, JSON, web UI)
- Explainable results with actionable recommendations
"""

__version__ = "1.0.0"
__author__ = "Olakunle Kuye"

from .analyser import JobAdAnalyser, MatchResult, FlaggedTerm
from .scoring import compute_bias_score, get_grade

__all__ = [
    "JobAdAnalyser",
    "MatchResult",
    "FlaggedTerm",
    "compute_bias_score",
    "get_grade",
]
