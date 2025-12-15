"""
Data loading and validation module.

This module handles:
- CSV file upload and validation
- Dataset preview generation
- Initial data quality checks
"""

import pandas as pd
from typing import Dict, Any, List
import io
from utils import logger, validate_file_extension


class DataLoader:
    """Handles dataset loading and validation."""
    
    def __init__(self):
        """Initialize the data loader."""
        self.dataframe: pd.DataFrame = None
        self.filename: str = None
        self.file_size: int = 0
    
    def load_csv_from_bytes(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        """
        Load CSV from uploaded bytes.
        
        Args:
            file_bytes: CSV file content as bytes
            filename: Name of the uploaded file
            
        Returns:
            Dictionary with loading status and preview information
            
        Raises:
            ValueError: If file format is invalid
        """
        logger.info(f"Loading CSV file: {filename}")
        
        # Validate file extension
        if not validate_file_extension(filename, ['.csv']):
            raise ValueError("Only CSV files are supported. Please upload a .csv file.")
        
        try:
            # Read CSV
            self.dataframe = pd.read_csv(io.BytesIO(file_bytes))
            self.filename = filename
            self.file_size = len(file_bytes)
            
            # Validate dataframe
            if self.dataframe.empty:
                raise ValueError("The uploaded CSV file is empty.")
            
            if len(self.dataframe.columns) < 2:
                raise ValueError("CSV must have at least 2 columns (ID and Item).")
            
            logger.info(f"Successfully loaded {len(self.dataframe)} rows and {len(self.dataframe.columns)} columns")
            
            return self.get_preview()
            
        except pd.errors.EmptyDataError:
            logger.error("Empty CSV file uploaded")
            raise ValueError("The CSV file is empty or corrupted.")
        except pd.errors.ParserError as e:
            logger.error(f"CSV parsing error: {str(e)}")
            raise ValueError(f"Failed to parse CSV file: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error loading CSV: {str(e)}")
            raise ValueError(f"Error loading file: {str(e)}")
    
    def get_preview(self, num_rows: int = 10) -> Dict[str, Any]:
        """
        Get dataset preview information.
        
        Args:
            num_rows: Number of rows to include in preview
            
        Returns:
            Dictionary with dataset information
        """
        if self.dataframe is None:
            raise ValueError("No dataset loaded. Please upload a CSV file first.")
        
        # Format file size
        if self.file_size < 1024:
            size_str = f"{self.file_size} bytes"
        elif self.file_size < 1024 * 1024:
            size_str = f"{self.file_size / 1024:.2f} KB"
        else:
            size_str = f"{self.file_size / (1024 * 1024):.2f} MB"
        
        preview_data = self.dataframe.head(num_rows).to_dict('records')
        
        return {
            "filename": self.filename,
            "rows": len(self.dataframe),
            "columns": list(self.dataframe.columns),
            "preview_data": preview_data,
            "file_size": size_str,
            "column_types": {col: str(dtype) for col, dtype in self.dataframe.dtypes.items()}
        }
    
    def get_dataframe(self) -> pd.DataFrame:
        """
        Get the loaded dataframe.
        
        Returns:
            Loaded pandas DataFrame
        """
        if self.dataframe is None:
            raise ValueError("No dataset loaded.")
        return self.dataframe
    
    def get_column_names(self) -> List[str]:
        """
        Get list of column names.
        
        Returns:
            List of column names
        """
        if self.dataframe is None:
            raise ValueError("No dataset loaded.")
        return list(self.dataframe.columns)
    
    def validate_columns(self, sequence_id_col: str, item_col: str, 
                        timestamp_col: str = None) -> Dict[str, bool]:
        """
        Validate if selected columns exist in the dataset.
        
        Args:
            sequence_id_col: Sequence ID column name
            item_col: Item column name
            timestamp_col: Optional timestamp column name
            
        Returns:
            Dictionary with validation results
        """
        if self.dataframe is None:
            raise ValueError("No dataset loaded.")
        
        columns = self.dataframe.columns
        result = {
            "sequence_id_valid": sequence_id_col in columns,
            "item_valid": item_col in columns,
            "timestamp_valid": timestamp_col in columns if timestamp_col else True
        }
        
        if not all(result.values()):
            logger.warning(f"Column validation failed: {result}")
        else:
            logger.info("All selected columns are valid")
        
        return result
