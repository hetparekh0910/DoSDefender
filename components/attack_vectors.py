"""
Attack Vectors Component - Detailed analysis of DoS attack methodologies
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from plotly.subplots import make_subplots
from data.dos_attacks_database import DoSAttackDatabase

class AttackVectors:
    def __init__(self):
        self.db = DoSAttackDatabase()
        self.attack_vectors = self.db.get_attack_vectors()
    
    def render(self):
        st.header("🔍 DoS Attack Vectors Analysis")
        st.markdown("""
        Comprehensive breakdown of DoS attack methodologies, techniques, and execution patterns.
        Understanding these vectors is crucial for developing effective defensive strategies.
        """)
        
        # Vector category selection
        categories = list(self.attack_vectors.keys())
        category_names = {
            'volumetric': '🌊 Volumetric Attacks',
            'protocol': '⚡ Protocol Attacks', 
            'application': '🎯 Application Layer Attacks'
        }
        
        selected_category = st.selectbox(
            "Select Attack Category",
            categories,
            format_func=lambda x: category_names.get(x, x.title())
        )
        
        # Display category overview
        self._render_category_overview(selected_category)
        
        st.markdown("---")
        
        # Detailed vector analysis
        self._render_detailed_vector_analysis(selected_category)
        
        st.markdown("---")
        
        # Attack methodology breakdown
        self._render_attack_methodology(selected_category)
        
        st.markdown("---")
        
        # Comparative analysis
        self._render_comparative_analysis()
    
    def _render_category_overview(self, category):
        category_data = self.attack_vectors[category]
        
        st.subheader(f"📋 {category_data['name']} Overview")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**Description**")
            st.write(category_data['description'])
            
            st.markdown("**Attack Subcategories**")
            subcategories = category_data['subcategories']
            
            # Create subcategory metrics
            col1a, col1b, col1c = st.columns(3)
            
            with col1a:
                st.metric("Total Variants", len(subcategories))
            
            with col1b:
                # Calculate average complexity (simulated)
                avg_complexity = sum([3, 4, 2][:len(subcategories)]) / len(subcategories)
                st.metric("Avg Complexity", f"{avg_complexity:.1f}/5")
            
            with col1c:
                st.metric("Detection Difficulty", "Medium-High")
        
        with col2:
            # Category characteristics visualization
            characteristics = []
            complexity_scores = []
            
            for sub in subcategories:
                characteristics.append(sub['name'])
                # Assign complexity based on characteristics (educational simulation)
                if 'amplification' in sub['name'].lower() or 'flood' in sub['name'].lower():
                    complexity_scores.append(4)
                elif 'syn' in sub['name'].lower():
                    complexity_scores.append(3)
                else:
                    complexity_scores.append(3.5)
            
            fig = go.Figure(data=go.Scatterpolar(
                r=complexity_scores,
                theta=characteristics,
                fill='toself',
                name=f'{category.title()} Complexity'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 5]
                    )),
                showlegend=False,
                title="Attack Complexity Profile",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def _render_detailed_vector_analysis(self, category):
        st.subheader("🔬 Detailed Vector Analysis")
        
        category_data = self.attack_vectors[category]
        subcategories = category_data['subcategories']
        
        # Vector selection
        vector_names = [sub['name'] for sub in subcategories]
        selected_vector = st.selectbox("Select Attack Vector", vector_names)
        
        # Find selected vector data
        vector_data = None
        for sub in subcategories:
            if sub['name'] == selected_vector:
                vector_data = sub
                break
        
        if vector_data:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown(f"**{vector_data['name']} - Technical Details**")
                st.write(vector_data['description'])
                
                st.markdown("**Key Characteristics**")
                for char in vector_data['characteristics']:
                    st.write(f"• {char}")
                
                st.markdown("**Mitigation Strategies**")
                for mitigation in vector_data['mitigation']:
                    st.write(f"• {mitigation}")
            
            with col2:
                # Create attack flow diagram
                self._create_attack_flow_diagram(vector_data)
        
        # Attack execution steps
        st.markdown("---")
        st.subheader("📝 Attack Execution Analysis")
        
        execution_steps = self._get_execution_steps(selected_vector)
        
        for i, step in enumerate(execution_steps, 1):
            with st.expander(f"Step {i}: {step['title']}"):
                st.write(f"**Description:** {step['description']}")
                st.write(f"**Technical Details:** {step['technical']}")
                st.write(f"**Indicators:** {step['indicators']}")
    
    def _create_attack_flow_diagram(self, vector_data):
        st.markdown("**Attack Flow Diagram**")
        
        # Create a network graph based on attack type
        G = nx.DiGraph()
        
        vector_name = vector_data['name']
        
        if 'UDP Flood' in vector_name:
            nodes = [
                ('Attacker', {'pos': (0, 0), 'type': 'attacker'}),
                ('Botnet', {'pos': (1, 0), 'type': 'resource'}),
                ('Internet', {'pos': (2, 0), 'type': 'network'}),
                ('Target Server', {'pos': (3, 0), 'type': 'target'}),
                ('UDP Ports', {'pos': (3, -1), 'type': 'resource'})
            ]
            
            edges = [
                ('Attacker', 'Botnet'),
                ('Botnet', 'Internet'),
                ('Internet', 'Target Server'),
                ('Target Server', 'UDP Ports')
            ]
        
        elif 'SYN Flood' in vector_name:
            nodes = [
                ('Attacker', {'pos': (0, 0), 'type': 'attacker'}),
                ('Spoofed IPs', {'pos': (1, 0), 'type': 'resource'}),
                ('Internet', {'pos': (2, 0), 'type': 'network'}),
                ('Target Server', {'pos': (3, 0), 'type': 'target'}),
                ('Connection Table', {'pos': (3, -1), 'type': 'resource'})
            ]
            
            edges = [
                ('Attacker', 'Spoofed IPs'),
                ('Spoofed IPs', 'Internet'),
                ('Internet', 'Target Server'),
                ('Target Server', 'Connection Table')
            ]
        
        elif 'HTTP Flood' in vector_name:
            nodes = [
                ('Attacker', {'pos': (0, 0), 'type': 'attacker'}),
                ('Bot Network', {'pos': (1, 0), 'type': 'resource'}),
                ('Internet', {'pos': (2, 0), 'type': 'network'}),
                ('Web Server', {'pos': (3, 0), 'type': 'target'}),
                ('CPU/Memory', {'pos': (3, -1), 'type': 'resource'})
            ]
            
            edges = [
                ('Attacker', 'Bot Network'),
                ('Bot Network', 'Internet'),
                ('Internet', 'Web Server'),
                ('Web Server', 'CPU/Memory')
            ]
        
        else:
            # Generic flow
            nodes = [
                ('Attacker', {'pos': (0, 0), 'type': 'attacker'}),
                ('Attack Vector', {'pos': (1, 0), 'type': 'resource'}),
                ('Network', {'pos': (2, 0), 'type': 'network'}),
                ('Target', {'pos': (3, 0), 'type': 'target'})
            ]
            
            edges = [
                ('Attacker', 'Attack Vector'),
                ('Attack Vector', 'Network'),
                ('Network', 'Target')
            ]
        
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        
        # Get positions
        pos = nx.get_node_attributes(G, 'pos')
        
        # Create edge traces
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        # Create node traces
        node_x = [pos[node][0] for node in G.nodes()]
        node_y = [pos[node][1] for node in G.nodes()]
        node_types = [G.nodes[node]['type'] for node in G.nodes()]
        
        # Color mapping
        color_map = {
            'attacker': 'red',
            'target': 'orange', 
            'network': 'blue',
            'resource': 'green'
        }
        
        node_colors = [color_map.get(t, 'gray') for t in node_types]
        
        fig = go.Figure()
        
        # Add edges
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines'
        ))
        
        # Add nodes
        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=list(G.nodes()),
            textposition="middle center",
            marker=dict(
                size=40,
                color=node_colors,
                line=dict(width=2, color='black')
            )
        ))
        
        fig.update_layout(
            title=f'{vector_name} Attack Flow',
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _get_execution_steps(self, vector_name):
        """Get detailed execution steps for specific attack vectors"""
        
        steps_map = {
            'UDP Flood': [
                {
                    'title': 'Reconnaissance',
                    'description': 'Identify target server and open UDP ports',
                    'technical': 'Port scanning, service enumeration, bandwidth assessment',
                    'indicators': 'Scanning activity, reconnaissance patterns'
                },
                {
                    'title': 'Resource Preparation',
                    'description': 'Assemble botnet or attack infrastructure',
                    'technical': 'Command and control setup, bot recruitment, bandwidth aggregation',
                    'indicators': 'C&C communications, bot registration patterns'
                },
                {
                    'title': 'Attack Initiation',
                    'description': 'Begin sending UDP packets to random ports',
                    'technical': 'High-rate UDP packet generation, random port targeting',
                    'indicators': 'Sudden UDP traffic increase, random port access'
                },
                {
                    'title': 'Amplification',
                    'description': 'Scale attack intensity and maintain persistence',
                    'technical': 'Packet rate escalation, distributed source coordination',
                    'indicators': 'Traffic volume spikes, network congestion'
                }
            ],
            
            'SYN Flood': [
                {
                    'title': 'Target Analysis',
                    'description': 'Analyze target TCP services and connection handling',
                    'technical': 'TCP service discovery, connection limits assessment',
                    'indicators': 'Service probing, connection testing patterns'
                },
                {
                    'title': 'IP Spoofing Setup',
                    'description': 'Prepare spoofed IP addresses for source concealment',
                    'technical': 'Random IP generation, spoofing capability testing',
                    'indicators': 'Unusual source IP patterns, geographic inconsistencies'
                },
                {
                    'title': 'SYN Packet Flood',
                    'description': 'Send high volume of TCP SYN packets without completing handshake',
                    'technical': 'TCP SYN generation, connection state manipulation',
                    'indicators': 'High SYN packet rate, incomplete connections'
                },
                {
                    'title': 'Resource Exhaustion',
                    'description': 'Overwhelm target connection table and memory',
                    'technical': 'Connection table overflow, memory consumption',
                    'indicators': 'Connection failures, resource utilization spikes'
                }
            ],
            
            'HTTP Flood': [
                {
                    'title': 'Web Application Analysis',
                    'description': 'Identify resource-intensive web application endpoints',
                    'technical': 'Endpoint discovery, response time analysis, resource mapping',
                    'indicators': 'Web crawling activity, endpoint enumeration'
                },
                {
                    'title': 'Request Crafting',
                    'description': 'Design HTTP requests to maximize server resource consumption',
                    'technical': 'Request optimization, parameter manipulation, session handling',
                    'indicators': 'Unusual request patterns, parameter variations'
                },
                {
                    'title': 'Distributed Execution',
                    'description': 'Coordinate HTTP requests across multiple sources',
                    'technical': 'Load distribution, rate coordination, session management',
                    'indicators': 'Coordinated request patterns, distributed sources'
                },
                {
                    'title': 'Application Overload',
                    'description': 'Overwhelm application server resources and database connections',
                    'technical': 'CPU/memory exhaustion, database connection pool depletion',
                    'indicators': 'Response time degradation, application errors'
                }
            ]
        }
        
        return steps_map.get(vector_name, [
            {
                'title': 'Attack Preparation',
                'description': 'Prepare attack infrastructure and resources',
                'technical': 'Resource allocation, target assessment',
                'indicators': 'Preparatory activities, reconnaissance'
            },
            {
                'title': 'Attack Execution',
                'description': 'Execute the primary attack vector',
                'technical': 'Attack implementation, traffic generation',
                'indicators': 'Attack traffic patterns, service degradation'
            },
            {
                'title': 'Impact Assessment',
                'description': 'Monitor attack effectiveness and adjust as needed',
                'technical': 'Impact measurement, attack tuning',
                'indicators': 'Service disruption, performance degradation'
            }
        ])
    
    def _render_attack_methodology(self, category):
        st.subheader("🛠️ Attack Methodology Breakdown")
        
        methodology_tabs = st.tabs(["🎯 Targeting", "⚡ Execution", "📊 Measurement", "🔄 Adaptation"])
        
        with methodology_tabs[0]:
            st.markdown("**Target Selection & Reconnaissance**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Common Target Criteria**")
                st.write("• High-value services or applications")
                st.write("• Limited DDoS protection")
                st.write("• Critical business operations")
                st.write("• Public-facing infrastructure")
                st.write("• Single points of failure")
            
            with col2:
                st.markdown("**Reconnaissance Techniques**")
                st.write("• Port scanning and service enumeration")
                st.write("• Infrastructure mapping")
                st.write("• Capacity and bandwidth assessment")
                st.write("• Defense mechanism identification")
                st.write("• Peak usage time analysis")
            
            # Target assessment matrix
            targets = ['Web Server', 'API Gateway', 'Database', 'DNS Server', 'CDN Edge']
            vulnerability_scores = [7, 6, 8, 9, 4]
            impact_scores = [8, 7, 9, 10, 6]
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=vulnerability_scores,
                y=impact_scores,
                mode='markers+text',
                text=targets,
                textposition="middle center",
                marker=dict(
                    size=[score * 5 for score in vulnerability_scores],
                    color=impact_scores,
                    colorscale='Reds',
                    colorbar=dict(title="Impact Score")
                ),
                name='Targets'
            ))
            
            fig.update_layout(
                title='Target Vulnerability vs Impact Assessment',
                xaxis_title='Vulnerability Score (1-10)',
                yaxis_title='Business Impact Score (1-10)',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with methodology_tabs[1]:
            st.markdown("**Attack Execution Patterns**")
            
            execution_data = {
                'Phase': ['Preparation', 'Initial Probe', 'Escalation', 'Peak Attack', 'Persistence', 'Evasion'],
                'Duration': [30, 5, 15, 60, 120, 30],  # minutes
                'Intensity': [1, 2, 5, 10, 8, 4],  # 1-10 scale
                'Detection Risk': [2, 3, 6, 9, 7, 5]  # 1-10 scale
            }
            
            df = pd.DataFrame(execution_data)
            
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Attack Intensity Over Time', 'Detection Risk vs Duration')
            )
            
            fig.add_trace(
                go.Scatter(x=df['Phase'], y=df['Intensity'], mode='lines+markers', name='Intensity'),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Bar(x=df['Phase'], y=df['Duration'], name='Duration (min)', marker_color='lightblue'),
                row=2, col=1
            )
            
            fig.update_layout(height=600, title_text="Attack Execution Analysis")
            st.plotly_chart(fig, use_container_width=True)
        
        with methodology_tabs[2]:
            st.markdown("**Attack Effectiveness Measurement**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Success Indicators**")
                st.write("• Service response time degradation")
                st.write("• Connection timeout increases")
                st.write("• Error rate elevation")
                st.write("• Resource utilization spikes")
                st.write("• User complaint volume")
            
            with col2:
                st.markdown("**Measurement Techniques**")
                st.write("• Response time monitoring")
                st.write("• Availability testing")
                st.write("• Resource utilization tracking")
                st.write("• Error rate analysis")
                st.write("• User experience metrics")
            
            # Create effectiveness metrics visualization
            metrics = ['Response Time', 'Availability', 'Error Rate', 'Resource Usage', 'User Experience']
            baseline = [100, 100, 0, 30, 100]
            under_attack = [300, 45, 25, 90, 20]
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=baseline,
                theta=metrics,
                fill='toself',
                name='Baseline Performance',
                line_color='green'
            ))
            
            fig.add_trace(go.Scatterpolar(
                r=under_attack,
                theta=metrics,
                fill='toself',
                name='Under Attack',
                line_color='red'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 400]
                    )),
                showlegend=True,
                title="System Performance: Normal vs Under Attack"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with methodology_tabs[3]:
            st.markdown("**Attack Adaptation & Evasion**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Adaptation Strategies**")
                st.write("• Traffic pattern variation")
                st.write("• Source rotation and diversification")
                st.write("• Attack vector switching")
                st.write("• Timing and rate adjustments")
                st.write("• Payload and protocol changes")
            
            with col2:
                st.markdown("**Evasion Techniques**")
                st.write("• Mimicking legitimate traffic")
                st.write("• Distributed source utilization")
                st.write("• Encrypted payload delivery")
                st.write("• Legitimate service exploitation")
                st.write("• Rate limiting circumvention")
            
            # Adaptation timeline
            adaptation_events = [
                {'hour': 0, 'event': 'Initial attack launch', 'effectiveness': 80},
                {'hour': 1, 'event': 'Rate limiting detected', 'effectiveness': 60},
                {'hour': 2, 'event': 'Source IP diversification', 'effectiveness': 75},
                {'hour': 3, 'event': 'Attack vector switching', 'effectiveness': 85},
                {'hour': 4, 'event': 'Pattern randomization', 'effectiveness': 70},
                {'hour': 5, 'event': 'Defensive adaptation', 'effectiveness': 40}
            ]
            
            hours = [event['hour'] for event in adaptation_events]
            effectiveness = [event['effectiveness'] for event in adaptation_events]
            events = [event['event'] for event in adaptation_events]
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=hours,
                y=effectiveness,
                mode='lines+markers',
                text=events,
                hovertemplate='<b>%{text}</b><br>Hour: %{x}<br>Effectiveness: %{y}%<extra></extra>',
                line=dict(color='red', width=3),
                marker=dict(size=8)
            ))
            
            fig.update_layout(
                title='Attack Adaptation Timeline',
                xaxis_title='Hours Since Attack Start',
                yaxis_title='Attack Effectiveness (%)',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def _render_comparative_analysis(self):
        st.subheader("⚖️ Attack Vector Comparison")
        
        # Comprehensive comparison of all attack vectors
        comparison_data = []
        
        for category_key, category_data in self.attack_vectors.items():
            for sub in category_data['subcategories']:
                comparison_data.append({
                    'Attack Vector': sub['name'],
                    'Category': category_key.title(),
                    'Complexity': self._estimate_complexity(sub),
                    'Detection Difficulty': self._estimate_detection_difficulty(sub),
                    'Impact Potential': self._estimate_impact_potential(sub),
                    'Resource Requirements': self._estimate_resource_requirements(sub),
                    'Persistence': self._estimate_persistence(sub)
                })
        
        df = pd.DataFrame(comparison_data)
        
        # Multi-dimensional comparison
        col1, col2 = st.columns(2)
        
        with col1:
            # Radar chart comparison
            selected_vectors = st.multiselect(
                "Select vectors to compare",
                df['Attack Vector'].tolist(),
                default=df['Attack Vector'].tolist()[:3]
            )
            
            if selected_vectors:
                self._create_radar_comparison(df, selected_vectors)
        
        with col2:
            # Scatter plot analysis
            x_metric = st.selectbox("X-axis metric", ['Complexity', 'Detection Difficulty', 'Impact Potential', 'Resource Requirements'])
            y_metric = st.selectbox("Y-axis metric", ['Impact Potential', 'Detection Difficulty', 'Complexity', 'Persistence'])
            
            if x_metric != y_metric:
                fig = px.scatter(
                    df,
                    x=x_metric,
                    y=y_metric,
                    color='Category',
                    size='Impact Potential',
                    hover_data=['Attack Vector'],
                    title=f'{x_metric} vs {y_metric}'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Detailed comparison table
        st.markdown("**Detailed Comparison Matrix**")
        st.dataframe(df, use_container_width=True)
        
        # Attack vector recommendations
        st.markdown("---")
        st.subheader("🎯 Defense Priority Recommendations")
        
        # Calculate defense priority scores
        df['Defense Priority'] = (df['Impact Potential'] * 0.4 + 
                                df['Detection Difficulty'] * 0.3 + 
                                df['Complexity'] * 0.2 + 
                                df['Persistence'] * 0.1)
        
        priority_df = df.nlargest(5, 'Defense Priority')[['Attack Vector', 'Category', 'Defense Priority']]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = px.bar(
                priority_df,
                x='Defense Priority',
                y='Attack Vector',
                color='Category',
                orientation='h',
                title='Top Defense Priorities'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Priority Rationale**")
            st.write("Defense priority calculated based on:")
            st.write("• Impact Potential (40%)")
            st.write("• Detection Difficulty (30%)")
            st.write("• Attack Complexity (20%)")  
            st.write("• Persistence (10%)")
            
            st.markdown("**Recommended Actions**")
            for _, row in priority_df.iterrows():
                st.write(f"• **{row['Attack Vector']}**: Enhanced monitoring and protection")
    
    def _create_radar_comparison(self, df, selected_vectors):
        """Create radar chart for vector comparison"""
        
        metrics = ['Complexity', 'Detection Difficulty', 'Impact Potential', 'Resource Requirements', 'Persistence']
        
        fig = go.Figure()
        
        colors = ['red', 'blue', 'green', 'orange', 'purple']
        
        for i, vector in enumerate(selected_vectors[:5]):  # Limit to 5 for readability
            vector_data = df[df['Attack Vector'] == vector].iloc[0]
            values = [vector_data[metric] for metric in metrics]
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=metrics,
                fill='toself',
                name=vector,
                line_color=colors[i % len(colors)]
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            showlegend=True,
            title="Attack Vector Comparison"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _estimate_complexity(self, vector_data):
        """Estimate attack complexity based on characteristics"""
        characteristics = vector_data.get('characteristics', [])
        complexity_indicators = ['amplification', 'spoofed', 'coordination', 'sophisticated']
        
        base_score = 5
        for indicator in complexity_indicators:
            for char in characteristics:
                if indicator in char.lower():
                    base_score += 1
        
        return min(base_score, 10)
    
    def _estimate_detection_difficulty(self, vector_data):
        """Estimate detection difficulty"""
        characteristics = vector_data.get('characteristics', [])
        detection_indicators = ['legitimate', 'mimics', 'stealth', 'low profile']
        
        base_score = 4
        for indicator in detection_indicators:
            for char in characteristics:
                if indicator in char.lower():
                    base_score += 2
        
        return min(base_score, 10)
    
    def _estimate_impact_potential(self, vector_data):
        """Estimate potential impact"""
        characteristics = vector_data.get('characteristics', [])
        impact_indicators = ['exhaustion', 'overflow', 'consumption', 'disruption']
        
        base_score = 6
        for indicator in impact_indicators:
            for char in characteristics:
                if indicator in char.lower():
                    base_score += 1
        
        return min(base_score, 10)
    
    def _estimate_resource_requirements(self, vector_data):
        """Estimate resource requirements"""
        name = vector_data.get('name', '').lower()
        
        if 'flood' in name:
            return 8
        elif 'amplification' in name:
            return 4
        elif 'slow' in name:
            return 2
        else:
            return 6
    
    def _estimate_persistence(self, vector_data):
        """Estimate attack persistence capability"""
        characteristics = vector_data.get('characteristics', [])
        persistence_indicators = ['sustained', 'continuous', 'persistent', 'long-term']
        
        base_score = 5
        for indicator in persistence_indicators:
            for char in characteristics:
                if indicator in char.lower():
                    base_score += 2
        
        return min(base_score, 10)
