"""
Core bias detection analysis engine.
"""

from typing import List, Optional, Set
import re
from pathlib import Path

from .models import FlaggedTerm, MatchResult
from .loaders import BiasTermsLoader

try:
    import spacy
    from spacy.language import Language
    _HAS_SPACY = True
except ImportError:
    _HAS_SPACY = False


class JobAdAnalyser:
    """
    Dictionary-driven, explainable analyser for biased terms in job ads.
    
    Uses rule-based pattern matching with optional spaCy integration for
    improved tokenization and context awareness.
    """
    
    def __init__(
        self,
        bias_terms_path: Optional[Path] = None,
        use_spacy: bool = True,
        spacy_model: str = "en_core_web_sm",
    ):
        """
        Initialize the analyser.
        
        Args:
            bias_terms_path: Path to bias terms CSV. Uses default if None.
            use_spacy: Whether to use spaCy for text processing.
            spacy_model: Name of spaCy model to load.
        """
        # Load bias terms
        loader = BiasTermsLoader(bias_terms_path)
        self.terms: List[FlaggedTerm] = loader.load()
        
        # Initialize spaCy if available and requested
        self._nlp: Optional['Language'] = None
        if use_spacy and _HAS_SPACY:
            try:
                self._nlp = spacy.load(
                    spacy_model,
                    disable=["ner", "tagger"]  # Disable unused components for speed
                )
            except OSError:
                print(f"Warning: spaCy model '{spacy_model}' not found. "
                      f"Run: python -m spacy download {spacy_model}")
                print("Falling back to regex-only mode.")
                self._nlp = None
    
    def _get_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences using spaCy or fallback regex.
        
        Args:
            text: Input text to split.
            
        Returns:
            List of sentences.
        """
        if self._nlp:
            doc = self._nlp(text)
            return [sent.text.strip() for sent in doc.sents]
        
        # Fallback: naive sentence splitting
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _find_sentence_for_offset(
        self,
        sentences: List[str],
        original_text: str,
        offset: int
    ) -> str:
        """
        Find the sentence containing a specific character offset.
        
        Args:
            sentences: List of sentences from the text.
            original_text: The complete original text.
            offset: Character offset to locate.
            
        Returns:
            The sentence containing the offset, or empty string.
        """
        running = 0
        for sent in sentences:
            # Find this sentence in the original text
            sent_start = original_text.find(sent, running)
            if sent_start == -1:
                running += len(sent) + 1
                continue
            
            sent_end = sent_start + len(sent)
            if sent_start <= offset <= sent_end:
                return sent
            
            running = sent_end
        
        return ""
    
    def _is_exception_context(self, term: FlaggedTerm, context: str) -> bool:
        """
        Check if term appears in an exception context.
        
        Args:
            term: The flagged term to check.
            context: The surrounding context.
            
        Returns:
            True if this is an exception case (should not be flagged).
        """
        if not term.context_exceptions:
            return False
        
        context_lower = context.lower()
        for exception in term.context_exceptions:
            if exception.lower() in context_lower:
                return True
        
        return False
    
    def analyse(self, text: str) -> List[MatchResult]:
        """
        Scan text for biased terms and return match results.
        
        Args:
            text: Job ad text to analyse.
            
        Returns:
            List of MatchResult objects for each biased term found.
        """
        if not text or not text.strip():
            return []
        
        results: List[MatchResult] = []
        lower_text = text.lower()
        sentences = self._get_sentences(text)
        
        # Track terms we've already matched to avoid duplicates
        seen_terms: Set[str] = set()
        
        for term in self.terms:
            term_key = term.term.lower()
            if term_key in seen_terms:
                continue
            
            # Create regex pattern with word boundaries
            # Escape special regex characters in the term
            escaped_term = re.escape(term_key)
            pattern = r'\b' + escaped_term + r'\b'
            
            positions: List[int] = []
            contexts: List[str] = []
            valid_matches = 0
            
            # Find all matches
            for match in re.finditer(pattern, lower_text):
                start = match.start()
                
                # Get sentence context
                sentence_context = self._find_sentence_for_offset(
                    sentences, text, start
                )
                
                # Check if this is an exception context
                if self._is_exception_context(term, sentence_context):
                    continue
                
                positions.append(start)
                contexts.append(sentence_context)
                valid_matches += 1
            
            # Only add to results if we found valid matches
            if valid_matches > 0:
                seen_terms.add(term_key)
                results.append(
                    MatchResult(
                        term=term.term,
                        category=term.category,
                        severity=term.severity,
                        suggestion=term.suggestion,
                        explanation=term.explanation,
                        count=valid_matches,
                        positions=positions,
                        contexts=contexts,
                    )
                )
        
        return results
    
    def get_statistics(self) -> dict:
        """
        Get statistics about the loaded bias terms.
        
        Returns:
            Dictionary with term counts by category and severity.
        """
        categories = {}
        severities = {}
        
        for term in self.terms:
            categories[term.category] = categories.get(term.category, 0) + 1
            severities[term.severity] = severities.get(term.severity, 0) + 1
        
        return {
            "total_terms": len(self.terms),
            "by_category": categories,
            "by_severity": severities,
        }
