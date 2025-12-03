"""
Gradio web interface for the Inclusive Job Ad Analyser.

Run this module directly to start the web interface:
    python -m inclusive_job_ad_analyser.webapp
"""

import re
import json
import tempfile
from typing import Tuple, List, Optional, Dict, Any
from pathlib import Path

try:
    import gradio as gr
except ImportError:
    print("Error: Gradio is not installed.")
    print("Install it with: pip install gradio")
    exit(1)

from .analyser import JobAdAnalyser
from .cli import analyse_text
from .loaders import ConfigLoader
from .reporting import ReportGenerator

# Try to import scraper (optional)
try:
    from .scraper import JobAdScraper
    _HAS_SCRAPING = True
except ImportError:
    _HAS_SCRAPING = False


# Initialize analyser (global for performance)
analyser = JobAdAnalyser(use_spacy=True)
config = ConfigLoader()
scraper = JobAdScraper() if _HAS_SCRAPING else None
report_generator = ReportGenerator()


def highlight_biased_terms(text: str, matches: list) -> List[Tuple[str, str | None]]:
    """
    Create highlighted text annotations for Gradio.
    
    Args:
        text: Original text.
        matches: List of MatchResult objects.
        
    Returns:
        List of (text_segment, label) tuples for HighlightedText component.
    """
    if not matches:
        return [(text, None)]
    
    # Collect all positions with their labels
    highlights = []
    for match in matches:
        for pos in match.positions:
            highlights.append({
                'start': pos,
                'end': pos + len(match.term),
                'label': f"{match.category}",
                'severity': match.severity
            })
    
    # Sort by start position
    highlights.sort(key=lambda x: x['start'])
    
    # Build annotated segments
    segments = []
    last_end = 0
    
    for hl in highlights:
        # Add text before highlight
        if hl['start'] > last_end:
            segments.append((text[last_end:hl['start']], None))
        
        # Add highlighted segment
        segments.append((
            text[hl['start']:hl['end']],
            hl['label']
        ))
        
        last_end = max(last_end, hl['end'])
    
    # Add remaining text
    if last_end < len(text):
        segments.append((text[last_end:], None))
    
    return segments


def analyze_job_ad(
    text: str,
    show_suggestions: bool = True
) -> Tuple[float, str, str, str, List[Tuple[str, str | None]]]:
    """
    Analyze job ad and return results for Gradio interface.
    
    Args:
        text: Job ad text to analyze.
        show_suggestions: Whether to include suggestions in output.
        
    Returns:
        Tuple of (score, grade, category_breakdown, recommendations, highlighted_text)
    """
    if not text or not text.strip():
        return (
            100.0,
            "No text provided",
            "",
            "Please enter a job ad to analyze.",
            [(text, None)]
        )
    
    # Run analysis
    result = analyse_text(text, analyser, config)
    
    # Format results
    return format_analysis_results(result, text, show_suggestions)


def analyze_file(
    file: gr.File,
    show_suggestions: bool = True
) -> Tuple[float, str, str, str, List[Tuple[str, str | None]], str]:
    """Analyze job ad from uploaded file."""
    if file is None:
        return (
            100.0,
            "No file provided",
            "",
            "Please upload a file to analyze.",
            [("", None)],
            ""
        )
    
    try:
        # Read file content
        file_path = Path(file.name)
        text = file_path.read_text(encoding='utf-8')
        
        # Run analysis
        result = analyse_text(text, analyser, config)
        score, grade, category_md, recommendations_md, highlighted = format_analysis_results(
            result, text, show_suggestions
        )
        
        return (score, grade, category_md, recommendations_md, highlighted, text)
    
    except Exception as e:
        return (
            0.0,
            "Error",
            "",
            f"Error reading file: {str(e)}",
            [("", None)],
            ""
        )


