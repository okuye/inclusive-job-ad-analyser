# Contributing to Inclusive Job Ad Analyser

Thank you for your interest in improving this tool! Contributions are welcome and encouraged.

## Ways to Contribute

### 1. Add Bias Terms

The most valuable contribution is expanding our bias term dictionary.

**How to contribute terms:**

1. Check `data/bias_terms.csv` to ensure the term isn't already included
2. Research the term's problematic nature (academic sources, HR guidelines)
3. Add a new row with all required fields:
   - `term`: The biased word or phrase
   - `category`: One of: gender-coded, ageist, ableist, culture-fit, socioeconomic, racial
   - `severity`: One of: critical, high, medium, low
   - `suggestion`: Alternative phrasing (use | to separate multiple options)
   - `explanation`: Why this term is problematic
   - `context_exceptions`: Acceptable uses (optional, use | separator)

**Example:**
```csv
ambitious,gender-coded,low,"motivated|goal-oriented|driven",Can be masculine-coded but less severe,
```

**Term Guidelines:**
- ✓ Research-backed (cite sources in PR description)
- ✓ Clear explanation of why it's problematic
- ✓ Practical alternative suggestions
- ✓ Consider context (add exceptions if needed)
- ✗ Avoid overly broad terms that are rarely problematic
- ✗ Don't include terms that are only problematic in very specific contexts

### 2. Report False Positives

If the tool flags something it shouldn't:

1. Open an issue with:
   - The term that was incorrectly flagged
   - The context where it appeared
   - Why you believe it should not be flagged
2. We'll review and either:
   - Add a context exception
   - Adjust the term's severity
   - Remove it from the dictionary (if inappropriate)

### 3. Improve Documentation

Help others understand and use the tool:

- Fix typos or unclear explanations
- Add examples and use cases
- Improve installation instructions
- Translate documentation (future)
- Write blog posts or tutorials (link them in issues!)

### 4. Code Contributions

**Areas for improvement:**
- Better context awareness (NLP improvements)
- Additional output formats
- Integration with CI/CD tools
- Performance optimization
- UI/UX enhancements in Gradio app
- API development

**Before coding:**
1. Open an issue to discuss your idea
2. Wait for maintainer feedback
3. Fork the repository
4. Create a feature branch
5. Make your changes with tests
6. Submit a pull request

### 5. Report Bugs

Found a bug? Please report it!

**Include:**
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Any error messages

## Development Setup

```bash
# Clone the repository
git clone https://github.com/okuye/inclusive-job-ad-analyser.git
cd inclusive-job-ad-analyser

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Download spaCy model
python -m spacy download en_core_web_sm

# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html

# Format code
black src/ tests/

# Lint code
flake8 src/ tests/
```

## Code Style

- Use **Black** for formatting (line length: 88)
- Follow **PEP 8** conventions
- Add **type hints** where appropriate
- Write **docstrings** for public functions (Google style)
- Keep functions focused and testable

## Testing Requirements

All code contributions must include tests:

- **Unit tests** for new functions
- **Integration tests** for new features
- **Regression tests** for bug fixes
- Aim for **80%+ coverage** on new code

Run tests before submitting:
```bash
pytest
```

## Pull Request Process

1. **Fork & Branch**: Create a feature branch from `main`
2. **Code**: Make your changes with tests
3. **Test**: Ensure all tests pass
4. **Commit**: Use clear, descriptive commit messages
5. **PR**: Submit with description of changes
6. **Review**: Address any feedback from maintainers

**PR Title Format:**
- `feat: Add support for X`
- `fix: Resolve issue with Y`
- `docs: Update README`
- `test: Add tests for Z`
- `refactor: Improve performance of X`

## Bias Term Contribution Guidelines

### Severity Levels

**Critical** (Legal/Compliance Risk):
- Explicit discrimination (age, race, disability)
- Protected class violations
- Examples: "native English speaker", "OCD about quality"

**High** (Strong Deterrent Effect):
- Strongly gendered language
- Clear ageist implications
- Examples: "rockstar", "digital native"

**Medium** (Potentially Problematic):
- Subtly coded language
- Context-dependent issues
- Examples: "competitive", "aggressive"

**Low** (Subtle Bias):
- Minor gendered default language
- Common metaphors with problematic roots
- Examples: "guys", "blind to differences"

### Categories

**gender-coded**: Language that research shows deters specific genders
- Masculine-coded: dominant, competitive, ninja, rockstar
- Feminine-coded: supportive, nurturing (less problematic but reinforces stereotypes)

**ageist**: Language that discriminates based on age
- Direct: young, recent grad, digital native
- Indirect: fast-paced, tech-savvy, energetic

**ableist**: Language that discriminates against disabilities
- Physical: able-bodied, stand for hours
- Mental health: crazy, insane, OCD

**culture-fit**: Language that promotes homogeneity
- Examples: bro culture, work hard play hard, beer o'clock

**socioeconomic**: Class-based discrimination
- Examples: Ivy League, top-tier university

**racial**: Racial coding or discrimination
- Examples: articulate, professional appearance, native speaker

## Review Process

### For Term Additions:
1. Maintainer reviews research basis
2. Community feedback period (if controversial)
3. Decision within 1 week
4. Merged or feedback provided

### For Code Changes:
1. Automated tests must pass
2. Code review by maintainer
3. Discussion if needed
4. Merge or feedback

## Recognition

Contributors will be:
- Listed in `CONTRIBUTORS.md`
- Mentioned in release notes
- Credited in any papers or presentations

## Questions?

- Open an issue for questions
- Tag with `question` label
- Maintainers will respond within 48 hours

## Code of Conduct

### Our Pledge

We pledge to make participation in this project a harassment-free experience for everyone, regardless of:
- Age, body size, disability, ethnicity
- Gender identity and expression
- Level of experience, education
- Nationality, personal appearance, race
- Religion, sexual identity and orientation

### Our Standards

**Positive behavior:**
- Using welcoming and inclusive language
- Respecting differing viewpoints
- Accepting constructive criticism
- Focusing on what's best for the community

**Unacceptable behavior:**
- Harassment, trolling, or insulting comments
- Personal or political attacks
- Publishing others' private information
- Any conduct that would be inappropriate in a professional setting

### Enforcement

Report violations to [your.email@example.com]. All reports will be reviewed and investigated.

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make job ads more inclusive! 🎉
