"""
Dataset upload component for Streamlit frontend.

This component handles:
- File upload interface
- Drag and drop functionality
- Upload status display
"""

import streamlit as st
import requests
from typing import Optional, Dict, Any


def render_upload_section(api_url: str) -> Optional[Dict[str, Any]]:
    """
    Render the dataset upload section.
    
    Args:
        api_url: Base URL of the backend API
        
    Returns:
        Dataset preview information if upload successful, None otherwise
    """
    st.markdown("### 📤 Upload Your Dataset")
    st.markdown("Upload a CSV file containing sequential transaction data.")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Upload a CSV file with columns like UserID, Item, Timestamp"
    )
    
    if uploaded_file is not None:
        # Show file info
        file_details = {
            "Filename": uploaded_file.name,
            "FileType": uploaded_file.type,
            "FileSize": f"{uploaded_file.size / 1024:.2f} KB"
        }
        
        with st.expander("📋 File Details", expanded=False):
            for key, value in file_details.items():
                st.write(f"**{key}:** {value}")
        
        # Upload button
        if st.button("🚀 Upload and Validate", type="primary", use_container_width=True):
            with st.spinner("Uploading and validating dataset..."):
                try:
                    # Prepare file for upload
                    files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'text/csv')}
                    
                    # Send to backend
                    response = requests.post(f"{api_url}/upload", files=files, timeout=30)
                    
                    if response.status_code == 200:
                        preview_data = response.json()
                        
                        st.success("✅ Dataset uploaded and validated successfully!")
                        
                        # Store in session state
                        st.session_state['dataset_uploaded'] = True
                        st.session_state['preview_data'] = preview_data
                        
                        return preview_data
                    else:
                        error_detail = response.json().get('detail', 'Unknown error')
                        st.error(f"❌ Upload failed: {error_detail}")
                        return None
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend server. Please ensure the API is running.")
                    st.info("Start the backend with: `python backend/main.py`")
                    return None
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    return None
    
    return None


def display_dataset_preview(preview_data: Dict[str, Any]) -> None:
    """
    Display dataset preview information.
    
    Args:
        preview_data: Preview information from backend
    """
    st.markdown("### 📊 Dataset Preview")
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Rows", f"{preview_data['rows']:,}")
    
    with col2:
        st.metric("Total Columns", len(preview_data['columns']))
    
    with col3:
        st.metric("File Size", preview_data['file_size'])
    
    # Column names
    with st.expander("📝 Available Columns", expanded=False):
        st.write(", ".join(preview_data['columns']))
    
    # Data preview
    st.markdown("#### First Few Rows")
    import pandas as pd
    preview_df = pd.DataFrame(preview_data['preview_data'])
    st.dataframe(preview_df, use_container_width=True, height=300)
