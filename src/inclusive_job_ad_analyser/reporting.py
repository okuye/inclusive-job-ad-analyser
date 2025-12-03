"""
Report generation utilities for different output formats.
"""

import json
from typing import List, Dict, Optional
from datetime import datetime

from .models import AnalysisResult, MatchResult, CategoryScore

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
    _HAS_COLORAMA = True
except ImportError:
    _HAS_COLORAMA = False
    # Fallback: no colors
    class Fore:
        RED = GREEN = YELLOW = BLUE = CYAN = MAGENTA = WHITE = RESET = ""
    class Style:
        BRIGHT = DIM = RESET_ALL = ""


class ReportGenerator:
    """Generate reports in various formats."""
    
    @staticmethod
    def generate_text_report(result: AnalysisResult, colored: bool = True) -> str:
        """
        Generate a human-readable text report.
        
        Args:
            result: Analysis result to report on.
            colored: Whether to use terminal colors (requires colorama).
            
        Returns:
            Formatted text report.
        """
        if not colored or not _HAS_COLORAMA:
            # Disable colors
            fore_red = fore_green = fore_yellow = fore_cyan = ""
            fore_magenta = style_bright = style_reset = ""
        else:
            fore_red = Fore.RED
            fore_green = Fore.GREEN
            fore_yellow = Fore.YELLOW
            fore_cyan = Fore.CYAN
            fore_magenta = Fore.MAGENTA
            style_bright = Style.BRIGHT
            style_reset = Style.RESET_ALL
        
        lines = []
        
        # Header
        lines.append(f"\n{style_bright}{'=' * 60}")
        lines.append("INCLUSIVE JOB AD ANALYSIS REPORT")
        lines.append(f"{'=' * 60}{style_reset}\n")
        
        # Overall score
        score = result.overall_score
        grade = result.grade
        
        if score >= 90:
            color = fore_green
            emoji = "🎉"
        elif score >= 75:
            color = fore_cyan
            emoji = "✓"
        elif score >= 60:
            color = fore_yellow
            emoji = "⚠️"
        else:
            color = fore_red
            emoji = "❌"
        
        lines.append(f"{style_bright}Overall Score: {color}{score}/100{style_reset} ({grade}) {emoji}")
        lines.append(f"Word Count: {result.word_count}")
        lines.append(f"Issues Found: {len(result.matches)}\n")
        
        # Category breakdown
        if result.category_scores:
            lines.append(f"{style_bright}CATEGORY BREAKDOWN:{style_reset}")
            lines.append("-" * 60)
            
            for category, cat_score in sorted(
                result.category_scores.items(),
                key=lambda x: x[1].score
            ):
                cat_name = category.replace('-', ' ').title()
                score_val = cat_score.score
                
                if score_val >= 80:
                    cat_color = fore_green
                    cat_emoji = "✓"
                elif score_val >= 60:
                    cat_color = fore_yellow
                    cat_emoji = "⚠️"
                else:
                    cat_color = fore_red
                    cat_emoji = "❌"
                
                lines.append(
                    f"{cat_name:20} {cat_color}{score_val:5.1f}/100{style_reset} "
                    f"{cat_emoji}  ({cat_score.issues_count} issue(s), "
                    f"max: {cat_score.max_severity})"
                )
            
            lines.append("")
        
        # Issues by severity
        if result.matches:
            lines.append(f"{style_bright}ISSUES DETECTED:{style_reset}")
            lines.append("-" * 60)
            
            # Group by severity
            severity_order = ['critical', 'high', 'medium', 'low']
            for severity in severity_order:
                matches_by_sev = [m for m in result.matches if m.severity == severity]
                if not matches_by_sev:
                    continue
                
                # Severity header
                sev_color = {
                    'critical': fore_red,
                    'high': fore_red,
                    'medium': fore_yellow,
                    'low': fore_cyan,
                }.get(severity, "")
                
                lines.append(f"\n{style_bright}{sev_color}{severity.upper()} SEVERITY:{style_reset}")
                
                for i, match in enumerate(matches_by_sev, 1):
                    lines.append(f"\n{i}. '{match.term}' [{match.category}] (found {match.count}x)")
                    lines.append(f"   Issue: {match.explanation}")
                    lines.append(f"   Suggestion: {fore_green}{match.suggestion}{style_reset}")
                    
                    if match.contexts:
                        context = match.contexts[0][:100]
                        if len(match.contexts[0]) > 100:
                            context += "..."
                        lines.append(f"   Context: \"{context}\"")
            
            lines.append("")
        
        # Recommendations
        if result.recommendations:
            lines.append(f"\n{style_bright}RECOMMENDATIONS:{style_reset}")
            lines.append("-" * 60)
            for rec in result.recommendations:
                lines.append(f"{rec}")
            lines.append("")
        
        # Positive aspects
        if result.positive_aspects:
            lines.append(f"\n{style_bright}{fore_green}POSITIVE ASPECTS:{style_reset}")
            lines.append("-" * 60)
            for aspect in result.positive_aspects:
                lines.append(f"✓ Contains '{aspect}'")
            lines.append("")
        
        # Footer
        lines.append("-" * 60)
        lines.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        return "\n".join(lines)
    
    @staticmethod
    def generate_json_report(result: AnalysisResult) -> str:
        """
        Generate a JSON report.
        
        Args:
            result: Analysis result to report on.
            
        Returns:
            JSON string.
        """
        data = result.to_dict()
        data['metadata'] = {
            'generated_at': datetime.now().isoformat(),
            'version': '1.0.0',
        }
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    @staticmethod
    def generate_csv_row(
        filename: str,
        result: AnalysisResult
    ) -> Dict[str, any]:
        """
        Generate a CSV row for batch processing results.
        
        Args:
            filename: Name of the analysed file.
            result: Analysis result.
            
        Returns:
            Dictionary representing a CSV row.
        """
        row = {
            'filename': filename,
            'overall_score': result.overall_score,
            'grade': result.grade,
            'word_count': result.word_count,
            'total_issues': len(result.matches),
        }
        
        # Add category scores
        for category, score in result.category_scores.items():
            col_name = f"{category}_score"
            row[col_name] = score.score
            row[f"{category}_issues"] = score.issues_count
        
        # Count by severity
        for severity in ['critical', 'high', 'medium', 'low']:
            count = sum(
                m.count for m in result.matches
                if m.severity == severity
            )
            row[f"{severity}_count"] = count
        
        return row
    
    @staticmethod
    def generate_markdown_report(result: AnalysisResult) -> str:
        """
        Generate a Markdown report.
        
        Args:
            result: Analysis result to report on.
            
        Returns:
            Markdown formatted string.
        """
        lines = []
        
        # Header
        lines.append("# Inclusive Job Ad Analysis Report\n")
        lines.append(f"**Overall Score:** {result.overall_score}/100 ({result.grade})\n")
        lines.append(f"**Word Count:** {result.word_count}\n")
        lines.append(f"**Issues Found:** {len(result.matches)}\n")
        
        # Category breakdown
        if result.category_scores:
            lines.append("## Category Breakdown\n")
            lines.append("| Category | Score | Issues | Max Severity |")
            lines.append("|----------|-------|--------|--------------|")
            
            for category, score in sorted(
                result.category_scores.items(),
                key=lambda x: x[1].score
            ):
                cat_name = category.replace('-', ' ').title()
                lines.append(
                    f"| {cat_name} | {score.score}/100 | {score.issues_count} | "
                    f"{score.max_severity} |"
                )
            
            lines.append("")
        
        # Issues
        if result.matches:
            lines.append("## Issues Detected\n")
            
            severity_order = ['critical', 'high', 'medium', 'low']
            for severity in severity_order:
                matches_by_sev = [m for m in result.matches if m.severity == severity]
                if not matches_by_sev:
                    continue
                
                lines.append(f"### {severity.upper()} Severity\n")
                
                for match in matches_by_sev:
                    lines.append(f"**{match.term}** ({match.category}, found {match.count}x)")
                    lines.append(f"- Issue: {match.explanation}")
                    lines.append(f"- Suggestion: {match.suggestion}")
                    if match.contexts:
                        lines.append(f"- Context: \"{match.contexts[0][:100]}...\"")
                    lines.append("")
        
        # Recommendations
        if result.recommendations:
            lines.append("## Recommendations\n")
            for rec in result.recommendations:
                lines.append(f"- {rec}")
            lines.append("")
        
        # Positive aspects
        if result.positive_aspects:
            lines.append("## Positive Aspects\n")
            for aspect in result.positive_aspects:
                lines.append(f"- ✓ Contains '{aspect}'")
            lines.append("")
        
        # Footer
        lines.append(f"\n---\n*Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        return "\n".join(lines)
