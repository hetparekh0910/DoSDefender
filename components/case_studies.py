"""
Case Studies Component - Real-world DoS attack case studies for educational purposes
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data.dos_attacks_database import DoSAttackDatabase

class CaseStudies:
    def __init__(self):
        self.db = DoSAttackDatabase()
        self.case_studies = self.db.get_all_case_studies()
    
    def render(self):
        st.header("📚 Real-World DoS Attack Case Studies")
        st.markdown("""
        Explore documented DoS attacks against major organizations and learn from their experiences.
        These case studies provide insights into attack methodologies, impacts, and mitigation strategies.
        """)
        
        # Case study selection
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("🔍 Browse Case Studies")
            
            # Search functionality
            search_query = st.text_input("Search cases", placeholder="Enter company name, attack type, or year...")
            
            if search_query:
                filtered_cases = self.db.search_cases(search_query)
            else:
                filtered_cases = self.case_studies
            
            # Case selection
            case_names = [f"{case['name']} ({case['date'][:4]})" for case in filtered_cases]
            
            if case_names:
                selected_case_name = st.selectbox("Select Case Study", case_names)
                selected_case_index = case_names.index(selected_case_name)
                selected_case = filtered_cases[selected_case_index]
            else:
                st.warning("No case studies found matching your search.")
                return
            
            # Quick stats
            st.markdown("---")
            st.markdown("**Quick Stats**")
            st.metric("Peak Traffic", selected_case.get('peak_traffic', 'N/A'))
            st.metric("Duration", selected_case.get('duration', 'N/A'))
            st.metric("Attack Type", selected_case.get('attack_type', 'N/A'))
        
        with col2:
            if selected_case:
                self._render_case_study_details(selected_case)
        
        # Case studies overview
        st.markdown("---")
        self._render_case_studies_overview()
    
    def _render_case_study_details(self, case):
        st.subheader(f"📖 {case['name']}")
        
        # Basic information
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Target**")
            st.write(case['target'])
        
        with col2:
            st.markdown("**Date**")
            st.write(case['date'])
        
        with col3:
            st.markdown("**Attack Type**")
            st.write(case['attack_type'])
        
        # Attack overview
        st.markdown("---")
        st.subheader("🎯 Attack Overview")
        
        # Create attack timeline
        if 'technical_details' in case:
            self._render_attack_timeline(case)
        
        # Impact analysis
        st.subheader("💥 Impact Analysis")
        
        impact = case.get('impact', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Service Impact**")
            st.write(f"**Disruption:** {impact.get('service_disruption', 'N/A')}")
            st.write(f"**Duration:** {impact.get('duration', 'N/A')}")
            st.write(f"**Affected Users:** {impact.get('affected_users', 'N/A')}")
        
        with col2:
            st.markdown("**Business Impact**")
            st.write(f"**Impact:** {impact.get('business_impact', 'N/A')}")
            
            # Visualize impact severity
            severity_score = self._calculate_impact_severity(case)
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = severity_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Impact Severity"},
                gauge = {
                    'axis': {'range': [None, 10]},
                    'bar': {'color': "darkred"},
                    'steps': [
                        {'range': [0, 3], 'color': "lightgray"},
                        {'range': [3, 7], 'color': "yellow"},
                        {'range': [7, 10], 'color': "red"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 8
                    }
                }
            ))
            
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        # Technical details
        st.subheader("🔧 Technical Details")
        
        if 'technical_details' in case:
            tech_details = case['technical_details']
            
            for key, value in tech_details.items():
                st.write(f"**{key.replace('_', ' ').title()}:** {value}")
        
        # Attack vectors
        st.subheader("🎯 Attack Vectors")
        
        attack_vectors = case.get('attack_vectors', [])
        
        if attack_vectors:
            # Create attack vector breakdown
            vector_data = pd.DataFrame({
                'Vector': attack_vectors,
                'Severity': [8, 6, 7][:len(attack_vectors)]  # Sample severity scores
            })
            
            fig = px.bar(
                vector_data, 
                x='Vector', 
                y='Severity',
                title='Attack Vector Breakdown',
                color='Severity',
                color_continuous_scale='Reds'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Mitigation strategies
        st.subheader("🛡️ Mitigation & Response")
        
        mitigation = case.get('mitigation', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Immediate Response**")
            st.write(mitigation.get('immediate', 'Not specified'))
        
        with col2:
            st.markdown("**Long-term Measures**")
            st.write(mitigation.get('long_term', 'Not specified'))
        
        # Lessons learned
        st.subheader("📝 Lessons Learned")
        
        lessons = case.get('lessons_learned', [])
        
        if lessons:
            for i, lesson in enumerate(lessons, 1):
                st.write(f"{i}. {lesson}")
        else:
            st.write("No specific lessons recorded for this case.")
        
        # Download case study
        st.markdown("---")
        
        if st.button("📄 Generate Case Study Report"):
            report = self._generate_case_study_report(case)
            st.download_button(
                label="Download Report",
                data=report,
                file_name=f"case_study_{case['id']}.txt",
                mime="text/plain"
            )
    
    def _render_attack_timeline(self, case):
        st.markdown("**Attack Timeline**")
        
        # Create a simplified timeline based on case data
        timeline_events = []
        
        if case['name'] == 'GitHub DDoS Attack (2018)':
            timeline_events = [
                {'time': '00:00', 'event': 'Normal operations', 'severity': 1},
                {'time': '17:21', 'event': 'Attack detection', 'severity': 5},
                {'time': '17:22', 'event': 'Peak traffic reached (1.35 Tbps)', 'severity': 10},
                {'time': '17:26', 'event': 'Mitigation activated', 'severity': 7},
                {'time': '17:31', 'event': 'Service restored', 'severity': 2}
            ]
        elif case['name'] == 'Dyn DNS Attack (2016)':
            timeline_events = [
                {'time': '07:00', 'event': 'First wave begins', 'severity': 8},
                {'time': '09:00', 'event': 'Major service outages reported', 'severity': 10},
                {'time': '12:00', 'event': 'Second wave detected', 'severity': 9},
                {'time': '16:00', 'event': 'Third wave begins', 'severity': 8},
                {'time': '22:00', 'event': 'Services gradually restored', 'severity': 4}
            ]
        else:
            # Generic timeline
            timeline_events = [
                {'time': '00:00', 'event': 'Attack initiation', 'severity': 6},
                {'time': '00:15', 'event': 'Peak intensity reached', 'severity': 9},
                {'time': '01:00', 'event': 'Mitigation efforts begin', 'severity': 5},
                {'time': '02:00', 'event': 'Services restored', 'severity': 2}
            ]
        
        # Create timeline visualization
        times = [event['time'] for event in timeline_events]
        severities = [event['severity'] for event in timeline_events]
        events = [event['event'] for event in timeline_events]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=times,
            y=severities,
            mode='lines+markers',
            name='Attack Intensity',
            line=dict(color='red', width=3),
            marker=dict(size=10),
            text=events,
            hovertemplate='<b>%{text}</b><br>Time: %{x}<br>Severity: %{y}/10<extra></extra>'
        ))
        
        fig.update_layout(
            title='Attack Timeline',
            xaxis_title='Time',
            yaxis_title='Attack Severity (1-10)',
            hovermode='closest',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _calculate_impact_severity(self, case):
        """Calculate impact severity score based on case details"""
        score = 0
        
        # Duration impact
        duration = case.get('duration', '')
        if 'hours' in duration.lower():
            try:
                hours = int(''.join(filter(str.isdigit, duration.split('hours')[0])))
                score += min(hours / 2, 3)  # Max 3 points for duration
            except:
                score += 2
        elif 'minutes' in duration.lower():
            score += 1
        elif 'days' in duration.lower():
            score += 4
        
        # Traffic volume impact
        peak_traffic = case.get('peak_traffic', '')
        if 'Tbps' in peak_traffic:
            try:
                tbps = float(''.join(filter(lambda x: x.isdigit() or x == '.', peak_traffic.split('Tbps')[0])))
                score += min(tbps, 4)  # Max 4 points for traffic
            except:
                score += 3
        elif 'Gbps' in peak_traffic:
            score += 2
        elif 'Mbps' in peak_traffic:
            score += 1
        
        # Service disruption impact
        impact = case.get('impact', {})
        disruption = impact.get('service_disruption', '').lower()
        if 'complete' in disruption or 'outage' in disruption:
            score += 3
        elif 'major' in disruption:
            score += 2
        elif 'partial' in disruption:
            score += 1
        
        return min(score, 10)  # Cap at 10
    
    def _render_case_studies_overview(self):
        st.subheader("📊 Case Studies Overview")
        
        # Create overview statistics
        case_data = []
        for case in self.case_studies:
            case_data.append({
                'Name': case['name'],
                'Year': int(case['date'][:4]),
                'Target': case['target'],
                'Attack Type': case['attack_type'],
                'Duration': case['duration'],
                'Peak Traffic': case['peak_traffic'],
                'Severity': self._calculate_impact_severity(case)
            })
        
        df = pd.DataFrame(case_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Attack types distribution
            attack_type_counts = df['Attack Type'].value_counts()
            
            fig_pie = px.pie(
                values=attack_type_counts.values,
                names=attack_type_counts.index,
                title="Attack Types Distribution"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Timeline of attacks
            fig_timeline = px.scatter(
                df,
                x='Year',
                y='Severity',
                size='Severity',
                color='Attack Type',
                hover_data=['Name', 'Target'],
                title="Attack Timeline & Severity"
            )
            st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Cases summary table
        st.subheader("📋 All Case Studies")
        
        display_df = df[['Name', 'Year', 'Target', 'Attack Type', 'Duration', 'Severity']].copy()
        display_df['Severity'] = display_df['Severity'].apply(lambda x: f"{x:.1f}/10")
        
        st.dataframe(display_df, use_container_width=True)
        
        # Industry impact analysis
        st.subheader("🏢 Industry Impact Analysis")
        
        # Categorize targets by industry
        industry_mapping = {
            'GitHub': 'Technology',
            'Dyn DNS Infrastructure': 'Internet Infrastructure',
            'CloudFlare Network': 'CDN/Security',
            'AWS Infrastructure': 'Cloud Services'
        }
        
        df['Industry'] = df['Target'].map(industry_mapping)
        
        industry_severity = df.groupby('Industry')['Severity'].mean().sort_values(ascending=False)
        
        fig_industry = px.bar(
            x=industry_severity.index,
            y=industry_severity.values,
            title="Average Attack Severity by Industry",
            labels={'y': 'Average Severity', 'x': 'Industry'}
        )
        
        st.plotly_chart(fig_industry, use_container_width=True)
    
    def _generate_case_study_report(self, case):
        """Generate a downloadable case study report"""
        report = f"""
