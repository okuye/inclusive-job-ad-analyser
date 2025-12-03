# Methodology

## How the Inclusive Job Ad Analyser Works

### Overview

The tool uses a **rule-based NLP approach** with a curated dictionary of potentially biased terms. This design choice prioritizes **transparency and explainability** over black-box machine learning models.

---

## 1. Bias Detection Approach

### Rule-Based System

**Why rule-based?**
- **Transparent**: Users can see exactly why a term was flagged
- **Explainable**: Each flagged term has a clear explanation
- **Auditable**: The term dictionary can be reviewed and improved
- **Predictable**: Consistent results across runs
- **Fast**: No model inference overhead
- **Maintainable**: Non-technical stakeholders (HR professionals) can contribute to the term database

### Dictionary Structure

Each bias term includes:
- **Term**: The potentially biased word or phrase
- **Category**: Type of bias (gender-coded, ageist, ableist, etc.)
- **Severity**: Impact level (critical, high, medium, low)
- **Suggestion**: Inclusive alternative(s)
- **Explanation**: Why it's problematic
- **Context Exceptions**: Phrases where the term is acceptable

Example:
```csv
term,category,severity,suggestion,explanation,context_exceptions
competitive,gender-coded,medium,"driven|results-focused",Masculine-leaning term,competitive salary|competitive benefits
```

---

## 2. Text Analysis Pipeline

### Step 1: Text Processing

1. **Normalization**: Convert to lowercase for matching
2. **Tokenization**: Split into words and sentences
   - Uses spaCy if available for better accuracy
   - Falls back to regex-based splitting
3. **Sentence Segmentation**: Identify sentence boundaries for context

### Step 2: Pattern Matching

1. **Word Boundary Detection**: Use regex `\b` to match whole words only
   - "rock" in "rocket" won't match "rockstar"
2. **Case-Insensitive**: Match regardless of capitalization
3. **Position Tracking**: Record character offsets for each match
4. **Context Capture**: Extract surrounding sentence for each match

### Step 3: Context Filtering

1. **Exception Checking**: Skip matches in acceptable contexts
   - "competitive salary" is OK
   - "competitive personality" is flagged
2. **Deduplication**: Avoid flagging the same instance multiple times

---

## 3. Scoring Algorithm

### Overall Score (0-100 scale, higher is better)

The score combines multiple factors:

```
Raw Penalty = Σ (count × base_points × category_weight × severity_weight)

Length-Normalized Penalty = Raw Penalty / length_factor

Score = 100 - min(100, 20 × log(penalty + 1))
```

**Components:**

1. **Base Points**: Default 10 points per issue
2. **Category Weight**: How important this bias category is
   - Gender-coded: 0.25
   - Ageist: 0.25
   - Ableist: 0.25
   - Culture-fit: 0.15
   - Socioeconomic: 0.05
   - Racial: 0.05

3. **Severity Weight**: Impact multiplier
   - Critical: 2.0× (may violate law)
   - High: 1.5× (strong deterrent effect)
   - Medium: 1.0× (moderately problematic)
   - Low: 0.5× (subtle bias)

4. **Length Normalization**: Longer ads aren't automatically worse
   - Normalizes by word count relative to standard 100-word ad
   - Prevents unfair penalization of detailed job descriptions

5. **Logarithmic Scaling**: Prevents extreme scores
   - First few issues have high impact
   - Additional issues have diminishing penalty
   - Reflects reality: 3 issues vs 30 both indicate problems

### Category Scores

Per-category scoring (0-100):
```
Category Raw Score = Σ (count × severity_weight)
Category Penalty = min(50, raw_score × 10)
Category Score = max(0, 100 - penalty)
```

Tracks:
- Number of issues per category
- Maximum severity in category
- Category-specific score

### Grade Assignment

| Score Range | Grade | Meaning |
|-------------|-------|---------|
| 90-100 | Excellent | Minimal or no bias detected |
| 75-89 | Good | Few issues, easily corrected |
| 60-74 | Fair | Multiple issues requiring attention |
| 0-59 | Poor | Significant revision needed |

---

## 4. Recommendation Generation

### Priority-Based Recommendations

1. **Critical Issues**: Flag legal compliance risks first
2. **High Severity**: Identify strongly biased terms
3. **Category Analysis**: Highlight problem categories
4. **Actionable Advice**: Provide specific next steps

Example logic:
```python
if critical_issues > 0:
    "Remove X critically biased terms immediately - may violate law"
if high_severity_issues > 0:
    "Replace X strongly biased terms with neutral alternatives"
if category_score < 75:
    "Review [category] language: X issues detected"
```

---

## 5. Positive Indicator Detection

Identifies inclusive language to provide balanced feedback:

