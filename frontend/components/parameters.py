"""
Mining parameters component for Streamlit frontend.

This component handles:
- Mining parameter configuration
- Parameter validation
- Mining execution trigger
"""

import streamlit as st
import requests
from typing import Optional, Dict, Any


def render_parameters_section() -> Dict[str, Any]:
    """
    Render the mining parameters configuration section.
    
    Returns:
        Dictionary with mining parameters
    """
    st.markdown("### ⚙️ Mining Parameters")
    st.markdown("Configure the sequential pattern mining algorithm parameters.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Support Threshold")
        
        # Min support slider
        min_support = st.slider(
            "Minimum Support",
            min_value=0.001,
            max_value=0.5,
            value=0.05,
            step=0.001,
            format="%.3f",
            help="Minimum frequency threshold for patterns (0.001 = 0.1%, 0.05 = 5%)"
        )
        
        # Show support info
        st.info(f"📊 Patterns must appear in at least **{min_support*100:.1f}%** of sequences")
    
    with col2:
        st.markdown("#### Pattern Length")
        
        # Max pattern length
        limit_length = st.checkbox("Limit Maximum Pattern Length", value=True)
        
        max_length = None
        if limit_length:
            max_length = st.slider(
                "Maximum Pattern Length",
                min_value=2,
                max_value=10,
                value=5,
                step=1,
                help="Maximum number of items in a pattern"
            )
            st.info(f"🔢 Find patterns with up to **{max_length}** items")
        else:
            st.info("🔢 No length limit (may take longer)")
    
    st.markdown("---")
    
    # Parameter summary
    with st.expander("📋 Parameter Summary", expanded=True):
        st.write(f"**Minimum Support:** {min_support} ({min_support*100:.1f}%)")
        st.write(f"**Maximum Pattern Length:** {max_length if max_length else 'Unlimited'}")
        
        # Mining recommendations
        st.markdown("##### 💡 Recommendations")
        if min_support < 0.01:
            st.warning("⚠️ Very low support may result in many patterns and longer execution time.")
        elif min_support > 0.2:
            st.warning("⚠️ High support may result in very few patterns.")
        else:
            st.success("✅ Good support threshold for balanced results.")
    
    return {
        'min_support': min_support,
        'max_sequence_length': max_length
    }


def execute_mining(api_url: str, parameters: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Execute pattern mining with given parameters.
    
    Args:
        api_url: Base URL of the backend API
        parameters: Mining parameters
        
    Returns:
        Mining results if successful, None otherwise
    """
    st.markdown("---")
    
    if st.button("⛏️ Start Mining Patterns", type="primary", use_container_width=True, key="mine_button"):
        with st.spinner("Mining sequential patterns... This may take a few moments."):
            # Progress placeholder
            progress_text = st.empty()
            progress_bar = st.progress(0)
            
            try:
                progress_text.text("Initializing PrefixSpan algorithm...")
                progress_bar.progress(20)
                
                # Send mining request
                response = requests.post(
                    f"{api_url}/mine",
                    json=parameters,
                    timeout=300  # 5 minutes timeout for large datasets
                )
                
                progress_bar.progress(80)
                progress_text.text("Processing results...")
                
                if response.status_code == 200:
                    result = response.json()
                    
                    progress_bar.progress(100)
                    progress_text.empty()
                    progress_bar.empty()
                    
                    st.success(f"✅ Mining completed! Found {result['total_patterns']} patterns in {result['execution_time']:.2f} seconds")
                    
                    # Store in session state
                    st.session_state['mining_done'] = True
                    st.session_state['mining_result'] = result
                    
                    return result
                else:
                    progress_text.empty()
                    progress_bar.empty()
                    
                    error_detail = response.json().get('detail', 'Unknown error')
                    st.error(f"❌ Mining failed: {error_detail}")
                    return None
                    
            except requests.exceptions.Timeout:
                progress_text.empty()
                progress_bar.empty()
                st.error("❌ Mining timed out. Try increasing minimum support or limiting pattern length.")
                return None
            except requests.exceptions.ConnectionError:
                progress_text.empty()
                progress_bar.empty()
                st.error("❌ Cannot connect to backend server.")
                return None
            except Exception as e:
                progress_text.empty()
                progress_bar.empty()
                st.error(f"❌ Error: {str(e)}")
                return None
    
    return None


def display_mining_summary(result: Dict[str, Any]) -> None:
    """
    Display mining results summary.
    
    Args:
        result: Mining results from backend
    """
    st.markdown("### 🎉 Mining Results Summary")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Patterns Found", f"{result['total_patterns']:,}")
    
    with col2:
        st.metric("Sequences Analyzed", f"{result['total_sequences']:,}")
    
    with col3:
        st.metric("Min Support Used", f"{result['min_support_used']*100:.1f}%")
    
    with col4:
        st.metric("Execution Time", f"{result['execution_time']:.2f}s")
    
    # Success message
    st.success("🎊 Pattern mining completed successfully! Scroll down to view visualizations.")
