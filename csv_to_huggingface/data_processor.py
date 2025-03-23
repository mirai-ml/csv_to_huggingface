"""
Data processing utilities for CSV to Hugging Face conversion.
"""

import pandas as pd
import numpy as np
from typing import Union, Optional
import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    """Class for processing and optimizing data."""
    
    def __init__(self):
        """Initialize the DataProcessor."""
        self.original_dtypes = None
    
    def optimize_dtypes(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Optimize data types to minimize memory usage.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with optimized data types
        """
        self.original_dtypes = df.dtypes.copy()
        
        for col in df.columns:
            col_type = df[col].dtype
            
            # Optimize integer columns
            if col_type in ['int64', 'int32']:
                c_min = df[col].min()
                c_max = df[col].max()
                
                if c_min >= 0:
                    if c_max < 255:
                        df[col] = df[col].astype(np.uint8)
                    elif c_max < 65535:
                        df[col] = df[col].astype(np.uint16)
                    elif c_max < 4294967295:
                        df[col] = df[col].astype(np.uint32)
                else:
                    if c_min > -128 and c_max < 127:
                        df[col] = df[col].astype(np.int8)
                    elif c_min > -32768 and c_max < 32767:
                        df[col] = df[col].astype(np.int16)
                    elif c_min > -2147483648 and c_max < 2147483647:
                        df[col] = df[col].astype(np.int32)
            
            # Optimize float columns
            elif col_type == 'float64':
                df[col] = df[col].astype(np.float32)
                
            # Optimize object columns
            elif col_type == 'object':
                if df[col].nunique() / len(df) < 0.5:  # If less than 50% unique values
                    df[col] = df[col].astype('category')
        
        return df
    
    def convert_to_parquet(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        optimize: bool = True
    ) -> str:
        """
        Convert CSV file to Parquet format with optimized storage.
        
        Args:
            input_path: Path to input CSV file
            output_path: Path to output Parquet file (optional)
            optimize: Whether to optimize data types
            
        Returns:
            Path to the created Parquet file
        """
        # Generate output path if not provided
        if output_path is None:
            output_path = str(Path(input_path).with_suffix('.parquet'))
        
        # Read CSV file
        logger.info(f"Reading CSV file: {input_path}")
        df = pd.read_csv(input_path)
        
        # Optimize data types if requested
        if optimize:
            logger.info("Optimizing data types...")
            df = self.optimize_dtypes(df)
        
        # Write to Parquet
        logger.info(f"Writing to Parquet: {output_path}")
        df.to_parquet(output_path, index=False)
        
        # Print file size comparison
        input_size = os.path.getsize(input_path)
        output_size = os.path.getsize(output_path)
        compression_ratio = (1 - output_size / input_size) * 100
        
        logger.info(f"\nFile size comparison:")
        logger.info(f"CSV file size: {input_size / 1024 / 1024:.2f} MB")
        logger.info(f"Parquet file size: {output_size / 1024 / 1024:.2f} MB")
        logger.info(f"Compression ratio: {compression_ratio:.2f}%")
        
        return output_path
    
    def analyze_data(self, df: pd.DataFrame) -> dict:
        """
        Analyze a DataFrame and return statistics.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary containing data statistics
        """
        stats = {
            "num_rows": len(df),
            "num_columns": len(df.columns),
            "columns": [],
            "missing_values": {},
            "memory_usage": df.memory_usage(deep=True).sum() / 1024**2  # in MB
        }
        
        for col in df.columns:
            col_stats = {
                "name": col,
                "dtype": str(df[col].dtype),
                "unique_values": df[col].nunique(),
                "missing_count": df[col].isna().sum(),
                "missing_percentage": (df[col].isna().sum() / len(df)) * 100
            }
            
            # Add specific statistics based on data type
            if pd.api.types.is_numeric_dtype(df[col]):
                col_stats.update({
                    "min": float(df[col].min()) if not pd.isna(df[col].min()) else None,
                    "max": float(df[col].max()) if not pd.isna(df[col].max()) else None,
                    "mean": float(df[col].mean()) if not pd.isna(df[col].mean()) else None,
                    "std": float(df[col].std()) if not pd.isna(df[col].std()) else None,
                    "median": float(df[col].median()) if not pd.isna(df[col].median()) else None
                })
            elif pd.api.types.is_string_dtype(df[col]):
                col_stats.update({
                    "max_length": df[col].str.len().max() if not df[col].empty else 0,
                    "avg_length": df[col].str.len().mean() if not df[col].empty else 0
                })
            
            stats["columns"].append(col_stats)
            if col_stats["missing_count"] > 0:
                stats["missing_values"][col] = col_stats["missing_percentage"]
        
        return stats 