def analyze_url(
    url: str,
    show_suggestions: bool = True
) -> Tuple[float, str, str, str, List[Tuple[str, str | None]], str, str]:
    """Scrape and analyze job ad from URL."""
    if not _HAS_SCRAPING:
        return (
            0.0,
            "Error",
            "",
            "⚠️ Web scraping not available. Install with: pip install requests beautifulsoup4",
            [("", None)],
            "",
            ""
        )
    
    if not url or not url.strip():
        return (
            100.0,
            "No URL provided",
            "",
            "Please enter a URL to scrape and analyze.",
            [("", None)],
            "",
            ""
        )
    
    try:
        # Scrape URL
        job_data = scraper.scrape(url)
        
        if 'error' in job_data:
            return (
                0.0,
                "Error",
                "",
                f"❌ Error scraping URL: {job_data['error']}",
                [("", None)],
                "",
                ""
            )
        
        text = job_data['text']
        title = f"{job_data['title']} at {job_data['company']}"
        
        # Run analysis
        result = analyse_text(text, analyser, config)
        score, grade, category_md, recommendations_md, highlighted = format_analysis_results(
            result, text, show_suggestions
        )
        
        return (score, grade, category_md, recommendations_md, highlighted, text, title)
    
    except Exception as e:
        return (
            0.0,
            "Error",
            "",
            f"❌ Error: {str(e)}",
            [("", None)],
            "",
            ""
        )


def search_and_analyze(
    query: str,
    source: str,
    location: str,
    max_results: int,
    show_suggestions: bool = True
) -> Tuple[str, str]:
    """Search job boards and analyze multiple results."""
    if not _HAS_SCRAPING:
        return (
            "⚠️ Web scraping not available. Install with: pip install requests beautifulsoup4",
            ""
        )
    
    if not query or not query.strip():
        return ("Please enter a search query.", "")
    
    try:
        # Search for jobs
        status_msg = f"🔍 Searching {source} for '{query}'..."
        if location:
            status_msg += f" in {location}"
        
        jobs = scraper.search_jobs(
            query=query,
            source=source,
            location=location,
            max_results=max_results
        )
        
        if not jobs:
            return ("❌ No jobs found matching your search.", "")
        
        # Analyze all jobs
        results_html = f"<h3>Found {len(jobs)} jobs - Analysis Results</h3><br>"
        all_results = []
        
        for idx, job in enumerate(jobs, 1):
            if 'error' in job:
                continue
            
            text = job['text']
            result = analyse_text(text, analyser, config)
            
            # Build result card
            grade_emoji = {
                "Excellent": "🎉",
                "Good": "✓",
                "Fair": "⚠️",
                "Poor": "❌"
            }.get(result.grade, "")
            
            score_color = "green" if result.overall_score >= 75 else "orange" if result.overall_score >= 60 else "red"
            
            results_html += f"""
            <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 8px;">
                <h4>{idx}. {job['title']} - {job['company']}</h4>
                <p><strong>Score:</strong> <span style="color: {score_color}; font-size: 1.2em;">{result.overall_score:.1f}/100</span> 
                   <strong>Grade:</strong> {result.grade} {grade_emoji}</p>
                <p><strong>Issues Found:</strong> {len(result.matches)}</p>
                <p><strong>Source:</strong> <a href="{job['url']}" target="_blank">{job['source']}</a></p>
                
                <details>
                    <summary><strong>Category Breakdown</strong></summary>
                    <ul>
            """
            
            for category, score in sorted(result.category_scores.items(), key=lambda x: x[1].score):
                cat_name = category.replace('-', ' ').title()
                results_html += f"<li>{cat_name}: {score.score:.1f}/100 ({score.issues_count} issues)</li>"
            
            results_html += "</ul></details>"
            
            if show_suggestions and result.matches:
                results_html += """
                <details>
                    <summary><strong>Issues & Suggestions</strong></summary>
                    <ul>
                """
                for match in result.matches[:5]:  # Show top 5
                    results_html += f"""
                    <li><strong>'{match.term}'</strong> ({match.category})
                        <br>→ Suggestion: {match.suggestion}</li>
                    """
                results_html += "</ul></details>"
            
            results_html += "</div>"
            
            all_results.append({
                'title': job['title'],
                'company': job['company'],
                'url': job['url'],
                'score': result.overall_score,
                'grade': result.grade,
                'issues': len(result.matches)
            })
        
        # Create downloadable CSV
        csv_data = "Title,Company,URL,Score,Grade,Issues\n"
        for r in all_results:
            csv_data += f'"{r["title"]}","{r["company"]}","{r["url"]}",{r["score"]},{r["grade"]},{r["issues"]}\n'
        
        return (results_html, csv_data)
    
    except Exception as e:
        return (f"❌ Error searching jobs: {str(e)}", "")


