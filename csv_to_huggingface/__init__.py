"""
CSV to Hugging Face

A Python library for converting CSV data to optimized formats and uploading to Hugging Face datasets.
This package provides tools for data optimization, dataset card generation, and seamless integration with Hugging Face.
"""

__version__ = "0.1.0"

from .data_processor import DataProcessor
from .dataset_card import DatasetCardGenerator
from .huggingface_utils import HuggingFaceManager

__all__ = ['DataProcessor', 'DatasetCardGenerator', 'HuggingFaceManager'] 