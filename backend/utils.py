"""
Utility functions and logging setup for the Sequential Pattern Mining project.

This module provides:
- Logging configuration
- Helper functions for file operations
- Common validation utilities
"""

import logging
import os
from datetime import datetime
from typing import Optional


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Configure and return a logger instance.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("SequentialPatternMining")
    logger.setLevel(getattr(logging, log_level))
    
    # Avoid duplicate handlers
    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
    
    return logger


def ensure_directory_exists(directory_path: str) -> None:
    """
    Create directory if it doesn't exist.
    
    Args:
        directory_path: Path to the directory
    """
    os.makedirs(directory_path, exist_ok=True)


def generate_timestamp_filename(base_name: str, extension: str) -> str:
    """
    Generate a filename with timestamp.
    
    Args:
        base_name: Base name of the file
        extension: File extension (without dot)
        
    Returns:
        Filename with timestamp
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}.{extension}"


def validate_file_extension(filename: str, allowed_extensions: list) -> bool:
    """
    Validate if file has an allowed extension.
    
    Args:
        filename: Name of the file
        allowed_extensions: List of allowed extensions (e.g., ['.csv', '.txt'])
        
    Returns:
        True if valid, False otherwise
    """
    _, ext = os.path.splitext(filename)
    return ext.lower() in allowed_extensions


def format_sequence_for_display(sequence: list) -> str:
    """
    Format a sequence list into a readable string.
    
    Args:
        sequence: List representing a sequence
        
    Returns:
        Formatted string representation
    """
    return " → ".join(str(item) for item in sequence)


def calculate_percentage(value: float, total: float) -> float:
    """
    Calculate percentage with error handling.
    
    Args:
        value: Numerator value
        total: Denominator value
        
    Returns:
        Percentage value
    """
    if total == 0:
        return 0.0
    return round((value / total) * 100, 2)


# Initialize logger
logger = setup_logging()
