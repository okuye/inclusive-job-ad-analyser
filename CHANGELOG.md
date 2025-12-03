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

### Planned
- ML-based context scoring
- LLM integration for suggestions
- REST API endpoint
- Chrome extension
- Multi-language support
- VS Code extension
- Historical tracking and analytics
