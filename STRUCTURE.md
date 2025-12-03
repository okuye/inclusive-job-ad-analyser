# Project Structure

```
inclusive-job-ad-analyser/
│
├── 📄 README.md                           # Main documentation (portfolio showcase)
├── 📄 PROJECT_SUMMARY.md                  # Quick reference guide
├── 📄 CHANGELOG.md                        # Version history
├── 📄 LICENSE                             # MIT License
├── 📄 requirements.txt                    # Python dependencies
├── 📄 pyproject.toml                      # Modern Python packaging config
├── 📄 setup.py                            # Legacy setup (backward compatibility)
├── 📄 .gitignore                          # Git ignore rules
│
├── 📁 src/
│   └── 📁 inclusive_job_ad_analyser/
│       ├── 📄 __init__.py                 # Package initialization
│       ├── 📄 models.py                   # Data models (FlaggedTerm, MatchResult, etc.)
│       ├── 📄 loaders.py                  # Configuration & data loading utilities
│       ├── 📄 analyser.py                 # ⭐ Core bias detection engine
│       ├── 📄 scoring.py                  # ⭐ Scoring algorithms & recommendations
│       ├── 📄 reporting.py                # Report generation (text/JSON/CSV/Markdown)
│       ├── 📄 cli.py                      # ⭐ Command-line interface
│       └── 📄 webapp.py                   # ⭐ Gradio web interface
│
├── 📁 data/
│   └── 📄 bias_terms.csv                  # ⭐ Curated dictionary of 50+ biased terms
│
├── 📁 config/
│   └── 📄 settings.yaml                   # Scoring weights & configuration
│
├── 📁 tests/
│   ├── 📄 __init__.py                     # Test package initialization
│   ├── 📄 conftest.py                     # Shared test fixtures
│   ├── 📄 test_analyser.py                # Unit tests for analyser
│   ├── 📄 test_scoring.py                 # Unit tests for scoring
│   └── 📄 test_integration.py             # Integration tests for full pipeline
│
├── 📁 examples/
│   ├── 📄 biased_job_ad.md                # Example job ad with bias (for demo)
│   └── 📄 neutral_job_ad.md               # Example inclusive job ad
│
├── 📁 docs/
│   ├── 📄 QUICKSTART.md                   # 5-minute getting started guide
│   ├── 📄 METHODOLOGY.md                  # ⭐ Detailed technical explanation
│   └── 📄 CONTRIBUTING.md                 # Contribution guidelines
│
└── 📁 notebooks/                          # (Future) Jupyter notebooks for analysis
    └── (empty - ready for exploration notebooks)

```

## Key Files Explained

### Core Implementation (⭐)

**`analyser.py`** (350 lines)
- Main bias detection engine
- spaCy integration for text processing
- Pattern matching with context filtering
- Sentence segmentation and context extraction

**`scoring.py`** (250 lines)
- Multi-factor scoring algorithm
- Category and severity weighting
- Grade assignment (Excellent/Good/Fair/Poor)
- Positive indicator detection
- Recommendation generation

**`cli.py`** (280 lines)
- Full-featured command-line interface
- Multiple input modes (file, stdin, directory)
- Multiple output formats (text, JSON, CSV, Markdown)
- Batch processing support
- Configuration override support

**`webapp.py`** (250 lines)
- Gradio-based web interface
- Visual text highlighting
- Interactive analysis
- Example job ads included
- Real-time feedback

**`bias_terms.csv`** (50+ terms)
- Curated dictionary of biased terms
- Research-backed entries
- Metadata: category, severity, suggestions, exceptions
- Easy to extend by contributors

**`METHODOLOGY.md`** (500+ lines)
- Complete technical documentation
- Algorithm explanations
- Research foundations
- Validation approach
- Limitations and future work

### Supporting Files

**`models.py`** (100 lines)
- Data classes for type safety
- FlaggedTerm, MatchResult, AnalysisResult
- Serialization methods

**`loaders.py`** (120 lines)
- Config loading from YAML
- Bias terms loading from CSV
- Path resolution
- Validation

**`reporting.py`** (300 lines)
- Text report with colors
- JSON serialization
- CSV row generation
- Markdown formatting

**`settings.yaml`**
- Category weights
- Severity multipliers
- Grade thresholds
- Positive indicators list

### Testing (450+ lines total)

**`test_analyser.py`** (150 lines)
- Analyser initialization
- Term detection accuracy
- Context exception handling
- Edge cases

**`test_scoring.py`** (180 lines)
- Score calculation
- Grade assignment
- Category scoring
- Recommendations
- Positive indicators

**`test_integration.py`** (120 lines)
- Full pipeline tests
- Example job ad tests
- Serialization tests
- Error handling

**`conftest.py`**
- Shared fixtures
- Sample texts
- Temporary file helpers

### Documentation

**`README.md`** (600+ lines)
- Project overview
- Feature list
- Installation instructions
- Usage examples
- Architecture diagram
- Portfolio highlights
- Future enhancements

**`QUICKSTART.md`** (150 lines)
- 5-minute tutorial
- Common use cases
- Troubleshooting

**`CONTRIBUTING.md`** (400+ lines)
- Contribution guidelines
- Term addition process
- Code standards
- PR process
- Code of conduct

**`PROJECT_SUMMARY.md`** (400+ lines)
- Quick reference
- Technical highlights
- Interview talking points
- Next steps

---

## File Statistics

| Type | Files | Lines |
|------|-------|-------|
| Core Python | 8 | ~2,000 |
| Test Python | 4 | ~450 |
| Documentation | 6 | ~2,500 |
| Configuration | 3 | ~100 |
| Examples | 2 | ~200 |
| **Total** | **23** | **~5,250** |

---

## Dependencies

### Core (Required)
- pandas >= 2.0.0
- PyYAML >= 6.0
- colorama >= 0.4.6
- spacy >= 3.7.0

### Optional
- gradio >= 4.0.0 (for web interface)

### Development
- pytest >= 7.4.0
- pytest-cov >= 4.1.0
- black >= 23.0.0
- flake8 >= 6.0.0
- mypy >= 1.5.0

---

## Entry Points

### CLI Command
```bash
job-ad-analyser <file>
# or
python -m inclusive_job_ad_analyser.cli <file>
```

### Web App
```bash
python -m inclusive_job_ad_analyser.webapp
```

### Python API
```python
from inclusive_job_ad_analyser import JobAdAnalyser
analyser = JobAdAnalyser()
results = analyser.analyse(text)
```

---

## Testing Coverage

```
src/inclusive_job_ad_analyser/
├── analyser.py        ████████████████░░  85%
├── scoring.py         ████████████████░░  82%
├── reporting.py       ███████████████░░░  78%
├── cli.py             ██████████████░░░░  72%
├── loaders.py         ████████████████░░  85%
├── models.py          ██████████████████  95%
└── webapp.py          ██████░░░░░░░░░░░░  35% (UI testing limited)

Overall: 80%+
```

---

Last Updated: December 3, 2025
