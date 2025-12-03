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

### Web Interface (Recommended)

```bash
# Start web app (easiest method)
python -m inclusive_job_ad_analyser

# Or use the launcher
python run_app.py
```

Open http://127.0.0.1:7860 in your browser and you'll see four tabs:
1. **Manual Input** - Paste job descriptions
2. **Upload File** - Drag & drop files
3. **Scrape URL** - Enter job posting URLs
4. **Search Jobs** - Search Indeed, LinkedIn, Glassdoor

### Command Line (Advanced)

```bash
# Analyse with CLI
python -m inclusive_job_ad_analyser --cli examples/biased_job_ad.md
```

## Analyse Your Own Job Ad (1 minute)

### Using Web Interface (No Code Required!)

Just open the web app and choose your method:

**Option 1: Manual Input Tab**
- Paste your job description
- Click "Analyze"
- Get instant results with visual highlighting

**Option 2: Upload File Tab**
- Drag and drop .txt, .md, or .doc files
- Click "Analyze File"
- View extracted text and analysis

**Option 3: Scrape URL Tab**
- Paste a LinkedIn, Indeed, or Glassdoor URL
- Click "Scrape & Analyze"
- Get job title, company, and full analysis

**Option 4: Search Jobs Tab**
- Enter search query (e.g., "software engineer")
- Select job board (Indeed, LinkedIn, Glassdoor)
- Add location (optional)
- Set max results (1-20)
- Click "Search & Analyze"
- Download CSV report of all results

**Note**: URL scraping and job search require optional dependencies:
```bash
pip install requests beautifulsoup4
```

### Using Command Line (Advanced Users)

```bash
# Search job boards
python -m inclusive_job_ad_analyser --cli --search "software engineer" --source indeed

# Scrape URL
python -m inclusive_job_ad_analyser --cli --url https://www.linkedin.com/jobs/view/123456

# Analyze file
python -m inclusive_job_ad_analyser --cli examples/biased_job_ad.md
```

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

### Batch Analysis of Multiple Job Postings

Use the **Search Jobs** tab in the web interface:
1. Enter your search query
2. Select job board
3. Set max results (up to 20)
4. Click "Search & Analyze"
5. Download CSV report with all results

### Analyzing Existing Job Postings

Use the **Scrape URL** tab:
1. Copy job posting URL from LinkedIn, Indeed, or Glassdoor
2. Paste into URL field
3. Click "Scrape & Analyze"
4. Review results and download report

### Quick Draft Review

Use the **Manual Input** tab:
1. Copy your draft job description
2. Paste into text field
3. Click "Analyze"
4. See highlighted biased terms instantly
5. Review suggestions and revise

### File-Based Workflow

Use the **Upload File** tab:
1. Save job descriptions as .txt or .md files
2. Drag and drop into upload area
3. Analyze and iterate

## Deployment Options

### Docker (Easiest for Teams)

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access at http://localhost:7860
```

### Manual Deployment

```bash
# Run on custom port
python run_app.py --port 8080

# Create public shareable link
python run_app.py --share
```

### Cloud Deployment

The app works out-of-the-box on:
- **Hugging Face Spaces** (free hosting)
- **Railway** 
- **Render**
- Any platform supporting Python + Gradio

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
