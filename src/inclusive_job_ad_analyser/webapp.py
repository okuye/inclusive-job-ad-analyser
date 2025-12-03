"""
Gradio web interface for the Inclusive Job Ad Analyser.

Run this module directly to start the web interface:
    python -m inclusive_job_ad_analyser.webapp
"""

import re
from typing import Tuple, List
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


# Initialize analyser (global for performance)
analyser = JobAdAnalyser(use_spacy=True)
config = ConfigLoader()


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
        theme=gr.themes.Soft()
    ) as interface:
        
        gr.Markdown("""
        # 🔍 Inclusive Job Ad Analyzer
        
        **Detect biased language in job descriptions and get suggestions for more inclusive alternatives.**
        
        This tool helps identify potentially exclusionary language across multiple categories:
        - Gender-coded terms
        - Ageist language
        - Ableist language
        - Culture-fit bias
        - Socioeconomic bias
        - Racial coding
        
        Simply paste your job description below and click "Analyze" to get started.
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                input_text = gr.Textbox(
                    label="Job Description",
                    placeholder="Paste your job ad here...",
                    lines=15,
                    max_lines=25
                )
                
                with gr.Row():
                    analyze_btn = gr.Button("🔍 Analyze", variant="primary", scale=2)
                    clear_btn = gr.ClearButton([input_text], value="Clear", scale=1)
                
                show_suggestions = gr.Checkbox(
                    label="Show detailed suggestions",
                    value=True
                )
            
            with gr.Column(scale=1):
                with gr.Row():
                    score_output = gr.Number(
                        label="Inclusivity Score",
                        precision=1,
                        scale=1
                    )
                    grade_output = gr.Textbox(
                        label="Grade",
                        scale=1
                    )
                
                category_output = gr.Markdown(
                    label="Category Breakdown"
                )
                
                recommendations_output = gr.Markdown(
                    label="Recommendations & Suggestions"
                )
        
        # Highlighted text output (full width)
        with gr.Row():
            highlighted_output = gr.HighlightedText(
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
                }
            )
        
        # Examples
        gr.Markdown("### 📝 Example Job Ads")
        gr.Examples(
            examples=examples,
            inputs=[input_text, show_suggestions],
            outputs=[
                score_output,
                grade_output,
                category_output,
                recommendations_output,
                highlighted_output
            ],
            fn=analyze_job_ad,
            cache_examples=False
        )
        
        # Info footer
        gr.Markdown("""
        ---
        
        ### ℹ️ About This Tool
        
        This analyzer uses a rule-based NLP approach with a curated dictionary of 
        potentially biased terms. The tool provides explanations and suggestions, 
        but human judgment is essential - context matters!
        
        **Not a final authority** - Use this as a supportive tool to help write 
        more inclusive job descriptions that attract diverse talent.
        
        **Portfolio Project** by Olakunle Kuye | [GitHub](https://github.com/okuye/inclusive-job-ad-analyser)
        """)
        
        # Connect the analyze button
        analyze_btn.click(
            fn=analyze_job_ad,
            inputs=[input_text, show_suggestions],
            outputs=[
                score_output,
                grade_output,
                category_output,
                recommendations_output,
                highlighted_output
            ]
        )
    
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
