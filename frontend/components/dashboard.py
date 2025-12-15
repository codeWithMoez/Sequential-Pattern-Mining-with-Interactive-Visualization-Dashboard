"""
Interactive dashboard component for Streamlit frontend.

This component handles:
- All visualization displays
- Interactive charts using Plotly
- Network graphs
- Heatmaps
"""

import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any


def render_dashboard(api_url: str) -> None:
    """
    Render the complete visualization dashboard.
    
    Args:
        api_url: Base URL of the backend API
    """
    st.markdown("## 📊 Interactive Visualization Dashboard")
    st.markdown("Explore mined patterns through interactive visualizations.")
    
    # Summary statistics
    render_summary_statistics(api_url)
    
    st.markdown("---")
    
    # Visualizations in tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Top Patterns",
        "📈 Support Trends",
        "🔥 Co-occurrence Heatmap",
        "🕸️ Sequence Flow Network"
    ])
    
    with tab1:
        render_bar_chart(api_url)
    
    with tab2:
        render_line_chart(api_url)
    
    with tab3:
        render_heatmap(api_url)
    
    with tab4:
        render_network_graph(api_url)


def render_summary_statistics(api_url: str) -> None:
    """
    Render summary statistics cards.
    
    Args:
        api_url: Base URL of the backend API
    """
    try:
        response = requests.get(f"{api_url}/results/summary", timeout=30)
        
        if response.status_code == 200:
            stats = response.json()
            
            st.markdown("### 📈 Summary Statistics")
            
            # First row of metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Patterns", f"{stats['total_patterns']:,}")
            
            with col2:
                st.metric("Total Sequences", f"{stats['total_sequences']:,}")
            
            with col3:
                st.metric("Unique Items", stats['unique_items'])
            
            with col4:
                st.metric("Execution Time", f"{stats['execution_time']:.2f}s")
            
            # Second row of metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Avg Pattern Length", f"{stats['avg_pattern_length']:.2f}")
            
            with col2:
                st.metric("Max Pattern Length", stats.get('max_pattern_length', 'N/A'))
            
            with col3:
                st.metric("Max Support", stats['max_support'])
            
            with col4:
                st.metric("Min Support Threshold", f"{stats['min_support_threshold']*100:.1f}%")
                
    except Exception as e:
        st.error(f"Error loading statistics: {str(e)}")


