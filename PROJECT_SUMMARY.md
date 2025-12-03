# Project Summary - Inclusive Job Ad Analyser

## Overview

A production-ready NLP tool that detects biased language in job descriptions and suggests inclusive alternatives. Built to showcase applied NLP skills, clean architecture, and ethics awareness in a portfolio-ready format.

---

## Quick Stats

- **Language**: Python 3.10+
- **Lines of Code**: ~2,500
- **Test Coverage**: 80%+
- **Bias Terms**: 50+ curated terms
- **Categories**: 6 (gender, age, ability, culture, socioeconomic, racial)
- **Interfaces**: CLI + Web UI (Gradio)
- **Output Formats**: 4 (text, JSON, CSV, Markdown)

---

## Key Features

✅ **Rule-based NLP** - Transparent, explainable detection
✅ **spaCy integration** - Industrial-strength text processing
✅ **Multi-factor scoring** - Category × severity × frequency
✅ **Context-aware** - Exception handling for false positives
✅ **Comprehensive testing** - Unit, integration, and regression tests
✅ **Production-ready** - Clean architecture, proper packaging
✅ **Well-documented** - README, methodology, contributing guidelines

---

## File Structure

```
inclusive-job-ad-analyser/
├── README.md                      # Main documentation (portfolio showcase)
├── LICENSE                        # MIT License
├── requirements.txt               # Dependencies
├── pyproject.toml                 # Modern Python packaging
├── setup.py                       # Backward compatibility
├── CHANGELOG.md                   # Version history
│
├── src/inclusive_job_ad_analyser/
│   ├── __init__.py               # Package interface
│   ├── models.py                 # Data models (FlaggedTerm, MatchResult, etc.)
│   ├── loaders.py                # Config & data loading
│   ├── analyser.py               # Core bias detection engine (350 lines)
│   ├── scoring.py                # Scoring algorithms (250 lines)
│   ├── reporting.py              # Report generation (300 lines)
│   ├── cli.py                    # Command-line interface (280 lines)
│   └── webapp.py                 # Gradio web interface (250 lines)
│
├── data/
│   └── bias_terms.csv            # 50+ curated bias terms with metadata
│
├── config/
│   └── settings.yaml             # Scoring weights & configuration
│
├── tests/
│   ├── conftest.py               # Shared fixtures
│   ├── test_analyser.py          # Analyser unit tests (150 lines)
│   ├── test_scoring.py           # Scoring unit tests (180 lines)
│   └── test_integration.py       # Full pipeline tests (120 lines)
│
├── examples/
│   ├── biased_job_ad.md          # Example with issues
│   └── neutral_job_ad.md         # Example with inclusive language
│
└── docs/
    ├── QUICKSTART.md             # 5-minute getting started
    ├── METHODOLOGY.md            # Detailed technical explanation
    └── CONTRIBUTING.md           # Contribution guidelines
```

---

## Technical Highlights

### NLP & AI
- **Text Processing**: spaCy for tokenization, sentence segmentation
- **Pattern Matching**: Regex with word boundaries, case-insensitive
- **Context Filtering**: Exception handling for ambiguous terms
- **Scoring Algorithm**: Multi-factor with length normalization

### Software Engineering
- **Architecture**: Clean separation (analyser, scoring, reporting)
- **Testing**: pytest with 80%+ coverage
- **Packaging**: Modern pyproject.toml + legacy setup.py
- **Configuration**: YAML-based, customizable weights
- **CLI Design**: argparse with multiple output formats
- **Web UI**: Gradio with visual highlighting

### Data Management
- **CSV-based dictionary**: Easy to maintain, non-technical friendly
- **Structured metadata**: Category, severity, suggestions, exceptions
- **Version control**: Git-tracked for transparency

---

## Usage Examples

### CLI - Basic Analysis
```bash
python -m inclusive_job_ad_analyser.cli job_ad.txt
```

### CLI - JSON Output
```bash
python -m inclusive_job_ad_analyser.cli job_ad.txt --format json
```

### CLI - Batch Processing
```bash
python -m inclusive_job_ad_analyser.cli --directory ads/ --format csv -o results.csv
```

### Web Interface
```bash
python -m inclusive_job_ad_analyser.webapp
# Open http://127.0.0.1:7860
```

