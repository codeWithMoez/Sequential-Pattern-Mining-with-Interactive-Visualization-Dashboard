"""
Pydantic schemas for request and response validation.

This module defines all data models used in the API for:
- Request validation
- Response serialization
- Type safety
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator


class ColumnSelectionRequest(BaseModel):
    """Request model for column selection during preprocessing."""
    
    sequence_id_column: str = Field(..., description="Column representing sequence/user/session ID")
    item_column: str = Field(..., description="Column representing items/events")
    timestamp_column: Optional[str] = Field(None, description="Optional timestamp column for ordering")
    
    class Config:
        schema_extra = {
            "example": {
                "sequence_id_column": "UserID",
                "item_column": "Product",
                "timestamp_column": "Date"
            }
        }


class MiningParameters(BaseModel):
    """Parameters for sequential pattern mining."""
    
    min_support: float = Field(0.01, ge=0.001, le=1.0, description="Minimum support threshold (0.001-1.0)")
    max_sequence_length: Optional[int] = Field(None, ge=2, le=10, description="Maximum pattern length")
    
    @validator('min_support')
    def validate_support(cls, v):
        """Ensure minimum support is valid."""
        if not 0.001 <= v <= 1.0:
            raise ValueError('Minimum support must be between 0.001 and 1.0')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "min_support": 0.05,
                "max_sequence_length": 5
            }
        }


class PreprocessingRequest(BaseModel):
    """Complete request for preprocessing and mining."""
    
    columns: ColumnSelectionRequest
    parameters: MiningParameters


class SequencePattern(BaseModel):
    """Model for a single mined pattern."""
    
    sequence: List[str] = Field(..., description="The sequential pattern")
    support: int = Field(..., description="Support count")
    support_percent: float = Field(..., description="Support percentage")
    length: int = Field(..., description="Pattern length")
    
    class Config:
        schema_extra = {
            "example": {
                "sequence": ["A", "B", "C"],
                "support": 150,
                "support_percent": 15.5,
                "length": 3
            }
        }


class MiningResult(BaseModel):
    """Complete mining result response."""
    
    patterns: List[SequencePattern] = Field(..., description="List of mined patterns")
    total_patterns: int = Field(..., description="Total number of patterns found")
    total_sequences: int = Field(..., description="Total sequences in dataset")
    min_support_used: float = Field(..., description="Minimum support threshold used")
    execution_time: float = Field(..., description="Execution time in seconds")
    
    class Config:
        schema_extra = {
            "example": {
                "patterns": [
                    {
                        "sequence": ["A", "B"],
                        "support": 200,
                        "support_percent": 20.0,
                        "length": 2
                    }
                ],
                "total_patterns": 50,
                "total_sequences": 1000,
                "min_support_used": 0.05,
                "execution_time": 2.5
            }
        }


class DatasetPreview(BaseModel):
    """Dataset preview information."""
    
    filename: str
    rows: int
    columns: List[str]
    preview_data: List[Dict[str, Any]]
    file_size: str
    
    class Config:
        schema_extra = {
            "example": {
                "filename": "transactions.csv",
                "rows": 10000,
                "columns": ["UserID", "Product", "Date"],
                "preview_data": [{"UserID": 1, "Product": "A", "Date": "2023-01-01"}],
                "file_size": "512 KB"
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response."""
    
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    
    class Config:
        schema_extra = {
            "example": {
                "error": "Invalid CSV format",
                "detail": "Missing required columns"
            }
        }
