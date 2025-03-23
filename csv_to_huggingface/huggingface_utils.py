"""
Utilities for interacting with Hugging Face datasets.
"""

import os
from typing import Optional, Union, List
import logging
from pathlib import Path
from huggingface_hub import HfApi, create_repo, RepoUrl
from datasets import load_dataset, Dataset
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HuggingFaceManager:
    """Class for managing Hugging Face dataset operations."""
    
    def __init__(
        self,
        token: Optional[str] = None,
        organization: Optional[str] = None
    ):
        """
        Initialize the HuggingFaceManager.
        
        Args:
            token: Hugging Face API token
            organization: Organization name (optional)
        """
        self.token = token or os.getenv("HUGGINGFACE_TOKEN")
        if not self.token:
            raise ValueError("Hugging Face token is required. Set it via HUGGINGFACE_TOKEN environment variable or pass it to the constructor.")
        
        self.organization = organization
        self.api = HfApi(token=self.token)
    
    def create_dataset_repo(
        self,
        dataset_name: str,
        private: bool = False,
        exist_ok: bool = False
    ) -> str:
        """
        Create a new dataset repository on Hugging Face.
        
        Args:
            dataset_name: Name of the dataset
            private: Whether the dataset should be private
            exist_ok: Whether to allow the repository to already exist
            
        Returns:
            Repository URL
        """
        if self.organization:
            dataset_name = f"{self.organization}/{dataset_name}"
        
        try:
            repo_url = create_repo(
                repo_id=dataset_name,
                token=self.token,
                repo_type="dataset",
                private=private,
                exist_ok=exist_ok
            )
            logger.info(f"Created dataset repository: {repo_url}")
            return repo_url
        except Exception as e:
            logger.error(f"Failed to create dataset repository: {e}")
            raise
    
    def upload_dataset(
        self,
        dataset_path: Union[str, Path],
        dataset_name: str,
        commit_message: str = "Upload dataset",
        private: bool = False
    ) -> None:
        """
        Upload a dataset to Hugging Face.
        
        Args:
            dataset_path: Path to the dataset directory
            dataset_name: Name of the dataset
            commit_message: Commit message for the upload
            private: Whether the dataset should be private
        """
        dataset_path = Path(dataset_path)
        if not dataset_path.exists():
            raise ValueError(f"Dataset path does not exist: {dataset_path}")
        
        # Create repository if it doesn't exist
        repo_url = self.create_dataset_repo(dataset_name, private=private, exist_ok=True)
        
        # Upload files
        try:
            self.api.upload_folder(
                folder_path=str(dataset_path),
                repo_id=dataset_name,
                repo_type="dataset",
                commit_message=commit_message
            )
            logger.info(f"Successfully uploaded dataset to {repo_url}")
        except Exception as e:
            logger.error(f"Failed to upload dataset: {e}")
            raise
    
    def load_dataset(
        self,
        dataset_name: str,
        split: Optional[str] = None,
        streaming: bool = False
    ) -> Dataset:
        """
        Load a dataset from Hugging Face.
        
        Args:
            dataset_name: Name of the dataset
            split: Dataset split to load (optional)
            streaming: Whether to stream the dataset
            
        Returns:
            Hugging Face Dataset object
        """
        try:
            dataset = load_dataset(
                dataset_name,
                split=split,
                streaming=streaming,
                token=self.token
            )
            logger.info(f"Successfully loaded dataset: {dataset_name}")
            return dataset
        except Exception as e:
            logger.error(f"Failed to load dataset: {e}")
            raise
    
    def update_dataset_card(
        self,
        dataset_name: str,
        card_path: Union[str, Path],
        commit_message: str = "Update dataset card"
    ) -> None:
        """
        Update the dataset card on Hugging Face.
        
        Args:
            dataset_name: Name of the dataset
            card_path: Path to the dataset card file
            commit_message: Commit message for the update
        """
        card_path = Path(card_path)
        if not card_path.exists():
            raise ValueError(f"Dataset card path does not exist: {card_path}")
        
        try:
            self.api.upload_file(
                path_or_fileobj=str(card_path),
                path_in_repo="dataset-card.json",
                repo_id=dataset_name,
                repo_type="dataset",
                commit_message=commit_message
            )
            logger.info(f"Successfully updated dataset card for {dataset_name}")
        except Exception as e:
            logger.error(f"Failed to update dataset card: {e}")
            raise
    
    def delete_dataset(
        self,
        dataset_name: str,
        commit_message: str = "Delete dataset"
    ) -> None:
        """
        Delete a dataset from Hugging Face.
        
        Args:
            dataset_name: Name of the dataset
            commit_message: Commit message for the deletion
        """
        try:
            self.api.delete_repo(
                repo_id=dataset_name,
                repo_type="dataset",
                commit_message=commit_message
            )
            logger.info(f"Successfully deleted dataset: {dataset_name}")
        except Exception as e:
            logger.error(f"Failed to delete dataset: {e}")
            raise 