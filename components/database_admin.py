"""
Database Administration Component
Provides interface for managing DoS attack data, case studies, and educational content
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from database.data_manager import DatabaseManager
import json

class DatabaseAdmin:
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    def render(self):
        """Render the database administration interface"""
        st.title("🗄️ Database Administration")
        st.markdown("---")
        
        # Database Statistics
        self._render_database_stats()
        
        # Management tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📚 Case Studies", 
            "🎯 Attack Vectors", 
            "📖 Educational Content",
            "📊 Data Analytics"
        ])
        
        with tab1:
            self._render_case_study_management()
        
        with tab2:
            self._render_attack_vector_management()
        
        with tab3:
            self._render_educational_content_management()
        
        with tab4:
            self._render_data_analytics()
    
    def _render_database_stats(self):
        """Display database statistics"""
        st.subheader("📊 Database Overview")
        
        stats = self.db_manager.get_statistics()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Case Studies", stats['total_case_studies'])
        with col2:
            st.metric("Attack Vectors", stats['total_attack_vectors'])
        with col3:
            st.metric("Educational Content", stats['total_educational_content'])
        with col4:
            st.metric("User Sessions", stats['total_user_sessions'])
        
        st.markdown("---")
    
    def _render_case_study_management(self):
        """Manage case studies"""
        st.subheader("📚 Case Study Management")
        
        # Add new case study
        with st.expander("➕ Add New Case Study", expanded=False):
            self._render_add_case_study_form()
        
        # View existing case studies
        st.subheader("Existing Case Studies")
        case_studies = self.db_manager.get_all_case_studies()
        
        if case_studies:
            for case in case_studies:
                with st.expander(f"{case.name} ({case.target})", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Date:** {case.date.strftime('%Y-%m-%d')}")
                        st.write(f"**Attack Type:** {case.attack_type}")
                        st.write(f"**Peak Traffic:** {case.peak_traffic}")
                        st.write(f"**Duration:** {case.duration}")
                    
                    with col2:
                        st.write(f"**Attack Vectors:** {', '.join(case.attack_vectors)}")
                        st.write(f"**Business Impact:** {case.impact.get('business_impact', 'N/A')}")
                    
                    # JSON display for detailed data
                    if st.button(f"View Details - {case.id}", key=f"details_{case.id}"):
                        st.json({
                            'impact': case.impact,
                            'mitigation': case.mitigation,
                            'lessons_learned': case.lessons_learned,
                            'technical_details': case.technical_details
                        })
        else:
            st.info("No case studies found in database.")
    
    def _render_add_case_study_form(self):
        """Form to add new case study"""
        with st.form("add_case_study"):
            col1, col2 = st.columns(2)
            
            with col1:
                case_id = st.text_input("Case ID", placeholder="case_005")
                name = st.text_input("Attack Name", placeholder="Company DDoS Attack (2024)")
                target = st.text_input("Target Organization", placeholder="Company Name")
                attack_type = st.text_input("Attack Type", placeholder="DDoS, Amplification, etc.")
            
            with col2:
                attack_date = st.date_input("Attack Date", value=date.today())
                peak_traffic = st.text_input("Peak Traffic", placeholder="1.5 Tbps")
                duration = st.text_input("Duration", placeholder="15 minutes")
                attack_vectors = st.text_area("Attack Vectors (one per line)", placeholder="UDP Amplification\nHTTP Flood")
            
            # Impact details
            st.subheader("Impact Details")
            impact_col1, impact_col2 = st.columns(2)
            
            with impact_col1:
                service_disruption = st.text_input("Service Disruption", placeholder="Complete outage")
                affected_users = st.text_input("Affected Users", placeholder="Global user base")
            
            with impact_col2:
                impact_duration = st.text_input("Impact Duration", placeholder="15 minutes")
                business_impact = st.text_input("Business Impact", placeholder="Service unavailability")
            
            # Mitigation details
            st.subheader("Mitigation Strategies")
            mitigation_col1, mitigation_col2 = st.columns(2)
            
            with mitigation_col1:
                immediate_mitigation = st.text_area("Immediate Response", placeholder="Traffic filtering and rate limiting")
            
            with mitigation_col2:
                long_term_mitigation = st.text_area("Long-term Measures", placeholder="Enhanced DDoS protection")
            
            # Lessons learned
            lessons = st.text_area("Lessons Learned (one per line)", placeholder="Lesson 1\nLesson 2")
            
            # Technical details
            st.subheader("Technical Details")
            tech_col1, tech_col2 = st.columns(2)
            
            with tech_col1:
                amplification_factor = st.text_input("Amplification Factor", placeholder="51,000x")
                attack_method = st.text_input("Attack Method", placeholder="UDP reflection with amplification")
            
            with tech_col2:
                source_info = st.text_input("Source Information", placeholder="~50,000 compromised servers")
                additional_tech = st.text_area("Additional Technical Details", placeholder="Other technical information")
            
            submitted = st.form_submit_button("Add Case Study")
            
            if submitted and case_id and name and target:
                # Prepare case study data
                case_data = {
                    'id': case_id,
                    'name': name,
                    'date': datetime.combine(attack_date, datetime.min.time()),
                    'target': target,
                    'attack_type': attack_type,
                    'peak_traffic': peak_traffic,
                    'duration': duration,
                    'attack_vectors': [v.strip() for v in attack_vectors.split('\n') if v.strip()],
                    'impact': {
                        'service_disruption': service_disruption,
                        'duration': impact_duration,
                        'affected_users': affected_users,
                        'business_impact': business_impact
                    },
                    'mitigation': {
                        'immediate': immediate_mitigation,
                        'long_term': long_term_mitigation
                    },
                    'lessons_learned': [l.strip() for l in lessons.split('\n') if l.strip()],
                    'technical_details': {
                        'amplification_factor': amplification_factor,
                        'attack_method': attack_method,
                        'source_info': source_info,
                        'additional_details': additional_tech
                    }
                }
                
                try:
                    self.db_manager.add_case_study(case_data)
                    st.success(f"Case study '{name}' added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error adding case study: {str(e)}")
    
    def _render_attack_vector_management(self):
        """Manage attack vectors"""
        st.subheader("🎯 Attack Vector Management")
        
        # Add new attack vector
        with st.expander("➕ Add New Attack Vector", expanded=False):
            self._render_add_attack_vector_form()
        
        # View existing vectors
        st.subheader("Existing Attack Vectors")
        vectors = self.db_manager.get_all_attack_vectors()
        
        if vectors:
            # Group by category
            categories = {}
            for vector in vectors:
                if vector.category not in categories:
                    categories[vector.category] = []
                categories[vector.category].append(vector)
            
            for category, category_vectors in categories.items():
                st.subheader(f"{category} Attacks")
                for vector in category_vectors:
                    with st.expander(f"{vector.name}", expanded=False):
                        st.write(f"**Description:** {vector.description}")
                        st.write(f"**Difficulty:** {vector.difficulty_level}")
                        st.write(f"**Impact Potential:** {vector.impact_potential}")
                        
                        if vector.technical_details:
                            st.write("**Technical Details:**")
                            st.json(vector.technical_details)
                        
                        if vector.mitigation_strategies:
                            st.write("**Mitigation Strategies:**")
                            for strategy in vector.mitigation_strategies:
                                st.write(f"• {strategy}")
        else:
            st.info("No attack vectors found in database.")
    
    def _render_add_attack_vector_form(self):
        """Form to add new attack vector"""
        with st.form("add_attack_vector"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Vector Name", placeholder="New Attack Vector")
                category = st.selectbox("Category", ["Volumetric", "Protocol", "Application"])
                difficulty = st.selectbox("Difficulty Level", ["Low", "Medium", "High"])
            
            with col2:
                impact = st.selectbox("Impact Potential", ["Low", "Medium", "High", "Very High"])
                description = st.text_area("Description", placeholder="Detailed description of the attack vector")
            
            # Technical details
            st.subheader("Technical Details")
            tech_details = st.text_area("Technical Details (JSON format)", 
                                       placeholder='{"method": "example", "requirements": ["item1", "item2"]}')
            
            # Mitigation strategies
            mitigation = st.text_area("Mitigation Strategies (one per line)", 
                                     placeholder="Strategy 1\nStrategy 2")
            
            # Detection methods
            detection = st.text_area("Detection Methods (one per line)", 
                                    placeholder="Method 1\nMethod 2")
            
            submitted = st.form_submit_button("Add Attack Vector")
            
            if submitted and name and category and description:
                # Parse technical details
                try:
                    tech_data = json.loads(tech_details) if tech_details else {}
                except json.JSONDecodeError:
                    tech_data = {"raw_input": tech_details}
                
                vector_data = {
                    'name': name,
                    'category': category,
                    'description': description,
                    'technical_details': tech_data,
                    'mitigation_strategies': [m.strip() for m in mitigation.split('\n') if m.strip()],
                    'difficulty_level': difficulty,
                    'impact_potential': impact,
                    'detection_methods': [d.strip() for d in detection.split('\n') if d.strip()]
                }
                
                try:
                    self.db_manager.add_attack_vector(vector_data)
                    st.success(f"Attack vector '{name}' added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error adding attack vector: {str(e)}")
    
    def _render_educational_content_management(self):
        """Manage educational content"""
        st.subheader("📖 Educational Content Management")
        
        # Add new educational content
        with st.expander("➕ Add New Educational Content", expanded=False):
            self._render_add_educational_content_form()
        
        # View existing content
        st.subheader("Existing Educational Content")
        content_list = self.db_manager.get_educational_content()
        
        if content_list:
            for content in content_list:
                with st.expander(f"{content.title} ({content.content_type})", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Type:** {content.content_type}")
                        st.write(f"**Category:** {content.category}")
                        st.write(f"**Difficulty:** {content.difficulty_level}")
                    
                    with col2:
                        st.write(f"**Duration:** {content.estimated_duration} minutes")
                        st.write(f"**Active:** {'Yes' if content.is_active else 'No'}")
                    
                    if content.learning_objectives:
                        st.write("**Learning Objectives:**")
                        for obj in content.learning_objectives:
                            st.write(f"• {obj}")
        else:
            st.info("No educational content found in database.")
    
    def _render_add_educational_content_form(self):
        """Form to add new educational content"""
        with st.form("add_educational_content"):
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("Content Title", placeholder="Introduction to DoS Attacks")
                content_type = st.selectbox("Content Type", ["module", "quiz", "exercise", "reference"])
                category = st.text_input("Category", placeholder="Fundamentals")
            
            with col2:
                difficulty = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"])
                duration = st.number_input("Estimated Duration (minutes)", min_value=1, value=30)
                is_active = st.checkbox("Active", value=True)
            
            # Learning objectives
            objectives = st.text_area("Learning Objectives (one per line)", 
                                     placeholder="Objective 1\nObjective 2")
            
            # Prerequisites
            prerequisites = st.text_area("Prerequisites (one per line)", 
                                        placeholder="Prerequisite 1\nPrerequisite 2")
            
            # Content data
            content_data = st.text_area("Content Data (JSON format)", 
                                       placeholder='{"sections": [], "questions": [], "exercises": []}')
            
            submitted = st.form_submit_button("Add Educational Content")
            
            if submitted and title and content_type:
                # Parse content data
                try:
                    content_json = json.loads(content_data) if content_data else {}
                except json.JSONDecodeError:
                    content_json = {"raw_content": content_data}
                
                content_data_dict = {
                    'title': title,
                    'content_type': content_type,
                    'category': category,
                    'content_data': content_json,
                    'difficulty_level': difficulty,
                    'estimated_duration': duration,
                    'prerequisites': [p.strip() for p in prerequisites.split('\n') if p.strip()],
                    'learning_objectives': [o.strip() for o in objectives.split('\n') if o.strip()],
                    'is_active': is_active
                }
                
                try:
                    self.db_manager.add_educational_content(content_data_dict)
                    st.success(f"Educational content '{title}' added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error adding educational content: {str(e)}")
    
    def _render_data_analytics(self):
        """Display data analytics and insights"""
        st.subheader("📊 Data Analytics")
        
        # Case study analytics
        case_studies = self.db_manager.get_all_case_studies()
        if case_studies:
            st.subheader("Case Study Analytics")
            
            # Create dataframe for analysis
            case_data = []
            for case in case_studies:
                case_data.append({
                    'name': case.name,
                    'target': case.target,
                    'attack_type': case.attack_type,
                    'date': case.date,
                    'peak_traffic': case.peak_traffic,
                    'duration': case.duration
                })
            
            df = pd.DataFrame(case_data)
            
            # Display analytics
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Attack Types Distribution:**")
                attack_type_counts = df['attack_type'].value_counts()
                st.bar_chart(attack_type_counts)
            
            with col2:
                st.write("**Timeline of Attacks:**")
                df['year'] = df['date'].dt.year
                yearly_counts = df['year'].value_counts().sort_index()
                st.line_chart(yearly_counts)
            
            # Data table
            st.subheader("Case Studies Overview")
            st.dataframe(df, use_container_width=True)
        
        # Attack vector analytics
        vectors = self.db_manager.get_all_attack_vectors()
        if vectors:
            st.subheader("Attack Vector Analytics")
            
            vector_data = []
            for vector in vectors:
                vector_data.append({
                    'name': vector.name,
                    'category': vector.category,
                    'difficulty': vector.difficulty_level,
                    'impact': vector.impact_potential
                })
            
            vector_df = pd.DataFrame(vector_data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Category Distribution:**")
                category_counts = vector_df['category'].value_counts()
                st.pie_chart(category_counts)
            
            with col2:
                st.write("**Difficulty vs Impact:**")
                pivot_table = vector_df.pivot_table(
                    values='name', 
                    index='difficulty', 
                    columns='impact', 
                    aggfunc='count',
                    fill_value=0
                )
                st.dataframe(pivot_table)