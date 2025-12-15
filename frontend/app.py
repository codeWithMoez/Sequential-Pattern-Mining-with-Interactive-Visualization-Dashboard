"""
Main Streamlit Application for Sequential Pattern Mining.

This is the entry point for the frontend interface.
It orchestrates all components and manages the application flow.
"""

import streamlit as st
import sys
from pathlib import Path

# Add components to path
sys.path.append(str(Path(__file__).parent / "components"))

from components import upload, column_selector, parameters, dashboard, tables


# Page configuration
st.set_page_config(
    page_title="Sequential Pattern Mining Dashboard",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        padding-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
    }
    div[data-testid="metric-container"] {
        background-color: #f0f2f6;
        border: 1px solid #e0e0e0;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        color: #155724;
    }
</style>
""", unsafe_allow_html=True)

# Backend API URL
API_URL = "http://localhost:8000"

# Initialize session state
if 'dataset_uploaded' not in st.session_state:
    st.session_state['dataset_uploaded'] = False
if 'preprocessing_done' not in st.session_state:
    st.session_state['preprocessing_done'] = False
if 'mining_done' not in st.session_state:
    st.session_state['mining_done'] = False


def render_header():
    """Render the application header and description."""
    st.markdown('<h1 class="main-header">⛏️ Sequential Pattern Mining Dashboard</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Discover hidden patterns in sequential data with interactive visualizations</p>',
        unsafe_allow_html=True
    )
    
    # Project description
    with st.expander("ℹ️ About This Project", expanded=False):
        st.markdown("""
        ### What is Sequential Pattern Mining?
        
        Sequential pattern mining is a data mining technique that discovers frequent patterns in sequences.
        It identifies subsequences that appear frequently across multiple sequences.
        
        **Use Cases:**
        - 🛒 **E-commerce:** Analyze customer purchase sequences
        - 🌐 **Web Analytics:** Discover navigation patterns
        - 🏥 **Healthcare:** Identify treatment sequences
        - 📱 **App Usage:** Understand user behavior flows
        
        ### Algorithm: PrefixSpan
        
        This project uses the **PrefixSpan** algorithm, which:
        - Efficiently mines sequential patterns without candidate generation
        - Uses a divide-and-conquer approach
        - Scales well with large datasets
        
        ### How to Use
        
        1. **Upload Dataset:** Upload a CSV file with sequential transaction data
        2. **Select Columns:** Map your dataset columns (ID, Item, Timestamp)
        3. **Configure Parameters:** Set minimum support and pattern length
        4. **Mine Patterns:** Execute the mining algorithm
        5. **Explore Results:** Interact with visualizations and download results
        """)


def render_sidebar():
    """Render the sidebar with navigation and status."""
    with st.sidebar:
        st.markdown("## 📋 Progress Tracker")
        
        # Progress indicators
        steps = [
            ("1. Upload Dataset", st.session_state.get('dataset_uploaded', False)),
            ("2. Preprocess Data", st.session_state.get('preprocessing_done', False)),
            ("3. Mine Patterns", st.session_state.get('mining_done', False))
        ]
        
        for step, completed in steps:
            if completed:
                st.success(f"✅ {step}")
            else:
                st.info(f"⏳ {step}")
        
        st.markdown("---")
        
        # Backend status
        st.markdown("### 🔌 Backend Status")
        try:
            import requests
            response = requests.get(f"{API_URL}/", timeout=2)
            if response.status_code == 200:
                st.success("✅ Connected")
            else:
                st.error("❌ Error")
        except:
            st.error("❌ Disconnected")
            st.warning("Start backend: `python backend/main.py`")
        
        st.markdown("---")
        
        # Additional info
        st.markdown("### 📚 Resources")
        st.markdown("""
        - [Documentation](#)
        - [GitHub Repository](#)
        - [Report Issue](#)
        """)
        
        st.markdown("---")
        st.markdown("### 👨‍💻 Developer")
        st.markdown("**University Final Year Project**")
        st.markdown("*Sequential Pattern Mining*")


def main():
    """Main application flow."""
    
    # Render header
    render_header()
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    st.markdown("---")
    
    # Step 1: Upload Dataset
    st.markdown("## Step 1: Upload Dataset")
    preview_data = upload.render_upload_section(API_URL)
    
    if preview_data or st.session_state.get('dataset_uploaded', False):
        # Use stored preview data if available
        if preview_data is None and 'preview_data' in st.session_state:
            preview_data = st.session_state['preview_data']
        
        if preview_data:
            upload.display_dataset_preview(preview_data)
        
        st.markdown("---")
        
        # Step 2: Column Selection and Preprocessing
        st.markdown("## Step 2: Configure Data Mapping")
        
        columns = preview_data['columns']
        column_selection = column_selector.render_column_selector(API_URL, columns)
        
        if column_selection:
            preprocessing_result = column_selector.preprocess_with_columns(API_URL, column_selection)
            
            if preprocessing_result or st.session_state.get('preprocessing_done', False):
                # Use stored preprocessing result if available
                if preprocessing_result is None and 'preprocessing_result' in st.session_state:
                    preprocessing_result = st.session_state['preprocessing_result']
                
                if preprocessing_result:
                    column_selector.display_preprocessing_results(preprocessing_result)
                
                st.markdown("---")
                
                # Step 3: Mining Parameters
                st.markdown("## Step 3: Configure Mining Parameters")
                
                mining_params = parameters.render_parameters_section()
                mining_result = parameters.execute_mining(API_URL, mining_params)
                
                if mining_result or st.session_state.get('mining_done', False):
                    # Use stored mining result if available
                    if mining_result is None and 'mining_result' in st.session_state:
                        mining_result = st.session_state['mining_result']
                    
                    if mining_result:
                        parameters.display_mining_summary(mining_result)
                    
                    st.markdown("---")
                    
                    # Step 4: Visualizations
                    dashboard.render_dashboard(API_URL)
                    
                    st.markdown("---")
                    
                    # Step 5: Results Table
                    tables.render_results_table(API_URL)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p>⛏️ Sequential Pattern Mining Dashboard | Built with Streamlit & FastAPI | © 2023</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
