"""
Database Data Manager
Handles database operations for the DoS Attack Analysis Platform
"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from database.schema import (
    CaseStudy, AttackVector, MitigationStrategy, 
    EducationalContent, UserProgress, create_database_engine, init_database
)
from datetime import datetime
import json

class DatabaseManager:
    def __init__(self):
        self.engine = create_database_engine()
        init_database()  # Create tables if they don't exist
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        # Initialize with sample data if database is empty
        if self.session.query(CaseStudy).count() == 0:
            self._populate_initial_data()
    
    def _populate_initial_data(self):
        """Populate database with initial case studies and data"""
        
        # Add case studies
        case_studies = [
            {
                'id': 'case_001',
                'name': 'GitHub DDoS Attack (2018)',
                'date': datetime(2018, 2, 28),
                'target': 'GitHub',
                'attack_type': 'Memcached DDoS Amplification',
                'peak_traffic': '1.35 Tbps',
                'duration': '10 minutes',
                'attack_vectors': ['UDP Amplification', 'Memcached Reflection'],
                'impact': {
                    'service_disruption': 'Complete outage',
                    'duration': '10 minutes',
                    'affected_users': 'Global user base',
                    'business_impact': 'Service unavailability'
                },
                'mitigation': {
                    'immediate': 'Traffic filtering and rate limiting',
                    'long_term': 'Enhanced DDoS protection, CDN improvements'
                },
                'lessons_learned': [
                    'Memcached servers should not be exposed to internet',
                    'Amplification attacks can reach unprecedented scales',
                    'Quick mitigation response is critical'
                ],
                'technical_details': {
                    'amplification_factor': '51,000x',
                    'source_servers': '~50,000 memcached servers',
                    'attack_method': 'UDP reflection with amplification'
                }
            },
            {
                'id': 'case_002',
                'name': 'Dyn DNS Attack (2016)',
                'date': datetime(2016, 10, 21),
                'target': 'Dyn DNS Infrastructure',
                'attack_type': 'IoT Botnet DDoS',
                'peak_traffic': '1.2 Tbps',
                'duration': 'Multiple waves over 24 hours',
                'attack_vectors': ['Mirai Botnet', 'IoT Device Exploitation'],
                'impact': {
                    'service_disruption': 'Major internet outage',
                    'duration': 'Several hours across multiple waves',
                    'affected_users': 'Twitter, Netflix, Spotify, Reddit users',
                    'business_impact': 'Multi-million dollar losses across affected services'
                },
                'mitigation': {
                    'immediate': 'Traffic rerouting, additional capacity',
                    'long_term': 'IoT security improvements, DNS resilience'
                },
                'lessons_learned': [
                    'IoT devices are vulnerable attack vectors',
                    'DNS infrastructure is critical single point of failure',
                    'Distributed attacks can affect multiple major services'
                ],
                'technical_details': {
                    'botnet_size': '~100,000 compromised IoT devices',
                    'attack_method': 'Coordinated HTTP floods',
                    'target_infrastructure': 'DNS resolution services'
                }
            },
            {
                'id': 'case_003',
                'name': 'CloudFlare Attack (2020)',
                'date': datetime(2020, 6, 18),
                'target': 'CloudFlare Network',
                'attack_type': 'Multi-vector DDoS',
                'peak_traffic': '754 Mbps',
                'duration': '15 minutes',
                'attack_vectors': ['HTTP Flood', 'UDP Amplification'],
                'impact': {
                    'service_disruption': 'Partial service degradation',
                    'duration': '15 minutes',
                    'affected_users': 'CloudFlare customers globally',
                    'business_impact': 'Minimal due to effective mitigation'
                },
                'mitigation': {
                    'immediate': 'Automated DDoS protection activation',
                    'long_term': 'Enhanced detection algorithms'
                },
                'lessons_learned': [
                    'Automated response systems are crucial',
                    'Multi-vector attacks require comprehensive protection',
                    'Quick detection reduces impact significantly'
                ],
                'technical_details': {
                    'attack_vectors_count': '3 different vectors',
                    'mitigation_time': '<2 minutes',
                    'protection_system': 'CloudFlare DDoS Protection'
                }
            },
            {
                'id': 'case_004',
                'name': 'Amazon Web Services Attack (2023)',
                'date': datetime(2023, 8, 23),
                'target': 'AWS Infrastructure',
                'attack_type': 'CLDAP Reflection Attack',
                'peak_traffic': '2.3 Tbps',
                'duration': '2 days',
                'attack_vectors': ['CLDAP Amplification', 'UDP Reflection'],
                'impact': {
                    'service_disruption': 'Targeted service impact',
                    'duration': '2 days with varying intensity',
                    'affected_users': 'Specific AWS customers',
                    'business_impact': 'Limited due to AWS Shield protection'
                },
                'mitigation': {
                    'immediate': 'AWS Shield Advanced activation',
                    'long_term': 'Enhanced monitoring and filtering'
                },
                'lessons_learned': [
                    'Cloud infrastructure requires specialized protection',
                    'CLDAP amplification can reach massive scales',
                    'Proactive defense systems are essential'
                ],
                'technical_details': {
                    'amplification_factor': '56x to 70x',
                    'attack_duration': '3 days continuous',
                    'protection_system': 'AWS Shield Advanced'
                }
            }
        ]
        
        # Insert case studies
        for case_data in case_studies:
            case_study = CaseStudy(**case_data)
            self.session.add(case_study)
        
        # Add attack vectors
        attack_vectors = [
            {
                'name': 'UDP Amplification',
                'category': 'Volumetric',
                'description': 'Exploits UDP services to amplify attack traffic',
                'technical_details': {
                    'amplification_factor': 'Up to 51,000x',
                    'common_services': ['DNS', 'NTP', 'SSDP', 'Memcached'],
                    'attack_method': 'Spoofed source IP with UDP requests'
                },
                'mitigation_strategies': [
                    'Source IP validation',
                    'Rate limiting on UDP services',
                    'Disable unnecessary UDP services'
                ],
                'difficulty_level': 'Medium',
                'impact_potential': 'Very High',
                'detection_methods': ['Traffic volume monitoring', 'Source IP analysis']
            },
            {
                'name': 'SYN Flood',
                'category': 'Protocol',
                'description': 'Exploits TCP handshake process to exhaust server resources',
                'technical_details': {
                    'attack_method': 'Half-open TCP connections',
                    'target_resource': 'Server connection table',
                    'packet_type': 'TCP SYN packets'
                },
                'mitigation_strategies': [
                    'SYN cookies implementation',
                    'Connection rate limiting',
                    'Firewall syn-flood protection'
                ],
                'difficulty_level': 'Low',
                'impact_potential': 'High',
                'detection_methods': ['Connection state monitoring', 'SYN/ACK ratio analysis']
            }
        ]
        
        for vector_data in attack_vectors:
            attack_vector = AttackVector(**vector_data)
            self.session.add(attack_vector)
        
        # Commit all changes
        self.session.commit()
    
    # Case Study operations
    def get_all_case_studies(self):
        """Retrieve all case studies"""
        return self.session.query(CaseStudy).order_by(desc(CaseStudy.date)).all()
    
    def get_case_study_by_id(self, case_id):
        """Retrieve specific case study by ID"""
        return self.session.query(CaseStudy).filter(CaseStudy.id == case_id).first()
    
    def search_case_studies(self, search_term):
        """Search case studies by name, target, or attack type"""
        return self.session.query(CaseStudy).filter(
            CaseStudy.name.contains(search_term) |
            CaseStudy.target.contains(search_term) |
            CaseStudy.attack_type.contains(search_term)
        ).all()
    
    def add_case_study(self, case_data):
        """Add new case study"""
        case_study = CaseStudy(**case_data)
        self.session.add(case_study)
        self.session.commit()
        return case_study
    
    # Attack Vector operations
    def get_all_attack_vectors(self):
        """Retrieve all attack vectors"""
        return self.session.query(AttackVector).all()
    
    def get_attack_vectors_by_category(self, category):
        """Retrieve attack vectors by category"""
        return self.session.query(AttackVector).filter(AttackVector.category == category).all()
    
    def add_attack_vector(self, vector_data):
        """Add new attack vector"""
        attack_vector = AttackVector(**vector_data)
        self.session.add(attack_vector)
        self.session.commit()
        return attack_vector
    
    # Educational Content operations
    def get_educational_content(self, content_type=None):
        """Retrieve educational content, optionally filtered by type"""
        query = self.session.query(EducationalContent).filter(EducationalContent.is_active == True)
        if content_type:
            query = query.filter(EducationalContent.content_type == content_type)
        return query.all()
    
    def add_educational_content(self, content_data):
        """Add new educational content"""
        content = EducationalContent(**content_data)
        self.session.add(content)
        self.session.commit()
        return content
    
    # User Progress operations
    def save_user_progress(self, session_id, content_id, content_type, progress_data):
        """Save user progress for educational content"""
        progress = UserProgress(
            user_session=session_id,
            content_id=content_id,
            content_type=content_type,
            **progress_data
        )
        self.session.add(progress)
        self.session.commit()
        return progress
    
    def get_user_progress(self, session_id):
        """Retrieve user progress by session ID"""
        return self.session.query(UserProgress).filter(
            UserProgress.user_session == session_id
        ).all()
    
    # Utility methods
    def close(self):
        """Close database session"""
        self.session.close()
    
    def get_statistics(self):
        """Get database statistics"""
        return {
            'total_case_studies': self.session.query(CaseStudy).count(),
            'total_attack_vectors': self.session.query(AttackVector).count(),
            'total_educational_content': self.session.query(EducationalContent).count(),
            'total_user_sessions': self.session.query(UserProgress.user_session).distinct().count()
        }