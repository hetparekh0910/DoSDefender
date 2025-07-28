"""
Attack Analyzer Component - Interactive DoS attack analysis tools
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
from plotly.subplots import make_subplots
import numpy as np

class AttackAnalyzer:
    def __init__(self):
        self.attack_patterns = self._get_attack_patterns()
    
    def render(self):
        st.header("🔍 DoS Attack Analyzer")
        st.markdown("""
        Analyze DoS attack patterns, methodologies, and system impacts.
        This tool helps understand how different attack vectors work and their potential impact.
        """)
        
        # Analysis type selection
        analysis_type = st.selectbox(
            "Select Analysis Type",
            ["Attack Flow Analysis", "Traffic Pattern Analysis", "System Impact Modeling", "Attack Vector Comparison"]
        )
        
        if analysis_type == "Attack Flow Analysis":
            self._render_attack_flow_analysis()
        elif analysis_type == "Traffic Pattern Analysis":
            self._render_traffic_pattern_analysis()
        elif analysis_type == "System Impact Modeling":
            self._render_system_impact_modeling()
        elif analysis_type == "Attack Vector Comparison":
            self._render_attack_vector_comparison()
    
    def _render_attack_flow_analysis(self):
        st.subheader("🌐 Attack Flow Analysis")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Configure Attack Scenario**")
            
            attack_type = st.selectbox(
                "Attack Type",
                ["DDoS Flood", "SYN Flood", "HTTP Flood", "Amplification Attack", "Slowloris"]
            )
            
            target_type = st.selectbox(
                "Target Infrastructure",
                ["Web Server", "API Gateway", "Database", "CDN", "Load Balancer"]
            )
            
            attack_intensity = st.slider(
                "Attack Intensity",
                min_value=1,
                max_value=10,
                value=5,
                help="1 = Low intensity, 10 = Maximum intensity"
            )
            
            if st.button("Generate Attack Flow"):
                st.session_state['attack_flow_generated'] = True
                st.session_state['attack_config'] = {
                    'type': attack_type,
                    'target': target_type,
                    'intensity': attack_intensity
                }
        
        with col2:
            if st.session_state.get('attack_flow_generated', False):
                self._generate_attack_flow_diagram()
    
    def _generate_attack_flow_diagram(self):
        st.markdown("**Attack Flow Diagram**")
        
        config = st.session_state.get('attack_config', {})
        
        # Create network graph
        G = nx.DiGraph()
        
        # Add nodes based on attack type
        if config['type'] == 'DDoS Flood':
            nodes = [
                ('Botnet', {'type': 'attacker', 'pos': (0, 0)}),
                ('Internet', {'type': 'network', 'pos': (1, 0)}),
                ('Firewall', {'type': 'defense', 'pos': (2, 0)}),
                ('Load Balancer', {'type': 'infrastructure', 'pos': (3, 0)}),
                ('Target Server', {'type': 'target', 'pos': (4, 0)})
            ]
            
            edges = [
                ('Botnet', 'Internet', {'weight': config['intensity'] * 10}),
                ('Internet', 'Firewall', {'weight': config['intensity'] * 8}),
                ('Firewall', 'Load Balancer', {'weight': config['intensity'] * 6}),
                ('Load Balancer', 'Target Server', {'weight': config['intensity'] * 4})
            ]
        
        elif config['type'] == 'SYN Flood':
            nodes = [
                ('Attacker', {'type': 'attacker', 'pos': (0, 0)}),
                ('Internet', {'type': 'network', 'pos': (1, 0)}),
                ('Target Server', {'type': 'target', 'pos': (2, 0)}),
                ('Connection Table', {'type': 'resource', 'pos': (2, -1)})
            ]
            
            edges = [
                ('Attacker', 'Internet', {'weight': config['intensity'] * 5}),
                ('Internet', 'Target Server', {'weight': config['intensity'] * 5}),
                ('Target Server', 'Connection Table', {'weight': config['intensity'] * 8})
            ]
        
        else:  # Default flow
            nodes = [
                ('Attacker', {'type': 'attacker', 'pos': (0, 0)}),
                ('Network', {'type': 'network', 'pos': (1, 0)}),
                ('Target', {'type': 'target', 'pos': (2, 0)})
            ]
            
            edges = [
                ('Attacker', 'Network', {'weight': config['intensity'] * 5}),
                ('Network', 'Target', {'weight': config['intensity'] * 5})
            ]
        
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        
        # Create plotly figure
        pos = nx.get_node_attributes(G, 'pos')
        
        # Extract node positions
        node_x = [pos[node][0] for node in G.nodes()]
        node_y = [pos[node][1] for node in G.nodes()]
        
        # Extract edge positions
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        # Create edge trace
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        
        # Create node trace
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=list(G.nodes()),
            textposition="middle center",
            marker=dict(
                size=50,
                color=['red' if G.nodes[node].get('type') == 'attacker' 
                      else 'orange' if G.nodes[node].get('type') == 'target'
                      else 'blue' if G.nodes[node].get('type') == 'defense'
                      else 'green' for node in G.nodes()],
                line=dict(width=2, color='black')
            )
        )
        
        # Create figure
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           title=f'{config["type"]} Attack Flow on {config["target"]}',
                           titlefont_size=16,
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20,l=5,r=5,t=40),
                           annotations=[ dict(
                               text="Attack Flow Analysis - Educational Purpose",
                               showarrow=False,
                               xref="paper", yref="paper",
                               x=0.005, y=-0.002,
                               xanchor='left', yanchor='bottom',
                               font=dict(color="gray", size=12)
                           )],
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                       ))
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Attack details
        st.markdown("**Attack Analysis**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Attack Intensity", f"{config['intensity']}/10")
        
        with col2:
            estimated_rps = config['intensity'] * 1000
            st.metric("Estimated RPS", f"{estimated_rps:,}")
        
        with col3:
            risk_level = "High" if config['intensity'] > 7 else "Medium" if config['intensity'] > 4 else "Low"
            st.metric("Risk Level", risk_level)
    
    def _render_traffic_pattern_analysis(self):
        st.subheader("📊 Traffic Pattern Analysis")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Analysis Parameters**")
            
            time_window = st.selectbox(
                "Time Window",
                ["1 Hour", "6 Hours", "24 Hours", "1 Week"]
            )
            
            pattern_type = st.selectbox(
                "Pattern Type",
                ["Normal vs Attack", "Attack Escalation", "Multi-vector Attack"]
            )
            
            data_granularity = st.selectbox(
                "Data Granularity",
                ["1 minute", "5 minutes", "15 minutes", "1 hour"]
            )
        
        with col2:
            # Generate synthetic traffic data for educational purposes
            if pattern_type == "Normal vs Attack":
                self._show_normal_vs_attack_pattern(time_window, data_granularity)
            elif pattern_type == "Attack Escalation":
                self._show_attack_escalation_pattern(time_window, data_granularity)
            elif pattern_type == "Multi-vector Attack":
                self._show_multivector_attack_pattern(time_window, data_granularity)
        
        # Pattern insights
        st.markdown("---")
        st.subheader("🔍 Pattern Insights")
        
        insights_col1, insights_col2 = st.columns(2)
        
        with insights_col1:
            st.markdown("**Key Indicators**")
            st.markdown("""
            - Sudden traffic spikes (>300% baseline)
            - Unusual protocol distributions
            - Geographic traffic anomalies
            - Request pattern irregularities
            - Connection behavior changes
            """)
        
        with insights_col2:
            st.markdown("**Detection Techniques**")
            st.markdown("""
            - Statistical anomaly detection
            - Machine learning pattern recognition
            - Threshold-based alerting
            - Behavioral analysis
            - Rate-based detection
            """)
    
    def _show_normal_vs_attack_pattern(self, time_window, granularity):
        st.markdown("**Normal vs Attack Traffic Pattern**")
        
        # Generate time series data
        hours = 24 if "24" in time_window else 6 if "6" in time_window else 1
        intervals = hours * (60 if "1 minute" in granularity else 
                           12 if "5 minutes" in granularity else 
                           4 if "15 minutes" in granularity else 1)
        
        time_points = pd.date_range(start='2024-01-01', periods=intervals, freq='1H' if "1 hour" in granularity else '5T')
        
        # Normal traffic (baseline with some variation)
        normal_traffic = np.random.normal(100, 20, intervals)
        normal_traffic = np.maximum(normal_traffic, 0)  # Ensure non-negative
        
        # Attack traffic (sudden spike)
        attack_start = intervals // 3
        attack_duration = intervals // 4
        attack_traffic = normal_traffic.copy()
        
        for i in range(attack_start, min(attack_start + attack_duration, intervals)):
            multiplier = 5 + np.random.normal(2, 1)  # 5-8x normal traffic
            attack_traffic[i] = normal_traffic[i] * multiplier
        
        # Create comparison chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=time_points,
            y=normal_traffic,
            mode='lines',
            name='Normal Traffic',
            line=dict(color='green', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=time_points,
            y=attack_traffic,
            mode='lines',
            name='Attack Traffic',
            line=dict(color='red', width=2)
        ))
        
        fig.update_layout(
            title='Traffic Pattern Comparison',
            xaxis_title='Time',
            yaxis_title='Requests per Second',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _show_attack_escalation_pattern(self, time_window, granularity):
        st.markdown("**Attack Escalation Pattern**")
        
        hours = 24 if "24" in time_window else 6 if "6" in time_window else 1
        intervals = hours * 12  # 5-minute intervals
        
        time_points = pd.date_range(start='2024-01-01', periods=intervals, freq='5T')
        
        # Escalating attack pattern
        baseline = 100
        traffic = []
        
        for i in range(intervals):
            if i < intervals * 0.2:  # Normal phase (20%)
                traffic.append(baseline + np.random.normal(0, 10))
            elif i < intervals * 0.3:  # Initial probe (10%)
                traffic.append(baseline * (1.5 + np.random.normal(0, 0.2)))
            elif i < intervals * 0.5:  # Escalation phase (20%)
                escalation_factor = 1.5 + (i - intervals * 0.3) / (intervals * 0.2) * 3
                traffic.append(baseline * (escalation_factor + np.random.normal(0, 0.3)))
            elif i < intervals * 0.8:  # Peak attack (30%)
                traffic.append(baseline * (5 + np.random.normal(0, 1)))
            else:  # Mitigation/decline (20%)
                decline_factor = 5 - (i - intervals * 0.8) / (intervals * 0.2) * 4
                traffic.append(baseline * max(1, decline_factor + np.random.normal(0, 0.5)))
        
        # Create escalation chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=time_points,
            y=traffic,
            mode='lines',
            name='Attack Traffic',
            line=dict(color='red', width=2),
            fill='tonexty'
        ))
        
        # Add phase annotations
        fig.add_vrect(
            x0=time_points[0], x1=time_points[int(intervals * 0.2)],
            fillcolor="green", opacity=0.1,
            annotation_text="Normal", annotation_position="top left"
        )
        
        fig.add_vrect(
            x0=time_points[int(intervals * 0.2)], x1=time_points[int(intervals * 0.3)],
            fillcolor="yellow", opacity=0.1,
            annotation_text="Probe", annotation_position="top left"
        )
        
        fig.add_vrect(
            x0=time_points[int(intervals * 0.3)], x1=time_points[int(intervals * 0.5)],
            fillcolor="orange", opacity=0.1,
            annotation_text="Escalation", annotation_position="top left"
        )
        
        fig.add_vrect(
            x0=time_points[int(intervals * 0.5)], x1=time_points[int(intervals * 0.8)],
            fillcolor="red", opacity=0.1,
            annotation_text="Peak Attack", annotation_position="top left"
        )
        
        fig.add_vrect(
            x0=time_points[int(intervals * 0.8)], x1=time_points[-1],
            fillcolor="blue", opacity=0.1,
            annotation_text="Mitigation", annotation_position="top left"
        )
        
        fig.update_layout(
            title='Attack Escalation Timeline',
            xaxis_title='Time',
            yaxis_title='Requests per Second',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _show_multivector_attack_pattern(self, time_window, granularity):
        st.markdown("**Multi-vector Attack Pattern**")
        
        hours = 6
        intervals = hours * 12  # 5-minute intervals
        
        time_points = pd.date_range(start='2024-01-01', periods=intervals, freq='5T')
        
        # Different attack vectors
        baseline = 50
        
        # HTTP Flood
        http_flood = [baseline + np.random.normal(0, 5) for _ in range(intervals)]
        for i in range(intervals // 4, intervals // 2):
            http_flood[i] *= (3 + np.random.normal(0, 0.5))
        
        # SYN Flood
        syn_flood = [baseline * 0.3 + np.random.normal(0, 3) for _ in range(intervals)]
        for i in range(intervals // 3, intervals * 2 // 3):
            syn_flood[i] *= (4 + np.random.normal(0, 0.7))
        
        # UDP Flood
        udp_flood = [baseline * 0.5 + np.random.normal(0, 4) for _ in range(intervals)]
        for i in range(intervals // 2, intervals * 3 // 4):
            udp_flood[i] *= (2.5 + np.random.normal(0, 0.4))
        
        # Create multi-vector chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=time_points, y=http_flood,
            mode='lines', name='HTTP Flood',
            line=dict(color='red', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=time_points, y=syn_flood,
            mode='lines', name='SYN Flood',
            line=dict(color='orange', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=time_points, y=udp_flood,
            mode='lines', name='UDP Flood',
            line=dict(color='purple', width=2)
        ))
        
        fig.update_layout(
            title='Multi-vector Attack Pattern',
            xaxis_title='Time',
            yaxis_title='Attack Intensity',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_system_impact_modeling(self):
        st.subheader("💥 System Impact Modeling")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**System Configuration**")
            
            system_type = st.selectbox(
                "System Type",
                ["Web Application", "API Service", "Database Server", "CDN Edge", "Microservices"]
            )
            
            capacity = st.slider(
                "System Capacity (RPS)",
                min_value=100,
                max_value=10000,
                value=1000,
                step=100
            )
            
            attack_intensity = st.slider(
                "Attack Intensity (RPS)",
                min_value=100,
                max_value=50000,
                value=5000,
                step=500
            )
            
            if st.button("Model System Impact"):
                st.session_state['impact_modeled'] = True
                st.session_state['system_config'] = {
                    'type': system_type,
                    'capacity': capacity,
                    'attack_intensity': attack_intensity
                }
        
        with col2:
            if st.session_state.get('impact_modeled', False):
                self._show_system_impact_analysis()
    
    def _show_system_impact_analysis(self):
        config = st.session_state.get('system_config', {})
        
        st.markdown("**System Impact Analysis**")
        
        # Calculate impact metrics
        capacity = config['capacity']
        attack_intensity = config['attack_intensity']
        
        # System performance degradation
        overload_ratio = attack_intensity / capacity
        
        if overload_ratio <= 1:
            performance_impact = "Minimal"
            availability = 95 + (1 - overload_ratio) * 5
        elif overload_ratio <= 2:
            performance_impact = "Moderate"
            availability = 90 - (overload_ratio - 1) * 20
        elif overload_ratio <= 5:
            performance_impact = "Severe"
            availability = 70 - (overload_ratio - 2) * 15
        else:
            performance_impact = "Critical"
            availability = max(0, 25 - (overload_ratio - 5) * 5)
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Performance Impact", performance_impact)
        
        with col2:
            st.metric("Estimated Availability", f"{availability:.1f}%")
        
        with col3:
            response_time = 100 * (1 + overload_ratio)
            st.metric("Response Time Impact", f"{response_time:.0f}ms")
        
        # System resource utilization
        st.markdown("**Resource Utilization Under Attack**")
        
        time_points = list(range(0, 61, 5))  # 1 hour in 5-minute intervals
        
        # Normal utilization
        cpu_normal = [20 + np.random.normal(0, 5) for _ in time_points]
        memory_normal = [30 + np.random.normal(0, 3) for _ in time_points]
        network_normal = [15 + np.random.normal(0, 4) for _ in time_points]
        
        # Attack utilization (spike in the middle)
        attack_start, attack_end = 15, 45
        cpu_attack = cpu_normal.copy()
        memory_attack = memory_normal.copy()
        network_attack = network_normal.copy()
        
        for i, t in enumerate(time_points):
            if attack_start <= t <= attack_end:
                intensity_factor = min(overload_ratio, 5)
                cpu_attack[i] = min(100, cpu_normal[i] + 60 * (intensity_factor / 5))
                memory_attack[i] = min(100, memory_normal[i] + 40 * (intensity_factor / 5))
                network_attack[i] = min(100, network_normal[i] + 70 * (intensity_factor / 5))
        
        # Create resource utilization chart
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=('CPU Utilization', 'Memory Utilization', 'Network Utilization'),
            vertical_spacing=0.08
        )
        
        fig.add_trace(go.Scatter(x=time_points, y=cpu_normal, name='CPU Normal', line=dict(color='green')), row=1, col=1)
        fig.add_trace(go.Scatter(x=time_points, y=cpu_attack, name='CPU Attack', line=dict(color='red')), row=1, col=1)
        
        fig.add_trace(go.Scatter(x=time_points, y=memory_normal, name='Memory Normal', line=dict(color='green'), showlegend=False), row=2, col=1)
        fig.add_trace(go.Scatter(x=time_points, y=memory_attack, name='Memory Attack', line=dict(color='red'), showlegend=False), row=2, col=1)
        
        fig.add_trace(go.Scatter(x=time_points, y=network_normal, name='Network Normal', line=dict(color='green'), showlegend=False), row=3, col=1)
        fig.add_trace(go.Scatter(x=time_points, y=network_attack, name='Network Attack', line=dict(color='red'), showlegend=False), row=3, col=1)
        
        fig.update_xaxes(title_text="Time (minutes)", row=3, col=1)
        fig.update_yaxes(title_text="CPU %", row=1, col=1)
        fig.update_yaxes(title_text="Memory %", row=2, col=1)
        fig.update_yaxes(title_text="Network %", row=3, col=1)
        
        fig.update_layout(height=600, title_text="System Resource Impact During Attack")
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_attack_vector_comparison(self):
        st.subheader("⚖️ Attack Vector Comparison")
        
        # Attack vector comparison data
        vectors = ['DDoS Flood', 'SYN Flood', 'HTTP Flood', 'Slowloris', 'UDP Flood', 'Amplification']
        
        # Comparison metrics (educational estimates)
        difficulty = [3, 4, 2, 3, 2, 5]  # 1-5 scale
        detectability = [2, 3, 4, 5, 2, 3]  # 1-5 scale (higher = easier to detect)
        impact = [5, 4, 4, 3, 4, 5]  # 1-5 scale
        bandwidth_req = [5, 2, 3, 1, 4, 1]  # 1-5 scale
        
        # Create comparison chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=difficulty,
            theta=vectors,
            fill='toself',
            name='Attack Difficulty',
            line_color='red'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=detectability,
            theta=vectors,
            fill='toself',
            name='Detection Difficulty',
            line_color='blue'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=impact,
            theta=vectors,
            fill='toself',
            name='Potential Impact',
            line_color='orange'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                )),
            showlegend=True,
            title="Attack Vector Comparison Matrix"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed comparison table
        st.markdown("**Detailed Comparison**")
        
        comparison_df = pd.DataFrame({
            'Attack Vector': vectors,
            'Difficulty (1-5)': difficulty,
            'Detection (1-5)': detectability,
            'Impact (1-5)': impact,
            'Bandwidth Required': ['Very High', 'Low', 'Medium', 'Very Low', 'High', 'Very Low'],
            'Primary Target': ['Network/Bandwidth', 'Connection Pool', 'Application Layer', 'Connection Pool', 'Network/Bandwidth', 'Network/Bandwidth'],
            'Typical Duration': ['Minutes to Hours', 'Minutes', 'Hours', 'Hours to Days', 'Minutes to Hours', 'Minutes']
        })
        
        st.dataframe(comparison_df, use_container_width=True)
        
        # Attack characteristics
        st.markdown("---")
        st.subheader("🎯 Attack Characteristics")
        
        selected_vector = st.selectbox("Select Attack Vector for Details", vectors)
        
        vector_details = {
            'DDoS Flood': {
                'description': 'Overwhelming the target with massive amounts of traffic from multiple sources',
                'characteristics': ['High volume traffic', 'Multiple attack sources', 'Network congestion'],
                'detection_methods': ['Traffic volume monitoring', 'Source IP analysis', 'Rate-based detection'],
                'mitigation': ['Rate limiting', 'Traffic filtering', 'DDoS protection services']
            },
            'SYN Flood': {
                'description': 'Exhausting server resources by sending many TCP SYN requests without completing handshake',
                'characteristics': ['Half-open connections', 'Resource exhaustion', 'Connection table overflow'],
                'detection_methods': ['Connection state monitoring', 'SYN/ACK ratio analysis', 'Resource utilization'],
                'mitigation': ['SYN cookies', 'Connection rate limiting', 'Firewall protection']
            },
            'HTTP Flood': {
                'description': 'Overwhelming web servers with HTTP requests that appear legitimate',
                'characteristics': ['Application layer attack', 'Legitimate-looking requests', 'Resource intensive'],
                'detection_methods': ['Request rate analysis', 'Behavioral patterns', 'User agent analysis'],
                'mitigation': ['Rate limiting', 'Web application firewalls', 'CAPTCHA challenges']
            },
            'Slowloris': {
                'description': 'Keeping many connections open to the server by sending partial HTTP requests',
                'characteristics': ['Low bandwidth attack', 'Connection exhaustion', 'Slow request completion'],
                'detection_methods': ['Connection duration monitoring', 'Incomplete request analysis', 'Connection patterns'],
                'mitigation': ['Connection timeouts', 'Concurrent connection limits', 'Reverse proxies']
            },
            'UDP Flood': {
                'description': 'Sending large volumes of UDP packets to random ports on the target',
                'characteristics': ['High packet rate', 'Random ports', 'Network congestion'],
                'detection_methods': ['UDP traffic analysis', 'Port scanning patterns', 'Traffic volume'],
                'mitigation': ['UDP rate limiting', 'Port filtering', 'Ingress filtering']
            },
            'Amplification': {
                'description': 'Using third-party servers to amplify attack traffic with spoofed source addresses',
                'characteristics': ['Traffic amplification', 'Spoofed sources', 'Reflection attacks'],
                'detection_methods': ['Amplification ratios', 'Source validation', 'Protocol analysis'],
                'mitigation': ['BCP38 implementation', 'Response rate limiting', 'Server hardening']
            }
        }
        
        if selected_vector in vector_details:
            details = vector_details[selected_vector]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Description**")
                st.write(details['description'])
                
                st.markdown("**Key Characteristics**")
                for char in details['characteristics']:
                    st.write(f"• {char}")
            
            with col2:
                st.markdown("**Detection Methods**")
                for method in details['detection_methods']:
                    st.write(f"• {method}")
                
                st.markdown("**Mitigation Strategies**")
                for mitigation in details['mitigation']:
                    st.write(f"• {mitigation}")
    
    def _get_attack_patterns(self):
        """Get predefined attack patterns for analysis"""
        return {
            'volumetric': {
                'characteristics': ['High bandwidth consumption', 'Network saturation', 'Infrastructure impact'],
                'detection_signatures': ['Traffic volume spikes', 'Bandwidth utilization', 'Network congestion']
            },
            'protocol': {
                'characteristics': ['Protocol exploitation', 'Resource exhaustion', 'Connection manipulation'],
                'detection_signatures': ['Connection anomalies', 'Protocol violations', 'State table overflow']
            },
            'application': {
                'characteristics': ['Application targeting', 'Resource consumption', 'Service disruption'],
                'detection_signatures': ['Request patterns', 'Response time degradation', 'Application errors']
            }
        }
