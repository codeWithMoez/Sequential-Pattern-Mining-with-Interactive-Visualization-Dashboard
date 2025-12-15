"""
Sequential pattern mining using PrefixSpan algorithm.

This module implements:
- PrefixSpan algorithm for sequential pattern mining
- Support calculation
- Pattern filtering and sorting
"""

from typing import List, Dict, Any, Set, Tuple
from collections import defaultdict
import time
from utils import logger


class PrefixSpan:
    """
    PrefixSpan algorithm implementation for sequential pattern mining.
    
    PrefixSpan is an efficient algorithm that:
    1. Finds frequent patterns in sequence databases
    2. Uses a divide-and-conquer approach
    3. Avoids candidate generation
    """
    
    def __init__(self, sequences: List[List[str]], min_support: float, 
                 max_pattern_length: int = None):
        """
        Initialize PrefixSpan miner.
        
        Args:
            sequences: List of sequences (each sequence is a list of items)
            min_support: Minimum support threshold (0.0 to 1.0)
            max_pattern_length: Maximum pattern length (None for unlimited)
        """
        self.sequences = sequences
        self.min_support = min_support
        self.max_pattern_length = max_pattern_length
        self.min_support_count = max(1, int(min_support * len(sequences)))
        self.frequent_patterns: List[Dict[str, Any]] = []
        self.total_sequences = len(sequences)
        
        logger.info(f"Initialized PrefixSpan with {self.total_sequences} sequences")
        logger.info(f"Min support: {min_support} ({self.min_support_count} sequences)")
    
    def mine_patterns(self) -> List[Dict[str, Any]]:
        """
        Execute the PrefixSpan algorithm to mine frequent patterns.
        
        Returns:
            List of frequent patterns with support information
        """
        logger.info("Starting PrefixSpan mining...")
        start_time = time.time()
        
        # Find frequent 1-patterns (single items)
        frequent_items = self._find_frequent_items()
        
        # Mine patterns recursively
        for item in frequent_items:
            pattern = [item]
            support = self._calculate_support(pattern)
            
            # Add this pattern
            self._add_pattern(pattern, support)
            
            # Build projected database and mine recursively
            if self.max_pattern_length is None or len(pattern) < self.max_pattern_length:
                projected_db = self._build_projected_database(pattern)
                self._mine_recursive(pattern, projected_db, 2)
        
        execution_time = time.time() - start_time
        logger.info(f"Mining completed in {execution_time:.2f} seconds")
        logger.info(f"Found {len(self.frequent_patterns)} frequent patterns")
        
        # Sort patterns by support (descending) and length (descending)
        self.frequent_patterns.sort(key=lambda x: (-x['support'], -x['length']))
        
        return self.frequent_patterns
    
    def _find_frequent_items(self) -> List[str]:
        """
        Find all frequent single items.
        
        Returns:
            List of frequent items
        """
        item_counts = defaultdict(int)
        
        for sequence in self.sequences:
            unique_items = set(sequence)
            for item in unique_items:
                item_counts[item] += 1
        
        frequent_items = [
            item for item, count in item_counts.items() 
            if count >= self.min_support_count
        ]
        
        logger.info(f"Found {len(frequent_items)} frequent single items")
        return sorted(frequent_items)
    
    def _mine_recursive(self, prefix: List[str], projected_db: List[List[str]], 
                       current_length: int) -> None:
        """
        Recursively mine patterns from projected database.
        
        Args:
            prefix: Current pattern prefix
            projected_db: Projected database for this prefix
            current_length: Current pattern length
        """
        # Check max length constraint
        if self.max_pattern_length and current_length > self.max_pattern_length:
            return
        
        # Find frequent items in projected database
        item_counts = defaultdict(int)
        for sequence in projected_db:
            unique_items = set(sequence)
            for item in unique_items:
                item_counts[item] += 1
        
        # Process each frequent item
        for item, count in item_counts.items():
            if count >= self.min_support_count:
                new_pattern = prefix + [item]
                support = self._calculate_support(new_pattern)
                
                # Add this pattern
                self._add_pattern(new_pattern, support)
                
                # Continue mining if within length limit
                if self.max_pattern_length is None or current_length < self.max_pattern_length:
                    new_projected_db = self._build_projected_database(new_pattern)
                    self._mine_recursive(new_pattern, new_projected_db, current_length + 1)
    
    def _build_projected_database(self, pattern: List[str]) -> List[List[str]]:
        """
        Build projected database for a given pattern.
        
        Args:
            pattern: Pattern to project on
            
        Returns:
            Projected database
        """
        projected_db = []
        
        for sequence in self.sequences:
            suffix = self._find_suffix(sequence, pattern)
            if suffix:
                projected_db.append(suffix)
        
        return projected_db
    
    def _find_suffix(self, sequence: List[str], pattern: List[str]) -> List[str]:
        """
        Find suffix of sequence after pattern occurrence.
        
        Args:
            sequence: Input sequence
            pattern: Pattern to match
            
        Returns:
            Suffix after pattern, or None if pattern not found
        """
        pattern_len = len(pattern)
        seq_len = len(sequence)
        
        # Try to match pattern
        for i in range(seq_len - pattern_len + 1):
            match = True
            pattern_idx = 0
            
            for j in range(i, seq_len):
                if pattern_idx < pattern_len:
                    if sequence[j] == pattern[pattern_idx]:
                        pattern_idx += 1
                    else:
                        match = False
                        break
                else:
                    break
            
            if pattern_idx == pattern_len:
                # Found match, return suffix
                end_idx = i + pattern_len
                if end_idx < seq_len:
                    return sequence[end_idx:]
                else:
                    return []
        
        return None
    
    def _calculate_support(self, pattern: List[str]) -> int:
        """
        Calculate support count for a pattern.
        
        Args:
            pattern: Pattern to calculate support for
            
        Returns:
            Support count
        """
        count = 0
        for sequence in self.sequences:
            if self._pattern_in_sequence(pattern, sequence):
                count += 1
        return count
    
    def _pattern_in_sequence(self, pattern: List[str], sequence: List[str]) -> bool:
        """
        Check if pattern appears in sequence.
        
        Args:
            pattern: Pattern to search for
            sequence: Sequence to search in
            
        Returns:
            True if pattern found, False otherwise
        """
        pattern_idx = 0
        pattern_len = len(pattern)
        
        for item in sequence:
            if pattern_idx < pattern_len and item == pattern[pattern_idx]:
                pattern_idx += 1
                if pattern_idx == pattern_len:
                    return True
        
        return False
    
    def _add_pattern(self, pattern: List[str], support: int) -> None:
        """
        Add a frequent pattern to results.
        
        Args:
            pattern: Frequent pattern
            support: Support count
        """
        support_percent = round((support / self.total_sequences) * 100, 2)
        
        self.frequent_patterns.append({
            'sequence': pattern.copy(),
            'support': support,
            'support_percent': support_percent,
            'length': len(pattern)
        })
    
    def get_top_patterns(self, n: int = 50) -> List[Dict[str, Any]]:
        """
        Get top N patterns by support.
        
        Args:
            n: Number of patterns to return
            
        Returns:
            Top N patterns
        """
        return self.frequent_patterns[:n]
    
    def get_patterns_by_length(self, length: int) -> List[Dict[str, Any]]:
        """
        Get all patterns of specific length.
        
        Args:
            length: Pattern length
            
        Returns:
            Patterns of specified length
        """
        return [p for p in self.frequent_patterns if p['length'] == length]
