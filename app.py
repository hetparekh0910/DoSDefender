import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from components.attack_analyzer import AttackAnalyzer
from components.case_studies import CaseStudies
from components.attack_vectors import AttackVectors
from components.impact_analysis import ImpactAnalysis
from components.timeline_viz import TimelineVisualizer
from components.educational_resources import EducationalResources
from components.database_admin import DatabaseAdmin

# Configure page
st.set_page_config(
    page_title="DoS Attack Analysis & Education Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🛡️ DoS Attack Analysis & Education Platform")
    st.markdown("""
    **Educational Cybersecurity Tool for Understanding Denial of Service Attacks**
    
    This platform provides comprehensive analysis of DoS attack methodologies, real-world case studies, 
    and system impact assessments for educational and defensive purposes.
    """)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    st.sidebar.markdown("---")
    
    pages = {
        "🏠 Dashboard": "dashboard",
        "📊 Attack Analyzer": "analyzer",
        "📚 Case Studies": "case_studies",
        "🔍 Attack Vectors": "attack_vectors",
        "💥 Impact Analysis": "impact_analysis",
        "📈 Timeline Visualization": "timeline",
        "📖 Educational Resources": "education",
        "🗄️ Database Admin": "database_admin"
    }
    
    selected_page = st.sidebar.selectbox("Select Page", list(pages.keys()))
    page_key = pages[selected_page]
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    **⚠️ Educational Purpose Only**
    
    This tool is designed for:
    - Cybersecurity education
    - Defensive strategy development
    - Understanding attack patterns
    - Security awareness training
    """)
    
    # Route to appropriate page
    if page_key == "dashboard":
        show_dashboard()
    elif page_key == "analyzer":
        AttackAnalyzer().render()
    elif page_key == "case_studies":
        CaseStudies().render()
    elif page_key == "attack_vectors":
        AttackVectors().render()
    elif page_key == "impact_analysis":
        ImpactAnalysis().render()
    elif page_key == "timeline":
        TimelineVisualizer().render()
    elif page_key == "education":
        EducationalResources().render()
    elif page_key == "database_admin":
        DatabaseAdmin().render()

def show_dashboard():
    st.header("📊 DoS Attack Analysis Dashboard")
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Attack Types", "12", delta="2 new")
    
    with col2:
        st.metric("Case Studies", "45", delta="5 recent")
    
    with col3:
        st.metric("Vulnerability Patterns", "8", delta="1 critical")
    
    with col4:
        st.metric("Mitigation Strategies", "23", delta="3 updated")
    
    st.markdown("---")
    
    # Main dashboard content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Attack Frequency Trends")
        
        # Sample data for educational purposes
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        volumetric = [45, 52, 48, 67, 59, 71]
        protocol = [23, 28, 31, 29, 34, 38]
        application = [12, 15, 18, 22, 19, 25]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=volumetric, mode='lines+markers', name='Volumetric', line=dict(color='#FF6B6B')))
        fig.add_trace(go.Scatter(x=months, y=protocol, mode='lines+markers', name='Protocol', line=dict(color='#4ECDC4')))
        fig.add_trace(go.Scatter(x=months, y=application, mode='lines+markers', name='Application Layer', line=dict(color='#45B7D1')))
        
        fig.update_layout(
            title="DoS Attack Types - Educational Analysis",
            xaxis_title="Month",
            yaxis_title="Attack Instances (Educational Data)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Attack Vector Distribution")
        
        attack_types = ['DDoS Flood', 'TCP SYN', 'UDP Flood', 'HTTP Flood', 'Slowloris', 'Other']
        percentages = [35, 22, 18, 12, 8, 5]
        
        fig_pie = px.pie(
            values=percentages, 
            names=attack_types,
            title="Common Attack Vectors (Educational)",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Recent activity section
    st.subheader("📋 Recent Educational Case Studies")
    
    recent_cases = pd.DataFrame({
        'Date': ['2024-01-15', '2024-01-10', '2024-01-05', '2024-01-01'],
        'Target Type': ['E-commerce', 'Financial Services', 'Gaming Platform', 'News Website'],
        'Attack Vector': ['DDoS Amplification', 'TCP SYN Flood', 'Application Layer', 'Volumetric'],
        'Duration': ['4 hours', '2 hours', '6 hours', '3 hours'],
        'Impact Level': ['High', 'Critical', 'Medium', 'High']
    })
    
    st.dataframe(recent_cases, use_container_width=True)
    
    # Quick links section
    st.subheader("🚀 Quick Access")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Analyze Attack Pattern", use_container_width=True):
            st.switch_page("pages/analyzer.py")
    
    with col2:
        if st.button("📚 Browse Case Studies", use_container_width=True):
            st.switch_page("pages/case_studies.py")
    
    with col3:
        if st.button("📖 Learn Mitigation", use_container_width=True):
            st.switch_page("pages/education.py")

if __name__ == "__main__":
    main()
