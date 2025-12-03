"""
Command-line interface for the Inclusive Job Ad Analyser.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional, List
import csv

from inclusive_job_ad_analyser.analyser import JobAdAnalyser
from inclusive_job_ad_analyser.scraper import JobAdScraper
from inclusive_job_ad_analyser.scoring import (
    compute_bias_score,
    get_grade,
    compute_category_scores,
    detect_positive_indicators,
    generate_recommendations,
)
from inclusive_job_ad_analyser.models import AnalysisResult
from inclusive_job_ad_analyser.reporting import ReportGenerator
from inclusive_job_ad_analyser.loaders import ConfigLoader


def analyse_text(
    text: str,
    analyser: JobAdAnalyser,
    config: Optional[ConfigLoader] = None
) -> AnalysisResult:
    """
    Analyse a job ad text and return complete results.
    
    Args:
        text: Job ad text to analyse.
        analyser: Configured JobAdAnalyser instance.
        config: Optional configuration loader.
        
    Returns:
        Complete AnalysisResult object.
    """
    # Run analysis
    matches = analyser.analyse(text)
    
    # Compute scores
    overall_score = compute_bias_score(matches, text, config)
    grade = get_grade(overall_score)
    category_scores = compute_category_scores(matches, config)
    
    # Detect positive indicators
    positive = detect_positive_indicators(text, config)
    
    # Generate recommendations
    recommendations = generate_recommendations(matches, category_scores)
    
    # Word count
    word_count = len(text.split())
    
    return AnalysisResult(
        text=text,
        overall_score=overall_score,
        grade=grade,
        word_count=word_count,
        matches=matches,
        category_scores=category_scores,
        recommendations=recommendations,
        positive_aspects=positive,
    )


def analyse_file(
    file_path: Path,
    analyser: JobAdAnalyser,
    config: Optional[ConfigLoader] = None
) -> AnalysisResult:
    """
    Analyse a job ad from a file.
    
    Args:
        file_path: Path to file containing job ad.
        analyser: Configured JobAdAnalyser instance.
        config: Optional configuration loader.
        
    Returns:
        Complete AnalysisResult object.
    """
    try:
        text = file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        # Try alternative encodings
        text = file_path.read_text(encoding='latin-1')
    
    return analyse_text(text, analyser, config)


def analyse_directory(
    dir_path: Path,
    analyser: JobAdAnalyser,
    config: Optional[ConfigLoader] = None,
    pattern: str = "*.txt"
) -> List[tuple[str, AnalysisResult]]:
    """
    Analyse all matching files in a directory.
    
    Args:
        dir_path: Directory to scan.
        analyser: Configured JobAdAnalyser instance.
        config: Optional configuration loader.
        pattern: Glob pattern for files to analyse.
        
    Returns:
        List of (filename, result) tuples.
    """
    results = []
    
    for file_path in dir_path.glob(pattern):
        if file_path.is_file():
            try:
                result = analyse_file(file_path, analyser, config)
                results.append((file_path.name, result))
                print(f"✓ Analysed: {file_path.name}", file=sys.stderr)
            except Exception as e:
                print(f"✗ Error analysing {file_path.name}: {e}", file=sys.stderr)
    
    return results


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Analyse job ads for biased language and suggest inclusive alternatives.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s job_ad.txt
  %(prog)s job_ad.txt --format json
  %(prog)s job_ad.txt --output report.txt
  %(prog)s --directory ads/ --format csv --output results.csv
  cat job_ad.txt | %(prog)s --stdin
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        'file',
        type=str,
        nargs='?',
        help='Path to job ad file to analyse'
    )
    input_group.add_argument(
        '--stdin',
        action='store_true',
        help='Read job ad from stdin'
    )
    input_group.add_argument(
        '--directory',
        '-d',
        type=str,
        help='Analyse all .txt files in a directory'
    )
    input_group.add_argument(
        '--url',
        '-u',
        type=str,
        help='Scrape and analyse job ad from URL (LinkedIn, Indeed, Glassdoor, etc.)'
    )
    input_group.add_argument(
        '--urls-file',
        type=str,
        help='File containing URLs (one per line) to scrape and analyse'
    )
    input_group.add_argument(
        '--search',
        '-s',
        type=str,
        help='Search query for jobs (e.g., "software engineer", "data analyst")'
    )

    parser.add_argument(
        '--source',
        choices=['indeed', 'linkedin', 'glassdoor'],
        default='indeed',
        help='Job board to search (default: indeed)'
    )
    parser.add_argument(
        '--location',
        '-l',
        type=str,
        default='',
        help='Location filter for job search (e.g., "New York, NY", "Remote")'
    )
    parser.add_argument(
        '--max-results',
        '-m',
        type=int,
        default=10,
        help='Maximum number of search results to analyse (default: 10)'
    )
    
    # Output options
    parser.add_argument(
        '--format',
        '-f',
        choices=['text', 'json', 'csv', 'markdown'],
        default='text',
        help='Output format (default: text)'
    )
    parser.add_argument(
        '--output',
        '-o',
        type=str,
        help='Write output to file instead of stdout'
    )
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output for text format'
    )
    
    # Analysis options
    parser.add_argument(
        '--config',
        '-c',
        type=str,
        help='Path to custom settings.yaml'
    )
    parser.add_argument(
        '--no-spacy',
        action='store_true',
        help='Disable spaCy (use regex only)'
    )
    parser.add_argument(
        '--pattern',
        type=str,
        default='*.txt',
        help='File pattern for directory mode (default: *.txt)'
    )
    
    # Info options
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show statistics about loaded bias terms'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = None
    if args.config:
        config = ConfigLoader(Path(args.config))
    
    # Initialize analyser
    try:
        analyser = JobAdAnalyser(use_spacy=not args.no_spacy)
    except Exception as e:
        print(f"Error initializing analyser: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Show stats if requested
    if args.stats:
        stats = analyser.get_statistics()
        print("\nBias Terms Statistics:")
        print(f"Total terms: {stats['total_terms']}")
        print("\nBy category:")
        for cat, count in sorted(stats['by_category'].items()):
            print(f"  {cat}: {count}")
        print("\nBy severity:")
        for sev, count in sorted(stats['by_severity'].items()):
            print(f"  {sev}: {count}")
        sys.exit(0)
    
    # Process input
    try:
        if args.stdin:
            # Read from stdin
            text = sys.stdin.read()
            result = analyse_text(text, analyser, config)
            results = [("stdin", result)]
        
        elif args.url:
            # Scrape single URL
            try:
                scraper = JobAdScraper()
                print(f"Scraping {args.url}...", file=sys.stderr)
                scraped = scraper.scrape(args.url)
                
                if 'error' in scraped:
                    print(f"Error: {scraped['error']}", file=sys.stderr)
                    sys.exit(1)
                
                print(f"✓ Scraped: {scraped['title']} at {scraped['company']}", file=sys.stderr)
                result = analyse_text(scraped['text'], analyser, config)
                results = [(f"{scraped['title']} - {scraped['company']}", result)]
            except ImportError:
                print("Error: Web scraping requires additional dependencies.", file=sys.stderr)
                print("Install with: pip install requests beautifulsoup4", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                print(f"Error scraping URL: {e}", file=sys.stderr)
                sys.exit(1)
        
        elif args.urls_file:
            # Scrape multiple URLs from file
            try:
                scraper = JobAdScraper()
                urls_path = Path(args.urls_file)
                
                if not urls_path.exists():
                    print(f"Error: URLs file not found: {urls_path}", file=sys.stderr)
                    sys.exit(1)
                
                urls = [line.strip() for line in urls_path.read_text().splitlines() 
                       if line.strip() and not line.startswith('#')]
                
                print(f"Scraping {len(urls)} URLs...", file=sys.stderr)
                scraped_jobs = scraper.scrape_multiple(urls)
                
                results = []
                for job in scraped_jobs:
                    if 'error' in job:
                        print(f"✗ Error scraping {job['url']}: {job['error']}", file=sys.stderr)
                        continue
                    
                    print(f"✓ Scraped: {job['title']} at {job['company']}", file=sys.stderr)
                    result = analyse_text(job['text'], analyser, config)
                    results.append((f"{job['title']} - {job['company']}", result))
                
                if not results:
                    print("No URLs successfully scraped", file=sys.stderr)
                    sys.exit(1)
            
            except ImportError:
                print("Error: Web scraping requires additional dependencies.", file=sys.stderr)
                print("Install with: pip install requests beautifulsoup4", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
        
        elif args.search:
            # Search job boards
            try:
                scraper = JobAdScraper()
                print(f"Searching {args.source} for '{args.search}'...", file=sys.stderr)
                if args.location:
                    print(f"Location: {args.location}", file=sys.stderr)
                
                scraped_jobs = scraper.search_jobs(
                    query=args.search,
                    source=args.source,
                    location=args.location,
                    max_results=args.max_results
                )
                
                if not scraped_jobs:
                    print("No jobs found matching your search", file=sys.stderr)
                    sys.exit(1)
                
                print(f"Found {len(scraped_jobs)} jobs, analyzing...\n", file=sys.stderr)
                
                results = []
                for job in scraped_jobs:
                    if 'error' in job:
                        print(f"✗ Error: {job['error']}", file=sys.stderr)
                        continue
                    
                    print(f"✓ Analyzing: {job['title']} at {job['company']}", file=sys.stderr)
                    result = analyse_text(job['text'], analyser, config)
                    results.append((f"{job['title']} - {job['company']}", result))
                
                if not results:
                    print("No jobs successfully analysed", file=sys.stderr)
                    sys.exit(1)
            
            except ImportError:
                print("Error: Web scraping requires additional dependencies.", file=sys.stderr)
                print("Install with: pip install requests beautifulsoup4", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                print(f"Error searching jobs: {e}", file=sys.stderr)
                sys.exit(1)
        
        elif args.directory:
            # Batch mode
            dir_path = Path(args.directory)
            if not dir_path.is_dir():
                print(f"Error: {dir_path} is not a directory", file=sys.stderr)
                sys.exit(1)
            
            results = analyse_directory(dir_path, analyser, config, args.pattern)
            
            if not results:
                print(f"No files matching pattern '{args.pattern}' found in {dir_path}",
                      file=sys.stderr)
                sys.exit(1)
        
        else:
            # Single file mode
            file_path = Path(args.file)
            if not file_path.exists():
                print(f"Error: File not found: {file_path}", file=sys.stderr)
                sys.exit(1)
            
            result = analyse_file(file_path, analyser, config)
            results = [(file_path.name, result)]
    
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Generate output
    reporter = ReportGenerator()
    
    try:
        if args.format == 'json':
            # JSON format (single file or array)
            if len(results) == 1:
                output = reporter.generate_json_report(results[0][1])
            else:
                # Multiple results as array
                import json
                data = [
                    {
                        'filename': filename,
                        **result.to_dict()
                    }
                    for filename, result in results
                ]
                output = json.dumps(data, indent=2, ensure_ascii=False)
        
        elif args.format == 'csv':
            # CSV format (for batch processing)
            import io
            output_buffer = io.StringIO()
            
            if results:
                # Get all possible column names
                first_result = results[0][1]
                sample_row = reporter.generate_csv_row(results[0][0], first_result)
                fieldnames = list(sample_row.keys())
                
                writer = csv.DictWriter(output_buffer, fieldnames=fieldnames)
                writer.writeheader()
                
                for filename, result in results:
                    row = reporter.generate_csv_row(filename, result)
                    writer.writerow(row)
            
            output = output_buffer.getvalue()
        
        elif args.format == 'markdown':
            # Markdown format
            if len(results) == 1:
                output = reporter.generate_markdown_report(results[0][1])
            else:
                # Multiple results concatenated
                output = "\n\n---\n\n".join(
                    f"# Analysis: {filename}\n\n{reporter.generate_markdown_report(result)}"
                    for filename, result in results
                )
        
        else:
            # Text format (default)
            colored = not args.no_color
            if len(results) == 1:
                output = reporter.generate_text_report(results[0][1], colored)
            else:
                # Multiple results concatenated
                output = "\n\n".join(
                    f"=== {filename} ===\n{reporter.generate_text_report(result, colored)}"
                    for filename, result in results
                )
        
        # Write output
        if args.output:
            Path(args.output).write_text(output, encoding='utf-8')
            print(f"Report written to: {args.output}", file=sys.stderr)
        else:
            print(output)
        
        # Exit code based on results
        # Non-zero if any result has score below 60 (Poor grade)
        poor_results = [r for _, r in results if r.overall_score < 60]
        sys.exit(1 if poor_results else 0)
    
    except Exception as e:
        print(f"Error generating report: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
