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
    /* Main header styling */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(120deg, #1f77b4 0%, #2ca02c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        font-size: 1.3rem;
        color: #555;
        text-align: center;
        padding-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: #f8f9fa;
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        background-color: white;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e8f4f8;
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(120deg, #1f77b4 0%, #2ca02c 100%) !important;
        color: white !important;
    }
    
    /* Metric container styling */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    div[data-testid="metric-container"] label {
        color: rgba(255,255,255,0.9) !important;
        font-weight: 600 !important;
    }
    
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(120deg, #1f77b4 0%, #2ca02c 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.2);
    }
    
    /* Progress indicators */
    .stProgress > div > div {
        background: linear-gradient(120deg, #1f77b4 0%, #2ca02c 100%);
    }
    
    /* Section separators */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #1f77b4, transparent);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* File uploader styling */
    [data-testid="stFileUploader"] {
        background-color: #f8f9fa;
        border: 2px dashed #1f77b4;
        border-radius: 10px;
        padding: 2rem;
    }
    
    /* Success/Error boxes */
    .success-box {
        padding: 1rem;
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 4px solid #28a745;
        border-radius: 8px;
        color: #155724;
        font-weight: 500;
    }
    
    .stAlert {
        border-radius: 8px;
        border-left-width: 4px;
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
    <div style='text-align: center; color: #888; padding: 2rem 0;'>
        <p style='font-size: 0.9rem; font-weight: 300;'>⛏️ Sequential Pattern Mining Dashboard | Built with Streamlit & FastAPI</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
