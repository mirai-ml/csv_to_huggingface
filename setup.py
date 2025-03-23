from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="csv_to_huggingface",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python library for converting CSV data to optimized formats and uploading to Hugging Face datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/csv_to_huggingface",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/csv_to_huggingface/issues",
        "Documentation": "https://github.com/yourusername/csv_to_huggingface#readme",
    },
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "csv-to-hf=csv_to_huggingface.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: General",
    ],
    keywords="csv, huggingface, datasets, data-processing, machine-learning, data-science",
    license="MIT",
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.21.0",
        "huggingface_hub>=0.16.0",
        "datasets>=2.12.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "flake8>=4.0.0",
            "build>=0.7.0",
            "twine>=3.4.2",
        ],
    },
) 