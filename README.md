# 🔍 Inclusive Job Ad Analyser

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**An NLP-powered tool for detecting biased language in job descriptions and suggesting inclusive alternatives.**

Designed for HR teams, recruiters, and organizations committed to fair hiring practices. This tool helps identify potentially exclusionary language across multiple bias categories and provides actionable recommendations.

---

## 🎯 Why This Matters

Job descriptions often contain subtle, unintended bias that can discourage qualified candidates from applying:

- **Gender-coded words** like "rockstar" or "aggressive" can deter women ([Gaucher et al., 2011](https://www.researchgate.net/publication/51072397_Evidence_That_Gendered_Wording_in_Job_Advertisements_Exists_and_Sustains_Gender_Inequality))
- **Ageist phrases** like "digital native" discriminate against older workers
- **Ableist language** excludes people with disabilities
- **Culture-fit coding** promotes homogeneity over diversity

Even a few problematic words can significantly reduce applicant diversity. This tool helps organizations write more inclusive job ads that attract broader, more qualified talent pools.

---

## ✨ Features

- 🔎 **Rule-based bias detection** across 50+ terms in 6 categories
- 📊 **Explainable scoring** (0-100 scale) with category breakdowns
- 💡 **Actionable suggestions** for every flagged term
- 🎨 **Multiple output formats**: CLI text, JSON, CSV, Markdown, Web UI
- 🌐 **Gradio web interface** with visual highlighting
- ⚡ **Fast analysis** (<1 second per job ad)
- 🔧 **Configurable** rules and scoring weights
- 🧪 **Well-tested** with 80%+ code coverage
- 📚 **Research-backed** term dictionary

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/okuye/inclusive-job-ad-analyser.git
cd inclusive-job-ad-analyser

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Optional: Install web scraping dependencies
pip install requests beautifulsoup4
```

### Web Interface (Recommended)

```bash
# Launch the web application (default method)
python -m inclusive_job_ad_analyser

# Or use the launcher script
python run_app.py

# With custom port
python run_app.py --port 8080

# Create public shareable link
python run_app.py --share
```

**Open http://127.0.0.1:7860 in your browser**

The web interface provides four ways to analyze job ads:
- ✍️ **Manual Input**: Paste job descriptions directly
- 📁 **File Upload**: Upload .txt, .md, .doc files
- 🌐 **URL Scraper**: Extract and analyze from LinkedIn, Indeed, Glassdoor
- 🔎 **Job Search**: Search job boards and analyze multiple positions at once

No command line required! Everything works through the browser.

### Command Line Interface

```bash
# Analyse a job ad file
python -m inclusive_job_ad_analyser --cli examples/biased_job_ad.md

# Search job boards and analyse results
python -m inclusive_job_ad_analyser --cli --search "software engineer" --source indeed --max-results 10

# Scrape and analyse job ad from URL
python -m inclusive_job_ad_analyser --cli --url https://www.linkedin.com/jobs/view/123456

# Analyse from stdin
cat job_ad.txt | python -m inclusive_job_ad_analyser.cli --stdin

# Batch process a directory
python -m inclusive_job_ad_analyser.cli --directory job_ads/ --format csv --output results.csv
```

### Web Interface

```bash
# Start the Gradio web app
python -m inclusive_job_ad_analyser.webapp

# Open browser to http://127.0.0.1:7860
```

---

## 📖 Example Output

### Input (Biased Job Ad):
```text
We're looking for a rockstar developer to join our young and energetic team!
Must be a digital native who can work in a fast-paced environment.
Join our bro culture - beer o'clock every Friday!
```

### Output:
```text
============================================================
INCLUSIVE JOB AD ANALYSIS REPORT
============================================================

Overall Score: 42.3/100 (Poor) ❌
Word Count: 32
Issues Found: 6

CATEGORY BREAKDOWN:
------------------------------------------------------------
Gender Coded         52.0/100 ⚠️  (2 issue(s), max: high)
Ageist              48.0/100 ⚠️  (2 issue(s), max: high)
Culture Fit         35.0/100 ❌  (2 issue(s), max: critical)

ISSUES DETECTED:
------------------------------------------------------------

HIGH SEVERITY:
1. 'rockstar' [gender-coded] (found 1x)
   Issue: Masculine-coded term that may deter women from applying
   Suggestion: skilled professional|expert|talented developer
   Context: "We're looking for a rockstar developer to join"

2. 'digital native' [ageist] (found 1x)
   Issue: Discriminates against older workers by implying only young people understand technology
   Suggestion: tech-proficient|digitally skilled|comfortable with technology
   Context: "Must be a digital native who can work"

CRITICAL SEVERITY:
3. 'bro culture' [culture-fit] (found 1x)
   Issue: Explicitly exclusionary language
   Suggestion: collaborative culture|inclusive environment
   Context: "Join our bro culture - beer o'clock"

RECOMMENDATIONS:
------------------------------------------------------------
🔴 CRITICAL: Remove 2 critically biased term(s) immediately - these may violate employment law
⚠️  HIGH PRIORITY: Replace 3 strongly biased term(s) with neutral alternatives
📝 Review Culture Fit language: 2 issue(s) detected
💡 Significant revision recommended - focus on removing gendered, age-specific, and exclusionary terms
```

---

## 🏗️ Architecture

### Project Structure

```
inclusive-job-ad-analyser/
├── src/inclusive_job_ad_analyser/
│   ├── __init__.py           # Package interface
│   ├── analyser.py           # Core bias detection engine
│   ├── scoring.py            # Scoring algorithms
│   ├── reporting.py          # Report generation
│   ├── loaders.py            # Configuration & data loading
│   ├── models.py             # Data models
│   ├── cli.py                # Command-line interface
│   └── webapp.py             # Gradio web interface
├── data/
│   └── bias_terms.csv        # Curated bias term dictionary
├── config/
│   └── settings.yaml         # Scoring weights & configuration
├── tests/                    # Comprehensive test suite
├── examples/                 # Sample job ads
├── docs/                     # Documentation
└── notebooks/                # Jupyter analysis notebooks
```

### Analysis Pipeline

```
Input Text
    ↓
[1] Text Processing (spaCy tokenization & sentence segmentation)
    ↓
[2] Pattern Matching (regex with word boundaries)
    ↓
[3] Context Filtering (check exceptions)
    ↓
[4] Multi-Factor Scoring (category × severity × frequency)
    ↓
[5] Report Generation (text/JSON/web UI)
```

---

## 📊 Bias Categories Detected

| Category | Description | Examples |
|----------|-------------|----------|
| **Gender-Coded** | Masculine/feminine-coded language | rockstar, ninja, aggressive, supportive |
| **Ageist** | Age discriminatory language | digital native, recent graduate, young |
| **Ableist** | Disability discriminatory language | able-bodied, crazy good, stand for hours |
| **Culture-Fit** | Homogeneity-promoting language | bro culture, beer o'clock, work hard play hard |
| **Socioeconomic** | Class-based discrimination | Ivy League preferred, top-tier university |
| **Racial** | Racial coding/discrimination | articulate, native English speaker |

See [`data/bias_terms.csv`](data/bias_terms.csv) for the complete list of 50+ terms.

---

## 🎓 Methodology

### Rule-Based Approach

This tool uses a **transparent, rule-based system** rather than a black-box ML model:

**Advantages:**
- ✅ Explainable - clear why each term is flagged
- ✅ Auditable - term list can be reviewed and improved
- ✅ Fast - no model inference overhead
- ✅ Predictable - consistent results
- ✅ Maintainable - HR professionals can contribute

**Scoring Formula:**
```
Raw Penalty = Σ (count × base_points × category_weight × severity_weight)
Normalized Penalty = Raw Penalty / length_factor
Score = 100 - min(100, 20 × log(penalty + 1))
```

**Key Features:**
- Length normalization (longer ads aren't automatically worse)
- Logarithmic scaling (diminishing penalty for additional issues)
- Configurable weights per category and severity
- Context-aware exceptions (e.g., "competitive salary" is OK)

See [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) for detailed explanation.

---

## 🔧 Configuration

Customize scoring and detection via `config/settings.yaml`:

```yaml
# Category weights (must sum to 1.0)
category_weights:
  gender-coded: 0.25
  ageist: 0.25
  ableist: 0.25
  culture-fit: 0.15
  socioeconomic: 0.05
  racial: 0.05

# Severity multipliers
severity_multipliers:
  critical: 2.0
  high: 1.5
  medium: 1.0
  low: 0.5

# Grade thresholds
grade_thresholds:
  excellent: 90
  good: 75
  fair: 60
  poor: 0
```

---

## 📚 CLI Reference

### Commands

```bash
# Analyse single file
python -m inclusive_job_ad_analyser.cli <file>

# Analyse from stdin
python -m inclusive_job_ad_analyser.cli --stdin

# Batch process directory
python -m inclusive_job_ad_analyser.cli --directory <path>

# Custom configuration
python -m inclusive_job_ad_analyser.cli <file> --config custom_settings.yaml

# Disable spaCy (regex only)
python -m inclusive_job_ad_analyser.cli <file> --no-spacy

# Show bias term statistics
python -m inclusive_job_ad_analyser.cli --stats
```

### Output Formats

```bash
# Text (default, colored)
python -m inclusive_job_ad_analyser.cli job_ad.txt

# JSON (for integration)
python -m inclusive_job_ad_analyser.cli job_ad.txt --format json

# CSV (for batch analysis)
python -m inclusive_job_ad_analyser.cli --directory ads/ --format csv --output results.csv

# Markdown
python -m inclusive_job_ad_analyser.cli job_ad.txt --format markdown

# Plain text (no colors)
python -m inclusive_job_ad_analyser.cli job_ad.txt --no-color
```

### Exit Codes

- `0` - Success, all scores ≥60
- `1` - Issues found, any score <60
- `130` - Interrupted by user

---

## 🌐 Web Interface

The Gradio web app provides an interactive interface with:

- 📝 Multi-line text input
- 📊 Visual score display with progress bars
- 🎨 **Highlighted text** with color-coded bias terms
- 💡 Detailed recommendations and suggestions
- 📋 Example job ads (biased vs. inclusive)
- 🎯 Category breakdown charts

**Launch:**
```bash
python -m inclusive_job_ad_analyser.webapp
```

**Access:** http://127.0.0.1:7860

---

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest

# With coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_analyser.py

# Run with verbose output
pytest -v
```

**Test Coverage:** 80%+

---

## 🤝 Contributing

Contributions are welcome! See [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) for guidelines.

**Ways to contribute:**
- 📝 Add bias terms to the dictionary (most valuable!)
- 🐛 Report bugs or false positives
- 💡 Suggest features or improvements
- 📚 Improve documentation
- 🔧 Submit code improvements

**Quick contribution:**
1. Fork the repo
2. Add terms to `data/bias_terms.csv`
3. Submit a pull request with research citations

---

## 🎯 Portfolio Highlights

This project demonstrates:

### NLP & AI Skills
- ✅ Rule-based NLP system design
- ✅ spaCy integration for text processing
- ✅ Pattern matching and regex expertise
- ✅ Configurable scoring algorithms
- ✅ Context-aware detection

### Software Engineering
- ✅ Clean architecture (separation of concerns)
- ✅ Comprehensive testing (unit, integration, regression)
- ✅ Multiple interfaces (CLI, web, API-ready)
- ✅ Configuration management
- ✅ Proper packaging (pyproject.toml)

### Ethics & Responsibility
- ✅ Addressing real-world bias problems
- ✅ Transparent, explainable AI
- ✅ Research-backed approach
- ✅ Human-in-the-loop design
- ✅ Privacy-preserving (no data collection)

### Professional Practice
- ✅ Comprehensive documentation
- ✅ Example-driven learning
- ✅ Contribution guidelines
- ✅ MIT licensed
- ✅ Production-ready code quality

---

## 🔮 Future Enhancements

### Planned Features

1. **ML-Based Context Scoring**
   - Train classifier on sentence context
   - Improve accuracy of context-dependent terms
   - Reduce false positives

2. **LLM Integration**
   - GPT-4/Claude for context analysis
   - Generate personalized suggestions
   - Explain implicit bias

3. **API Endpoint**
   - FastAPI REST API
   - Webhook support for ATS integration
   - Batch processing endpoint

4. **Chrome Extension**
   - Real-time analysis while writing
   - Integration with LinkedIn, Indeed
   - Inline suggestions

5. **Multi-Language Support**
   - Internationalization (i18n)
   - Language-specific bias terms
   - Cultural context awareness

6. **Advanced Analytics**
   - Historical tracking
   - Company benchmarking
   - Trend analysis over time

7. **VS Code Extension**
   - IDE integration for HR teams
   - Real-time linting
   - Inline fixes

---

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) for details.

You are free to:
- ✅ Use commercially
- ✅ Modify and distribute
- ✅ Use privately
- ✅ Include in larger projects

**Attribution appreciated but not required.**

---

## 🙏 Acknowledgments

### Research Foundation
- Gaucher, D., Friesen, J., & Kay, A. C. (2011). "Evidence that gendered wording in job advertisements exists and sustains gender inequality." *Journal of Personality and Social Psychology*

### Inspiration
- [Textio](https://textio.com/) - Commercial augmented writing platform
- EEOC Guidelines on Discriminatory Language
- Harvard Implicit Bias Research

### Tools & Libraries
- [spaCy](https://spacy.io/) - Industrial-strength NLP
- [Gradio](https://gradio.app/) - ML web interfaces
- [pandas](https://pandas.pydata.org/) - Data manipulation
- [pytest](https://pytest.org/) - Testing framework

---

## 📞 Contact & Support

**Author:** Olakunle Kuye

**GitHub:** [@okuye](https://github.com/okuye)

**Project Link:** [https://github.com/okuye/inclusive-job-ad-analyser](https://github.com/okuye/inclusive-job-ad-analyser)

### Get Help

- 📖 Read the [docs](docs/)
- 💬 Open an [issue](https://github.com/okuye/inclusive-job-ad-analyser/issues)
- 🐛 Report a [bug](https://github.com/okuye/inclusive-job-ad-analyser/issues/new)
- 💡 Request a [feature](https://github.com/okuye/inclusive-job-ad-analyser/issues/new)

---

## ⭐ Star This Project

If you find this tool useful, please ⭐ star the repository to help others discover it!

---

## 📊 Project Stats

- **Lines of Code:** ~2,500
- **Test Coverage:** 80%+
- **Bias Terms:** 50+
- **Supported Formats:** 4 (text, JSON, CSV, Markdown)
- **Python Version:** 3.10+
- **Dependencies:** 6 core, 3 optional

---

<div align="center">

**Built with ❤️ for fairer, more inclusive hiring practices**

[Report Bug](https://github.com/okuye/inclusive-job-ad-analyser/issues) · [Request Feature](https://github.com/okuye/inclusive-job-ad-analyser/issues) · [Contribute](docs/CONTRIBUTING.md)

</div>
