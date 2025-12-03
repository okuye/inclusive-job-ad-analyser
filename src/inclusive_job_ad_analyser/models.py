"""
Data models for bias analysis results.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class FlaggedTerm:
    """A potentially biased term from the dictionary."""
    term: str
    category: str
    severity: str
    suggestion: str
    explanation: str = ""
    context_exceptions: List[str] = field(default_factory=list)


@dataclass
class MatchResult:
    """Result of finding a biased term in text."""
    term: str
    category: str
    severity: str
    suggestion: str
    explanation: str
    count: int
    positions: List[int]
    contexts: List[str]


@dataclass
class CategoryScore:
    """Score breakdown for a specific bias category."""
    category: str
    score: float
    issues_count: int
    max_severity: str


@dataclass
class AnalysisResult:
    """Complete analysis result for a job ad."""
    text: str
    overall_score: float
    grade: str
    word_count: int
    matches: List[MatchResult]
    category_scores: Dict[str, CategoryScore]
    recommendations: List[str]
    positive_aspects: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "overall_score": self.overall_score,
            "grade": self.grade,
            "word_count": self.word_count,
            "category_scores": {
                cat: {
                    "score": score.score,
                    "issues_count": score.issues_count,
                    "max_severity": score.max_severity,
                }
                for cat, score in self.category_scores.items()
            },
            "issues_found": len(self.matches),
            "issues": [
                {
                    "term": m.term,
                    "category": m.category,
                    "severity": m.severity,
                    "count": m.count,
                    "suggestion": m.suggestion,
                    "explanation": m.explanation,
                    "positions": m.positions,
                    "contexts": m.contexts[:3],  # Limit contexts to first 3
                }
                for m in self.matches
            ],
            "recommendations": self.recommendations,
            "positive_aspects": self.positive_aspects,
        }