DoS ATTACK CASE STUDY REPORT
============================

Case: {case['name']}
Date: {case['date']}
Target: {case['target']}
Attack Type: {case['attack_type']}

ATTACK OVERVIEW
---------------
Peak Traffic: {case.get('peak_traffic', 'N/A')}
Duration: {case.get('duration', 'N/A')}
Attack Vectors: {', '.join(case.get('attack_vectors', []))}

IMPACT ANALYSIS
---------------
Service Disruption: {case.get('impact', {}).get('service_disruption', 'N/A')}
Duration: {case.get('impact', {}).get('duration', 'N/A')}
Affected Users: {case.get('impact', {}).get('affected_users', 'N/A')}
Business Impact: {case.get('impact', {}).get('business_impact', 'N/A')}

TECHNICAL DETAILS
-----------------
"""
        
        if 'technical_details' in case:
            for key, value in case['technical_details'].items():
                report += f"{key.replace('_', ' ').title()}: {value}\n"
        
        report += f"""
MITIGATION & RESPONSE
---------------------
Immediate Response: {case.get('mitigation', {}).get('immediate', 'N/A')}
Long-term Measures: {case.get('mitigation', {}).get('long_term', 'N/A')}

LESSONS LEARNED
---------------
"""
        
        lessons = case.get('lessons_learned', [])
        for i, lesson in enumerate(lessons, 1):
            report += f"{i}. {lesson}\n"
        
        report += f"""

EDUCATIONAL NOTE
----------------
This case study is provided for educational and defensive cybersecurity purposes only.
The information is intended to help security professionals understand attack patterns
and develop better defensive strategies.

Generated by DoS Attack Analysis & Education Platform
Report Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return report
