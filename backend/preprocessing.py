"""
Data preprocessing module for sequence generation.

This module handles:
- Automatic column mapping
- Data cleaning and transformation
- Sequence generation from transactional data
"""

import pandas as pd
from typing import List, Dict, Any, Optional
from utils import logger


class DataPreprocessor:
    """Handles data preprocessing and sequence generation."""
    
    def __init__(self, dataframe: pd.DataFrame):
        """
        Initialize the preprocessor with a dataframe.
        
        Args:
            dataframe: Input pandas DataFrame
        """
        self.raw_data = dataframe.copy()
        self.sequences: List[List[str]] = []
        self.sequence_count = 0
        self.unique_items = set()
    
    def generate_sequences(self, sequence_id_col: str, item_col: str, 
                          timestamp_col: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate sequences from transactional data.
        
        Args:
            sequence_id_col: Column name for sequence/user/session ID
            item_col: Column name for items/events
            timestamp_col: Optional column name for timestamps
            
        Returns:
            Dictionary with sequence generation results
        """
        logger.info(f"Generating sequences using columns: ID={sequence_id_col}, Item={item_col}, Time={timestamp_col}")
        
        try:
            # Validate columns exist
            required_cols = [sequence_id_col, item_col]
            if timestamp_col:
                required_cols.append(timestamp_col)
            
            missing_cols = [col for col in required_cols if col not in self.raw_data.columns]
            if missing_cols:
                raise ValueError(f"Missing columns in dataset: {missing_cols}")
            
            # Clean data
            df = self.raw_data.copy()
            
            # Remove rows with missing values in key columns
            df = df.dropna(subset=required_cols)
            logger.info(f"Rows after removing null values: {len(df)}")
            
            # Convert item column to string
            df[item_col] = df[item_col].astype(str)
            
            # Sort by timestamp if provided
            if timestamp_col:
                try:
                    df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors='coerce')
                    df = df.dropna(subset=[timestamp_col])
                    df = df.sort_values([sequence_id_col, timestamp_col])
                    logger.info("Sorted sequences by timestamp")
                except Exception as e:
                    logger.warning(f"Could not parse timestamps: {e}. Proceeding without sorting.")
            
            # Group by sequence ID and create sequences
            grouped = df.groupby(sequence_id_col)[item_col].apply(list)
            self.sequences = grouped.tolist()
            self.sequence_count = len(self.sequences)
            
            # Collect unique items
            for sequence in self.sequences:
                self.unique_items.update(sequence)
            
            logger.info(f"Generated {self.sequence_count} sequences with {len(self.unique_items)} unique items")
            
            # Generate statistics
            sequence_lengths = [len(seq) for seq in self.sequences]
            
            result = {
                "total_sequences": self.sequence_count,
                "unique_items": len(self.unique_items),
                "avg_sequence_length": sum(sequence_lengths) / len(sequence_lengths) if sequence_lengths else 0,
                "min_sequence_length": min(sequence_lengths) if sequence_lengths else 0,
                "max_sequence_length": max(sequence_lengths) if sequence_lengths else 0,
                "sample_sequences": [self.sequences[i] for i in range(min(5, len(self.sequences)))]
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating sequences: {str(e)}")
            raise ValueError(f"Failed to generate sequences: {str(e)}")
    
    def get_sequences(self) -> List[List[str]]:
        """
        Get the generated sequences.
        
        Returns:
            List of sequences
        """
        if not self.sequences:
            raise ValueError("No sequences generated. Call generate_sequences() first.")
        return self.sequences
    
    def get_unique_items(self) -> List[str]:
        """
        Get list of unique items across all sequences.
        
        Returns:
            Sorted list of unique items
        """
        return sorted(list(self.unique_items))
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get preprocessing statistics.
        
        Returns:
            Dictionary with statistics
        """
        if not self.sequences:
            return {
                "total_sequences": 0,
                "unique_items": 0,
                "avg_sequence_length": 0
            }
        
        sequence_lengths = [len(seq) for seq in self.sequences]
        
        return {
            "total_sequences": self.sequence_count,
            "unique_items": len(self.unique_items),
            "avg_sequence_length": round(sum(sequence_lengths) / len(sequence_lengths), 2),
            "min_sequence_length": min(sequence_lengths),
            "max_sequence_length": max(sequence_lengths),
            "total_transactions": sum(sequence_lengths)
        }
    
    def filter_sequences(self, min_length: int = 2, max_length: int = None) -> int:
        """
        Filter sequences by length.
        
        Args:
            min_length: Minimum sequence length
            max_length: Maximum sequence length (optional)
            
        Returns:
            Number of sequences after filtering
        """
        original_count = len(self.sequences)
        
        filtered = [seq for seq in self.sequences if len(seq) >= min_length]
        
        if max_length:
            filtered = [seq for seq in filtered if len(seq) <= max_length]
        
        self.sequences = filtered
        self.sequence_count = len(self.sequences)
        
        logger.info(f"Filtered sequences: {original_count} -> {self.sequence_count}")
        return self.sequence_count
