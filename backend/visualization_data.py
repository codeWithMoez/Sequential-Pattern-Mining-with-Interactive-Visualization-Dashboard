"""
Visualization data preparation module.

This module converts mining results into formats suitable for:
- Charts and graphs
- Interactive visualizations
- Dashboard displays
"""

import pandas as pd
from typing import List, Dict, Any
from collections import defaultdict, Counter
from utils import logger, format_sequence_for_display


class VisualizationDataGenerator:
    """Prepares mining results for visualization."""
    
    def __init__(self, patterns: List[Dict[str, Any]], sequences: List[List[str]]):
        """
        Initialize the visualization data generator.
        
        Args:
            patterns: List of mined patterns
            sequences: Original sequences
        """
        self.patterns = patterns
        self.sequences = sequences
        self.all_items = self._extract_all_items()
    
    def _extract_all_items(self) -> List[str]:
        """Extract all unique items from sequences."""
        items = set()
        for sequence in self.sequences:
            items.update(sequence)
        return sorted(list(items))
    
    def prepare_bar_chart_data(self, top_n: int = 20) -> Dict[str, Any]:
        """
        Prepare data for bar chart of top patterns.
        
        Args:
            top_n: Number of top patterns to include
            
        Returns:
            Dictionary with chart data
        """
        logger.info(f"Preparing bar chart data for top {top_n} patterns")
        
        top_patterns = self.patterns[:top_n]
        
        labels = [format_sequence_for_display(p['sequence']) for p in top_patterns]
        supports = [p['support'] for p in top_patterns]
        support_percents = [p['support_percent'] for p in top_patterns]
        
        return {
            'labels': labels,
            'support_counts': supports,
            'support_percents': support_percents,
            'pattern_lengths': [p['length'] for p in top_patterns]
        }
    
    def prepare_line_chart_data(self) -> Dict[str, Any]:
        """
        Prepare data for line chart showing support trends by pattern length.
        
        Returns:
            Dictionary with chart data
        """
        logger.info("Preparing line chart data for support trends")
        
        # Group by length
        length_groups = defaultdict(list)
        for pattern in self.patterns:
            length_groups[pattern['length']].append(pattern['support'])
        
        lengths = sorted(length_groups.keys())
        avg_supports = [sum(length_groups[l]) / len(length_groups[l]) for l in lengths]
        max_supports = [max(length_groups[l]) for l in lengths]
        min_supports = [min(length_groups[l]) for l in lengths]
        pattern_counts = [len(length_groups[l]) for l in lengths]
        
        return {
            'lengths': lengths,
            'avg_support': avg_supports,
            'max_support': max_supports,
            'min_support': min_supports,
            'pattern_count': pattern_counts
        }
    
    def prepare_heatmap_data(self) -> Dict[str, Any]:
        """
        Prepare co-occurrence heatmap data.
        
        Returns:
            Dictionary with heatmap data
        """
        logger.info("Preparing heatmap data for item co-occurrence")
        
        # Limit to top items for performance
        top_items = self._get_top_items(20)
        
        # Create co-occurrence matrix
        matrix = defaultdict(lambda: defaultdict(int))
        
        for sequence in self.sequences:
            # Count co-occurrences within sequences
            unique_seq = list(set(sequence))
            for i, item1 in enumerate(unique_seq):
                if item1 in top_items:
                    for item2 in unique_seq[i+1:]:
                        if item2 in top_items:
                            matrix[item1][item2] += 1
                            matrix[item2][item1] += 1
        
        # Convert to list format
        heatmap_data = []
        for item1 in top_items:
            row = []
            for item2 in top_items:
                row.append(matrix[item1][item2])
            heatmap_data.append(row)
        
        return {
            'items': top_items,
            'matrix': heatmap_data
        }
    
    def prepare_network_data(self, top_n: int = 15) -> Dict[str, Any]:
        """
        Prepare network graph data showing sequence transitions.
        
        Args:
            top_n: Number of top patterns to visualize
            
        Returns:
            Dictionary with nodes and edges for network graph
        """
        logger.info(f"Preparing network graph data for top {top_n} patterns")
        
        # Use top patterns
        top_patterns = self.patterns[:top_n]
        
        # Extract nodes and edges
        nodes = set()
        edges = []
        edge_weights = defaultdict(int)
        
        for pattern in top_patterns:
            sequence = pattern['sequence']
            support = pattern['support']
            
            # Add nodes
            nodes.update(sequence)
            
            # Add edges (transitions)
            for i in range(len(sequence) - 1):
                source = sequence[i]
                target = sequence[i + 1]
                edge_key = (source, target)
                edge_weights[edge_key] += support
        
        # Format edges
        for (source, target), weight in edge_weights.items():
            edges.append({
                'source': source,
                'target': target,
                'weight': weight
            })
        
        # Format nodes
        node_list = [{'id': node, 'label': node} for node in nodes]
        
        return {
            'nodes': node_list,
            'edges': edges
        }
    
    def prepare_table_data(self) -> List[Dict[str, Any]]:
        """
        Prepare data for results table.
        
        Returns:
            List of pattern dictionaries formatted for table display
        """
        logger.info("Preparing table data")
        
        table_data = []
        for i, pattern in enumerate(self.patterns, 1):
            table_data.append({
                'rank': i,
                'pattern': format_sequence_for_display(pattern['sequence']),
                'sequence': pattern['sequence'],
                'length': pattern['length'],
                'support': pattern['support'],
                'support_percent': f"{pattern['support_percent']}%"
            })
        
        return table_data
    
    def prepare_summary_stats(self, total_sequences: int, execution_time: float, 
                             min_support: float) -> Dict[str, Any]:
        """
        Prepare summary statistics for dashboard.
        
        Args:
            total_sequences: Total number of sequences
            execution_time: Mining execution time
            min_support: Minimum support used
            
        Returns:
            Dictionary with summary statistics
        """
        if not self.patterns:
            return {
                'total_patterns': 0,
                'total_sequences': total_sequences,
                'unique_items': len(self.all_items),
                'avg_pattern_length': 0,
                'max_support': 0,
                'execution_time': execution_time,
                'min_support_threshold': min_support
            }
        
        pattern_lengths = [p['length'] for p in self.patterns]
        supports = [p['support'] for p in self.patterns]
        
        return {
            'total_patterns': len(self.patterns),
            'total_sequences': total_sequences,
            'unique_items': len(self.all_items),
            'avg_pattern_length': round(sum(pattern_lengths) / len(pattern_lengths), 2),
            'max_pattern_length': max(pattern_lengths),
            'min_pattern_length': min(pattern_lengths),
            'max_support': max(supports),
            'min_support_threshold': min_support,
            'execution_time': round(execution_time, 2)
        }
    
    def _get_top_items(self, n: int) -> List[str]:
        """
        Get top N most frequent items.
        
        Args:
            n: Number of items to return
            
        Returns:
            List of top items
        """
        item_counts = Counter()
        for sequence in self.sequences:
            item_counts.update(sequence)
        
        return [item for item, count in item_counts.most_common(n)]
    
    def export_to_csv(self, filepath: str) -> None:
        """
        Export patterns to CSV file.
        
        Args:
            filepath: Path to save CSV file
        """
        logger.info(f"Exporting patterns to {filepath}")
        
        table_data = self.prepare_table_data()
        df = pd.DataFrame(table_data)
        df.to_csv(filepath, index=False)
        
        logger.info(f"Exported {len(table_data)} patterns to CSV")
