#!/bin/bash
# Installation and Setup Script for Inclusive Job Ad Analyser

set -e  # Exit on error

echo "================================================"
echo "Inclusive Job Ad Analyser - Setup Script"
echo "================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

if [[ $(python3 -c "import sys; print(sys.version_info >= (3, 10))") != "True" ]]; then
    echo "❌ Error: Python 3.10+ is required"
    exit 1
fi
echo "✓ Python version is compatible"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --quiet
echo "✓ Dependencies installed"
echo ""

# Download spaCy model
echo "Downloading spaCy model..."
if python -c "import spacy; spacy.load('en_core_web_sm')" 2>/dev/null; then
    echo "✓ spaCy model already installed"
else
    python -m spacy download en_core_web_sm
    echo "✓ spaCy model downloaded"
fi
echo ""

# Run tests
echo "Running tests..."
if pytest -q; then
    echo "✓ All tests passed"
else
    echo "⚠️  Some tests failed (this is OK for first setup)"
fi
echo ""

# Test CLI
echo "Testing CLI..."
if python -m inclusive_job_ad_analyser.cli --help > /dev/null 2>&1; then
    echo "✓ CLI is working"
else
    echo "❌ CLI test failed"
    exit 1
fi
echo ""

echo "================================================"
echo "Setup Complete! 🎉"
echo "================================================"
echo ""
echo "Try these commands:"
echo ""
echo "  # Analyse example job ad"
echo "  python -m inclusive_job_ad_analyser.cli examples/biased_job_ad.md"
echo ""
echo "  # Start web interface"
echo "  python -m inclusive_job_ad_analyser.webapp"
echo ""
echo "  # Run tests"
echo "  pytest"
echo ""
echo "  # Show statistics"
echo "  python -m inclusive_job_ad_analyser.cli --stats"
echo ""
echo "See README.md for full documentation."
echo ""
