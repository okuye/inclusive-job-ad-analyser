# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-03

### Added
- Initial release of Inclusive Job Ad Analyser
- Rule-based bias detection across 50+ terms
- Support for 6 bias categories (gender-coded, ageist, ableist, culture-fit, socioeconomic, racial)
- Multi-factor scoring algorithm (0-100 scale)
- Command-line interface with multiple output formats (text, JSON, CSV, Markdown)
- Gradio web interface with visual highlighting
- spaCy integration for improved tokenization
- Configurable scoring weights via YAML
- Context-aware exception handling
- Positive indicator detection
- Comprehensive test suite (80%+ coverage)
- Detailed documentation (README, METHODOLOGY, CONTRIBUTING)
- Example job ads (biased and neutral)
- MIT License

### Features
- Batch processing support for directories
- Stdin input support for piping
- Colored terminal output
- Category score breakdowns
- Actionable recommendations
- Length-normalized scoring
- Word boundary detection
- Case-insensitive matching

### Documentation
- Complete README with quick start
- Methodology explanation
- Contributing guidelines
- Example outputs
- API reference

---

## [Unreleased]

### Added
- **Web-first architecture**: Complete redesign with tabbed Gradio interface
- **Four input methods in web UI**: Manual input, file upload, URL scraping, job board search
- **Batch job search**: Search and analyze up to 20 positions simultaneously
- **CSV export**: Download analysis results for multiple jobs
- **Enhanced web UI**: Visual highlighting, expandable details, progress indicators
- **Multiple deployment options**: Docker, Docker Compose, cloud platforms
- **Simplified launcher**: `python -m inclusive_job_ad_analyser` launches web UI by default
- **Standalone script**: `run_app.py` with port and share options
- **Deployment guide**: Complete documentation for Docker, Hugging Face, Railway, Render, AWS/GCP/Azure
- Job board search functionality for finding and analyzing multiple jobs
- CLI arguments: `--search` for queries, `--source` for job board selection, `--location` for filtering, `--max-results` for limiting results
- Support for searching Indeed, LinkedIn, and Glassdoor job boards
- Web scraping functionality for extracting job ads from URLs
- Support for LinkedIn, Indeed, Glassdoor, and generic job sites
- CLI arguments: `--url` for single URLs, `--urls-file` for batch scraping
- `JobAdScraper` class with site-specific extractors and search methods
- Optional dependencies: requests and beautifulsoup4
- Test suite for scraper module
- Example URLs file for testing web scraping

### Changed
- **Default interface**: Web UI is now primary interface; CLI accessible via `--cli` flag
- **Documentation**: Reorganized to emphasize web interface first
- **README**: Updated with web-first quick start
- **QUICKSTART**: Simplified to 4 steps with web interface prominence

### Technical
- Added `__main__.py` for module execution
- Created `run_app.py` launcher script
- Added Dockerfile and docker-compose.yml
- Enhanced webapp.py with 4 tabbed input methods
- Integrated file upload handling
- Added HTML report generation for batch results

### Planned
- ML-based context scoring
- LLM integration for suggestions
- REST API endpoint
- Chrome extension
- Multi-language support
- VS Code extension
- Historical tracking and analytics
