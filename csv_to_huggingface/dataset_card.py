"""
Dataset card generation utilities for Hugging Face datasets.
"""

import pandas as pd
from typing import Dict, List, Optional, Union
import json
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatasetCardGenerator:
    """Class for generating dataset cards for Hugging Face."""
    
    def __init__(
        self,
        dataset_name: str,
        description: str,
        task_categories: List[str],
        language: str = "en",
        license: str = "MIT",
        version: str = "0.1.0"
    ):
        """
        Initialize the DatasetCardGenerator.
        
        Args:
            dataset_name: Name of the dataset
            description: Description of the dataset
            task_categories: List of task categories (e.g., ["text-classification", "language-modelling"])
            language: Language of the dataset
            license: License for the dataset
            version: Version of the dataset
        """
        self.dataset_name = dataset_name
        self.description = description
        self.task_categories = task_categories
        self.language = language
        self.license = license
        self.version = version
        self.metadata = {}
        self.data_stats = {}
    
    def add_metadata(self, metadata: Dict) -> None:
        """
        Add metadata to the dataset card.
        
        Args:
            metadata: Dictionary containing metadata
        """
        self.metadata.update(metadata)
    
    def add_data_stats(self, stats: Dict) -> None:
        """
        Add data statistics to the dataset card.
        
        Args:
            stats: Dictionary containing data statistics
        """
        self.data_stats.update(stats)
    
    def generate_card(self) -> Dict:
        """
        Generate the dataset card as a dictionary.
        
        Returns:
            Dictionary containing the dataset card
        """
        card = {
            "annotations_creators": ["no-annotation"],
            "language_creators": ["found"],
            "language": self.language,
            "license": self.license,
            "multilinguality": ["monolingual"],
            "size_categories": ["n<1K", "1K<n<10K", "10K<n<100K", "100K<n<1M", "1M<n<10M", "10M<n<100M", "100M<n<1B", "1B<n<10B", "10B<n<100B", "100B<n<1T"],
            "source_datasets": ["original"],
            "task_categories": self.task_categories,
            "task_ids": [],
            "paperswithcode_id": None,
            "pretty_name": self.dataset_name,
            "version": self.version,
            "configs": [
                {
                    "name": "default",
                    "data_files": {
                        "train": "data/train.parquet",
                        "validation": "data/validation.parquet",
                        "test": "data/test.parquet"
                    }
                }
            ],
            "data": {
                "description": self.description,
                "features": self._generate_features(),
                "splits": self._generate_splits(),
                "download_size": None,
                "dataset_size": None,
                "size_in_bytes": None,
                "total_num_rows": None,
                "missing_values": {},
                "statistics": self.data_stats
            },
            "metadata": self.metadata,
            "date_created": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat()
        }
        
        return card
    
    def _generate_features(self) -> Dict:
        """
        Generate feature descriptions based on data statistics.
        
        Returns:
            Dictionary containing feature descriptions
        """
        features = {}
        if "columns" in self.data_stats:
            for col in self.data_stats["columns"]:
                features[col["name"]] = {
                    "dtype": col["dtype"],
                    "num_unique_values": col["unique_values"],
                    "missing_count": col["missing_count"],
                    "missing_percentage": col["missing_percentage"]
                }
                
                # Add specific statistics based on data type
                if "min" in col:
                    features[col["name"]].update({
                        "min": col["min"],
                        "max": col["max"],
                        "mean": col["mean"],
                        "std": col["std"],
                        "median": col["median"]
                    })
                elif "max_length" in col:
                    features[col["name"]].update({
                        "max_length": col["max_length"],
                        "avg_length": col["avg_length"]
                    })
        
        return features
    
    def _generate_splits(self) -> Dict:
        """
        Generate split information.
        
        Returns:
            Dictionary containing split information
        """
        splits = {
            "train": {
                "name": "train",
                "num_bytes": None,
                "num_examples": None,
                "dataset_name": self.dataset_name
            },
            "validation": {
                "name": "validation",
                "num_bytes": None,
                "num_examples": None,
                "dataset_name": self.dataset_name
            },
            "test": {
                "name": "test",
                "num_bytes": None,
                "num_examples": None,
                "dataset_name": self.dataset_name
            }
        }
        
        return splits
    
    def save_card(self, output_path: Union[str, Path]) -> None:
        """
        Save the dataset card to a file.
        
        Args:
            output_path: Path to save the dataset card
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        card = self.generate_card()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(card, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Dataset card saved to: {output_path}") 