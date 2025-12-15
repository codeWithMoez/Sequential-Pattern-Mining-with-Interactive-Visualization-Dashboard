"""
Results table component for Streamlit frontend.

This component handles:
- Display of mined patterns in table format
- Filtering and sorting
- Export functionality
"""

import streamlit as st
import requests
import pandas as pd
from typing import Dict, Any


def render_results_table(api_url: str) -> None:
    """
    Render the results table with all mined patterns.
    
    Args:
        api_url: Base URL of the backend API
    """
    st.markdown("### 📋 All Mined Patterns")
    
    try:
        # Fetch table data from backend
        response = requests.get(f"{api_url}/results/table", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            patterns = data['patterns']
            
            if not patterns:
                st.info("No patterns found with the current parameters.")
                return
            
            # Convert to DataFrame
            df = pd.DataFrame(patterns)
            
            # Filters
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Length filter
                lengths = sorted(df['length'].unique())
                selected_lengths = st.multiselect(
                    "Filter by Length",
                    options=lengths,
                    default=lengths,
                    help="Select pattern lengths to display"
                )
            
            with col2:
                # Support filter
                min_support = st.number_input(
                    "Minimum Support Count",
                    min_value=int(df['support'].min()),
                    max_value=int(df['support'].max()),
                    value=int(df['support'].min()),
                    help="Filter patterns by minimum support"
                )
            
            with col3:
                # Top N filter
                top_n = st.number_input(
                    "Show Top N Patterns",
                    min_value=10,
                    max_value=len(patterns),
                    value=min(50, len(patterns)),
                    step=10,
                    help="Limit number of patterns displayed"
                )
            
            # Apply filters
            filtered_df = df[
                (df['length'].isin(selected_lengths)) &
                (df['support'] >= min_support)
            ].head(top_n)
            
            # Display count
            st.markdown(f"Showing **{len(filtered_df)}** of **{len(patterns)}** patterns")
            
            # Display table
            st.dataframe(
                filtered_df,
                use_container_width=True,
                height=400,
                column_config={
                    "rank": "Rank",
                    "pattern": "Pattern",
                    "length": "Length",
                    "support": "Support",
                    "support_percent": "Support %"
                },
                hide_index=True
            )
            
            # Export options
            st.markdown("---")
            col1, col2 = st.columns([3, 1])
            
            with col2:
                # Download as CSV
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name="mined_patterns.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
        else:
            st.error("Failed to fetch results from backend.")
            
    except Exception as e:
        st.error(f"Error displaying results: {str(e)}")


def render_pattern_details(pattern: Dict[str, Any]) -> None:
    """
    Render detailed view of a specific pattern.
    
    Args:
        pattern: Pattern information
    """
    with st.container():
        st.markdown(f"#### Pattern: {pattern['pattern']}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Support Count", pattern['support'])
        
        with col2:
            st.metric("Support %", pattern['support_percent'])
        
        with col3:
            st.metric("Length", pattern['length'])
        
        # Show sequence
        st.markdown("**Sequence:**")
        st.code(" → ".join(pattern['sequence']))
