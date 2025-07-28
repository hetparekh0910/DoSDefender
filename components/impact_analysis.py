"""
Impact Analysis Component - System impact assessment for DoS attacks
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from data.dos_attacks_database import DoSAttackDatabase

class ImpactAnalysis:
    def __init__(self):
        self.db = DoSAttackDatabase()
        self.infrastructure_components = self._get_infrastructure_components()
        self.impact_categories = self._get_impact_categories()
    
    def render(self):
        st.header("💥 System Impact Analysis")
        st.markdown("""
        Comprehensive analysis of how DoS attacks affect different system components and business operations.
        This tool helps understand the cascading effects and prioritize protection strategies.
        """)
        
        # Analysis mode selection
        analysis_mode = st.selectbox(
            "Select Analysis Mode",
            ["Infrastructure Impact", "Business Impact", "Recovery Analysis", "Comparative Impact"]
        )
        
        if analysis_mode == "Infrastructure Impact":
            self._render_infrastructure_impact()
        elif analysis_mode == "Business Impact":
            self._render_business_impact()
        elif analysis_mode == "Recovery Analysis":
            self._render_recovery_analysis()
        elif analysis_mode == "Comparative Impact":
            self._render_comparative_impact()
    
    def _render_infrastructure_impact(self):
        st.subheader("🏗️ Infrastructure Impact Analysis")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Configuration**")
            
            # Infrastructure selection
            selected_components = st.multiselect(
                "Select Infrastructure Components",
                list(self.infrastructure_components.keys()),
                default=list(self.infrastructure_components.keys())[:4]
            )
            
            # Attack scenario
            attack_type = st.selectbox(
                "Attack Type",
                ["DDoS Flood", "SYN Flood", "HTTP Flood", "Amplification Attack", "Multi-vector Attack"]
            )
            
            attack_intensity = st.slider(
                "Attack Intensity",
                min_value=1,
                max_value=10,
                value=7,
                help="1 = Low intensity, 10 = Maximum intensity"
            )
            
            duration_hours = st.slider(
                "Attack Duration (hours)",
                min_value=1,
                max_value=24,
                value=4
            )
            
            if st.button("Analyze Infrastructure Impact"):
                st.session_state['infra_analysis'] = {
                    'components': selected_components,
                    'attack_type': attack_type,
                    'intensity': attack_intensity,
                    'duration': duration_hours
                }
        
        with col2:
            if 'infra_analysis' in st.session_state:
                self._show_infrastructure_impact_analysis()
        
        # Detailed component analysis
        if 'infra_analysis' in st.session_state:
            st.markdown("---")
            self._render_component_details()
    
    def _show_infrastructure_impact_analysis(self):
        config = st.session_state['infra_analysis']
        
        st.markdown("**Infrastructure Impact Assessment**")
        
        # Calculate impact scores for each component
        impact_data = []
        for component in config['components']:
            component_info = self.infrastructure_components[component]
            
            # Calculate impact based on attack type and component vulnerability
            base_impact = self._calculate_component_impact(component, config['attack_type'], config['intensity'])
            
            impact_data.append({
                'Component': component,
                'Impact Score': base_impact,
                'Availability': max(0, 100 - base_impact * 8),
                'Performance': max(10, 100 - base_impact * 10),
                'Recovery Time': base_impact * config['duration'] * 0.5
            })
        
        df = pd.DataFrame(impact_data)
        
        # Impact overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_impact = df['Impact Score'].mean()
            st.metric("Average Impact", f"{avg_impact:.1f}/10")
        
        with col2:
            min_availability = df['Availability'].min()
            st.metric("Minimum Availability", f"{min_availability:.1f}%")
        
        with col3:
            avg_performance = df['Performance'].mean()
            st.metric("Average Performance", f"{avg_performance:.1f}%")
        
        with col4:
            max_recovery = df['Recovery Time'].max()
            st.metric("Max Recovery Time", f"{max_recovery:.1f}h")
        
        # Component impact visualization
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Impact Scores', 'Availability Impact', 'Performance Degradation', 'Recovery Time'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        fig.add_trace(
            go.Bar(x=df['Component'], y=df['Impact Score'], name='Impact Score', marker_color='red'),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(x=df['Component'], y=df['Availability'], name='Availability %', marker_color='orange'),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Bar(x=df['Component'], y=df['Performance'], name='Performance %', marker_color='yellow'),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Bar(x=df['Component'], y=df['Recovery Time'], name='Recovery Hours', marker_color='purple'),
            row=2, col=2
        )
        
        fig.update_layout(height=600, showlegend=False, title_text="Infrastructure Impact Analysis")
        st.plotly_chart(fig, use_container_width=True)
        
        # Critical components identification
        st.markdown("**Critical Components Analysis**")
        critical_threshold = 7
        critical_components = df[df['Impact Score'] >= critical_threshold]
        
        if not critical_components.empty:
            st.error(f"⚠️ {len(critical_components)} critical components identified:")
            for _, comp in critical_components.iterrows():
                st.write(f"• **{comp['Component']}**: Impact {comp['Impact Score']:.1f}/10, "
                        f"Availability {comp['Availability']:.1f}%")
        else:
            st.success("✅ No critical impact levels detected")
    
    def _render_component_details(self):
        st.subheader("🔍 Component-Level Analysis")
        
        config = st.session_state['infra_analysis']
        
        # Component selection for detailed analysis
        selected_component = st.selectbox(
            "Select Component for Detailed Analysis",
            config['components']
        )
        
        if selected_component:
            component_info = self.infrastructure_components[selected_component]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**{selected_component} Details**")
                st.write(f"**Type**: {component_info['type']}")
                st.write(f"**Role**: {component_info['role']}")
                st.write(f"**Criticality**: {component_info['criticality']}")
                
                st.markdown("**Vulnerabilities**")
                for vuln in component_info['vulnerabilities']:
                    st.write(f"• {vuln}")
                
                st.markdown("**Failure Impact**")
                for impact in component_info['failure_impact']:
                    st.write(f"• {impact}")
            
            with col2:
                # Component-specific impact over time
                st.markdown("**Impact Timeline**")
                
                hours = list(range(0, config['duration'] + 1))
                impact_progression = self._calculate_impact_progression(
                    selected_component, config['attack_type'], config['intensity'], config['duration']
                )
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=hours,
                    y=impact_progression['availability'],
                    mode='lines+markers',
                    name='Availability %',
                    line=dict(color='green')
                ))
                
                fig.add_trace(go.Scatter(
                    x=hours,
                    y=impact_progression['performance'],
                    mode='lines+markers',
                    name='Performance %',
                    line=dict(color='blue')
                ))
                
                fig.add_trace(go.Scatter(
                    x=hours,
                    y=impact_progression['error_rate'],
                    mode='lines+markers',
                    name='Error Rate %',
                    line=dict(color='red')
                ))
                
                fig.update_layout(
                    title=f'{selected_component} Impact Over Time',
                    xaxis_title='Hours',
                    yaxis_title='Percentage',
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    def _render_business_impact(self):
        st.subheader("💼 Business Impact Analysis")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Business Parameters**")
            
            # Business context
            business_type = st.selectbox(
                "Business Type",
                ["E-commerce", "Financial Services", "SaaS Platform", "Media/Content", "Gaming", "Enterprise"]
            )
            
            # Revenue model
            revenue_model = st.selectbox(
                "Primary Revenue Model",
                ["Transaction-based", "Subscription", "Advertising", "Freemium", "Enterprise Licenses"]
            )
            
            # Peak hours
            is_peak_time = st.checkbox("Attack during peak hours", value=True)
            
            # Duration
            outage_duration = st.slider(
                "Service Disruption Duration (hours)",
                min_value=0.5,
                max_value=48.0,
                value=4.0,
                step=0.5
            )
            
            # Revenue data
            daily_revenue = st.number_input(
                "Daily Revenue ($)",
                min_value=1000,
                max_value=10000000,
                value=100000,
                step=10000,
                help="Educational simulation - enter realistic figures for your scenario"
            )
            
            if st.button("Calculate Business Impact"):
                st.session_state['business_impact'] = {
                    'business_type': business_type,
                    'revenue_model': revenue_model,
                    'peak_time': is_peak_time,
                    'duration': outage_duration,
                    'daily_revenue': daily_revenue
                }
        
        with col2:
            if 'business_impact' in st.session_state:
                self._show_business_impact_analysis()
        
        # Industry benchmarks
        if 'business_impact' in st.session_state:
            st.markdown("---")
            self._render_industry_benchmarks()
    
    def _show_business_impact_analysis(self):
        config = st.session_state['business_impact']
        
        st.markdown("**Business Impact Assessment**")
        
        # Calculate financial impact
        hourly_revenue = config['daily_revenue'] / 24
        
        # Peak time multiplier
        peak_multiplier = 2.5 if config['peak_time'] else 1.0
        
        # Revenue model multiplier
        model_multipliers = {
            'Transaction-based': 3.0,  # High immediate impact
            'Subscription': 1.2,       # Lower immediate impact
            'Advertising': 2.0,        # Medium impact
            'Freemium': 1.5,          # Medium-low impact
            'Enterprise Licenses': 1.8 # Medium-high impact
        }
        
        model_multiplier = model_multipliers.get(config['revenue_model'], 1.0)
        
        # Direct revenue loss
        direct_loss = hourly_revenue * config['duration'] * peak_multiplier * model_multiplier
        
        # Indirect costs
        reputation_damage = direct_loss * 0.3  # 30% of direct loss
        recovery_costs = direct_loss * 0.15    # 15% of direct loss
        opportunity_cost = direct_loss * 0.25  # 25% of direct loss
        
        total_impact = direct_loss + reputation_damage + recovery_costs + opportunity_cost
        
        # Display financial metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Direct Revenue Loss", f"${direct_loss:,.0f}")
        
        with col2:
            st.metric("Reputation Damage", f"${reputation_damage:,.0f}")
        
        with col3:
            st.metric("Recovery Costs", f"${recovery_costs:,.0f}")
        
        with col4:
            st.metric("Total Business Impact", f"${total_impact:,.0f}")
        
        # Impact breakdown visualization
        impact_categories = ['Direct Revenue Loss', 'Reputation Damage', 'Recovery Costs', 'Opportunity Cost']
        impact_values = [direct_loss, reputation_damage, recovery_costs, opportunity_cost]
        
        fig_pie = px.pie(
            values=impact_values,
            names=impact_categories,
            title="Business Impact Breakdown",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Impact severity assessment
        revenue_percentage = (total_impact / config['daily_revenue']) * 100
        
        st.markdown("**Impact Severity Assessment**")
        
        if revenue_percentage < 10:
            severity = "Low"
            color = "green"
        elif revenue_percentage < 25:
            severity = "Medium"
            color = "yellow"
        elif revenue_percentage < 50:
            severity = "High"
            color = "orange"
        else:
            severity = "Critical"
            color = "red"
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Impact as % of Daily Revenue", f"{revenue_percentage:.1f}%")
            st.markdown(f"**Severity Level**: :{color}[{severity}]")
        
        with col2:
            # Create severity gauge
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=min(revenue_percentage, 100),
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Business Impact Severity"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': color},
                    'steps': [
                        {'range': [0, 10], 'color': "lightgray"},
                        {'range': [10, 25], 'color': "yellow"},
                        {'range': [25, 50], 'color': "orange"},
                        {'range': [50, 100], 'color': "red"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 50
                    }
                }
            ))
            
            fig_gauge.update_layout(height=300)
            st.plotly_chart(fig_gauge, use_container_width=True)
    
    def _render_industry_benchmarks(self):
        st.subheader("📊 Industry Impact Benchmarks")
        
        config = st.session_state['business_impact']
        
        # Industry benchmark data (educational estimates)
        benchmark_data = {
            'E-commerce': {'avg_hourly_loss_pct': 4.2, 'recovery_time': 2.5, 'reputation_impact': 'High'},
            'Financial Services': {'avg_hourly_loss_pct': 8.1, 'recovery_time': 1.0, 'reputation_impact': 'Critical'},
            'SaaS Platform': {'avg_hourly_loss_pct': 2.8, 'recovery_time': 3.0, 'reputation_impact': 'Medium'},
            'Media/Content': {'avg_hourly_loss_pct': 3.5, 'recovery_time': 4.0, 'reputation_impact': 'Medium'},
            'Gaming': {'avg_hourly_loss_pct': 6.2, 'recovery_time': 2.0, 'reputation_impact': 'High'},
            'Enterprise': {'avg_hourly_loss_pct': 1.8, 'recovery_time': 6.0, 'reputation_impact': 'Low'}
        }
        
        # Create industry comparison
        industries = list(benchmark_data.keys())
        hourly_loss_pcts = [benchmark_data[ind]['avg_hourly_loss_pct'] for ind in industries]
        recovery_times = [benchmark_data[ind]['recovery_time'] for ind in industries]
        
        # Highlight current business type
        colors = ['red' if ind == config['business_type'] else 'lightblue' for ind in industries]
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_loss = px.bar(
                x=industries,
                y=hourly_loss_pcts,
                title="Average Hourly Loss % by Industry",
                color=colors,
                color_discrete_map={'red': 'red', 'lightblue': 'lightblue'}
            )
            fig_loss.update_layout(showlegend=False)
            st.plotly_chart(fig_loss, use_container_width=True)
        
        with col2:
            fig_recovery = px.bar(
                x=industries,
                y=recovery_times,
                title="Average Recovery Time (hours) by Industry",
                color=colors,
                color_discrete_map={'red': 'red', 'lightblue': 'lightblue'}
            )
            fig_recovery.update_layout(showlegend=False)
            st.plotly_chart(fig_recovery, use_container_width=True)
        
        # Benchmark comparison
        current_benchmark = benchmark_data.get(config['business_type'], {})
        user_hourly_loss_pct = (config['daily_revenue'] / 24) / config['daily_revenue'] * 100
        
        st.markdown("**Your Business vs Industry Benchmark**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            industry_avg = current_benchmark.get('avg_hourly_loss_pct', 0)
            st.metric(
                "Industry Avg Hourly Loss",
                f"{industry_avg}%",
                delta=f"{user_hourly_loss_pct - industry_avg:.1f}%"
            )
        
        with col2:
            recovery_benchmark = current_benchmark.get('recovery_time', 0)
            st.metric(
                "Industry Avg Recovery Time",
                f"{recovery_benchmark}h",
                delta=f"{config['duration'] - recovery_benchmark:.1f}h"
            )
        
        with col3:
            reputation_impact = current_benchmark.get('reputation_impact', 'Medium')
            st.metric("Reputation Impact Level", reputation_impact)
    
    def _render_recovery_analysis(self):
        st.subheader("🔄 Recovery Analysis")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Recovery Scenario**")
            
            # Recovery parameters
            recovery_strategy = st.selectbox(
                "Recovery Strategy",
                ["Automated Response", "Manual Intervention", "Hybrid Approach", "Emergency Protocol"]
            )
            
            team_readiness = st.selectbox(
                "Team Readiness Level",
                ["24/7 On-call", "Business Hours", "Best Effort", "Limited Resources"]
            )
            
            backup_systems = st.checkbox("Backup systems available", value=True)
            
            dr_plan = st.checkbox("Disaster recovery plan in place", value=True)
            
            cloud_resources = st.checkbox("Cloud auto-scaling available", value=False)
            
            if st.button("Analyze Recovery Timeline"):
                st.session_state['recovery_analysis'] = {
                    'strategy': recovery_strategy,
                    'team_readiness': team_readiness,
                    'backup_systems': backup_systems,
                    'dr_plan': dr_plan,
                    'cloud_resources': cloud_resources
                }
        
        with col2:
            if 'recovery_analysis' in st.session_state:
                self._show_recovery_timeline()
        
        if 'recovery_analysis' in st.session_state:
            st.markdown("---")
            self._render_recovery_recommendations()
    
    def _show_recovery_timeline(self):
        config = st.session_state['recovery_analysis']
        
        st.markdown("**Recovery Timeline Analysis**")
        
        # Calculate recovery phases and durations
        phases = self._calculate_recovery_phases(config)
        
        # Create timeline visualization
        phase_names = [phase['name'] for phase in phases]
        durations = [phase['duration'] for phase in phases]
        cumulative_time = np.cumsum([0] + durations[:-1])
        
        # Recovery progress over time
        total_duration = sum(durations)
        time_points = list(range(0, int(total_duration) + 1, max(1, int(total_duration // 20))))
        
        recovery_progress = []
        for t in time_points:
            progress = 0
            current_time = 0
            for phase in phases:
                if t >= current_time and t < current_time + phase['duration']:
                    phase_progress = (t - current_time) / phase['duration']
                    progress = phase['progress_start'] + phase_progress * (phase['progress_end'] - phase['progress_start'])
                    break
                elif t >= current_time + phase['duration']:
                    progress = phase['progress_end']
                current_time += phase['duration']
            recovery_progress.append(progress)
        
        # Create recovery timeline chart
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Recovery Phases Duration', 'Recovery Progress Over Time'),
            row_heights=[0.4, 0.6]
        )
        
        # Phase duration chart
        fig.add_trace(
            go.Bar(x=phase_names, y=durations, name='Duration (minutes)', marker_color='skyblue'),
            row=1, col=1
        )
        
        # Recovery progress chart
        fig.add_trace(
            go.Scatter(x=time_points, y=recovery_progress, mode='lines+markers', 
                      name='Recovery Progress %', line=dict(color='green', width=3)),
            row=2, col=1
        )
        
        fig.update_layout(height=600, title_text="Recovery Timeline Analysis")
        fig.update_xaxes(title_text="Recovery Phase", row=1, col=1)
        fig.update_yaxes(title_text="Duration (minutes)", row=1, col=1)
        fig.update_xaxes(title_text="Time (minutes)", row=2, col=1)
        fig.update_yaxes(title_text="Recovery Progress (%)", row=2, col=1)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recovery summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Recovery Time", f"{total_duration:.0f} minutes")
        
        with col2:
            mttr = self._calculate_mttr(config)
            st.metric("MTTR Estimate", f"{mttr:.0f} minutes")
        
        with col3:
            confidence = self._calculate_recovery_confidence(config)
            st.metric("Recovery Confidence", f"{confidence:.0f}%")
    
    def _render_recovery_recommendations(self):
        st.subheader("🎯 Recovery Recommendations")
        
        config = st.session_state['recovery_analysis']
        
        # Generate recommendations based on configuration
        recommendations = self._generate_recovery_recommendations(config)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Immediate Improvements**")
            for rec in recommendations['immediate']:
                st.write(f"• {rec}")
        
        with col2:
            st.markdown("**Long-term Enhancements**")
            for rec in recommendations['long_term']:
                st.write(f"• {rec}")
        
        # Recovery maturity assessment
        st.markdown("**Recovery Maturity Assessment**")
        
        maturity_score = self._calculate_recovery_maturity(config)
        
        maturity_levels = ['Basic', 'Developing', 'Defined', 'Managed', 'Optimized']
        current_level = maturity_levels[min(maturity_score - 1, 4)]
        
        fig_maturity = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=maturity_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"Recovery Maturity: {current_level}"},
            delta={'reference': 3},
            gauge={
                'axis': {'range': [None, 5]},
                'bar': {'color': "darkgreen"},
                'steps': [
                    {'range': [0, 1], 'color': "lightgray"},
                    {'range': [1, 2], 'color': "yellow"},
                    {'range': [2, 3], 'color': "orange"},
                    {'range': [3, 4], 'color': "lightgreen"},
                    {'range': [4, 5], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 4
                }
            }
        ))
        
        fig_maturity.update_layout(height=400)
        st.plotly_chart(fig_maturity, use_container_width=True)
    
    def _render_comparative_impact(self):
        st.subheader("⚖️ Comparative Impact Analysis")
        
        st.markdown("Compare impact across different attack scenarios and business contexts.")
        
        # Scenario comparison setup
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Scenario A**")
            scenario_a = {
                'attack_type': st.selectbox("Attack Type A", ["DDoS Flood", "SYN Flood", "HTTP Flood"], key="a_attack"),
                'intensity': st.slider("Intensity A", 1, 10, 5, key="a_intensity"),
                'duration': st.slider("Duration A (hours)", 1, 24, 4, key="a_duration"),
                'business_type': st.selectbox("Business Type A", ["E-commerce", "Financial Services", "SaaS Platform"], key="a_business")
            }
        
        with col2:
            st.markdown("**Scenario B**")
            scenario_b = {
                'attack_type': st.selectbox("Attack Type B", ["DDoS Flood", "SYN Flood", "HTTP Flood"], key="b_attack"),
                'intensity': st.slider("Intensity B", 1, 10, 7, key="b_intensity"),
                'duration': st.slider("Duration B (hours)", 1, 24, 2, key="b_duration"),
                'business_type': st.selectbox("Business Type B", ["E-commerce", "Financial Services", "SaaS Platform"], key="b_business")
            }
        
        if st.button("Compare Scenarios"):
            self._show_scenario_comparison(scenario_a, scenario_b)
    
    def _show_scenario_comparison(self, scenario_a, scenario_b):
        st.markdown("**Scenario Comparison Results**")
        
        # Calculate impacts for both scenarios
        impact_a = self._calculate_scenario_impact(scenario_a)
        impact_b = self._calculate_scenario_impact(scenario_b)
        
        # Comparison metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Infrastructure Impact",
                f"A: {impact_a['infrastructure']:.1f}",
                delta=f"{impact_a['infrastructure'] - impact_b['infrastructure']:.1f}",
                help="Scenario A vs B"
            )
        
        with col2:
            st.metric(
                "Business Impact ($)",
                f"A: ${impact_a['business']:,.0f}",
                delta=f"{impact_a['business'] - impact_b['business']:,.0f}"
            )
        
        with col3:
            st.metric(
                "Recovery Time (hrs)",
                f"A: {impact_a['recovery']:.1f}",
                delta=f"{impact_a['recovery'] - impact_b['recovery']:.1f}"
            )
        
        # Detailed comparison visualization
        categories = ['Infrastructure Impact', 'Business Impact', 'Recovery Time', 'Overall Severity']
        
        # Normalize values for comparison
        values_a = [
            impact_a['infrastructure'],
            impact_a['business'] / 10000,  # Scale down for visualization
            impact_a['recovery'],
            (impact_a['infrastructure'] + impact_a['business']/10000 + impact_a['recovery']) / 3
        ]
        
        values_b = [
            impact_b['infrastructure'],
            impact_b['business'] / 10000,
            impact_b['recovery'],
            (impact_b['infrastructure'] + impact_b['business']/10000 + impact_b['recovery']) / 3
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values_a,
            theta=categories,
            fill='toself',
            name='Scenario A',
            line_color='red'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=values_b,
            theta=categories,
            fill='toself',
            name='Scenario B',
            line_color='blue'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            showlegend=True,
            title="Scenario Impact Comparison"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        st.markdown("**Comparison Insights**")
        
        if impact_a['infrastructure'] > impact_b['infrastructure']:
            st.write("• Scenario A has higher infrastructure impact")
        else:
            st.write("• Scenario B has higher infrastructure impact")
        
        if impact_a['business'] > impact_b['business']:
            st.write("• Scenario A has higher business impact")
        else:
            st.write("• Scenario B has higher business impact")
        
        if impact_a['recovery'] > impact_b['recovery']:
            st.write("• Scenario A requires longer recovery time")
        else:
            st.write("• Scenario B requires longer recovery time")
    
    def _get_infrastructure_components(self):
        """Get infrastructure components and their properties"""
        return {
            'Load Balancer': {
                'type': 'Network Infrastructure',
                'role': 'Traffic distribution and routing',
                'criticality': 'High',
                'vulnerabilities': ['Connection exhaustion', 'Bandwidth saturation', 'CPU overload'],
                'failure_impact': ['Service unavailability', 'Traffic bottleneck', 'Cascading failures']
            },
            'Web Server': {
                'type': 'Application Infrastructure',
                'role': 'HTTP request processing',
                'criticality': 'High',
                'vulnerabilities': ['Connection limits', 'Memory exhaustion', 'CPU overload'],
                'failure_impact': ['Request timeouts', 'Service degradation', 'User experience issues']
            },
            'Database': {
                'type': 'Data Infrastructure',
                'role': 'Data storage and retrieval',
                'criticality': 'Critical',
                'vulnerabilities': ['Connection pool exhaustion', 'Query performance', 'Lock contention'],
                'failure_impact': ['Data unavailability', 'Transaction failures', 'Application errors']
            },
            'CDN': {
                'type': 'Content Delivery',
                'role': 'Content caching and distribution',
                'criticality': 'Medium',
                'vulnerabilities': ['Cache flooding', 'Origin overload', 'Edge saturation'],
                'failure_impact': ['Slow content delivery', 'Origin exposure', 'Regional outages']
            },
            'DNS Server': {
                'type': 'Name Resolution',
                'role': 'Domain name resolution',
                'criticality': 'Critical',
                'vulnerabilities': ['Query flooding', 'Amplification attacks', 'Cache poisoning'],
                'failure_impact': ['Service unreachability', 'Resolution delays', 'Complete outage']
            },
            'Firewall': {
                'type': 'Security Infrastructure',
                'role': 'Traffic filtering and protection',
                'criticality': 'High',
                'vulnerabilities': ['Rule processing limits', 'State table overflow', 'Bandwidth limits'],
                'failure_impact': ['Security bypass', 'Traffic blocking', 'Performance degradation']
            },
            'API Gateway': {
                'type': 'Application Infrastructure',
                'role': 'API request management',
                'criticality': 'High',
                'vulnerabilities': ['Rate limit bypass', 'Authentication overload', 'Request flooding'],
                'failure_impact': ['API unavailability', 'Service integration failures', 'Data access issues']
            }
        }
    
    def _get_impact_categories(self):
        """Get impact categories for analysis"""
        return {
            'availability': 'Service availability and uptime',
            'performance': 'Response time and throughput',
            'functionality': 'Feature availability and correctness',
            'security': 'Data protection and access control',
            'compliance': 'Regulatory and policy adherence',
            'reputation': 'Brand and customer trust',
            'financial': 'Revenue and cost impact'
        }
    
    def _calculate_component_impact(self, component, attack_type, intensity):
        """Calculate impact score for a component"""
        base_scores = {
            'Load Balancer': 7,
            'Web Server': 8,
            'Database': 9,
            'CDN': 5,
            'DNS Server': 10,
            'Firewall': 6,
            'API Gateway': 7
        }
        
        attack_multipliers = {
            'DDoS Flood': 1.2,
            'SYN Flood': 1.0,
            'HTTP Flood': 1.1,
            'Amplification Attack': 1.3,
            'Multi-vector Attack': 1.4
        }
        
        base_score = base_scores.get(component, 5)
        attack_multiplier = attack_multipliers.get(attack_type, 1.0)
        intensity_factor = intensity / 10.0
        
        return min(base_score * attack_multiplier * intensity_factor, 10)
    
    def _calculate_impact_progression(self, component, attack_type, intensity, duration):
        """Calculate how impact progresses over time"""
        hours = list(range(duration + 1))
        
        # Base degradation patterns
        availability = []
        performance = []
        error_rate = []
        
        for hour in hours:
            # Availability degrades more slowly
            avail = 100 - (intensity * 8 * (1 - np.exp(-hour / 2)))
            availability.append(max(0, avail))
            
            # Performance degrades quickly initially
            perf = 100 - (intensity * 10 * (1 - np.exp(-hour / 1.5)))
            performance.append(max(10, perf))
            
            # Error rate increases
            error = intensity * 3 * (1 - np.exp(-hour / 1))
            error_rate.append(min(50, error))
        
        return {
            'availability': availability,
            'performance': performance,
            'error_rate': error_rate
        }
    
    def _calculate_recovery_phases(self, config):
        """Calculate recovery phases and their durations"""
        base_phases = [
            {'name': 'Detection', 'progress_start': 0, 'progress_end': 10},
            {'name': 'Assessment', 'progress_start': 10, 'progress_end': 25},
            {'name': 'Response', 'progress_start': 25, 'progress_end': 60},
            {'name': 'Mitigation', 'progress_start': 60, 'progress_end': 85},
            {'name': 'Recovery', 'progress_start': 85, 'progress_end': 100}
        ]
        
        # Adjust durations based on configuration
        strategy_multipliers = {
            'Automated Response': 0.5,
            'Manual Intervention': 1.5,
            'Hybrid Approach': 0.8,
            'Emergency Protocol': 0.3
        }
        
        team_multipliers = {
            '24/7 On-call': 0.6,
            'Business Hours': 1.2,
            'Best Effort': 1.8,
            'Limited Resources': 2.5
        }
        
        base_durations = [5, 10, 20, 15, 30]  # minutes
        
        strategy_mult = strategy_multipliers.get(config['strategy'], 1.0)
        team_mult = team_multipliers.get(config['team_readiness'], 1.0)
        
        # Additional factors
        backup_mult = 0.7 if config['backup_systems'] else 1.0
        dr_mult = 0.6 if config['dr_plan'] else 1.0
        cloud_mult = 0.5 if config['cloud_resources'] else 1.0
        
        total_mult = strategy_mult * team_mult * backup_mult * dr_mult * cloud_mult
        
        for i, phase in enumerate(base_phases):
            phase['duration'] = base_durations[i] * total_mult
        
        return base_phases
    
    def _calculate_mttr(self, config):
        """Calculate Mean Time To Recovery"""
        phases = self._calculate_recovery_phases(config)
        return sum(phase['duration'] for phase in phases)
    
    def _calculate_recovery_confidence(self, config):
        """Calculate recovery confidence percentage"""
        confidence = 50  # Base confidence
        
        if config['backup_systems']:
            confidence += 15
        if config['dr_plan']:
            confidence += 20
        if config['cloud_resources']:
            confidence += 10
        
        strategy_bonus = {
            'Automated Response': 15,
            'Manual Intervention': 5,
            'Hybrid Approach': 10,
            'Emergency Protocol': 20
        }
        
        team_bonus = {
            '24/7 On-call': 15,
            'Business Hours': 10,
            'Best Effort': 5,
            'Limited Resources': 0
        }
        
        confidence += strategy_bonus.get(config['strategy'], 0)
        confidence += team_bonus.get(config['team_readiness'], 0)
        
        return min(confidence, 95)  # Cap at 95%
    
    def _generate_recovery_recommendations(self, config):
        """Generate recovery recommendations"""
        immediate = []
        long_term = []
        
        if not config['backup_systems']:
            immediate.append("Implement backup systems and failover mechanisms")
        
        if not config['dr_plan']:
            immediate.append("Develop and test disaster recovery procedures")
        
        if config['team_readiness'] in ['Best Effort', 'Limited Resources']:
            immediate.append("Establish 24/7 incident response capability")
        
        if config['strategy'] == 'Manual Intervention':
            immediate.append("Implement automated response systems")
        
        if not config['cloud_resources']:
            long_term.append("Deploy auto-scaling cloud infrastructure")
        
        long_term.append("Conduct regular disaster recovery drills")
        long_term.append("Implement comprehensive monitoring and alerting")
        long_term.append("Develop incident response playbooks")
        
        return {'immediate': immediate, 'long_term': long_term}
    
    def _calculate_recovery_maturity(self, config):
        """Calculate recovery maturity level (1-5)"""
        score = 1
        
        if config['dr_plan']:
            score += 1
        
        if config['backup_systems']:
            score += 1
        
        if config['strategy'] in ['Automated Response', 'Hybrid Approach']:
            score += 1
        
        if config['team_readiness'] == '24/7 On-call':
            score += 1
        
        return score
    
    def _calculate_scenario_impact(self, scenario):
        """Calculate overall impact for a scenario"""
        # Infrastructure impact
        intensity_factor = scenario['intensity'] / 10.0
        duration_factor = min(scenario['duration'] / 24.0, 1.0)
        
        attack_severity = {
            'DDoS Flood': 8,
            'SYN Flood': 7,
            'HTTP Flood': 6
        }
        
        infrastructure = attack_severity.get(scenario['attack_type'], 7) * intensity_factor
        
        # Business impact
        business_multipliers = {
            'E-commerce': 50000,
            'Financial Services': 100000,
            'SaaS Platform': 30000
        }
        
        business = business_multipliers.get(scenario['business_type'], 40000) * duration_factor
        
        # Recovery time
        recovery = scenario['duration'] * 0.5 + scenario['intensity'] * 0.3
        
        return {
            'infrastructure': infrastructure,
            'business': business,
            'recovery': recovery
        }
