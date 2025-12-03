#!/usr/bin/env python
"""
Setup script for package installation.
This is kept for backward compatibility. See pyproject.toml for modern config.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read long description from README
readme = Path("README.md").read_text(encoding="utf-8")

setup(
    name="inclusive-job-ad-analyser",
    version="1.0.0",
    description="NLP-powered tool for detecting biased language in job descriptions",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Olakunle Kuye",
    author_email="your.email@example.com",
    url="https://github.com/okuye/inclusive-job-ad-analyser",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "pandas>=2.0.0,<3.0.0",
        "PyYAML>=6.0,<7.0",
        "colorama>=0.4.6,<1.0.0",
        "spacy>=3.7.0,<4.0.0",
    ],
    extras_require={
        "web": ["gradio>=4.0.0,<5.0.0"],
        "dev": [
            "pytest>=7.4.0,<8.0.0",
            "pytest-cov>=4.1.0,<5.0.0",
            "black>=23.0.0,<24.0.0",
            "flake8>=6.0.0,<7.0.0",
            "mypy>=1.5.0,<2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "job-ad-analyser=inclusive_job_ad_analyser.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Human Resources",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="nlp bias-detection inclusive-hiring job-ads ethics",
    project_urls={
        "Bug Reports": "https://github.com/okuye/inclusive-job-ad-analyser/issues",
        "Source": "https://github.com/okuye/inclusive-job-ad-analyser",
        "Documentation": "https://github.com/okuye/inclusive-job-ad-analyser/tree/main/docs",
    },
)
