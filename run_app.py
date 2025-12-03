#!/usr/bin/env python3
"""
Simple launcher for Inclusive Job Ad Analyzer.

Usage:
    python run_app.py          # Launch web interface (default)
    python run_app.py --cli    # Use CLI mode instead
"""

import sys
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Inclusive Job Ad Analyzer - Detect biased language in job descriptions"
    )
    parser.add_argument(
        '--cli',
        action='store_true',
        help='Run in CLI mode instead of launching web interface'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=7860,
        help='Port for web interface (default: 7860)'
    )
    parser.add_argument(
        '--share',
        action='store_true',
        help='Create public shareable link for web interface'
    )
    
    args, remaining = parser.parse_known_args()
    
    if args.cli:
        # Launch CLI
        from inclusive_job_ad_analyser.cli import main as cli_main
        sys.argv = [sys.argv[0]] + remaining
        cli_main()
    else:
        # Launch web interface
        print("\n" + "="*70)
        print("🔍 Inclusive Job Ad Analyzer - Web Interface")
        print("="*70)
        print("\nStarting web application...")
        print(f"→ Local URL: http://127.0.0.1:{args.port}")
        if args.share:
            print("→ Creating public share link...")
        print("\nPress Ctrl+C to stop the server")
        print("="*70 + "\n")
        
        from inclusive_job_ad_analyser.webapp import create_interface
        
        interface = create_interface()
        interface.launch(
            server_name="127.0.0.1",
            server_port=args.port,
            share=args.share,
            show_error=True,
            show_api=False
        )


if __name__ == "__main__":
    main()
