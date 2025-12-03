"""
Entry point for running the package as a module.

Usage:
    python -m inclusive_job_ad_analyser          # Launch web interface
    python -m inclusive_job_ad_analyser --cli    # Launch CLI
"""

from .webapp import main as webapp_main
from .cli import main as cli_main
import sys


if __name__ == "__main__":
    # Check if --cli flag is present
    if '--cli' in sys.argv:
        sys.argv.remove('--cli')
        cli_main()
    else:
        # Default to web interface
        webapp_main()