def format_analysis_results(
    result,
    text: str,
    show_suggestions: bool
) -> Tuple[float, str, str, str, List[Tuple[str, str | None]]]:
    """Format analysis results for display."""
    # Format category breakdown
    category_md = "### Category Scores\n\n"
    if result.category_scores:
        for category, score in sorted(
            result.category_scores.items(),
            key=lambda x: x[1].score
        ):
            cat_name = category.replace('-', ' ').title()
            score_val = score.score
            
            # Emoji based on score
            if score_val >= 80:
                emoji = "✅"
            elif score_val >= 60:
                emoji = "⚠️"
            else:
                emoji = "❌"
            
            category_md += (
                f"**{cat_name}:** {score_val:.1f}/100 {emoji} "
                f"({score.issues_count} issue(s))\n\n"
            )
    else:
        category_md += "No issues detected! 🎉\n\n"
    
    # Format recommendations
    recommendations_md = "### Recommendations\n\n"
    for rec in result.recommendations:
        recommendations_md += f"- {rec}\n"
    
    if result.positive_aspects:
        recommendations_md += "\n### Positive Aspects ✨\n\n"
        for aspect in result.positive_aspects:
            recommendations_md += f"- ✓ Contains '{aspect}'\n"
    
    # Format issues with suggestions
    issues_md = ""
    if result.matches and show_suggestions:
        issues_md = "\n\n### Detailed Issues\n\n"
        
        severity_order = ['critical', 'high', 'medium', 'low']
        for severity in severity_order:
            sev_matches = [m for m in result.matches if m.severity == severity]
            if not sev_matches:
                continue
            
            issues_md += f"#### {severity.upper()} Severity\n\n"
            
            for match in sev_matches:
                issues_md += f"**'{match.term}'** ({match.category}) - found {match.count}x\n"
                issues_md += f"- **Issue:** {match.explanation}\n"
                issues_md += f"- **Suggestion:** {match.suggestion}\n\n"
    
    recommendations_md += issues_md
    
    # Create highlighted text
    highlighted = highlight_biased_terms(text, result.matches)
    
    # Grade with emoji
    grade_emoji = {
        "Excellent": "🎉",
        "Good": "✓",
        "Fair": "⚠️",
        "Poor": "❌"
    }.get(result.grade, "")
    
    grade_display = f"{result.grade} {grade_emoji}"
    
    return (
        result.overall_score,
        grade_display,
        category_md,
        recommendations_md,
        highlighted
    )


