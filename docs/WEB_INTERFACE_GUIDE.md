# Web Interface Guide

## Overview

The Inclusive Job Ad Analyzer now runs as a **web application** - no command line skills required! Simply launch the app and use your browser.

---

## Getting Started

### 1. Launch the App

```bash
# After installation, just run:
python -m inclusive_job_ad_analyser
```

This opens your browser to http://127.0.0.1:7860

---

## Four Ways to Analyze Job Ads

### Tab 1: ✍️ Manual Input

**Best for:** Quick analysis of draft job descriptions

1. Paste your job description into the text box
2. Check "Show detailed suggestions" (recommended)
3. Click "🔍 Analyze"
4. View results instantly:
   - Overall score and grade
   - Category breakdown
   - Detailed recommendations
   - Visual highlighting of biased terms

**Try the examples!** Click "Load Example" to see how it works.

---

### Tab 2: 📁 Upload File

**Best for:** Analyzing saved job descriptions

1. Click "Upload Job Description File" or drag & drop
2. Supports: .txt, .md, .doc, .docx files
3. Click "🔍 Analyze File"
4. View extracted text and analysis

**Workflow tip:** Save all your job descriptions as .txt files and upload them one by one for review.

---

### Tab 3: 🌐 Scrape URL

**Best for:** Analyzing existing job postings online

1. Copy the URL of a job posting from:
   - LinkedIn (linkedin.com/jobs/view/...)
   - Indeed (indeed.com/viewjob?jk=...)
   - Glassdoor (glassdoor.com/job-listing/...)
   - Any career page

2. Paste the URL
3. Click "🔍 Scrape & Analyze"
4. View:
   - Extracted job title and company
   - Full text from the posting
   - Complete bias analysis

**Note:** Requires optional dependencies:
```bash
pip install requests beautifulsoup4
```

---

### Tab 4: 🔎 Search Jobs

**Best for:** Researching multiple positions at once

1. Enter search query (e.g., "software engineer", "data analyst")
2. Select job board (Indeed, LinkedIn, or Glassdoor)
3. Add location (optional, e.g., "New York, NY" or "Remote")
4. Set max results (1-20)
5. Check "Show detailed suggestions"
6. Click "🔍 Search & Analyze"

**Results show:**
- Score and grade for each position
- Issues found count
- Company and title
- Link to original posting
- Expandable category breakdown
- Top 5 suggestions per job

**Download results:**
- Click "📥 Download CSV Report"
- Get spreadsheet with all jobs analyzed
- Perfect for comparing multiple companies

**Use cases:**
- Research how competitors write job ads
- Analyze industry trends in language
- Find best examples to model from
- Bulk check your company's posted jobs

---

## Understanding Results

### Inclusivity Score (0-100)
- **90-100 (Excellent) 🎉**: Ready to publish
- **75-89 (Good) ✓**: Minor issues, easy fixes
- **60-74 (Fair) ⚠️**: Multiple issues, revision recommended
- **0-59 (Poor) ❌**: Significant bias, major rewrite needed

### Category Breakdown
Each category is scored separately:
- **Gender-coded**: Masculine/feminine-coded words
- **Ageist**: Age-related bias
- **Ableist**: Disability-related bias
- **Culture-fit**: Homogeneity promotion
- **Socioeconomic**: Class-based assumptions
- **Racial**: Race-related coding

### Visual Highlighting
Biased terms are color-coded in the analyzed text:
- 🔴 Red: Gender-coded
- 🟠 Orange: Ageist
- 🟣 Purple: Ableist
- 🔵 Blue: Culture-fit
- 🟤 Brown: Socioeconomic
- ⚫ Dark Red: Racial

### Recommendations
For each issue found:
- **Term**: What was flagged
- **Category**: Type of bias
- **Issue**: Why it's problematic
- **Suggestion**: Alternative phrasing

---

## Tips for Best Results

### Writing Inclusive Job Ads

**DO:**
- Use gender-neutral language ("they" instead of "he/she")
- Focus on skills and outcomes, not personality traits
- Include flexibility and accommodation statements
- Mention diverse team and equal opportunity
- Use "you will" instead of "must have"

