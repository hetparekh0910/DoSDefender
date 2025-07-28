"""
Timeline Visualization Component - Interactive DoS attack timeline analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
from data.dos_attacks_database import DoSAttackDatabase

class TimelineVisualizer:
    def __init__(self):
        self.db = DoSAttackDatabase()
        self.case_studies = self.db.get_all_case_studies()
    
    def render(self):
        st.header("📈 Attack Timeline Visualization")
        st.markdown("""
        Visualize DoS attack progression, escalation patterns, and temporal characteristics.
        Understanding attack timelines helps in developing better detection and response strategies.
        """)
        
        # Timeline analysis mode
        analysis_mode = st.selectbox(
            "Select Timeline Analysis",
            ["Attack Progression", "Historical Timeline", "Escalation Patterns", "Multi-Attack Comparison"]
        )
        
        if analysis_mode == "Attack Progression":
            self._render_attack_progression()
        elif analysis_mode == "Historical Timeline":
            self._render_historical_timeline()
        elif analysis_mode == "Escalation Patterns":
            self._render_escalation_patterns()
        elif analysis_mode == "Multi-Attack Comparison":
            self._render_multi_attack_comparison()
    
    def _render_attack_progression(self):
        st.subheader("⏱️ Attack Progression Analysis")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Attack Configuration**")
            
            # Attack parameters
            attack_type = st.selectbox(
                "Attack Type",
                ["DDoS Volumetric", "SYN Flood", "HTTP Flood", "Slowloris", "Multi-vector"]
            )
            
            attack_duration = st.slider(
                "Attack Duration (hours)",
                min_value=1,
                max_value=48,
                value=8
            )
            
            intensity_pattern = st.selectbox(
                "Intensity Pattern",
                ["Constant", "Escalating", "Pulsing", "Decreasing", "Random"]
            )
            
            start_intensity = st.slider(
                "Starting Intensity (1-10)",
                min_value=1,
                max_value=10,
                value=5
            )
            
            if st.button("Generate Attack Timeline"):
                st.session_state['attack_timeline'] = {
                    'type': attack_type,
                    'duration': attack_duration,
                    'pattern': intensity_pattern,
                    'start_intensity': start_intensity
                }
        
        with col2:
            if 'attack_timeline' in st.session_state:
                self._show_attack_progression_timeline()
        
        # Attack phases analysis
        if 'attack_timeline' in st.session_state:
            st.markdown("---")
            self._render_attack_phases()
    
    def _show_attack_progression_timeline(self):
        config = st.session_state['attack_timeline']
        
        st.markdown("**Attack Progression Timeline**")
        
        # Generate timeline data
        hours = config['duration']
        time_points = np.linspace(0, hours, hours * 12)  # 5-minute intervals
        
        # Generate intensity based on pattern
        intensities = self._generate_intensity_pattern(
            time_points, config['pattern'], config['start_intensity']
        )
        
        # Convert to datetime for better visualization
        start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        timestamps = [start_time + timedelta(hours=t) for t in time_points]
        
        # Create main timeline
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=(
                'Attack Intensity Over Time',
                'System Performance Impact',
                'Network Utilization'
            ),
            vertical_spacing=0.08,
            shared_xaxes=True
        )
        
        # Attack intensity
        fig.add_trace(
            go.Scatter(
                x=timestamps,
                y=intensities,
                mode='lines+markers',
                name='Attack Intensity',
                line=dict(color='red', width=2),
                marker=dict(size=4)
            ),
            row=1, col=1
        )
        
        # System performance (inverse of attack intensity)
        performance = [max(10, 100 - (i * 9)) for i in intensities]
        fig.add_trace(
            go.Scatter(
                x=timestamps,
                y=performance,
                mode='lines',
                name='System Performance %',
                line=dict(color='blue', width=2),
                fill='tonexty'
            ),
            row=2, col=1
        )
        
        # Network utilization
        network_util = [min(100, i * 8 + np.random.normal(0, 5)) for i in intensities]
        fig.add_trace(
            go.Scatter(
                x=timestamps,
                y=network_util,
                mode='lines',
                name='Network Utilization %',
                line=dict(color='orange', width=2)
            ),
            row=3, col=1
        )
        
        # Add attack phases annotations
        self._add_attack_phase_annotations(fig, timestamps, intensities, config)
        
        fig.update_layout(
            height=800,
            title_text=f"{config['type']} Attack Progression - {config['pattern']} Pattern",
            showlegend=True
        )
        
        fig.update_xaxes(title_text="Time", row=3, col=1)
        fig.update_yaxes(title_text="Intensity (1-10)", row=1, col=1)
        fig.update_yaxes(title_text="Performance %", row=2, col=1)
        fig.update_yaxes(title_text="Network %", row=3, col=1)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Timeline statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            peak_intensity = max(intensities)
            st.metric("Peak Intensity", f"{peak_intensity:.1f}/10")
        
        with col2:
            avg_intensity = np.mean(intensities)
            st.metric("Average Intensity", f"{avg_intensity:.1f}/10")
        
        with col3:
            min_performance = min(performance)
            st.metric("Minimum Performance", f"{min_performance:.1f}%")
        
        with col4:
            max_network_util = max(network_util)
            st.metric("Peak Network Usage", f"{max_network_util:.1f}%")
    
    def _render_attack_phases(self):
        st.subheader("📊 Attack Phases Analysis")
        
        config = st.session_state['attack_timeline']
        
        # Define attack phases based on duration and pattern
        phases = self._identify_attack_phases(config)
        
        # Create phase analysis visualization
        col1, col2 = st.columns(2)
        
        with col1:
            # Phase duration chart
            phase_names = [phase['name'] for phase in phases]
            phase_durations = [phase['duration'] for phase in phases]
            phase_intensities = [phase['avg_intensity'] for phase in phases]
            
            fig_phases = go.Figure()
            
            fig_phases.add_trace(go.Bar(
                x=phase_names,
                y=phase_durations,
                name='Duration (hours)',
                marker_color='lightblue',
                yaxis='y'
            ))
            
            fig_phases.add_trace(go.Scatter(
                x=phase_names,
                y=phase_intensities,
                mode='lines+markers',
                name='Avg Intensity',
                line=dict(color='red', width=3),
                yaxis='y2'
            ))
            
            fig_phases.update_layout(
                title='Attack Phases Breakdown',
                xaxis=dict(title='Phase'),
                yaxis=dict(title='Duration (hours)', side='left'),
                yaxis2=dict(title='Intensity', side='right', overlaying='y'),
                legend=dict(x=0.7, y=1)
            )
            
            st.plotly_chart(fig_phases, use_container_width=True)
        
        with col2:
            # Phase characteristics
            st.markdown("**Phase Characteristics**")
            
            for phase in phases:
                with st.expander(f"{phase['name']} ({phase['duration']:.1f}h)"):
                    st.write(f"**Average Intensity**: {phase['avg_intensity']:.1f}/10")
                    st.write(f"**Peak Intensity**: {phase['peak_intensity']:.1f}/10")
                    st.write(f"**Characteristics**: {phase['description']}")
                    st.write(f"**Typical Activities**: {phase['activities']}")
        
        # Phase transition analysis
        st.markdown("---")
        st.subheader("🔄 Phase Transitions")
        
        # Create phase transition matrix
        transition_data = self._calculate_phase_transitions(phases)
        
        if transition_data:
            transition_df = pd.DataFrame(transition_data)
            
            fig_transitions = px.line(
                transition_df,
                x='Time',
                y='Transition_Rate',
                title='Phase Transition Rates',
                labels={'Transition_Rate': 'Transition Intensity'}
            )
            
            st.plotly_chart(fig_transitions, use_container_width=True)
    
    def _render_historical_timeline(self):
        st.subheader("📅 Historical DoS Attacks Timeline")
        
        # Timeline configuration
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Timeline Configuration**")
            
            # Date range
            start_year = st.selectbox("Start Year", [2015, 2016, 2017, 2018, 2019, 2020], index=0)
            end_year = st.selectbox("End Year", [2020, 2021, 2022, 2023, 2024], index=4)
            
            # Filter options
            attack_types = st.multiselect(
                "Filter by Attack Type",
                ["DDoS", "Amplification", "Volumetric", "Protocol", "Application"],
                default=["DDoS", "Amplification"]
            )
            
            # Industry filter
            industries = st.multiselect(
                "Filter by Industry",
                ["Technology", "Financial", "Gaming", "Media", "E-commerce"],
                default=["Technology", "Financial"]
            )
            
            show_details = st.checkbox("Show attack details", value=True)
        
        with col2:
            self._show_historical_timeline(start_year, end_year, attack_types, industries, show_details)
        
        # Historical trends analysis
        st.markdown("---")
        self._render_historical_trends()
    
    def _show_historical_timeline(self, start_year, end_year, attack_types, industries, show_details):
        st.markdown("**Historical Attack Timeline**")
        
        # Filter case studies
        filtered_cases = []
        for case in self.case_studies:
            case_year = int(case['date'][:4])
            if start_year <= case_year <= end_year:
                filtered_cases.append(case)
        
        if not filtered_cases:
            st.warning("No attacks found in the selected time range.")
            return
        
        # Create timeline data
        timeline_data = []
        for case in filtered_cases:
            timeline_data.append({
                'Date': case['date'],
                'Name': case['name'],
                'Target': case['target'],
                'Attack_Type': case['attack_type'],
                'Peak_Traffic': case['peak_traffic'],
                'Duration': case['duration'],
                'Severity': self._calculate_severity_score(case)
            })
        
        df = pd.DataFrame(timeline_data)
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Create interactive timeline
        fig = go.Figure()
        
        # Add attack events as scatter points
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Severity'],
            mode='markers+text',
            marker=dict(
                size=df['Severity'] * 2,
                color=df['Severity'],
                colorscale='Reds',
                colorbar=dict(title="Severity Score"),
                line=dict(width=1, color='black')
            ),
            text=df['Name'] if show_details else '',
            textposition='top center',
            hovertemplate='<b>%{text}</b><br>' +
                         'Date: %{x}<br>' +
                         'Target: %{customdata[0]}<br>' +
                         'Type: %{customdata[1]}<br>' +
                         'Peak Traffic: %{customdata[2]}<br>' +
                         'Duration: %{customdata[3]}<br>' +
                         'Severity: %{y}/10<extra></extra>',
            customdata=df[['Target', 'Attack_Type', 'Peak_Traffic', 'Duration']].values,
            name='DoS Attacks'
        ))
        
        fig.update_layout(
            title='Historical DoS Attacks Timeline',
            xaxis_title='Date',
            yaxis_title='Attack Severity (1-10)',
            hovermode='closest',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Attack summary table
        if show_details:
            st.markdown("**Attack Details**")
            display_df = df[['Date', 'Name', 'Target', 'Attack_Type', 'Peak_Traffic', 'Duration', 'Severity']].copy()
            display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
            display_df['Severity'] = display_df['Severity'].apply(lambda x: f"{x:.1f}/10")
            st.dataframe(display_df, use_container_width=True)
    
    def _render_historical_trends(self):
        st.subheader("📈 Historical Trends Analysis")
        
        # Create trend analysis
        trend_data = []
        for case in self.case_studies:
            year = int(case['date'][:4])
            
            # Extract traffic volume (simplified)
            traffic_str = case['peak_traffic']
            if 'Tbps' in traffic_str:
                traffic = float(''.join(filter(lambda x: x.isdigit() or x == '.', traffic_str.split('Tbps')[0]))) * 1000
            elif 'Gbps' in traffic_str:
                traffic = float(''.join(filter(lambda x: x.isdigit() or x == '.', traffic_str.split('Gbps')[0])))
            else:
                traffic = 500  # Default
            
            trend_data.append({
                'Year': year,
                'Traffic_Gbps': traffic,
                'Attack_Type': case['attack_type'],
                'Target_Industry': self._categorize_target(case['target'])
            })
        
        trend_df = pd.DataFrame(trend_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Traffic volume trends
            yearly_traffic = trend_df.groupby('Year')['Traffic_Gbps'].agg(['mean', 'max']).reset_index()
            
            fig_traffic = go.Figure()
            
            fig_traffic.add_trace(go.Scatter(
                x=yearly_traffic['Year'],
                y=yearly_traffic['mean'],
                mode='lines+markers',
                name='Average Traffic',
                line=dict(color='blue')
            ))
            
            fig_traffic.add_trace(go.Scatter(
                x=yearly_traffic['Year'],
                y=yearly_traffic['max'],
                mode='lines+markers',
                name='Peak Traffic',
                line=dict(color='red')
            ))
            
            fig_traffic.update_layout(
                title='Attack Traffic Volume Trends',
                xaxis_title='Year',
                yaxis_title='Traffic (Gbps)',
                yaxis_type='log'
            )
            
            st.plotly_chart(fig_traffic, use_container_width=True)
        
        with col2:
            # Attack type evolution
            attack_evolution = trend_df.groupby(['Year', 'Attack_Type']).size().unstack(fill_value=0)
            
            fig_evolution = go.Figure()
            
            colors = ['red', 'blue', 'green', 'orange', 'purple']
            for i, attack_type in enumerate(attack_evolution.columns):
                fig_evolution.add_trace(go.Scatter(
                    x=attack_evolution.index,
                    y=attack_evolution[attack_type],
                    mode='lines+markers',
                    name=attack_type,
                    line=dict(color=colors[i % len(colors)]),
                    stackgroup='one'
                ))
            
            fig_evolution.update_layout(
                title='Attack Type Evolution',
                xaxis_title='Year',
                yaxis_title='Number of Attacks'
            )
            
            st.plotly_chart(fig_evolution, use_container_width=True)
        
        # Industry targeting trends
        st.markdown("**Industry Targeting Trends**")
        
        industry_trends = trend_df.groupby(['Year', 'Target_Industry']).size().unstack(fill_value=0)
        
        fig_industry = px.bar(
            industry_trends,
            title='Industry Targeting Over Time',
            labels={'value': 'Number of Attacks', 'index': 'Year'}
        )
        
        st.plotly_chart(fig_industry, use_container_width=True)
    
    def _render_escalation_patterns(self):
        st.subheader("📊 Attack Escalation Patterns")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Pattern Analysis**")
            
            # Pattern type selection
            pattern_type = st.selectbox(
                "Escalation Pattern",
                ["Linear Escalation", "Exponential Growth", "Step Function", "Oscillating", "Multi-phase"]
            )
            
            # Time parameters
            analysis_window = st.slider(
                "Analysis Window (hours)",
                min_value=1,
                max_value=24,
                value=8
            )
            
            escalation_factor = st.slider(
                "Escalation Factor",
                min_value=1.1,
                max_value=5.0,
                value=2.0,
                step=0.1
            )
            
            if st.button("Analyze Escalation Pattern"):
                st.session_state['escalation_analysis'] = {
                    'pattern': pattern_type,
                    'window': analysis_window,
                    'factor': escalation_factor
                }
        
        with col2:
            if 'escalation_analysis' in st.session_state:
                self._show_escalation_analysis()
        
        # Pattern detection methods
        if 'escalation_analysis' in st.session_state:
            st.markdown("---")
            self._render_pattern_detection_methods()
    
    def _show_escalation_analysis(self):
        config = st.session_state['escalation_analysis']
        
        st.markdown("**Escalation Pattern Analysis**")
        
        # Generate escalation pattern
        time_points = np.linspace(0, config['window'], config['window'] * 12)
        pattern_data = self._generate_escalation_pattern(
            time_points, config['pattern'], config['factor']
        )
        
        # Create multi-metric visualization
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Attack Intensity Escalation',
                'Resource Consumption',
                'Detection Difficulty',
                'Mitigation Effectiveness'
            )
        )
        
        # Attack intensity
        fig.add_trace(
            go.Scatter(
                x=time_points,
                y=pattern_data['intensity'],
                mode='lines+markers',
                name='Intensity',
                line=dict(color='red', width=2)
            ),
            row=1, col=1
        )
        
        # Resource consumption
        fig.add_trace(
            go.Scatter(
                x=time_points,
                y=pattern_data['resources'],
                mode='lines',
                name='CPU/Memory',
                line=dict(color='orange'),
                fill='tonexty'
            ),
            row=1, col=2
        )
        
        # Detection difficulty
        fig.add_trace(
            go.Scatter(
                x=time_points,
                y=pattern_data['detection'],
                mode='lines',
                name='Detection Score',
                line=dict(color='blue')
            ),
            row=2, col=1
        )
        
        # Mitigation effectiveness
        fig.add_trace(
            go.Scatter(
                x=time_points,
                y=pattern_data['mitigation'],
                mode='lines',
                name='Mitigation %',
                line=dict(color='green')
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            height=600,
            title_text=f"{config['pattern']} Escalation Analysis",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Escalation metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            escalation_rate = (max(pattern_data['intensity']) - min(pattern_data['intensity'])) / config['window']
            st.metric("Escalation Rate", f"{escalation_rate:.2f}/hr")
        
        with col2:
            peak_resources = max(pattern_data['resources'])
            st.metric("Peak Resource Usage", f"{peak_resources:.1f}%")
        
        with col3:
            avg_detection = np.mean(pattern_data['detection'])
            st.metric("Avg Detection Score", f"{avg_detection:.1f}/10")
        
        with col4:
            final_mitigation = pattern_data['mitigation'][-1]
            st.metric("Final Mitigation", f"{final_mitigation:.1f}%")
    
    def _render_pattern_detection_methods(self):
        st.subheader("🔍 Pattern Detection Methods")
        
        config = st.session_state['escalation_analysis']
        
        detection_methods = {
            'Statistical Analysis': {
                'description': 'Detect anomalies using statistical techniques',
                'effectiveness': 75,
                'implementation': 'Moving averages, standard deviation analysis',
                'pros': ['Simple to implement', 'Low false positives'],
                'cons': ['May miss gradual escalations', 'Requires baseline data']
            },
            'Machine Learning': {
                'description': 'Use ML models to identify escalation patterns',
                'effectiveness': 85,
                'implementation': 'Neural networks, clustering algorithms',
                'pros': ['Adaptive learning', 'Complex pattern recognition'],
                'cons': ['Requires training data', 'Higher complexity']
            },
            'Threshold-based': {
                'description': 'Simple threshold monitoring with escalation detection',
                'effectiveness': 60,
                'implementation': 'Rate-of-change thresholds, multi-level alerts',
                'pros': ['Fast detection', 'Easy to understand'],
                'cons': ['High false positives', 'Static thresholds']
            },
            'Behavioral Analysis': {
                'description': 'Analyze traffic behavior patterns',
                'effectiveness': 80,
                'implementation': 'Flow analysis, protocol inspection',
                'pros': ['Context-aware', 'Low false positives'],
                'cons': ['Complex implementation', 'Resource intensive']
            }
        }
        
        # Method comparison
        col1, col2 = st.columns(2)
        
        with col1:
            # Effectiveness comparison
            methods = list(detection_methods.keys())
            effectiveness = [detection_methods[m]['effectiveness'] for m in methods]
            
            fig_effectiveness = px.bar(
                x=methods,
                y=effectiveness,
                title='Detection Method Effectiveness',
                labels={'y': 'Effectiveness %', 'x': 'Method'}
            )
            
            st.plotly_chart(fig_effectiveness, use_container_width=True)
        
        with col2:
            # Method details
            selected_method = st.selectbox("Select Method for Details", methods)
            
            if selected_method:
                method_data = detection_methods[selected_method]
                
                st.markdown(f"**{selected_method}**")
                st.write(method_data['description'])
                
                st.markdown("**Implementation**")
                st.write(method_data['implementation'])
                
                col2a, col2b = st.columns(2)
                
                with col2a:
                    st.markdown("**Pros**")
                    for pro in method_data['pros']:
                        st.write(f"• {pro}")
                
                with col2b:
                    st.markdown("**Cons**")
                    for con in method_data['cons']:
                        st.write(f"• {con}")
        
        # Detection timeline simulation
        st.markdown("**Detection Performance Simulation**")
        
        time_to_detect = {
            'Statistical Analysis': 15,  # minutes
            'Machine Learning': 8,
            'Threshold-based': 3,
            'Behavioral Analysis': 12
        }
        
        accuracy_rates = {
            'Statistical Analysis': 0.85,
            'Machine Learning': 0.92,
            'Threshold-based': 0.70,
            'Behavioral Analysis': 0.88
        }
        
        detection_df = pd.DataFrame({
            'Method': methods,
            'Time_to_Detect': [time_to_detect[m] for m in methods],
            'Accuracy': [accuracy_rates[m] for m in methods],
            'Effectiveness': effectiveness
        })
        
        fig_scatter = px.scatter(
            detection_df,
            x='Time_to_Detect',
            y='Accuracy',
            size='Effectiveness',
            color='Method',
            title='Detection Performance: Speed vs Accuracy',
            labels={'Time_to_Detect': 'Time to Detect (minutes)', 'Accuracy': 'Accuracy Rate'}
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    def _render_multi_attack_comparison(self):
        st.subheader("🔄 Multi-Attack Timeline Comparison")
        
        # Attack scenario setup
        st.markdown("**Compare Multiple Attack Scenarios**")
        
        num_attacks = st.slider("Number of attacks to compare", 2, 5, 3)
        
        scenarios = []
        cols = st.columns(num_attacks)
        
        for i in range(num_attacks):
            with cols[i]:
                st.markdown(f"**Attack {i+1}**")
                scenario = {
                    'name': st.text_input(f"Name", f"Attack {i+1}", key=f"name_{i}"),
                    'type': st.selectbox("Type", ["DDoS", "SYN Flood", "HTTP Flood"], key=f"type_{i}"),
                    'intensity': st.slider("Intensity", 1, 10, 5, key=f"intensity_{i}"),
                    'duration': st.slider("Duration (h)", 1, 24, 4, key=f"duration_{i}")
                }
                scenarios.append(scenario)
        
        if st.button("Compare Attack Timelines"):
            self._show_multi_attack_comparison(scenarios)
    
    def _show_multi_attack_comparison(self, scenarios):
        st.markdown("**Multi-Attack Timeline Comparison**")
        
        # Generate timeline data for each scenario
        max_duration = max(s['duration'] for s in scenarios)
        time_points = np.linspace(0, max_duration, max_duration * 12)
        
        fig = go.Figure()
        
        colors = ['red', 'blue', 'green', 'orange', 'purple']
        
        for i, scenario in enumerate(scenarios):
            # Generate intensity pattern for this scenario
            scenario_times = np.linspace(0, scenario['duration'], scenario['duration'] * 12)
            intensities = self._generate_intensity_pattern(
                scenario_times, 'Escalating', scenario['intensity']
            )
            
            # Pad with zeros for remaining time
            if len(scenario_times) < len(time_points):
                intensities.extend([0] * (len(time_points) - len(scenario_times)))
                scenario_times = time_points
            
            fig.add_trace(go.Scatter(
                x=scenario_times[:len(intensities)],
                y=intensities,
                mode='lines+markers',
                name=f"{scenario['name']} ({scenario['type']})",
                line=dict(color=colors[i % len(colors)], width=2)
            ))
        
        fig.update_layout(
            title='Multi-Attack Timeline Comparison',
            xaxis_title='Time (hours)',
            yaxis_title='Attack Intensity (1-10)',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Comparison metrics
        st.markdown("**Comparison Metrics**")
        
        comparison_data = []
        for scenario in scenarios:
            comparison_data.append({
                'Attack': scenario['name'],
                'Type': scenario['type'],
                'Peak Intensity': scenario['intensity'],
                'Duration': scenario['duration'],
                'Total Impact': scenario['intensity'] * scenario['duration'],
                'Avg Intensity': scenario['intensity'] * 0.7  # Approximate average
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True)
        
        # Impact comparison visualization
        col1, col2 = st.columns(2)
        
        with col1:
            fig_impact = px.bar(
                comparison_df,
                x='Attack',
                y='Total Impact',
                color='Type',
                title='Total Attack Impact Comparison'
            )
            st.plotly_chart(fig_impact, use_container_width=True)
        
        with col2:
            fig_duration = px.scatter(
                comparison_df,
                x='Duration',
                y='Peak Intensity',
                size='Total Impact',
                color='Type',
                hover_data=['Attack'],
                title='Duration vs Intensity'
            )
            st.plotly_chart(fig_duration, use_container_width=True)
    
    def _generate_intensity_pattern(self, time_points, pattern, start_intensity):
        """Generate attack intensity pattern over time"""
        if pattern == "Constant":
            return [start_intensity] * len(time_points)
        
        elif pattern == "Escalating":
            return [start_intensity + (t / max(time_points)) * (10 - start_intensity) for t in time_points]
        
        elif pattern == "Pulsing":
            return [start_intensity + 3 * np.sin(t * 2 * np.pi / 2) + np.random.normal(0, 0.5) for t in time_points]
        
        elif pattern == "Decreasing":
            return [start_intensity * np.exp(-t / max(time_points) * 2) for t in time_points]
        
        elif pattern == "Random":
            return [max(1, start_intensity + np.random.normal(0, 2)) for _ in time_points]
        
        else:
            return [start_intensity] * len(time_points)
    
    def _identify_attack_phases(self, config):
        """Identify attack phases based on configuration"""
        total_duration = config['duration']
        
        if config['pattern'] == "Escalating":
            phases = [
                {
                    'name': 'Initial Probe',
                    'duration': total_duration * 0.1,
                    'avg_intensity': config['start_intensity'] * 0.5,
                    'peak_intensity': config['start_intensity'],
                    'description': 'Reconnaissance and initial testing',
                    'activities': 'Port scanning, vulnerability assessment'
                },
                {
                    'name': 'Escalation',
                    'duration': total_duration * 0.4,
                    'avg_intensity': config['start_intensity'] * 1.5,
                    'peak_intensity': config['start_intensity'] * 2,
                    'description': 'Gradual intensity increase',
                    'activities': 'Resource mobilization, attack amplification'
                },
                {
                    'name': 'Peak Attack',
                    'duration': total_duration * 0.3,
                    'avg_intensity': 9,
                    'peak_intensity': 10,
                    'description': 'Maximum attack intensity',
                    'activities': 'Full resource deployment, maximum impact'
                },
                {
                    'name': 'Persistence',
                    'duration': total_duration * 0.2,
                    'avg_intensity': 6,
                    'peak_intensity': 8,
                    'description': 'Sustained attack with variations',
                    'activities': 'Evasion techniques, pattern changes'
                }
            ]
        else:
            # Generic phases
            phases = [
                {
                    'name': 'Launch',
                    'duration': total_duration * 0.2,
                    'avg_intensity': config['start_intensity'],
                    'peak_intensity': config['start_intensity'] * 1.2,
                    'description': 'Attack initiation',
                    'activities': 'Initial attack deployment'
                },
                {
                    'name': 'Execution',
                    'duration': total_duration * 0.6,
                    'avg_intensity': config['start_intensity'] * 1.2,
                    'peak_intensity': config['start_intensity'] * 1.5,
                    'description': 'Main attack phase',
                    'activities': 'Primary attack execution'
                },
                {
                    'name': 'Conclusion',
                    'duration': total_duration * 0.2,
                    'avg_intensity': config['start_intensity'] * 0.8,
                    'peak_intensity': config['start_intensity'],
                    'description': 'Attack wind-down',
                    'activities': 'Attack termination or mitigation'
                }
            ]
        
        return phases
    
    def _add_attack_phase_annotations(self, fig, timestamps, intensities, config):
        """Add phase annotations to timeline"""
        phases = self._identify_attack_phases(config)
        
        current_time = 0
        colors = ['rgba(255,0,0,0.1)', 'rgba(255,165,0,0.1)', 'rgba(0,255,0,0.1)', 'rgba(0,0,255,0.1)']
        
        for i, phase in enumerate(phases):
            end_time = current_time + phase['duration']
            
            # Find corresponding timestamps
            start_idx = int((current_time / config['duration']) * len(timestamps))
            end_idx = int((end_time / config['duration']) * len(timestamps))
            
            if start_idx < len(timestamps) and end_idx <= len(timestamps):
                fig.add_vrect(
                    x0=timestamps[start_idx],
                    x1=timestamps[min(end_idx, len(timestamps)-1)],
                    fillcolor=colors[i % len(colors)],
                    opacity=0.3,
                    annotation_text=phase['name'],
                    annotation_position="top left",
                    row=1, col=1
                )
            
            current_time = end_time
    
    def _calculate_phase_transitions(self, phases):
        """Calculate phase transition data"""
        transition_data = []
        
        current_time = 0
        for i, phase in enumerate(phases[:-1]):
            transition_time = current_time + phase['duration']
            next_phase = phases[i + 1]
            
            # Calculate transition intensity
            transition_rate = abs(next_phase['avg_intensity'] - phase['avg_intensity'])
            
            transition_data.append({
                'Time': transition_time,
                'Transition_Rate': transition_rate,
                'From_Phase': phase['name'],
                'To_Phase': next_phase['name']
            })
            
            current_time += phase['duration']
        
        return transition_data
    
    def _calculate_severity_score(self, case):
        """Calculate severity score for a case study"""
        score = 5  # Base score
        
        # Traffic-based scoring
        traffic = case.get('peak_traffic', '')
        if 'Tbps' in traffic:
            score += 3
        elif 'Gbps' in traffic:
            score += 2
        elif 'Mbps' in traffic:
            score += 1
        
        # Duration-based scoring
        duration = case.get('duration', '')
        if 'hours' in duration.lower():
            try:
                hours = int(''.join(filter(str.isdigit, duration.split('hours')[0])))
                score += min(hours / 4, 2)
            except:
                score += 1
        elif 'days' in duration.lower():
            score += 3
        
        return min(score, 10)
    
    def _categorize_target(self, target):
        """Categorize target by industry"""
        target_lower = target.lower()
        
        if any(word in target_lower for word in ['github', 'aws', 'cloudflare']):
            return 'Technology'
        elif any(word in target_lower for word in ['bank', 'financial', 'payment']):
            return 'Financial'
        elif any(word in target_lower for word in ['dns', 'infrastructure']):
            return 'Infrastructure'
        else:
            return 'Other'
    
    def _generate_escalation_pattern(self, time_points, pattern, factor):
        """Generate escalation pattern data"""
        if pattern == "Linear Escalation":
            intensity = [1 + (factor - 1) * (t / max(time_points)) for t in time_points]
        elif pattern == "Exponential Growth":
            intensity = [1 * (factor ** (t / max(time_points))) for t in time_points]
        elif pattern == "Step Function":
            intensity = []
            for t in time_points:
                if t < max(time_points) * 0.3:
                    intensity.append(1)
                elif t < max(time_points) * 0.7:
                    intensity.append(factor * 0.6)
                else:
                    intensity.append(factor)
        elif pattern == "Oscillating":
            intensity = [1 + (factor - 1) * (0.5 + 0.5 * np.sin(t * 2 * np.pi / 4)) for t in time_points]
        else:  # Multi-phase
            intensity = []
            for t in time_points:
                if t < max(time_points) * 0.2:
                    intensity.append(1)
                elif t < max(time_points) * 0.5:
                    intensity.append(factor * 0.4)
                elif t < max(time_points) * 0.8:
                    intensity.append(factor)
                else:
                    intensity.append(factor * 0.7)
        
        # Generate related metrics
        resources = [min(100, i * 10) for i in intensity]
        detection = [min(10, 2 + i * 0.8) for i in intensity]
        mitigation = [max(0, 100 - i * 15) for i in intensity]
        
        return {
            'intensity': intensity,
            'resources': resources,
            'detection': detection,
            'mitigation': mitigation
        }