def render_bar_chart(api_url: str) -> None:
    """
    Render bar chart of top patterns.
    
    Args:
        api_url: Base URL of the backend API
    """
    st.markdown("### 📊 Top Frequent Patterns")
    
    # Parameter for top N
    top_n = st.slider("Number of patterns to display", 5, 50, 20, 5, key="bar_top_n")
    
    try:
        response = requests.get(f"{api_url}/visualizations/bar?top_n={top_n}", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # Create bar chart
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=data['support_counts'],
                y=data['labels'],
                orientation='h',
                marker=dict(
                    color=data['support_percents'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Support %")
                ),
                text=data['support_percents'],
                texttemplate='%{text:.1f}%',
                textposition='auto',
                hovertemplate='<b>%{y}</b><br>Support: %{x}<br>Support: %{text:.1f}%<extra></extra>'
            ))
            
            fig.update_layout(
                title=f"Top {top_n} Sequential Patterns by Support",
                xaxis_title="Support Count",
                yaxis_title="Pattern",
                height=max(400, top_n * 25),
                showlegend=False,
                hovermode='closest'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.info(f"💡 Showing the {top_n} most frequent patterns. Higher support indicates more common patterns.")
            
        else:
            st.error("Failed to load bar chart data.")
            
    except Exception as e:
        st.error(f"Error rendering bar chart: {str(e)}")


def render_line_chart(api_url: str) -> None:
    """
    Render line chart showing support trends by pattern length.
    
    Args:
        api_url: Base URL of the backend API
    """
    st.markdown("### 📈 Support Trends by Pattern Length")
    
    try:
        response = requests.get(f"{api_url}/visualizations/line", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # Create line chart
            fig = go.Figure()
            
            # Average support line
            fig.add_trace(go.Scatter(
                x=data['lengths'],
                y=data['avg_support'],
                mode='lines+markers',
                name='Average Support',
                line=dict(color='blue', width=3),
                marker=dict(size=10),
                hovertemplate='Length: %{x}<br>Avg Support: %{y:.1f}<extra></extra>'
            ))
            
            # Max support line
            fig.add_trace(go.Scatter(
                x=data['lengths'],
                y=data['max_support'],
                mode='lines+markers',
                name='Maximum Support',
                line=dict(color='green', width=2, dash='dash'),
                marker=dict(size=8),
                hovertemplate='Length: %{x}<br>Max Support: %{y}<extra></extra>'
            ))
            
            # Min support line
            fig.add_trace(go.Scatter(
                x=data['lengths'],
                y=data['min_support'],
                mode='lines+markers',
                name='Minimum Support',
                line=dict(color='red', width=2, dash='dot'),
                marker=dict(size=8),
                hovertemplate='Length: %{x}<br>Min Support: %{y}<extra></extra>'
            ))
            
            fig.update_layout(
                title="Support Statistics by Pattern Length",
                xaxis_title="Pattern Length",
                yaxis_title="Support Count",
                height=500,
                hovermode='x unified',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Pattern count bar chart
            fig2 = go.Figure()
            
            fig2.add_trace(go.Bar(
                x=data['lengths'],
                y=data['pattern_count'],
                marker_color='lightblue',
                text=data['pattern_count'],
                textposition='auto',
                hovertemplate='Length: %{x}<br>Pattern Count: %{y}<extra></extra>'
            ))
            
            fig2.update_layout(
                title="Number of Patterns by Length",
                xaxis_title="Pattern Length",
                yaxis_title="Number of Patterns",
                height=400
            )
            
            st.plotly_chart(fig2, use_container_width=True)
            
            st.info("💡 Longer patterns typically have lower support. This shows the distribution of support across different pattern lengths.")
            
        else:
            st.error("Failed to load line chart data.")
            
    except Exception as e:
        st.error(f"Error rendering line chart: {str(e)}")


def render_heatmap(api_url: str) -> None:
    """
    Render heatmap showing item co-occurrence.
    
    Args:
        api_url: Base URL of the backend API
    """
    st.markdown("### 🔥 Item Co-occurrence Heatmap")
    
    try:
        response = requests.get(f"{api_url}/visualizations/heatmap", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # Create heatmap
            fig = go.Figure(data=go.Heatmap(
                z=data['matrix'],
                x=data['items'],
                y=data['items'],
                colorscale='YlOrRd',
                hovertemplate='%{y} ↔ %{x}<br>Co-occurrence: %{z}<extra></extra>'
            ))
            
            fig.update_layout(
                title="Item Co-occurrence Matrix (Top 20 Items)",
                xaxis_title="Item",
                yaxis_title="Item",
                height=600,
                width=600
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.info("💡 Darker colors indicate items that frequently appear together in sequences. Use this to identify strong item associations.")
            
        else:
            st.error("Failed to load heatmap data.")
            
    except Exception as e:
        st.error(f"Error rendering heatmap: {str(e)}")


def render_network_graph(api_url: str) -> None:
    """
    Render network graph showing sequence flows.
    
    Args:
        api_url: Base URL of the backend API
    """
    st.markdown("### 🕸️ Sequence Flow Network")
    
    # Parameter for top N patterns
    top_n = st.slider("Number of patterns to include", 5, 30, 15, 5, key="network_top_n")
    
    try:
        response = requests.get(f"{api_url}/visualizations/network?top_n={top_n}", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # Build network using Plotly
            nodes = data['nodes']
            edges = data['edges']
            
            # Create edge trace
            edge_traces = []
            
            # Simple layout - circular
            import math
            n_nodes = len(nodes)
            node_positions = {}
            
            for i, node in enumerate(nodes):
                angle = 2 * math.pi * i / n_nodes
                x = math.cos(angle)
                y = math.sin(angle)
                node_positions[node['id']] = (x, y)
            
            # Draw edges
            for edge in edges:
                x0, y0 = node_positions[edge['source']]
                x1, y1 = node_positions[edge['target']]
                
                edge_trace = go.Scatter(
                    x=[x0, x1, None],
                    y=[y0, y1, None],
                    mode='lines',
                    line=dict(
                        width=min(edge['weight'] / 10, 5),
                        color='lightgray'
                    ),
                    hoverinfo='none',
                    showlegend=False
                )
                edge_traces.append(edge_trace)
            
            # Draw nodes
            node_x = [node_positions[node['id']][0] for node in nodes]
            node_y = [node_positions[node['id']][1] for node in nodes]
            node_text = [node['label'] for node in nodes]
            
            node_trace = go.Scatter(
                x=node_x,
                y=node_y,
                mode='markers+text',
                text=node_text,
                textposition="top center",
                marker=dict(
                    size=30,
                    color='lightblue',
                    line=dict(width=2, color='darkblue')
                ),
                hovertemplate='<b>%{text}</b><extra></extra>',
                showlegend=False
            )
            
            # Create figure
            fig = go.Figure(data=edge_traces + [node_trace])
            
            fig.update_layout(
                title=f"Sequence Flow Network (Top {top_n} Patterns)",
                showlegend=False,
                hovermode='closest',
                height=600,
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.info("💡 Nodes represent items, edges represent transitions. Thicker edges indicate more frequent transitions.")
            
        else:
            st.error("Failed to load network data.")
            
    except Exception as e:
        st.error(f"Error rendering network graph: {str(e)}")
