"""Setup script for the Nomenic package."""

from setuptools import setup, find_packages

setup(
    name="nomenic",
    version="0.1.0",
    description="Nomenic Document Language (NDL) Parser and Toolkit",
    author="Nomenic Team",
    author_email="info@nomenic.org",
    url="https://github.com/nomenic/nomenic-core",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        # No external dependencies for core functionality
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "ruff>=0.0.1",
            "mypy>=1.0.0",
            "hypothesis>=6.0.0",
            "pytest-cov>=4.0.0",
        ],
        "cli": [
            "rich>=12.0.0",  # Optional for enhanced output
        ],
    },
    entry_points={
        "console_scripts": [
            "nomenic=nomenic.cli.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
    ],
)