**DON'T:**
- Use sports/military metaphors ("ninja", "warrior", "dominate")
- Specify age-related terms ("recent graduate", "digital native")
- Require physical abilities unless essential
- Use culture-fit language ("culture add" is better)
- Make assumptions about background

### Iterative Process

1. Write your draft
2. Analyze in the tool
3. Review flagged terms
4. Revise using suggestions
5. Re-analyze until score is 75+
6. Have diverse team members review
7. Publish!

---

## Advanced Features

### Custom Port
```bash
python run_app.py --port 8080
```

### Public Sharing
```bash
# Creates temporary public URL
python run_app.py --share
```

### CLI Mode (for automation)
```bash
# Still available for power users
python -m inclusive_job_ad_analyser --cli examples/job_ad.md
```

---

## Deployment Options

### Docker (Recommended for teams)
```bash
docker-compose up -d
# Access at http://localhost:7860
```

### Cloud Deployment
- **Hugging Face Spaces**: Free public hosting
- **Railway**: Easy deployment from GitHub
- **Render**: Free tier available
- See [DEPLOYMENT.md](DEPLOYMENT.md) for details

---

## Troubleshooting

### "Module not found" error
Make sure you're in the virtual environment:
```bash
source .venv/bin/activate
```

### Web scraping not working
Install optional dependencies:
```bash
pip install requests beautifulsoup4
```

### Port already in use
Use a different port:
```bash
python run_app.py --port 8080
```

### spaCy model missing
Download the language model:
```bash
python -m spacy download en_core_web_sm
```

---

## Examples

### Example 1: Quick Draft Check

**Scenario:** You wrote a job description and want to check it before posting.

**Steps:**
1. Launch app: `python -m inclusive_job_ad_analyser`
2. Go to "Manual Input" tab
3. Paste your draft
4. Click "Analyze"
5. Review score and suggestions
6. Edit your draft based on recommendations
7. Paste updated version and re-analyze
8. Repeat until score is 75+

**Time:** 5-10 minutes

---

### Example 2: Competitive Analysis

**Scenario:** You want to see how competitors are writing job ads for similar roles.

**Steps:**
1. Launch app
2. Go to "Search Jobs" tab
3. Enter: "data analyst"
4. Select: "Indeed"
5. Location: "San Francisco, CA"
6. Max results: 10
7. Click "Search & Analyze"
8. Review all results
9. Download CSV for spreadsheet analysis
10. Identify best and worst examples

**Time:** 5 minutes + analysis time

---

### Example 3: Audit Existing Postings

**Scenario:** Your company has 15 jobs posted on LinkedIn that you want to audit.

**Steps:**
1. Create file `linkedin_urls.txt` with all job URLs (one per line)
2. Launch app
3. Go to "Scrape URL" tab
4. Copy/paste each URL one at a time
5. Document scores in a spreadsheet
6. OR use CLI for batch: `python -m inclusive_job_ad_analyser --cli --urls-file linkedin_urls.txt --format csv --output audit.csv`

**Time:** 1-2 minutes per job

---

### Example 4: Team Training

**Scenario:** Train HR team on inclusive language.

**Steps:**
1. Deploy app with Docker: `docker-compose up -d`
2. Share URL with team (http://your-server:7860)
3. Have team try the example job ads
4. Discuss why certain terms are flagged
5. Have each person paste a real job description
6. Review results together
7. Create team guidelines based on common issues

**Time:** 1 hour training session

---

## Feedback and Support

- **Issues**: https://github.com/okuye/inclusive-job-ad-analyser/issues
- **Documentation**: See README.md and other docs/
- **Contributions**: See CONTRIBUTING.md

---

## What's Next?

Future enhancements being considered:
- Save analysis history
- Compare multiple jobs side-by-side
- Export to PDF reports
- Browser extension for analyzing on job boards
- API endpoint for integrations
- More languages beyond English

**Your feedback shapes the roadmap!** Open an issue to suggest features.
