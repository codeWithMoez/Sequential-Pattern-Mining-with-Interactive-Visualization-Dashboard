"""
Column selector component for Streamlit frontend.

This component handles:
- Column selection for preprocessing
- Column mapping interface
- Validation of selections
"""

import streamlit as st
import requests
from typing import Optional, Dict, Any


def render_column_selector(api_url: str, columns: list) -> Optional[Dict[str, str]]:
    """
    Render the column selection interface.
    
    Args:
        api_url: Base URL of the backend API
        columns: List of available column names
        
    Returns:
        Dictionary with selected column names if valid, None otherwise
    """
    st.markdown("### 🎯 Select Columns for Mining")
    st.markdown("Map your dataset columns to the required fields for sequential pattern mining.")
    
    # Create two columns layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Required Fields")
        
        # Sequence ID column
        sequence_id_col = st.selectbox(
            "Sequence/User/Session ID Column",
            options=columns,
            help="Column that identifies different sequences (e.g., UserID, SessionID, TransactionID)"
        )
        
        # Item column
        item_col = st.selectbox(
            "Item/Event Column",
            options=columns,
            index=min(1, len(columns)-1) if len(columns) > 1 else 0,
            help="Column containing items or events in the sequence"
        )
    
    with col2:
        st.markdown("#### Optional Fields")
        
        # Timestamp column (optional)
        use_timestamp = st.checkbox("Use Timestamp for Ordering", value=False)
        
        timestamp_col = None
        if use_timestamp:
            timestamp_col = st.selectbox(
                "Timestamp Column",
                options=columns,
                index=min(2, len(columns)-1) if len(columns) > 2 else 0,
                help="Column containing timestamps for ordering sequences"
            )
    
    # Validation
    st.markdown("---")
    
    # Check for duplicate selections
    selected_cols = [sequence_id_col, item_col]
    if timestamp_col:
        selected_cols.append(timestamp_col)
    
    if len(selected_cols) != len(set(selected_cols)):
        st.warning("⚠️ Please select different columns for each field.")
        return None
    
    # Show selection summary
    with st.expander("📋 Selection Summary", expanded=True):
        st.write(f"**Sequence ID:** `{sequence_id_col}`")
        st.write(f"**Item/Event:** `{item_col}`")
        if timestamp_col:
            st.write(f"**Timestamp:** `{timestamp_col}`")
        else:
            st.write("**Timestamp:** Not selected (sequences will be ordered as they appear)")
    
    return {
        'sequence_id_column': sequence_id_col,
        'item_column': item_col,
        'timestamp_column': timestamp_col
    }


def preprocess_with_columns(api_url: str, column_selection: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """
    Send column selection to backend for preprocessing.
    
    Args:
        api_url: Base URL of the backend API
        column_selection: Dictionary with selected column names
        
    Returns:
        Preprocessing results if successful, None otherwise
    """
    if st.button("🔄 Generate Sequences", type="primary", use_container_width=True):
        with st.spinner("Preprocessing data and generating sequences..."):
            try:
                # Send to backend
                response = requests.post(
                    f"{api_url}/preprocess",
                    json=column_selection,
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success("✅ Sequences generated successfully!")
                    
                    # Store in session state
                    st.session_state['preprocessing_done'] = True
                    st.session_state['preprocessing_result'] = result
                    
                    return result
                else:
                    error_detail = response.json().get('detail', 'Unknown error')
                    st.error(f"❌ Preprocessing failed: {error_detail}")
                    return None
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend server.")
                return None
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                return None
    
    return None


def display_preprocessing_results(result: Dict[str, Any]) -> None:
    """
    Display preprocessing results and statistics.
    
    Args:
        result: Preprocessing results from backend
    """
    st.markdown("### 📈 Preprocessing Results")
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Sequences", f"{result['total_sequences']:,}")
    
    with col2:
        st.metric("Unique Items", result['unique_items'])
    
    with col3:
        st.metric("Avg. Sequence Length", f"{result['avg_sequence_length']:.2f}")
    
    # Additional stats
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Min Sequence Length", result['min_sequence_length'])
    
    with col2:
        st.metric("Max Sequence Length", result['max_sequence_length'])
    
    # Sample sequences
    if 'sample_sequences' in result:
        with st.expander("🔍 Sample Sequences", expanded=False):
            for i, seq in enumerate(result['sample_sequences'], 1):
                seq_str = " → ".join(str(item) for item in seq)
                st.write(f"{i}. {seq_str}")
