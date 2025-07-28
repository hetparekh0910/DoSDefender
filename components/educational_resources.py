"""
Educational Resources Component - Learning materials and guides for DoS attack education
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from data.dos_attacks_database import DoSAttackDatabase

class EducationalResources:
    def __init__(self):
        self.db = DoSAttackDatabase()
        self.learning_modules = self._get_learning_modules()
        self.quiz_questions = self._get_quiz_questions()
        self.practical_exercises = self._get_practical_exercises()
    
    def render(self):
        st.header("📖 Educational Resources")
        st.markdown("""
        Comprehensive learning materials for understanding DoS attacks, defense strategies, 
        and cybersecurity best practices. All content is designed for educational and defensive purposes.
        """)
        
        # Resource type selection
        resource_type = st.selectbox(
            "Select Learning Resource",
            ["Learning Modules", "Interactive Guides", "Knowledge Assessment", "Practical Exercises", "Reference Materials"]
        )
        
        if resource_type == "Learning Modules":
            self._render_learning_modules()
        elif resource_type == "Interactive Guides":
            self._render_interactive_guides()
        elif resource_type == "Knowledge Assessment":
            self._render_knowledge_assessment()
        elif resource_type == "Practical Exercises":
            self._render_practical_exercises()
        elif resource_type == "Reference Materials":
            self._render_reference_materials()
    
    def _render_learning_modules(self):
        st.subheader("📚 Learning Modules")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Available Modules**")
            
            module_names = list(self.learning_modules.keys())
            selected_module = st.selectbox("Select Module", module_names)
            
            # Module progress tracking
            if 'module_progress' not in st.session_state:
                st.session_state.module_progress = {}
            
            current_progress = st.session_state.module_progress.get(selected_module, 0)
            st.progress(current_progress / 100, f"Progress: {current_progress}%")
            
            # Module navigation
            st.markdown("---")
            st.markdown("**Module Navigation**")
            
            if selected_module in self.learning_modules:
                module_data = self.learning_modules[selected_module]
                sections = list(module_data['sections'].keys())
                
                selected_section = st.selectbox("Select Section", sections)
        
        with col2:
            if selected_module and selected_section:
                self._show_module_content(selected_module, selected_section)
    
    def _show_module_content(self, module_name, section_name):
        module_data = self.learning_modules[module_name]
        section_data = module_data['sections'][section_name]
        
        st.markdown(f"### {section_name}")
        
        # Learning objectives
        if 'objectives' in section_data:
            st.markdown("**Learning Objectives**")
            for objective in section_data['objectives']:
                st.write(f"• {objective}")
            st.markdown("---")
        
        # Content delivery
        content_type = section_data.get('type', 'text')
        
        if content_type == 'text':
            st.markdown(section_data['content'])
        
        elif content_type == 'interactive':
            self._render_interactive_content(section_data)
        
        elif content_type == 'visualization':
            self._render_visualization_content(section_data)
        
        # Key concepts
        if 'key_concepts' in section_data:
            st.markdown("---")
            st.markdown("**Key Concepts**")
            
            for concept, definition in section_data['key_concepts'].items():
                with st.expander(f"🔑 {concept}"):
                    st.write(definition)
        
        # Practice questions
        if 'practice_questions' in section_data:
            st.markdown("---")
            st.markdown("**Practice Questions**")
            
            for i, question in enumerate(section_data['practice_questions']):
                with st.expander(f"Question {i+1}: {question['question']}"):
                    user_answer = st.radio(
                        "Select your answer:",
                        question['options'],
                        key=f"q_{module_name}_{section_name}_{i}"
                    )
                    
                    if st.button(f"Check Answer", key=f"check_{module_name}_{section_name}_{i}"):
                        if user_answer == question['correct_answer']:
                            st.success("✅ Correct! " + question['explanation'])
                        else:
                            st.error("❌ Incorrect. " + question['explanation'])
        
        # Section completion
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Mark Section Complete", key=f"complete_{module_name}_{section_name}"):
                # Update progress
                total_sections = len(module_data['sections'])
                progress_increment = 100 / total_sections
                
                current_progress = st.session_state.module_progress.get(module_name, 0)
                new_progress = min(100, current_progress + progress_increment)
                st.session_state.module_progress[module_name] = new_progress
                
                st.success("Section marked as complete!")
                st.rerun()
        
        with col2:
            if st.button("Download Section Notes", key=f"download_{module_name}_{section_name}"):
                notes = self._generate_section_notes(module_name, section_name, section_data)
                st.download_button(
                    label="Download Notes",
                    data=notes,
                    file_name=f"{module_name}_{section_name}_notes.txt",
                    mime="text/plain"
                )
    
    def _render_interactive_content(self, section_data):
        """Render interactive learning content"""
        content = section_data['content']
        
        if 'simulation' in content:
            simulation = content['simulation']
            
            if simulation['type'] == 'attack_flow':
                st.markdown("**Interactive Attack Flow Simulation**")
                
                # User controls
                col1, col2 = st.columns(2)
                
                with col1:
                    attack_intensity = st.slider("Attack Intensity", 1, 10, 5, key="sim_intensity")
                    attack_duration = st.slider("Duration (minutes)", 1, 60, 10, key="sim_duration")
                
                with col2:
                    defense_level = st.slider("Defense Level", 1, 10, 5, key="sim_defense")
                    response_time = st.slider("Response Time (minutes)", 1, 30, 5, key="sim_response")
                
                # Generate simulation data
                time_points = list(range(0, attack_duration + 1))
                attack_power = [min(10, attack_intensity * (1 + 0.1 * t)) for t in time_points]
                
                # Apply defense
                defense_effectiveness = []
                for t in time_points:
                    if t >= response_time:
                        effectiveness = min(attack_power[t], defense_level * (t - response_time + 1) * 0.2)
                        defense_effectiveness.append(effectiveness)
                    else:
                        defense_effectiveness.append(0)
                
                system_health = [max(0, 100 - (attack_power[t] - defense_effectiveness[t]) * 10) for t in time_points]
                
                # Visualization
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=time_points, y=attack_power,
                    mode='lines+markers', name='Attack Power',
                    line=dict(color='red', width=3)
                ))
                
                fig.add_trace(go.Scatter(
                    x=time_points, y=defense_effectiveness,
                    mode='lines+markers', name='Defense Effectiveness',
                    line=dict(color='blue', width=3)
                ))
                
                fig.add_trace(go.Scatter(
                    x=time_points, y=system_health,
                    mode='lines+markers', name='System Health %',
                    line=dict(color='green', width=3),
                    yaxis='y2'
                ))
                
                fig.update_layout(
                    title='Attack vs Defense Simulation',
                    xaxis_title='Time (minutes)',
                    yaxis_title='Power/Effectiveness',
                    yaxis2=dict(title='System Health %', overlaying='y', side='right'),
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Simulation results
                final_health = system_health[-1]
                if final_health > 80:
                    result = "🛡️ Defense Successful"
                    color = "green"
                elif final_health > 50:
                    result = "⚠️ Partial Defense"
                    color = "orange"
                else:
                    result = "❌ Defense Failed"
                    color = "red"
                
                st.markdown(f"**Simulation Result**: :{color}[{result}]")
                st.write(f"Final System Health: {final_health:.1f}%")
    
    def _render_visualization_content(self, section_data):
        """Render visualization-based learning content"""
        content = section_data['content']
        
        if 'chart_type' in content:
            chart_type = content['chart_type']
            
            if chart_type == 'attack_taxonomy':
                st.markdown("**DoS Attack Taxonomy**")
                
                # Create hierarchical attack taxonomy
                attack_categories = {
                    'Volumetric': ['UDP Flood', 'ICMP Flood', 'Amplification'],
                    'Protocol': ['SYN Flood', 'Ping of Death', 'Smurf Attack'],
                    'Application': ['HTTP Flood', 'Slowloris', 'SSL/TLS Exhaustion']
                }
                
                # Create sunburst chart
                labels = ['DoS Attacks']
                parents = ['']
                values = [100]
                
                for category, attacks in attack_categories.items():
                    labels.append(category)
                    parents.append('DoS Attacks')
                    values.append(len(attacks) * 10)
                    
                    for attack in attacks:
                        labels.append(attack)
                        parents.append(category)
                        values.append(10)
                
                fig = go.Figure(go.Sunburst(
                    labels=labels,
                    parents=parents,
                    values=values,
                    branchvalues="total"
                ))
                
                fig.update_layout(
                    title="DoS Attack Classification",
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            elif chart_type == 'defense_layers':
                st.markdown("**Defense in Depth Strategy**")
                
                # Create defense layers visualization
                layers = ['Network Perimeter', 'Traffic Filtering', 'Rate Limiting', 'Application Protection', 'Monitoring']
                effectiveness = [85, 75, 80, 70, 90]
                complexity = [60, 70, 50, 80, 85]
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatterpolar(
                    r=effectiveness,
                    theta=layers,
                    fill='toself',
                    name='Effectiveness %',
                    line_color='blue'
                ))
                
                fig.add_trace(go.Scatterpolar(
                    r=complexity,
                    theta=layers,
                    fill='toself',
                    name='Implementation Complexity %',
                    line_color='red'
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )),
                    showlegend=True,
                    title="Defense Strategy Analysis"
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    def _render_interactive_guides(self):
        st.subheader("🎯 Interactive Guides")
        
        guide_type = st.selectbox(
            "Select Guide Type",
            ["DoS Detection Setup", "Incident Response", "Network Hardening", "Monitoring Implementation"]
        )
        
        if guide_type == "DoS Detection Setup":
            self._render_detection_setup_guide()
        elif guide_type == "Incident Response":
            self._render_incident_response_guide()
        elif guide_type == "Network Hardening":
            self._render_network_hardening_guide()
        elif guide_type == "Monitoring Implementation":
            self._render_monitoring_guide()
    
    def _render_detection_setup_guide(self):
        st.markdown("### 🔍 DoS Detection Setup Guide")
        
        # Step-by-step guide
        steps = [
            {
                'title': 'Baseline Establishment',
                'description': 'Establish normal traffic patterns and system behavior',
                'tasks': [
                    'Monitor traffic for 2-4 weeks during normal operations',
                    'Document peak usage times and patterns',
                    'Record normal resource utilization levels',
                    'Identify legitimate traffic sources and patterns'
                ],
                'tools': ['Network monitoring tools', 'SIEM systems', 'Traffic analyzers'],
                'metrics': ['Requests per second', 'Bandwidth utilization', 'Connection counts']
            },
            {
                'title': 'Threshold Configuration',
                'description': 'Set appropriate detection thresholds based on baseline data',
                'tasks': [
                    'Calculate baseline statistics (mean, standard deviation)',
                    'Set thresholds at 3-4 standard deviations above normal',
                    'Configure rate-based detection rules',
                    'Implement adaptive thresholds for time-of-day variations'
                ],
                'tools': ['Statistical analysis tools', 'Threshold calculators', 'Alert systems'],
                'metrics': ['Threshold values', 'False positive rates', 'Detection sensitivity']
            },
            {
                'title': 'Detection Rules',
                'description': 'Implement comprehensive detection rules and signatures',
                'tasks': [
                    'Create traffic volume detection rules',
                    'Implement protocol-specific signatures',
                    'Configure behavioral analysis rules',
                    'Set up geographic anomaly detection'
                ],
                'tools': ['IDS/IPS systems', 'Rule engines', 'Signature databases'],
                'metrics': ['Rule coverage', 'Detection accuracy', 'Response time']
            }
        ]
        
        # Interactive step progression
        if 'guide_step' not in st.session_state:
            st.session_state.guide_step = 0
        
        current_step = st.session_state.guide_step
        
        # Step navigation
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("⬅️ Previous", disabled=current_step == 0):
                st.session_state.guide_step = max(0, current_step - 1)
                st.rerun()
        
        with col2:
            st.markdown(f"**Step {current_step + 1} of {len(steps)}**")
            progress = (current_step + 1) / len(steps)
            st.progress(progress)
        
        with col3:
            if st.button("Next ➡️", disabled=current_step == len(steps) - 1):
                st.session_state.guide_step = min(len(steps) - 1, current_step + 1)
                st.rerun()
        
        # Display current step
        step_data = steps[current_step]
        
        st.markdown(f"### {step_data['title']}")
        st.write(step_data['description'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Tasks to Complete**")
            for i, task in enumerate(step_data['tasks']):
                completed = st.checkbox(task, key=f"task_{current_step}_{i}")
        
        with col2:
            st.markdown("**Required Tools**")
            for tool in step_data['tools']:
                st.write(f"• {tool}")
            
            st.markdown("**Key Metrics**")
            for metric in step_data['metrics']:
                st.write(f"• {metric}")
        
        # Step completion check
        all_tasks_completed = all([
            st.session_state.get(f"task_{current_step}_{i}", False) 
            for i in range(len(step_data['tasks']))
        ])
        
        if all_tasks_completed:
            st.success("✅ Step completed! You can proceed to the next step.")
    
    def _render_incident_response_guide(self):
        st.markdown("### 🚨 Incident Response Guide")
        
        # Interactive incident response playbook
        response_phases = {
            'Detection & Analysis': {
                'duration': '5-15 minutes',
                'activities': [
                    'Confirm attack detection',
                    'Classify attack type and severity',
                    'Assess immediate impact',
                    'Activate incident response team'
                ],
                'tools': ['Monitoring dashboards', 'Alert systems', 'Analysis tools'],
                'decisions': [
                    'Is this a confirmed DoS attack?',
                    'What is the attack severity level?',
                    'Which systems are affected?'
                ]
            },
            'Containment': {
                'duration': '15-30 minutes',
                'activities': [
                    'Implement traffic filtering',
                    'Activate DDoS protection services',
                    'Block malicious sources',
                    'Reroute traffic if necessary'
                ],
                'tools': ['Firewalls', 'DDoS protection', 'Load balancers'],
                'decisions': [
                    'Should we block specific IP ranges?',
                    'Do we need to activate cloud protection?',
                    'Should traffic be rerouted?'
                ]
            },
            'Eradication': {
                'duration': '30-60 minutes',
                'activities': [
                    'Eliminate attack sources',
                    'Patch vulnerabilities',
                    'Update security rules',
                    'Strengthen defenses'
                ],
                'tools': ['Security tools', 'Patch management', 'Configuration tools'],
                'decisions': [
                    'Are all attack vectors eliminated?',
                    'Do we need immediate patches?',
                    'What rules need updating?'
                ]
            },
            'Recovery': {
                'duration': '1-4 hours',
                'activities': [
                    'Restore affected services',
                    'Verify system integrity',
                    'Monitor for attack resumption',
                    'Communicate with stakeholders'
                ],
                'tools': ['Backup systems', 'Monitoring tools', 'Communication systems'],
                'decisions': [
                    'Are services fully operational?',
                    'Is monitoring adequate?',
                    'When to communicate all-clear?'
                ]
            }
        }
        
        # Phase selection
        selected_phase = st.selectbox("Select Response Phase", list(response_phases.keys()))
        
        if selected_phase:
            phase_data = response_phases[selected_phase]
            
            st.markdown(f"### {selected_phase}")
            st.write(f"**Typical Duration**: {phase_data['duration']}")
            
            # Interactive checklist
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Activities Checklist**")
                for i, activity in enumerate(phase_data['activities']):
                    completed = st.checkbox(activity, key=f"activity_{selected_phase}_{i}")
            
            with col2:
                st.markdown("**Required Tools**")
                for tool in phase_data['tools']:
                    st.write(f"• {tool}")
            
            # Decision points
            st.markdown("**Key Decision Points**")
            for decision in phase_data['decisions']:
                st.write(f"❓ {decision}")
            
            # Phase timer simulation
            if st.button(f"Start {selected_phase} Timer"):
                st.info(f"⏱️ {selected_phase} phase in progress...")
                st.markdown("Remember to complete all activities and make necessary decisions.")
    
    def _render_network_hardening_guide(self):
        st.markdown("### 🔒 Network Hardening Guide")
        
        hardening_categories = {
            'Network Perimeter': [
                'Configure firewall rules to block unnecessary traffic',
                'Implement ingress and egress filtering',
                'Set up intrusion detection/prevention systems',
                'Enable DDoS protection services'
            ],
            'Rate Limiting': [
                'Configure connection rate limits',
                'Implement bandwidth throttling',
                'Set up request rate limiting',
                'Configure concurrent connection limits'
            ],
            'Protocol Security': [
                'Disable unnecessary network services',
                'Secure routing protocols',
                'Implement source address validation',
                'Configure protocol-specific protections'
            ],
            'Monitoring & Logging': [
                'Enable comprehensive network logging',
                'Set up real-time monitoring',
                'Configure automated alerting',
                'Implement traffic analysis tools'
            ]
        }
        
        # Category selection and progress tracking
        for category, items in hardening_categories.items():
            with st.expander(f"🛡️ {category}"):
                completed_items = 0
                
                for i, item in enumerate(items):
                    if st.checkbox(item, key=f"hardening_{category}_{i}"):
                        completed_items += 1
                
                progress = completed_items / len(items)
                st.progress(progress, f"Progress: {completed_items}/{len(items)} items completed")
        
        # Overall hardening score
        total_items = sum(len(items) for items in hardening_categories.values())
        completed_total = sum([
            1 for category, items in hardening_categories.items()
            for i in range(len(items))
            if st.session_state.get(f"hardening_{category}_{i}", False)
        ])
        
        overall_progress = completed_total / total_items
        
        st.markdown("---")
        st.subheader("Overall Hardening Status")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Hardening Progress", f"{completed_total}/{total_items}")
            st.progress(overall_progress, f"{overall_progress*100:.1f}% Complete")
        
        with col2:
            if overall_progress >= 0.8:
                st.success("🛡️ Excellent hardening level!")
            elif overall_progress >= 0.6:
                st.warning("⚠️ Good progress, continue hardening")
            else:
                st.error("❌ More hardening needed")
    
    def _render_monitoring_guide(self):
        st.markdown("### 📊 Monitoring Implementation Guide")
        
        # Monitoring setup wizard
        st.markdown("**Step-by-Step Monitoring Setup**")
        
        # Monitoring requirements assessment
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Infrastructure Assessment**")
            
            network_size = st.selectbox(
                "Network Size",
                ["Small (< 100 devices)", "Medium (100-1000 devices)", "Large (1000+ devices)"]
            )
            
            traffic_volume = st.selectbox(
                "Daily Traffic Volume",
                ["Low (< 1GB)", "Medium (1-10GB)", "High (10-100GB)", "Very High (> 100GB)"]
            )
            
            criticality = st.selectbox(
                "Service Criticality",
                ["Low", "Medium", "High", "Critical"]
            )
        
        with col2:
            st.markdown("**Monitoring Recommendations**")
            
            # Generate recommendations based on selections
            recommendations = self._generate_monitoring_recommendations(network_size, traffic_volume, criticality)
            
            for rec in recommendations:
                st.write(f"• {rec}")
        
        # Monitoring checklist
        st.markdown("---")
        st.markdown("**Monitoring Implementation Checklist**")
        
        monitoring_tasks = [
            "Install network monitoring software",
            "Configure SNMP monitoring for devices",
            "Set up traffic flow analysis",
            "Implement log collection and analysis",
            "Configure real-time alerting",
            "Create monitoring dashboards",
            "Test alert mechanisms",
            "Document monitoring procedures"
        ]
        
        completed_tasks = 0
        for i, task in enumerate(monitoring_tasks):
            if st.checkbox(task, key=f"monitoring_task_{i}"):
                completed_tasks += 1
        
        progress = completed_tasks / len(monitoring_tasks)
        st.progress(progress, f"Monitoring Setup: {completed_tasks}/{len(monitoring_tasks)} tasks completed")
    
    def _render_knowledge_assessment(self):
        st.subheader("🧠 Knowledge Assessment")
        
        assessment_type = st.selectbox(
            "Select Assessment Type",
            ["Quick Quiz", "Comprehensive Test", "Scenario Analysis", "Practical Challenge"]
        )
        
        if assessment_type == "Quick Quiz":
            self._render_quick_quiz()
        elif assessment_type == "Comprehensive Test":
            self._render_comprehensive_test()
        elif assessment_type == "Scenario Analysis":
            self._render_scenario_analysis()
        elif assessment_type == "Practical Challenge":
            self._render_practical_challenge()
    
    def _render_quick_quiz(self):
        st.markdown("### ⚡ Quick Knowledge Quiz")
        
        if 'quiz_started' not in st.session_state:
            st.session_state.quiz_started = False
            st.session_state.quiz_answers = {}
            st.session_state.current_question = 0
        
        if not st.session_state.quiz_started:
            st.write("Test your knowledge of DoS attacks and defenses with this quick quiz.")
            if st.button("Start Quiz"):
                st.session_state.quiz_started = True
                st.rerun()
            return
        
        # Quiz questions
        questions = self.quiz_questions['quick_quiz']
        current_q = st.session_state.current_question
        
        if current_q < len(questions):
            question = questions[current_q]
            
            st.markdown(f"**Question {current_q + 1} of {len(questions)}**")
            st.write(question['question'])
            
            answer = st.radio(
                "Select your answer:",
                question['options'],
                key=f"quiz_q_{current_q}"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Previous", disabled=current_q == 0):
                    st.session_state.current_question -= 1
                    st.rerun()
            
            with col2:
                if st.button("Next" if current_q < len(questions) - 1 else "Finish"):
                    st.session_state.quiz_answers[current_q] = answer
                    if current_q < len(questions) - 1:
                        st.session_state.current_question += 1
                    else:
                        st.session_state.current_question += 1  # Move to results
                    st.rerun()
        
        else:
            # Show results
            self._show_quiz_results(questions, st.session_state.quiz_answers)
    
    def _show_quiz_results(self, questions, answers):
        st.markdown("### 📊 Quiz Results")
        
        correct_answers = 0
        total_questions = len(questions)
        
        for i, question in enumerate(questions):
            user_answer = answers.get(i, "")
            correct = user_answer == question['correct_answer']
            
            if correct:
                correct_answers += 1
            
            with st.expander(f"Question {i+1} - {'✅' if correct else '❌'}"):
                st.write(f"**Question**: {question['question']}")
                st.write(f"**Your Answer**: {user_answer}")
                st.write(f"**Correct Answer**: {question['correct_answer']}")
                st.write(f"**Explanation**: {question['explanation']}")
        
        # Overall score
        score_percentage = (correct_answers / total_questions) * 100
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Score", f"{correct_answers}/{total_questions}")
        
        with col2:
            st.metric("Percentage", f"{score_percentage:.1f}%")
        
        with col3:
            if score_percentage >= 80:
                grade = "Excellent"
                color = "green"
            elif score_percentage >= 70:
                grade = "Good"
                color = "blue"
            elif score_percentage >= 60:
                grade = "Fair"
                color = "orange"
            else:
                grade = "Needs Improvement"
                color = "red"
            
            st.markdown(f"**Grade**: :{color}[{grade}]")
        
        # Restart option
        if st.button("Retake Quiz"):
            st.session_state.quiz_started = False
            st.session_state.quiz_answers = {}
            st.session_state.current_question = 0
            st.rerun()
    
    def _render_scenario_analysis(self):
        st.markdown("### 🎭 Scenario Analysis")
        
        scenarios = [
            {
                'title': 'E-commerce Site Under Attack',
                'description': 'Your e-commerce website is experiencing a sudden 10x increase in traffic during Black Friday sales.',
                'context': 'Peak shopping day, high legitimate traffic expected, revenue critical',
                'indicators': ['Response time degradation', 'Database connection timeouts', 'Payment processing failures'],
                'questions': [
                    'How would you differentiate between legitimate shopping traffic and a DoS attack?',
                    'What immediate actions would you take to maintain service availability?',
                    'How would you communicate with customers during the incident?'
                ]
            },
            {
                'title': 'Financial Services DDoS',
                'description': 'A banking application is under a sophisticated DDoS attack affecting online banking services.',
                'context': 'Critical financial services, regulatory compliance required, customer trust at stake',
                'indicators': ['Login failures', 'Transaction timeouts', 'Mobile app connectivity issues'],
                'questions': [
                    'What are your priorities for service restoration?',
                    'How would you handle regulatory reporting requirements?',
                    'What communication strategy would you implement?'
                ]
            }
        ]
        
        selected_scenario = st.selectbox("Select Scenario", [s['title'] for s in scenarios])
        
        scenario = next(s for s in scenarios if s['title'] == selected_scenario)
        
        st.markdown(f"### {scenario['title']}")
        st.write(scenario['description'])
        
        st.markdown("**Context**")
        st.write(scenario['context'])
        
        st.markdown("**Observed Indicators**")
        for indicator in scenario['indicators']:
            st.write(f"• {indicator}")
        
        st.markdown("**Analysis Questions**")
        for i, question in enumerate(scenario['questions']):
            with st.expander(f"Question {i+1}"):
                st.write(question)
                response = st.text_area(
                    "Your response:",
                    key=f"scenario_{selected_scenario}_{i}",
                    height=100
                )
                
                if response and st.button(f"Get Feedback", key=f"feedback_{selected_scenario}_{i}"):
                    feedback = self._generate_scenario_feedback(question, response)
                    st.info(f"💡 **Feedback**: {feedback}")
    
    def _render_practical_exercises(self):
        st.subheader("🛠️ Practical Exercises")
        
        exercise_names = list(self.practical_exercises.keys())
        selected_exercise = st.selectbox("Select Exercise", exercise_names)
        
        if selected_exercise:
            exercise = self.practical_exercises[selected_exercise]
            
            st.markdown(f"### {exercise['title']}")
            st.write(exercise['description'])
            
            st.markdown("**Learning Objectives**")
            for objective in exercise['objectives']:
                st.write(f"• {objective}")
            
            st.markdown("**Exercise Steps**")
            for i, step in enumerate(exercise['steps']):
                with st.expander(f"Step {i+1}: {step['title']}"):
                    st.write(step['instruction'])
                    
                    if 'code' in step:
                        st.code(step['code'], language=step.get('language', 'text'))
                    
                    completed = st.checkbox(f"Mark step {i+1} complete", key=f"exercise_{selected_exercise}_step_{i}")
            
            # Exercise completion
            total_steps = len(exercise['steps'])
            completed_steps = sum([
                1 for i in range(total_steps)
                if st.session_state.get(f"exercise_{selected_exercise}_step_{i}", False)
            ])
            
            progress = completed_steps / total_steps
            st.progress(progress, f"Exercise Progress: {completed_steps}/{total_steps} steps completed")
            
            if progress == 1.0:
                st.success("🎉 Exercise completed! Well done!")
    
    def _render_reference_materials(self):
        st.subheader("📚 Reference Materials")
        
        reference_tabs = st.tabs(["Standards & Frameworks", "Best Practices", "Tools & Resources", "Glossary"])
        
        with reference_tabs[0]:
            st.markdown("### 📋 Standards & Frameworks")
            
            standards = {
                'NIST Cybersecurity Framework': {
                    'description': 'Framework for improving critical infrastructure cybersecurity',
                    'relevance': 'Identify, Protect, Detect, Respond, Recover phases for DoS incidents',
                    'link': 'https://www.nist.gov/cyberframework'
                },
                'ISO 27001': {
                    'description': 'Information security management systems standard',
                    'relevance': 'Risk management and security controls for DoS protection',
                    'link': 'https://www.iso.org/isoiec-27001-information-security.html'
                },
                'OWASP Security Guidelines': {
                    'description': 'Open Web Application Security Project guidelines',
                    'relevance': 'Application-layer DoS protection and mitigation techniques',
                    'link': 'https://owasp.org/'
                }
            }
            
            for standard, info in standards.items():
                with st.expander(standard):
                    st.write(f"**Description**: {info['description']}")
                    st.write(f"**DoS Relevance**: {info['relevance']}")
                    st.write(f"**Reference**: {info['link']}")
        
        with reference_tabs[1]:
            st.markdown("### ✅ Best Practices")
            
            best_practices = {
                'Prevention': [
                    'Implement network segmentation and access controls',
                    'Use rate limiting and traffic shaping',
                    'Deploy DDoS protection services',
                    'Regular security assessments and penetration testing'
                ],
                'Detection': [
                    'Establish baseline traffic patterns',
                    'Implement real-time monitoring and alerting',
                    'Use behavioral analysis and anomaly detection',
                    'Deploy intrusion detection/prevention systems'
                ],
                'Response': [
                    'Develop and test incident response procedures',
                    'Maintain communication plans and contact lists',
                    'Practice regular incident response drills',
                    'Document all incidents for lessons learned'
                ],
                'Recovery': [
                    'Implement robust backup and recovery procedures',
                    'Test disaster recovery plans regularly',
                    'Maintain business continuity plans',
                    'Conduct post-incident reviews and improvements'
                ]
            }
            
            for category, practices in best_practices.items():
                st.markdown(f"**{category}**")
                for practice in practices:
                    st.write(f"• {practice}")
                st.markdown("---")
        
        with reference_tabs[2]:
            st.markdown("### 🛠️ Tools & Resources")
            
            tools = {
                'Open Source': [
                    'Wireshark - Network protocol analyzer',
                    'Nagios - Network monitoring',
                    'Suricata - Network IDS/IPS',
                    'pfSense - Firewall and router'
                ],
                'Commercial': [
                    'Cloudflare - DDoS protection service',
                    'Arbor Networks - DDoS protection',
                    'F5 - Application delivery controllers',
                    'Radware - DDoS protection solutions'
                ],
                'Cloud Services': [
                    'AWS Shield - DDoS protection',
                    'Azure DDoS Protection - Microsoft cloud protection',
                    'Google Cloud Armor - Google cloud security',
                    'Cloudflare - Global DDoS protection'
                ]
            }
            
            for category, tool_list in tools.items():
                st.markdown(f"**{category} Tools**")
                for tool in tool_list:
                    st.write(f"• {tool}")
                st.markdown("---")
        
        with reference_tabs[3]:
            st.markdown("### 📖 Glossary")
            
            glossary_terms = {
                'DDoS': 'Distributed Denial of Service - attack using multiple compromised systems',
                'Botnet': 'Network of compromised computers controlled remotely',
                'Amplification': 'Attack technique that leverages servers to multiply attack traffic',
                'Rate Limiting': 'Controlling the rate of requests to prevent overload',
                'SYN Flood': 'Attack that exploits TCP handshake process',
                'Volumetric Attack': 'Attack designed to consume bandwidth or system resources',
                'Protocol Attack': 'Attack that exploits weaknesses in network protocols',
                'Application Layer Attack': 'Attack targeting specific applications or services'
            }
            
            for term, definition in glossary_terms.items():
                with st.expander(term):
                    st.write(definition)
    
    def _get_learning_modules(self):
        """Define learning modules structure"""
        return {
            'DoS Fundamentals': {
                'description': 'Introduction to Denial of Service attacks',
                'duration': '2 hours',
                'sections': {
                    'What are DoS Attacks?': {
                        'type': 'text',
                        'objectives': [
                            'Understand the definition and purpose of DoS attacks',
                            'Distinguish between DoS and DDoS attacks',
                            'Identify common attack motivations'
                        ],
                        'content': """
                        **Denial of Service (DoS) Attacks Overview**
                        
                        A Denial of Service attack is a malicious attempt to disrupt the normal traffic of a targeted server, 
                        service, or network by overwhelming the target or its surrounding infrastructure with a flood of Internet traffic.
                        
                        **Key Characteristics:**
                        - Designed to make services unavailable to legitimate users
                        - Can target network bandwidth, system resources, or application logic
                        - Range from simple to highly sophisticated attacks
                        
                        **DoS vs DDoS:**
                        - **DoS**: Attack from a single source
                        - **DDoS**: Distributed attack from multiple sources (more common and effective)
                        
                        **Common Motivations:**
                        - Financial gain (extortion, competitive advantage)
                        - Political activism (hacktivism)
                        - Personal grievances
                        - Testing and research (educational/defensive)
                        """,
                        'key_concepts': {
                            'Availability': 'One of the CIA triad - ensuring services remain accessible to authorized users',
                            'Traffic Flood': 'Overwhelming a target with more requests than it can handle',
                            'Resource Exhaustion': 'Consuming system resources like CPU, memory, or network connections'
                        },
                        'practice_questions': [
                            {
                                'question': 'What is the main goal of a DoS attack?',
                                'options': ['Steal data', 'Make services unavailable', 'Gain system access', 'Install malware'],
                                'correct_answer': 'Make services unavailable',
                                'explanation': 'DoS attacks specifically aim to deny service availability to legitimate users.'
                            }
                        ]
                    },
                    'Attack Categories': {
                        'type': 'visualization',
                        'objectives': [
                            'Classify different types of DoS attacks',
                            'Understand attack vector characteristics',
                            'Identify appropriate defenses for each category'
                        ],
                        'content': {
                            'chart_type': 'attack_taxonomy'
                        }
                    },
                    'Defense Strategies': {
                        'type': 'visualization',
                        'objectives': [
                            'Learn defense-in-depth approaches',
                            'Understand layered security models',
                            'Evaluate defense effectiveness'
                        ],
                        'content': {
                            'chart_type': 'defense_layers'
                        }
                    }
                }
            },
            'Attack Vectors': {
                'description': 'Detailed study of DoS attack methodologies',
                'duration': '3 hours',
                'sections': {
                    'Volumetric Attacks': {
                        'type': 'text',
                        'content': """
                        **Volumetric Attacks Overview**
                        
                        Volumetric attacks aim to overwhelm the target's bandwidth or consume network resources.
                        These attacks focus on generating high volumes of traffic to saturate network links.
                        
                        **Common Types:**
                        - UDP Floods
                        - ICMP Floods  
                        - Amplification attacks (DNS, NTP, Memcached)
                        
                        **Characteristics:**
                        - High bandwidth consumption
                        - Network infrastructure targeting
                        - Measurable in bits per second (bps)
                        """,
                        'key_concepts': {
                            'Bandwidth Saturation': 'Filling network pipes with malicious traffic',
                            'Amplification Factor': 'Ratio of response size to request size in reflection attacks'
                        }
                    }
                }
            }
        }
    
    def _get_quiz_questions(self):
        """Define quiz questions for assessments"""
        return {
            'quick_quiz': [
                {
                    'question': 'Which type of DoS attack uses multiple compromised systems?',
                    'options': ['DoS', 'DDoS', 'UDP Flood', 'SYN Flood'],
                    'correct_answer': 'DDoS',
                    'explanation': 'DDoS (Distributed Denial of Service) attacks use multiple compromised systems to attack a target.'
                },
                {
                    'question': 'What is the primary goal of rate limiting as a defense mechanism?',
                    'options': ['Block all traffic', 'Control request frequency', 'Encrypt traffic', 'Monitor logs'],
                    'correct_answer': 'Control request frequency',
                    'explanation': 'Rate limiting controls the frequency of requests to prevent system overload.'
                },
                {
                    'question': 'Which attack vector targets the TCP handshake process?',
                    'options': ['UDP Flood', 'SYN Flood', 'HTTP Flood', 'ICMP Flood'],
                    'correct_answer': 'SYN Flood',
                    'explanation': 'SYN Flood attacks exploit the TCP three-way handshake by sending many SYN requests without completing the handshake.'
                }
            ]
        }
    
    def _get_practical_exercises(self):
        """Define practical exercises"""
        return {
            'Traffic Analysis': {
                'title': 'Network Traffic Analysis Exercise',
                'description': 'Learn to identify DoS attack patterns in network traffic',
                'objectives': [
                    'Analyze network traffic patterns',
                    'Identify anomalous behavior',
                    'Calculate baseline metrics'
                ],
                'steps': [
                    {
                        'title': 'Establish Baseline',
                        'instruction': 'Calculate normal traffic baseline from sample data',
                        'code': '''
# Sample traffic analysis
import pandas as pd
import numpy as np

# Load traffic data
traffic_data = pd.read_csv('traffic_sample.csv')

# Calculate baseline metrics
baseline_rps = traffic_data['requests_per_second'].mean()
baseline_std = traffic_data['requests_per_second'].std()

print(f"Baseline RPS: {baseline_rps:.2f}")
print(f"Standard Deviation: {baseline_std:.2f}")
print(f"Upper threshold: {baseline_rps + 3*baseline_std:.2f}")
                        ''',
                        'language': 'python'
                    },
                    {
                        'title': 'Anomaly Detection',
                        'instruction': 'Implement simple anomaly detection algorithm'
                    }
                ]
            }
        }
    
    def _generate_monitoring_recommendations(self, network_size, traffic_volume, criticality):
        """Generate monitoring recommendations based on requirements"""
        recommendations = []
        
        if "Large" in network_size:
            recommendations.append("Deploy distributed monitoring infrastructure")
            recommendations.append("Implement centralized log aggregation")
        
        if "High" in traffic_volume or "Very High" in traffic_volume:
            recommendations.append("Use high-performance monitoring tools")
            recommendations.append("Implement traffic sampling for analysis")
        
        if criticality in ["High", "Critical"]:
            recommendations.append("Set up 24/7 monitoring with immediate alerting")
            recommendations.append("Implement redundant monitoring systems")
        
        return recommendations
    
    def _generate_scenario_feedback(self, question, response):
        """Generate feedback for scenario analysis responses"""
        feedback_templates = {
            'differentiate': 'Consider analyzing traffic patterns, source IP distributions, and user behavior patterns to distinguish legitimate from malicious traffic.',
            'immediate actions': 'Focus on preserving critical functionality, implementing traffic controls, and activating incident response procedures.',
            'communication': 'Develop clear, honest communication that maintains customer confidence while providing necessary information.'
        }
        
        # Simple keyword matching for feedback
        for key, feedback in feedback_templates.items():
            if key in question.lower():
                return feedback
        
        return 'Good analysis. Consider the technical, business, and communication aspects of your response.'
    
    def _generate_section_notes(self, module_name, section_name, section_data):
        """Generate downloadable section notes"""
        notes = f"""
{module_name.upper()} - {section_name.upper()}
{'='*50}

LEARNING OBJECTIVES:
"""
        
        if 'objectives' in section_data:
            for obj in section_data['objectives']:
                notes += f"• {obj}\n"
        
        notes += f"""
CONTENT:
{'-'*20}
"""
        
        if isinstance(section_data.get('content'), str):
            notes += section_data['content']
        
        if 'key_concepts' in section_data:
            notes += f"""

KEY CONCEPTS:
{'-'*20}
"""
            for concept, definition in section_data['key_concepts'].items():
                notes += f"{concept}: {definition}\n"
        
        notes += f"""

Generated by DoS Attack Analysis & Education Platform
Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return notes
