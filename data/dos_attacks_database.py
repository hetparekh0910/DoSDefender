"""
DoS Attacks Database - Educational case studies and attack data
This module provides database connectivity and data access for the DoS Analysis Platform
"""

import pandas as pd
from datetime import datetime, timedelta
import random
from database.data_manager import DatabaseManager

class DoSAttackDatabase:
    def __init__(self):
        self.db_manager = DatabaseManager()
        # Legacy support - convert database data to original format
        self.case_studies = self._load_case_studies_from_db()
        self.attack_vectors = self._load_attack_vectors_from_db()
        self.mitigation_strategies = self._load_mitigation_strategies()
    
    def _load_case_studies_from_db(self):
        """Load case studies from database"""
        db_case_studies = self.db_manager.get_all_case_studies()
        case_studies = []
        
        for case in db_case_studies:
            case_dict = {
                'id': case.id,
                'name': case.name,
                'date': case.date.strftime('%Y-%m-%d'),
                'target': case.target,
                'attack_type': case.attack_type,
                'peak_traffic': case.peak_traffic,
                'duration': case.duration,
                'attack_vectors': case.attack_vectors,
                'impact': case.impact,
                'mitigation': case.mitigation,
                'lessons_learned': case.lessons_learned,
                'technical_details': case.technical_details
            }
            case_studies.append(case_dict)
        
        return case_studies
    
    def _load_case_studies_legacy(self):
        """Legacy method - kept for fallback"""
        return [
            {
                'id': 'case_001',
                'name': 'GitHub DDoS Attack (2018)',
                'date': '2018-02-28',
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
                'date': '2016-10-21',
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
                'date': '2020-06-18',
                'target': 'CloudFlare Network',
                'attack_type': 'Multi-vector DDoS',
                'peak_traffic': '754 Mbps',
                'duration': '15 minutes',
                'attack_vectors': ['SYN Flood', 'UDP Flood', 'HTTP Flood'],
                'impact': {
                    'service_disruption': 'Partial service degradation',
                    'duration': '15 minutes',
                    'affected_users': 'CloudFlare customers globally',
                    'business_impact': 'Minimal due to quick mitigation'
                },
                'mitigation': {
                    'immediate': 'Automated DDoS protection activation',
                    'long_term': 'Enhanced detection algorithms'
                },
                'lessons_learned': [
                    'Multi-vector attacks require comprehensive defense',
                    'Automated response systems are crucial',
                    'Quick detection and response minimize impact'
                ],
                'technical_details': {
                    'attack_sources': 'Global botnet',
                    'attack_method': 'Coordinated multi-protocol assault',
                    'defense_mechanism': 'AI-powered traffic analysis'
                }
            },
            {
                'id': 'case_004',
                'name': 'Amazon Web Services Attack (2023)',
                'date': '2020-09-28',
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
                    'CLDAP servers pose amplification risks',
                    'Extended attacks require sustained defense',
                    'Cloud provider protection is essential'
                ],
                'technical_details': {
                    'amplification_factor': '56-70x',
                    'source_servers': 'Misconfigured CLDAP servers',
                    'attack_method': 'Connectionless LDAP reflection'
                }
            }
        ]
    
    def _load_attack_vectors_from_db(self):
        """Load attack vectors from database"""
        db_vectors = self.db_manager.get_all_attack_vectors()
        
        # If no vectors in database, return legacy format
        if not db_vectors:
            return self._load_attack_vectors_legacy()
        
        # Convert database format to legacy format for compatibility
        attack_vectors = {}
        for vector in db_vectors:
            category = vector.category.lower()
            if category not in attack_vectors:
                attack_vectors[category] = {
                    'name': f'{vector.category} Attacks',
                    'description': f'Attacks that fall under the {vector.category.lower()} category',
                    'subcategories': []
                }
            
            subcategory = {
                'name': vector.name,
                'description': vector.description,
                'characteristics': vector.technical_details.get('characteristics', []) if vector.technical_details else [],
                'mitigation': vector.mitigation_strategies if vector.mitigation_strategies else []
            }
            attack_vectors[category]['subcategories'].append(subcategory)
        
        return attack_vectors
    
    def _load_attack_vectors_legacy(self):
        """Load detailed attack vector information"""
        return {
            'volumetric': {
                'name': 'Volumetric Attacks',
                'description': 'Overwhelm network bandwidth or consume network resources',
                'subcategories': [
                    {
                        'name': 'UDP Flood',
                        'description': 'Send large volumes of UDP packets to random ports',
                        'characteristics': ['High packet rate', 'Random destination ports', 'Difficult to filter'],
                        'mitigation': ['Rate limiting', 'UDP traffic filtering', 'Ingress filtering']
                    },
                    {
                        'name': 'ICMP Flood',
                        'description': 'Overwhelm target with ICMP Echo Request packets',
                        'characteristics': ['High ICMP traffic', 'Network congestion', 'Bandwidth exhaustion'],
                        'mitigation': ['ICMP rate limiting', 'ICMP filtering', 'Traffic shaping']
                    },
                    {
                        'name': 'Amplification Attacks',
                        'description': 'Use third-party servers to amplify attack traffic',
                        'characteristics': ['Spoofed source IPs', 'High amplification ratios', 'Legitimate servers as reflectors'],
                        'mitigation': ['BCP38 implementation', 'Server hardening', 'Response rate limiting']
                    }
                ]
            },
            'protocol': {
                'name': 'Protocol Attacks',
                'description': 'Exploit weaknesses in network protocols',
                'subcategories': [
                    {
                        'name': 'SYN Flood',
                        'description': 'Exhaust server resources by initiating many TCP connections',
                        'characteristics': ['Half-open connections', 'Resource exhaustion', 'Connection table overflow'],
                        'mitigation': ['SYN cookies', 'Connection rate limiting', 'Firewall protection']
                    },
                    {
                        'name': 'Ping of Death',
                        'description': 'Send malformed or oversized packets to crash systems',
                        'characteristics': ['Oversized packets', 'Protocol violations', 'System crashes'],
                        'mitigation': ['Packet size validation', 'Protocol compliance checking', 'System updates']
                    },
                    {
                        'name': 'Smurf Attack',
                        'description': 'ICMP echo requests to broadcast addresses with spoofed source',
                        'characteristics': ['Broadcast amplification', 'Spoofed source addresses', 'Network congestion'],
                        'mitigation': ['Disable IP directed broadcasts', 'Ingress filtering', 'Network segmentation']
                    }
                ]
            },
            'application': {
                'name': 'Application Layer Attacks',
                'description': 'Target specific applications or services',
                'subcategories': [
                    {
                        'name': 'HTTP Flood',
                        'description': 'Overwhelm web servers with HTTP requests',
                        'characteristics': ['High request rate', 'Resource consumption', 'Legitimate-looking traffic'],
                        'mitigation': ['Rate limiting', 'Web application firewalls', 'Load balancing']
                    },
                    {
                        'name': 'Slowloris',
                        'description': 'Keep many connections open with partial HTTP requests',
                        'characteristics': ['Low bandwidth', 'Connection exhaustion', 'Partial requests'],
                        'mitigation': ['Connection timeouts', 'Concurrent connection limits', 'Reverse proxies']
                    },
                    {
                        'name': 'SSL/TLS Exhaustion',
                        'description': 'Overwhelm servers with SSL/TLS handshake requests',
                        'characteristics': ['CPU intensive', 'Handshake floods', 'Certificate processing'],
                        'mitigation': ['SSL acceleration', 'Rate limiting', 'Connection pooling']
                    }
                ]
            }
        }
    
    def _load_mitigation_strategies(self):
        """Load comprehensive mitigation strategies"""
        return {
            'prevention': [
                {
                    'strategy': 'Network Segmentation',
                    'description': 'Isolate critical systems from potential attack vectors',
                    'implementation': ['VLANs', 'Firewalls', 'Access control lists'],
                    'effectiveness': 'High for targeted attacks'
                },
                {
                    'strategy': 'Rate Limiting',
                    'description': 'Limit the rate of incoming requests or connections',
                    'implementation': ['Router/firewall rules', 'Application-level limiting', 'API throttling'],
                    'effectiveness': 'Medium to High depending on attack type'
                },
                {
                    'strategy': 'Ingress Filtering',
                    'description': 'Filter traffic at network entry points',
                    'implementation': ['BCP38 compliance', 'Source address validation', 'Spoofing prevention'],
                    'effectiveness': 'High for spoofed traffic attacks'
                }
            ],
            'detection': [
                {
                    'strategy': 'Traffic Analysis',
                    'description': 'Monitor network traffic patterns for anomalies',
                    'implementation': ['SIEM systems', 'Flow analysis', 'Baseline comparisons'],
                    'effectiveness': 'High with proper baseline'
                },
                {
                    'strategy': 'Behavioral Analysis',
                    'description': 'Analyze user and system behavior patterns',
                    'implementation': ['Machine learning', 'Statistical analysis', 'Anomaly detection'],
                    'effectiveness': 'High for sophisticated attacks'
                }
            ],
            'mitigation': [
                {
                    'strategy': 'Load Balancing',
                    'description': 'Distribute traffic across multiple servers',
                    'implementation': ['Hardware load balancers', 'Software solutions', 'Cloud-based services'],
                    'effectiveness': 'High for capacity-based attacks'
                },
                {
                    'strategy': 'Content Delivery Networks',
                    'description': 'Distribute content and absorb attack traffic',
                    'implementation': ['CDN services', 'Edge caching', 'Geographic distribution'],
                    'effectiveness': 'Very High for volumetric attacks'
                },
                {
                    'strategy': 'DDoS Protection Services',
                    'description': 'Specialized services for DDoS mitigation',
                    'implementation': ['Cloud-based protection', 'Scrubbing centers', 'Always-on protection'],
                    'effectiveness': 'Very High when properly configured'
                }
            ]
        }
    
    def get_case_study(self, case_id):
        """Get specific case study by ID"""
        for case in self.case_studies:
            if case['id'] == case_id:
                return case
        return None
    
    def get_all_case_studies(self):
        """Get all case studies"""
        return self.case_studies
    
    def get_attack_vectors(self):
        """Get all attack vector information"""
        return self.attack_vectors
    
    def get_mitigation_strategies(self):
        """Get all mitigation strategies"""
        return self.mitigation_strategies
    
    def search_cases(self, query):
        """Search case studies by query"""
        results = []
        query_lower = query.lower()
        
        for case in self.case_studies:
            if (query_lower in case['name'].lower() or 
                query_lower in case['target'].lower() or
                query_lower in case['attack_type'].lower()):
                results.append(case)
        
        return results