def create_interface() -> gr.Blocks:
    """Create and configure the Gradio interface."""
    
    # Load examples
    examples = [
        [
            """Senior Software Engineer

We're looking for a rockstar developer to join our young and energetic team! 
Must be a digital native who can work in a fast-paced environment.

Requirements:
- Recent graduate or 2-5 years experience
- Aggressive problem solver
- Must be able to stand for long periods
- Join our bro culture and work hard, play hard mentality
- Beer o'clock every Friday!

We need someone who's crazy good at coding and can crush it under pressure.
""",
            True
        ],
        [
            """Senior Software Engineer

We're seeking a skilled professional to join our collaborative team.

Requirements:
- 2+ years of experience or equivalent skills
- Proactive problem solver
- Strong technical abilities
- Thrive in a dynamic, evolving environment

We offer:
- Flexible working arrangements
- Comprehensive parental leave
- Equal opportunity employer
- Accommodations available
- All backgrounds welcome
""",
            True
        ]
    ]
    
    with gr.Blocks(
        title="Inclusive Job Ad Analyzer",
        theme=gr.themes.Soft(),
        css="""
        .output-section { margin-top: 20px; }
        .tab-section { padding: 20px; }
        """
    ) as interface:
        
        gr.Markdown("""
        # 🔍 Inclusive Job Ad Analyzer
        
        **Detect biased language in job descriptions and get suggestions for more inclusive alternatives.**
        
        This tool helps identify potentially exclusionary language across multiple categories:
        Gender-coded • Ageist • Ableist • Culture-fit • Socioeconomic • Racial coding
        """)
        
        with gr.Tabs() as tabs:
            # Tab 1: Manual Text Input
            with gr.Tab("✍️ Manual Input"):
                gr.Markdown("### Paste your job description to analyze")
                
                with gr.Row():
                    with gr.Column(scale=1):
                        text_input = gr.Textbox(
                            label="Job Description",
                            placeholder="Paste your job ad here...",
                            lines=15,
                            max_lines=30
                        )
                        
                        with gr.Row():
                            text_analyze_btn = gr.Button("🔍 Analyze", variant="primary", scale=2)
                            text_clear_btn = gr.ClearButton([text_input], value="Clear", scale=1)
                        
                        text_show_suggestions = gr.Checkbox(
                            label="Show detailed suggestions",
                            value=True
                        )
                        
                        gr.Markdown("### 📝 Try Examples")
                        gr.Examples(
                            examples=examples,
                            inputs=[text_input, text_show_suggestions],
                            label="Load Example"
                        )
                    
                    with gr.Column(scale=1):
                        text_score = gr.Number(label="Inclusivity Score", precision=1)
                        text_grade = gr.Textbox(label="Grade")
                        text_categories = gr.Markdown(label="Category Breakdown")
                        text_recommendations = gr.Markdown(label="Recommendations")
                
                text_highlighted = gr.HighlightedText(
                    label="Analyzed Text (biased terms highlighted)",
                    combine_adjacent=True,
                    show_legend=True,
                    color_map={
                        "gender-coded": "red",
                        "ageist": "orange",
                        "ableist": "purple",
                        "culture-fit": "blue",
                        "socioeconomic": "brown",
                        "racial": "darkred",
                    },
                    elem_classes="output-section"
                )
                
                text_analyze_btn.click(
                    fn=analyze_job_ad,
                    inputs=[text_input, text_show_suggestions],
                    outputs=[text_score, text_grade, text_categories, text_recommendations, text_highlighted]
                )
            
            # Tab 2: File Upload
            with gr.Tab("📁 Upload File"):
                gr.Markdown("### Upload a job description file (.txt, .md, .doc)")
                
                with gr.Row():
                    with gr.Column(scale=1):
                        file_input = gr.File(
                            label="Upload Job Description File",
                            file_types=[".txt", ".md", ".doc", ".docx"],
                            type="filepath"
                        )
                        
                        file_analyze_btn = gr.Button("🔍 Analyze File", variant="primary")
                        
                        file_show_suggestions = gr.Checkbox(
                            label="Show detailed suggestions",
                            value=True
                        )
                        
                        file_text_display = gr.Textbox(
                            label="Extracted Text",
                            lines=10,
                            interactive=False
                        )
                    
                    with gr.Column(scale=1):
                        file_score = gr.Number(label="Inclusivity Score", precision=1)
                        file_grade = gr.Textbox(label="Grade")
                        file_categories = gr.Markdown(label="Category Breakdown")
                        file_recommendations = gr.Markdown(label="Recommendations")
                
                file_highlighted = gr.HighlightedText(
                    label="Analyzed Text",
                    combine_adjacent=True,
                    show_legend=True,
                    color_map={
                        "gender-coded": "red",
                        "ageist": "orange",
                        "ableist": "purple",
                        "culture-fit": "blue",
                        "socioeconomic": "brown",
                        "racial": "darkred",
                    },
                    elem_classes="output-section"
                )
                
                file_analyze_btn.click(
                    fn=analyze_file,
                    inputs=[file_input, file_show_suggestions],
                    outputs=[file_score, file_grade, file_categories, file_recommendations, file_highlighted, file_text_display]
                )
            
            # Tab 3: URL Scraper
            with gr.Tab("🌐 Scrape URL"):
                gr.Markdown("### Scrape and analyze a job posting from a URL")
                
                if not _HAS_SCRAPING:
                    gr.Markdown("⚠️ **Web scraping not available.** Install with: `pip install requests beautifulsoup4`")
                
                with gr.Row():
                    with gr.Column(scale=1):
                        url_input = gr.Textbox(
                            label="Job Posting URL",
                            placeholder="https://www.linkedin.com/jobs/view/...",
                            lines=1
                        )
                        
                        gr.Markdown("""
                        **Supported sites:**
                        - LinkedIn
                        - Indeed
                        - Glassdoor
                        - Generic career pages
                        """)
                        
                        url_analyze_btn = gr.Button("🔍 Scrape & Analyze", variant="primary")
                        
                        url_show_suggestions = gr.Checkbox(
                            label="Show detailed suggestions",
                            value=True
                        )
                        
                        url_job_title = gr.Textbox(
                            label="Scraped Job Title",
                            interactive=False
                        )
                        
                        url_text_display = gr.Textbox(
                            label="Scraped Text",
                            lines=8,
                            interactive=False
                        )
                    
                    with gr.Column(scale=1):
                        url_score = gr.Number(label="Inclusivity Score", precision=1)
                        url_grade = gr.Textbox(label="Grade")
                        url_categories = gr.Markdown(label="Category Breakdown")
                        url_recommendations = gr.Markdown(label="Recommendations")
                
                url_highlighted = gr.HighlightedText(
                    label="Analyzed Text",
                    combine_adjacent=True,
                    show_legend=True,
                    color_map={
                        "gender-coded": "red",
                        "ageist": "orange",
                        "ableist": "purple",
                        "culture-fit": "blue",
                        "socioeconomic": "brown",
                        "racial": "darkred",
                    },
                    elem_classes="output-section"
                )
                
                url_analyze_btn.click(
                    fn=analyze_url,
                    inputs=[url_input, url_show_suggestions],
                    outputs=[url_score, url_grade, url_categories, url_recommendations, url_highlighted, url_text_display, url_job_title]
                )
            
            # Tab 4: Job Board Search
            with gr.Tab("🔎 Search Jobs"):
                gr.Markdown("### Search job boards and analyze multiple positions")
                
                if not _HAS_SCRAPING:
                    gr.Markdown("⚠️ **Web scraping not available.** Install with: `pip install requests beautifulsoup4`")
                
                with gr.Row():
                    with gr.Column(scale=1):
                        search_query = gr.Textbox(
                            label="Search Query",
                            placeholder="e.g., software engineer, data analyst",
                            lines=1
                        )
                        
                        search_source = gr.Dropdown(
                            label="Job Board",
                            choices=["indeed", "linkedin", "glassdoor"],
                            value="indeed"
                        )
                        
                        search_location = gr.Textbox(
                            label="Location (optional)",
                            placeholder="e.g., New York, NY or Remote",
                            lines=1
                        )
                        
                        search_max_results = gr.Slider(
                            label="Max Results",
                            minimum=1,
                            maximum=20,
                            value=5,
                            step=1
                        )
                        
                        search_show_suggestions = gr.Checkbox(
                            label="Show detailed suggestions",
                            value=True
                        )
                        
                        search_btn = gr.Button("🔍 Search & Analyze", variant="primary", size="lg")
                    
                    with gr.Column(scale=2):
                        search_results = gr.HTML(label="Analysis Results")
                        
                        search_csv = gr.Textbox(
                            label="Download Results (CSV)",
                            lines=5,
                            interactive=False,
                            visible=False
                        )
                        
                        search_download_btn = gr.DownloadButton(
                            label="📥 Download CSV Report",
                            visible=True
                        )
                
                def search_with_download(query, source, location, max_results, show_suggestions):
                    html_results, csv_data = search_and_analyze(query, source, location, max_results, show_suggestions)
                    
                    if csv_data:
                        # Save CSV to temp file
                        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
                            f.write(csv_data)
                            csv_path = f.name
                        return html_results, csv_path
                    
                    return html_results, None
                
                search_btn.click(
                    fn=search_with_download,
                    inputs=[search_query, search_source, search_location, search_max_results, search_show_suggestions],
                    outputs=[search_results, search_download_btn]
                )
        
        # Info footer
        gr.Markdown("""
        ---
        
        ### ℹ️ About This Tool
        
        This analyzer uses a rule-based NLP approach with a curated dictionary of 50+ potentially biased terms. 
        The tool provides explanations and suggestions, but **human judgment is essential** - context matters!
        
        **Not a final authority** - Use this as a supportive tool to help write more inclusive job descriptions 
        that attract diverse talent.
        
        **How to Use:**
        1. **Manual Input**: Paste job description text directly
        2. **Upload File**: Upload .txt or .md files
        3. **Scrape URL**: Extract job ads from LinkedIn, Indeed, Glassdoor
        4. **Search Jobs**: Find and analyze multiple positions from job boards
        
        **Portfolio Project** by Olakunle Kuye | [GitHub](https://github.com/okuye/inclusive-job-ad-analyser)
        """)
    
    return interface


def main():
    """Launch the Gradio web interface."""
    interface = create_interface()
    
    print("\n" + "="*60)
    print("Starting Inclusive Job Ad Analyzer Web Interface")
    print("="*60 + "\n")
    
    interface.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True
    )


if __name__ == "__main__":
    main()
