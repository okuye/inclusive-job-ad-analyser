# Quick Start Guide

This guide will get you analyzing job ads in 5 minutes.

## Installation (2 minutes)

```bash
# Clone and navigate
git clone https://github.com/okuye/inclusive-job-ad-analyser.git
cd inclusive-job-ad-analyser

# Setup Python environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Try It Out (1 minute)

### Command Line

```bash
# Analyse the biased example
python -m inclusive_job_ad_analyser.cli examples/biased_job_ad.md

# Analyse the neutral example
python -m inclusive_job_ad_analyser.cli examples/neutral_job_ad.md
```

### Web Interface

```bash
# Start web app
python -m inclusive_job_ad_analyser.webapp

# Open http://127.0.0.1:7860 in browser
# Paste a job ad and click "Analyze"
```

## Analyse Your Own Job Ad (2 minutes)

### Option 1: Save to file

```bash
# Create a file with your job ad
cat > my_job_ad.txt << 'EOF'
Senior Developer

We need a rockstar engineer to join our young team...
EOF

# Analyse it
python -m inclusive_job_ad_analyser.cli my_job_ad.txt
```

### Option 2: Use stdin

```bash
echo "We need a rockstar developer" | python -m inclusive_job_ad_analyser.cli --stdin
```

### Option 3: Web interface

Just paste your text into the web app!

## Understanding the Output

```text
Overall Score: 42/100 (Poor) ❌
```
- **90-100 (Excellent)**: Minimal bias, ready to publish
- **75-89 (Good)**: Few issues, quick fixes needed
- **60-74 (Fair)**: Multiple issues, revision recommended
- **0-59 (Poor)**: Significant bias, major revision needed

```text
Issues Found: 6

'rockstar' [gender-coded] (found 1x)
   Issue: Masculine-coded term that may deter women
   Suggestion: skilled professional|expert|talented developer
```

For each issue:
- **Term**: The problematic word/phrase
- **Category**: Type of bias
- **Issue**: Why it's problematic
- **Suggestion**: Alternative phrasing

## Common Use Cases

### Batch Processing Multiple Job Ads

```bash
# Put all job ads in a folder
mkdir job_ads
# ... add your .txt files

# Analyse all and get CSV report
python -m inclusive_job_ad_analyser.cli --directory job_ads/ --format csv --output results.csv
```

### JSON for Integration

```bash
# Get JSON output for programmatic use
python -m inclusive_job_ad_analyser.cli my_ad.txt --format json > result.json
```

### Custom Configuration

```bash
# Use custom scoring weights
python -m inclusive_job_ad_analyser.cli my_ad.txt --config custom_settings.yaml
```

## Next Steps

- 📖 Read the full [README](../README.md)
- 🔬 Understand the [Methodology](METHODOLOGY.md)
- 🤝 Learn how to [Contribute](CONTRIBUTING.md)
- 🧪 Run tests: `pytest`
- 📊 View statistics: `python -m inclusive_job_ad_analyser.cli --stats`

## Troubleshooting

### "spaCy model not found"

```bash
python -m spacy download en_core_web_sm
```

### "Module not found"

Make sure you're in the virtual environment:
```bash
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

### Still stuck?

Open an issue: https://github.com/okuye/inclusive-job-ad-analyser/issues

---

Happy analysing! 🎉