**Positive Indicators:**
- "equal opportunity employer"
- "diverse" / "diversity"
- "inclusive"
- "accommodations available"
- "flexible working"
- "parental leave"
- "all backgrounds"
- "equivalent experience"

**Impact:**
- Included in report
- Provides positive reinforcement
- Does NOT artificially inflate score (to maintain objectivity)

---

## 6. Context Awareness

### Current Capabilities

1. **Context Exceptions**: Pre-defined acceptable uses
   - "competitive salary" ✓ (not flagged)
   - "competitive personality" ✗ (flagged)

2. **Sentence-Level Context**: Shows surrounding text

### Limitations & Future Improvements

**Current Limitations:**
- Cannot fully understand semantic context
- May flag some acceptable uses
- Cannot detect implicit bias or subtle discrimination

**Planned Enhancements:**
1. **ML-Based Context Scoring**: Train classifier on context
2. **Dependency Parsing**: Understand grammatical relationships
3. **Named Entity Recognition**: Distinguish job titles from descriptions
4. **Sentiment Analysis**: Detect tone and implications

---

## 7. Research Basis

### Academic Foundation

**Key Research:**
- Gaucher, D., Friesen, J., & Kay, A. C. (2011). "Evidence that gendered wording in job advertisements exists and sustains gender inequality." *Journal of Personality and Social Psychology*
  - Found masculine-coded words deter women from applying
  - Identified specific gendered word lists

**Industry Standards:**
- EEOC (Equal Employment Opportunity Commission) guidelines
- Textio (commercial tool) findings on bias impact
- LinkedIn job ad research
- Harvard implicit bias research

### Term Curation Process

1. **Research-backed**: Terms drawn from academic studies
2. **Legal review**: Compliance with employment law
3. **Community input**: Open for contributions via GitHub
4. **Regular updates**: Dictionary evolves with language norms

---

## 8. Validation & Evaluation

### Testing Approach

1. **Unit Tests**: Individual components (detection, scoring)
2. **Integration Tests**: Full pipeline
3. **Regression Tests**: Known bias patterns
4. **Manual Review**: Expert evaluation of results

### Quality Metrics

- **Precision**: % of flagged terms that are actually problematic
- **Recall**: % of actual biased terms detected
- **False Positive Rate**: Acceptable uses incorrectly flagged
- **User Feedback**: Incorporated through GitHub issues

### Known Limitations

1. **Context Dependency**: Some terms acceptable in specific contexts
2. **Language Evolution**: What's biased changes over time
3. **Cultural Variation**: Different norms across regions
4. **Tone Detection**: Cannot detect patronizing or condescending tone
5. **Omission Bias**: Cannot detect what's *missing* (e.g., no benefits)

---

## 9. Ethical Considerations

### Design Principles

1. **Human-in-the-Loop**: Tool assists, doesn't decide
2. **Transparency**: Clear explanations for all flags
3. **Accountability**: Open-source, auditable logic
4. **Continuous Improvement**: Community-driven updates
5. **Privacy**: No data collection, runs locally

### Responsible Use

**This tool:**
- ✓ Helps identify potentially problematic language
- ✓ Provides educational explanations
- ✓ Suggests inclusive alternatives
- ✓ Supports fair hiring practices

**This tool does NOT:**
- ✗ Make final decisions
- ✗ Replace human judgment
- ✗ Guarantee legal compliance
- ✗ Eliminate all bias
- ✗ Judge the writer's intent

**Recommendations:**
- Review all flagged terms in context
- Consider your specific industry/role requirements
- Seek legal counsel for compliance questions
- Use as one tool among many for inclusive hiring

---

## 10. Technical Implementation

### Architecture

```
User Input (text)
    ↓
Text Processing (spaCy/regex)
    ↓
Pattern Matching (term dictionary)
    ↓
Context Filtering (exceptions)
    ↓
Scoring (multi-factor algorithm)
    ↓
Report Generation (text/JSON/web)
```

### Performance

- **Analysis Speed**: <1 second for typical job ad (200-500 words)
- **Memory**: ~50MB with spaCy model loaded
- **Scalability**: Can batch process hundreds of ads

### Extensibility

**Plugin Points:**
1. Custom bias term dictionaries
2. Alternative scoring algorithms
3. ML model integration
4. LLM-based suggestions
5. API endpoints for integration

---

## References

1. Gaucher, D., Friesen, J., & Kay, A. C. (2011). Evidence that gendered wording in job advertisements exists and sustains gender inequality. *JPSP*, 101(1), 109-128.

2. EEOC Guidelines on Discriminatory Language. https://www.eeoc.gov/

3. Textio. (2022). The Language of Bias in Job Ads. Industry Report.

4. Bohnet, I. (2016). *What Works: Gender Equality by Design*. Harvard University Press.

5. Applied Research on Ageism in Job Ads. Stanford Center on Longevity.
