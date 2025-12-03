"""
Utilities for loading configuration and data files.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import yaml
import pandas as pd

from .models import FlaggedTerm


class ConfigLoader:
    """Load and manage configuration files."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize config loader.
        
        Args:
            config_path: Path to settings.yaml. If None, uses default location.
        """
        if config_path is None:
            # Default to config/settings.yaml relative to package root
            package_dir = Path(__file__).parent.parent.parent
            config_path = package_dir / "config" / "settings.yaml"
        
        self.config_path = Path(config_path)
        self._config: Optional[Dict[str, Any]] = None
    
    def load(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if self._config is None:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f)
        return self._config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key (supports dot notation)."""
        config = self.load()
        keys = key.split('.')
        value = config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value


class BiasTermsLoader:
    """Load and manage bias terms database."""
    
    def __init__(self, terms_path: Optional[Path] = None):
        """
        Initialize terms loader.
        
        Args:
            terms_path: Path to bias_terms.csv. If None, uses default location.
        """
        if terms_path is None:
            # Default to data/bias_terms.csv relative to package root
            package_dir = Path(__file__).parent.parent.parent
            terms_path = package_dir / "data" / "bias_terms.csv"
        
        self.terms_path = Path(terms_path)
        self._terms: Optional[List[FlaggedTerm]] = None
    
    def load(self) -> List[FlaggedTerm]:
        """Load bias terms from CSV file."""
        if self._terms is None:
            df = pd.read_csv(self.terms_path)
            self._terms = []
            
            for _, row in df.iterrows():
                # Handle context exceptions (pipe-separated)
                exceptions = []
                if pd.notna(row.get('context_exceptions', '')):
                    exceptions_str = str(row['context_exceptions'])
                    if exceptions_str.strip():
                        exceptions = [e.strip() for e in exceptions_str.split('|')]
                
                term = FlaggedTerm(
                    term=row['term'],
                    category=row['category'],
                    severity=row['severity'],
                    suggestion=row['suggestion'],
                    explanation=row.get('explanation', ''),
                    context_exceptions=exceptions
                )
                self._terms.append(term)
        
        return self._terms
    
    def get_by_category(self, category: str) -> List[FlaggedTerm]:
        """Get all terms for a specific category."""
        terms = self.load()
        return [t for t in terms if t.category == category]
    
    def get_by_severity(self, severity: str) -> List[FlaggedTerm]:
        """Get all terms of a specific severity."""
        terms = self.load()
        return [t for t in terms if t.severity == severity]