### Python API
```python
from inclusive_job_ad_analyser import JobAdAnalyser
from inclusive_job_ad_analyser.cli import analyse_text

analyser = JobAdAnalyser()
result = analyse_text("We need a rockstar developer...", analyser)
print(f"Score: {result.overall_score}/100")
print(f"Issues: {len(result.matches)}")
```

---

## Portfolio Value

### What This Project Demonstrates

1. **Applied NLP Skills**
   - Real-world problem solving
   - Text processing pipeline design
   - Pattern matching and context awareness
   - Scoring algorithm development

2. **Software Engineering**
   - Clean architecture and modularity
   - Comprehensive testing strategy
   - Multiple interface designs (CLI, web, API)
   - Configuration management
   - Proper Python packaging

3. **Ethics & Responsibility**
   - Addressing bias in AI/hiring
   - Transparent, explainable AI
   - Human-in-the-loop design
   - Research-backed approach

4. **Professional Practice**
   - Production-ready code quality
   - Comprehensive documentation
   - Contribution-friendly
   - Git best practices
   - Open-source licensing

### Interview Talking Points

**Q: Tell me about this project**
- Built an NLP tool that helps HR teams write inclusive job ads
- Detects biased language across 6 categories (gender, age, ability, etc.)
- Rule-based approach for transparency and explainability
- Multiple interfaces: CLI for automation, web UI for interactivity

**Q: What technical challenges did you face?**
- Context awareness: "competitive salary" is OK, "competitive personality" isn't
- Designed exception system to reduce false positives
- Scoring algorithm: balanced multiple factors (severity, category, frequency)
- Length normalization: ensure fair scoring regardless of ad length

**Q: How did you ensure quality?**
- 80%+ test coverage with unit, integration, and regression tests
- Research-backed term dictionary (cited academic papers)
- Manual evaluation with example job ads
- Clear documentation for maintainability

**Q: How would you extend this?**
- ML-based context scoring to improve accuracy
- LLM integration for personalized suggestions
- REST API for ATS (Applicant Tracking System) integration
- Historical tracking to show improvement over time

---

## Next Steps for Enhancement

### Near-Term (Easy Wins)
1. Add more bias terms (community contributions)
2. Improve documentation with video demo
3. Create GitHub Actions CI/CD pipeline
4. Add more example job ads

### Medium-Term (ML Integration)
1. Train context classifier on labeled data
2. Implement severity prediction model
3. Add sentiment analysis for tone detection
4. Build dashboard for analytics

### Long-Term (Production Features)
1. REST API with FastAPI
2. Authentication and rate limiting
3. Database for tracking/analytics
4. Chrome/VS Code extensions
5. Multi-language support

---

## Installation & Testing

### Quick Setup
```bash
git clone https://github.com/okuye/inclusive-job-ad-analyser.git
cd inclusive-job-ad-analyser
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Run Tests
```bash
pytest
pytest --cov=src --cov-report=html
```

### Try Examples
```bash
python -m inclusive_job_ad_analyser.cli examples/biased_job_ad.md
python -m inclusive_job_ad_analyser.cli examples/neutral_job_ad.md
```

---

## Research Foundation

### Key Papers
- Gaucher et al. (2011) - Gendered wording in job ads
- EEOC Guidelines - Discriminatory language
- Harvard Implicit Bias Research

### Bias Categories Based On
- **Gender**: Research on masculine/feminine word lists
- **Age**: ADEA (Age Discrimination in Employment Act) compliance
- **Ability**: ADA (Americans with Disabilities Act) guidelines
- **Culture**: DEI (Diversity, Equity, Inclusion) best practices

---

## License & Attribution

**License**: MIT - Free for commercial and personal use

**Attribution**: Appreciated but not required

**Research Citations**: Included in documentation

---

## Contact

**GitHub**: [@okuye](https://github.com/okuye)
**Project**: [inclusive-job-ad-analyser](https://github.com/okuye/inclusive-job-ad-analyser)

---

## Recognition & Achievements

✨ **Portfolio-Ready**: Professional quality codebase
🎓 **Research-Backed**: Academic foundations
🧪 **Well-Tested**: 80%+ coverage
📚 **Documented**: Comprehensive guides
🤝 **Open Source**: MIT licensed, contribution-friendly
🌐 **Accessible**: Multiple interfaces (CLI, web)
⚡ **Performant**: <1 second analysis time
🎯 **Practical**: Solves real-world problem

---

**Last Updated**: December 3, 2025
**Version**: 1.0.0
**Status**: Production Ready ✅
