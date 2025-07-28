"""
Data Processing Utilities - Helper functions for DoS attack data analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
from typing import Dict, List, Tuple, Optional, Any
import json

class DoSDataProcessor:
    """Main class for processing DoS attack data and metrics"""
    
    def __init__(self):
        self.traffic_patterns = {}
        self.attack_signatures = {}
        self.baseline_metrics = {}
    
    def process_traffic_data(self, traffic_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Process raw traffic data to extract DoS-relevant metrics
        
        Args:
            traffic_data: DataFrame with columns ['timestamp', 'source_ip', 'requests', 'bytes']
            
        Returns:
            Dictionary containing processed metrics
        """
        if traffic_data.empty:
            return {'error': 'No traffic data provided'}
        
        # Ensure timestamp column is datetime
        if 'timestamp' in traffic_data.columns:
            traffic_data['timestamp'] = pd.to_datetime(traffic_data['timestamp'])
        
        # Calculate time-based metrics
        time_metrics = self._calculate_time_metrics(traffic_data)
        
        # Calculate source-based metrics
        source_metrics = self._calculate_source_metrics(traffic_data)
        
        # Calculate volume metrics
        volume_metrics = self._calculate_volume_metrics(traffic_data)
        
        # Detect anomalies
        anomalies = self._detect_traffic_anomalies(traffic_data)
        
        return {
            'time_metrics': time_metrics,
            'source_metrics': source_metrics,
            'volume_metrics': volume_metrics,
            'anomalies': anomalies,
            'processed_at': datetime.now().isoformat()
        }
    
    def _calculate_time_metrics(self, data: pd.DataFrame) -> Dict[str, float]:
        """Calculate time-based traffic metrics"""
        if 'timestamp' not in data.columns:
            return {}
        
        # Group by time intervals
        data.set_index('timestamp', inplace=True)
        
        # Requests per minute
        rpm_data = data.resample('1T').size()
        
        # Bytes per minute  
        if 'bytes' in data.columns:
            bpm_data = data.resample('1T')['bytes'].sum()
        else:
            bpm_data = pd.Series(dtype=float)
        
        return {
            'avg_requests_per_minute': float(rpm_data.mean()) if not rpm_data.empty else 0.0,
            'max_requests_per_minute': float(rpm_data.max()) if not rpm_data.empty else 0.0,
            'std_requests_per_minute': float(rpm_data.std()) if not rpm_data.empty else 0.0,
            'avg_bytes_per_minute': float(bpm_data.mean()) if not bpm_data.empty else 0.0,
            'max_bytes_per_minute': float(bpm_data.max()) if not bpm_data.empty else 0.0,
            'total_duration_minutes': len(rpm_data),
            'traffic_variability': float(rpm_data.std() / rpm_data.mean()) if rpm_data.mean() > 0 else 0.0
        }
    
    def _calculate_source_metrics(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate source IP-based metrics"""
        if 'source_ip' not in data.columns:
            return {}
        
        # Source IP analysis
        source_counts = data['source_ip'].value_counts()
        
        # Geographic distribution (simplified)
        unique_sources = len(source_counts)
        
        # Top sources analysis
        top_10_sources = source_counts.head(10)
        top_source_percentage = (top_10_sources.sum() / len(data)) * 100
        
        return {
            'unique_source_ips': unique_sources,
            'top_source_requests': int(source_counts.iloc[0]) if not source_counts.empty else 0,
            'top_10_source_percentage': float(top_source_percentage),
            'source_ip_entropy': float(self._calculate_entropy(source_counts.values)),
            'source_distribution': source_counts.head(20).to_dict(),
            'suspicious_sources': self._identify_suspicious_sources(source_counts)
        }
    
    def _calculate_volume_metrics(self, data: pd.DataFrame) -> Dict[str, float]:
        """Calculate volume-based metrics"""
        total_requests = len(data)
        
        volume_metrics = {
            'total_requests': total_requests,
            'requests_per_second': total_requests / 3600 if total_requests > 0 else 0.0  # Assuming 1-hour window
        }
        
        if 'bytes' in data.columns:
            total_bytes = data['bytes'].sum()
            volume_metrics.update({
                'total_bytes': float(total_bytes),
                'avg_bytes_per_request': float(data['bytes'].mean()) if not data['bytes'].empty else 0.0,
                'bytes_per_second': float(total_bytes) / 3600 if total_bytes > 0 else 0.0
            })
        
        return volume_metrics
    
    def _detect_traffic_anomalies(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Detect traffic anomalies that might indicate DoS attacks"""
        anomalies = {
            'high_volume_periods': [],
            'source_concentration': False,
            'unusual_patterns': [],
            'anomaly_score': 0.0
        }
        
        if data.empty:
            return anomalies
        
        # High volume detection
        if 'timestamp' in data.columns:
            data_indexed = data.set_index('timestamp')
            minute_counts = data_indexed.resample('1T').size()
            
            if not minute_counts.empty:
                threshold = minute_counts.mean() + 3 * minute_counts.std()
                high_volume_periods = minute_counts[minute_counts > threshold]
                
                anomalies['high_volume_periods'] = [
                    {
                        'timestamp': ts.isoformat(),
                        'request_count': int(count),
                        'threshold': float(threshold)
                    }
                    for ts, count in high_volume_periods.items()
                ]
        
        # Source concentration detection
        if 'source_ip' in data.columns:
            source_counts = data['source_ip'].value_counts()
            if not source_counts.empty:
                top_source_percentage = (source_counts.iloc[0] / len(data)) * 100
                anomalies['source_concentration'] = top_source_percentage > 20  # More than 20% from single source
        
        # Calculate overall anomaly score
        anomalies['anomaly_score'] = self._calculate_anomaly_score(data, anomalies)
        
        return anomalies
    
    def _calculate_entropy(self, values: np.ndarray) -> float:
        """Calculate Shannon entropy for data distribution"""
        if len(values) == 0:
            return 0.0
        
        # Normalize values to probabilities
        total = np.sum(values)
        if total == 0:
            return 0.0
        
        probabilities = values / total
        probabilities = probabilities[probabilities > 0]  # Remove zeros
        
        # Calculate entropy
        entropy = -np.sum(probabilities * np.log2(probabilities))
        return entropy
    
    def _identify_suspicious_sources(self, source_counts: pd.Series) -> List[Dict[str, Any]]:
        """Identify potentially suspicious source IPs"""
        if source_counts.empty:
            return []
        
        suspicious = []
        
        # High volume sources (top 1% with unusually high request counts)
        total_requests = source_counts.sum()
        threshold = total_requests * 0.05  # 5% of total traffic from single source
        
        high_volume_sources = source_counts[source_counts > threshold]
        
        for ip, count in high_volume_sources.items():
            suspicious.append({
                'source_ip': ip,
                'request_count': int(count),
                'percentage': float((count / total_requests) * 100),
                'reason': 'High volume source'
            })
        
        return suspicious
    
    def _calculate_anomaly_score(self, data: pd.DataFrame, anomalies: Dict) -> float:
        """Calculate overall anomaly score (0-10 scale)"""
        score = 0.0
        
        # High volume periods contribute to score
        if anomalies['high_volume_periods']:
            score += min(3.0, len(anomalies['high_volume_periods']) * 0.5)
        
        # Source concentration contributes to score
        if anomalies['source_concentration']:
            score += 3.0
        
        # Source distribution entropy (lower entropy = higher anomaly)
        if 'source_ip' in data.columns:
            source_counts = data['source_ip'].value_counts()
            if not source_counts.empty:
                entropy = self._calculate_entropy(source_counts.values)
                max_possible_entropy = np.log2(len(source_counts))
                if max_possible_entropy > 0:
                    normalized_entropy = entropy / max_possible_entropy
                    score += (1 - normalized_entropy) * 2.0  # Low entropy = high score
        
        # Traffic volume compared to typical baseline
        if len(data) > 1000:  # Arbitrary threshold for "high" traffic
            score += 2.0
        
        return min(10.0, score)

class AttackPatternAnalyzer:
    """Analyzer for identifying DoS attack patterns"""
    
    def __init__(self):
        self.known_patterns = self._load_known_patterns()
    
    def analyze_attack_pattern(self, traffic_data: pd.DataFrame, attack_type: str = None) -> Dict[str, Any]:
        """
        Analyze traffic data for specific attack patterns
        
        Args:
            traffic_data: Traffic data to analyze
            attack_type: Optional specific attack type to look for
            
        Returns:
            Analysis results with pattern matches and confidence scores
        """
        results = {
            'detected_patterns': [],
            'confidence_scores': {},
            'recommendations': [],
            'attack_characteristics': {}
        }
        
        if traffic_data.empty:
            return results
        
        # Pattern-specific analysis
        if attack_type:
            pattern_result = self._analyze_specific_pattern(traffic_data, attack_type)
            results['detected_patterns'].append(pattern_result)
        else:
            # Analyze for all known patterns
            for pattern_name in self.known_patterns.keys():
                pattern_result = self._analyze_specific_pattern(traffic_data, pattern_name)
                if pattern_result['confidence'] > 0.3:  # Only include likely matches
                    results['detected_patterns'].append(pattern_result)
        
        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(results['detected_patterns'])
        
        return results
    
    def _load_known_patterns(self) -> Dict[str, Dict]:
        """Load known DoS attack patterns"""
        return {
            'syn_flood': {
                'description': 'TCP SYN flood attack pattern',
                'characteristics': {
                    'high_syn_ratio': True,
                    'incomplete_connections': True,
                    'rapid_connection_attempts': True
                },
                'detection_rules': [
                    'syn_packet_rate > normal_rate * 10',
                    'connection_completion_rate < 0.1'
                ]
            },
            'udp_flood': {
                'description': 'UDP flood attack pattern',
                'characteristics': {
                    'high_udp_volume': True,
                    'random_ports': True,
                    'small_packet_sizes': True
                },
                'detection_rules': [
                    'udp_packet_rate > normal_rate * 5',
                    'port_distribution_entropy > threshold'
                ]
            },
            'http_flood': {
                'description': 'HTTP flood attack pattern',
                'characteristics': {
                    'high_request_rate': True,
                    'similar_user_agents': True,
                    'repetitive_requests': True
                },
                'detection_rules': [
                    'http_request_rate > normal_rate * 3',
                    'user_agent_diversity < threshold'
                ]
            },
            'amplification': {
                'description': 'DNS/NTP amplification attack',
                'characteristics': {
                    'spoofed_sources': True,
                    'large_response_packets': True,
                    'specific_query_types': True
                },
                'detection_rules': [
                    'response_size / request_size > 10',
                    'source_ip_spoofing_indicators'
                ]
            }
        }
    
    def _analyze_specific_pattern(self, data: pd.DataFrame, pattern_name: str) -> Dict[str, Any]:
        """Analyze data for a specific attack pattern"""
        pattern = self.known_patterns.get(pattern_name, {})
        
        result = {
            'pattern_name': pattern_name,
            'description': pattern.get('description', ''),
            'confidence': 0.0,
            'indicators': [],
            'severity': 'low'
        }
        
        if not pattern or data.empty:
            return result
        
        # Pattern-specific analysis
        confidence_factors = []
        
        if pattern_name == 'syn_flood':
            confidence_factors.extend(self._analyze_syn_flood_pattern(data))
        elif pattern_name == 'udp_flood':
            confidence_factors.extend(self._analyze_udp_flood_pattern(data))
        elif pattern_name == 'http_flood':
            confidence_factors.extend(self._analyze_http_flood_pattern(data))
        elif pattern_name == 'amplification':
            confidence_factors.extend(self._analyze_amplification_pattern(data))
        
        # Calculate overall confidence
        if confidence_factors:
            result['confidence'] = np.mean(confidence_factors)
            result['indicators'] = [f"Factor {i+1}: {cf:.2f}" for i, cf in enumerate(confidence_factors)]
        
        # Determine severity
        if result['confidence'] > 0.8:
            result['severity'] = 'high'
        elif result['confidence'] > 0.5:
            result['severity'] = 'medium'
        else:
            result['severity'] = 'low'
        
        return result
    
    def _analyze_syn_flood_pattern(self, data: pd.DataFrame) -> List[float]:
        """Analyze for SYN flood pattern indicators"""
        confidence_factors = []
        
        # Simulated analysis - in real implementation, would analyze actual packet data
        # High request rate indicator
        if len(data) > 1000:  # High volume
            confidence_factors.append(0.7)
        
        # Source IP concentration
        if 'source_ip' in data.columns:
            source_counts = data['source_ip'].value_counts()
            if not source_counts.empty:
                top_source_percentage = (source_counts.iloc[0] / len(data)) * 100
                if top_source_percentage > 30:
                    confidence_factors.append(0.8)
                else:
                    confidence_factors.append(0.3)
        
        return confidence_factors
    
    def _analyze_udp_flood_pattern(self, data: pd.DataFrame) -> List[float]:
        """Analyze for UDP flood pattern indicators"""
        confidence_factors = []
        
        # Volume-based analysis
        if len(data) > 500:
            confidence_factors.append(0.6)
        
        # Source distribution analysis
        if 'source_ip' in data.columns:
            unique_sources = data['source_ip'].nunique()
            if unique_sources > 100:  # Many sources
                confidence_factors.append(0.7)
            else:
                confidence_factors.append(0.4)
        
        return confidence_factors
    
    def _analyze_http_flood_pattern(self, data: pd.DataFrame) -> List[float]:
        """Analyze for HTTP flood pattern indicators"""
        confidence_factors = []
        
        # Request rate analysis
        if len(data) > 2000:  # Very high request volume
            confidence_factors.append(0.8)
        elif len(data) > 800:
            confidence_factors.append(0.5)
        else:
            confidence_factors.append(0.2)
        
        return confidence_factors
    
    def _analyze_amplification_pattern(self, data: pd.DataFrame) -> List[float]:
        """Analyze for amplification attack indicators"""
        confidence_factors = []
        
        # Simulated amplification analysis
        if 'bytes' in data.columns:
            avg_size = data['bytes'].mean()
            if avg_size > 1000:  # Large response packets
                confidence_factors.append(0.7)
            else:
                confidence_factors.append(0.3)
        
        return confidence_factors
    
    def _generate_recommendations(self, detected_patterns: List[Dict]) -> List[str]:
        """Generate mitigation recommendations based on detected patterns"""
        recommendations = []
        
        if not detected_patterns:
            return ['No specific attack patterns detected - continue normal monitoring']
        
        # Pattern-specific recommendations
        pattern_names = [p['pattern_name'] for p in detected_patterns if p['confidence'] > 0.5]
        
        if 'syn_flood' in pattern_names:
            recommendations.extend([
                'Enable SYN cookies on servers',
                'Configure SYN flood protection on firewalls',
                'Implement connection rate limiting'
            ])
        
        if 'udp_flood' in pattern_names:
            recommendations.extend([
                'Implement UDP rate limiting',
                'Configure ingress filtering',
                'Enable UDP flood protection'
            ])
        
        if 'http_flood' in pattern_names:
            recommendations.extend([
                'Enable HTTP request rate limiting',
                'Deploy Web Application Firewall (WAF)',
                'Implement CAPTCHA challenges for suspicious sources'
            ])
        
        if 'amplification' in pattern_names:
            recommendations.extend([
                'Implement BCP38 ingress filtering',
                'Configure response rate limiting on public services',
                'Monitor for source IP spoofing'
            ])
        
        # General recommendations
        recommendations.extend([
            'Activate enhanced monitoring and alerting',
            'Consider enabling DDoS protection services',
            'Document incident for future analysis'
        ])
        
        return list(set(recommendations))  # Remove duplicates

class MetricsCalculator:
    """Calculator for DoS-related security metrics"""
    
    @staticmethod
    def calculate_attack_severity(traffic_volume: float, baseline_volume: float, 
                                duration_minutes: float, affected_services: int) -> Dict[str, float]:
        """
        Calculate attack severity score based on multiple factors
        
        Args:
            traffic_volume: Attack traffic volume
            baseline_volume: Normal traffic baseline
            duration_minutes: Attack duration in minutes
            affected_services: Number of affected services
            
        Returns:
            Dictionary with severity metrics
        """
        # Volume impact score (0-4)
        volume_ratio = traffic_volume / baseline_volume if baseline_volume > 0 else 1
        if volume_ratio > 10:
            volume_score = 4.0
        elif volume_ratio > 5:
            volume_score = 3.0
        elif volume_ratio > 2:
            volume_score = 2.0
        elif volume_ratio > 1.5:
            volume_score = 1.0
        else:
            volume_score = 0.0
        
        # Duration impact score (0-3)
        if duration_minutes > 240:  # > 4 hours
            duration_score = 3.0
        elif duration_minutes > 60:  # > 1 hour
            duration_score = 2.0
        elif duration_minutes > 15:  # > 15 minutes
            duration_score = 1.0
        else:
            duration_score = 0.5
        
        # Service impact score (0-3)
        if affected_services > 5:
            service_score = 3.0
        elif affected_services > 2:
            service_score = 2.0
        elif affected_services > 0:
            service_score = 1.0
        else:
            service_score = 0.0
        
        # Calculate overall severity (0-10)
        total_score = volume_score + duration_score + service_score
        
        return {
            'overall_severity': total_score,
            'volume_impact': volume_score,
            'duration_impact': duration_score,
            'service_impact': service_score,
            'severity_level': MetricsCalculator._get_severity_level(total_score)
        }
    
    @staticmethod
    def _get_severity_level(score: float) -> str:
        """Convert numeric severity score to descriptive level"""
        if score >= 8:
            return 'Critical'
        elif score >= 6:
            return 'High'
        elif score >= 4:
            return 'Medium'
        elif score >= 2:
            return 'Low'
        else:
            return 'Minimal'
    
    @staticmethod
    def calculate_mitigation_effectiveness(baseline_metrics: Dict[str, float], 
                                         current_metrics: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate mitigation effectiveness based on before/after metrics
        
        Args:
            baseline_metrics: Metrics during attack (before mitigation)
            current_metrics: Current metrics (after mitigation)
            
        Returns:
            Effectiveness metrics
        """
        effectiveness = {}
        
        # Traffic reduction effectiveness
        if 'traffic_volume' in baseline_metrics and 'traffic_volume' in current_metrics:
            baseline_traffic = baseline_metrics['traffic_volume']
            current_traffic = current_metrics['traffic_volume']
            
            if baseline_traffic > 0:
                reduction_percentage = ((baseline_traffic - current_traffic) / baseline_traffic) * 100
                effectiveness['traffic_reduction'] = max(0, min(100, reduction_percentage))
        
        # Response time improvement
        if 'response_time' in baseline_metrics and 'response_time' in current_metrics:
            baseline_time = baseline_metrics['response_time']
            current_time = current_metrics['response_time']
            
            if baseline_time > 0:
                improvement_percentage = ((baseline_time - current_time) / baseline_time) * 100
                effectiveness['response_time_improvement'] = max(0, min(100, improvement_percentage))
        
        # Error rate reduction
        if 'error_rate' in baseline_metrics and 'error_rate' in current_metrics:
            baseline_errors = baseline_metrics['error_rate']
            current_errors = current_metrics['error_rate']
            
            if baseline_errors > 0:
                error_reduction = ((baseline_errors - current_errors) / baseline_errors) * 100
                effectiveness['error_rate_reduction'] = max(0, min(100, error_reduction))
        
        # Calculate overall effectiveness
        if effectiveness:
            overall = np.mean(list(effectiveness.values()))
            effectiveness['overall_effectiveness'] = overall
        
        return effectiveness
    
    @staticmethod
    def calculate_business_impact(hourly_revenue: float, outage_duration_hours: float,
                                performance_degradation_percent: float, reputation_impact_factor: float = 0.3) -> Dict[str, float]:
        """
        Calculate business impact of DoS attack
        
        Args:
            hourly_revenue: Revenue per hour
            outage_duration_hours: Duration of service impact
            performance_degradation_percent: Performance impact percentage (0-100)
            reputation_impact_factor: Long-term reputation impact factor (0-1)
            
        Returns:
            Business impact metrics in monetary terms
        """
        # Direct revenue loss
        if performance_degradation_percent >= 100:
            # Complete outage
            direct_loss = hourly_revenue * outage_duration_hours
        else:
            # Partial impact
            impact_factor = performance_degradation_percent / 100
            direct_loss = hourly_revenue * outage_duration_hours * impact_factor
        
        # Indirect costs
        recovery_costs = direct_loss * 0.15  # 15% of direct loss
        opportunity_cost = direct_loss * 0.25  # 25% of direct loss
        reputation_damage = direct_loss * reputation_impact_factor
        
        total_impact = direct_loss + recovery_costs + opportunity_cost + reputation_damage
        
        return {
            'direct_revenue_loss': direct_loss,
            'recovery_costs': recovery_costs,
            'opportunity_cost': opportunity_cost,
            'reputation_damage': reputation_damage,
            'total_business_impact': total_impact,
            'impact_per_hour': total_impact / max(outage_duration_hours, 0.1)
        }

def parse_log_entry(log_line: str, log_format: str = 'apache_common') -> Optional[Dict[str, str]]:
    """
    Parse log entry and extract relevant fields for DoS analysis
    
    Args:
        log_line: Raw log line
        log_format: Log format type ('apache_common', 'nginx', 'custom')
        
    Returns:
        Parsed log entry as dictionary or None if parsing fails
    """
    try:
        if log_format == 'apache_common':
            # Apache Common Log Format
            pattern = r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?)" (\d+) (\d+|-)'
            match = re.match(pattern, log_line)
            
            if match:
                return {
                    'source_ip': match.group(1),
                    'timestamp': match.group(2),
                    'request': match.group(3),
                    'status_code': match.group(4),
                    'bytes_sent': match.group(5) if match.group(5) != '-' else '0'
                }
        
        elif log_format == 'nginx':
            # Basic Nginx log format
            pattern = r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"'
            match = re.match(pattern, log_line)
            
            if match:
                return {
                    'source_ip': match.group(1),
                    'timestamp': match.group(2),
                    'request': match.group(3),
                    'status_code': match.group(4),
                    'bytes_sent': match.group(5),
                    'referrer': match.group(6),
                    'user_agent': match.group(7)
                }
        
    except Exception as e:
        print(f"Error parsing log line: {e}")
    
    return None

def extract_traffic_features(traffic_data: pd.DataFrame) -> pd.DataFrame:
    """
    Extract features from traffic data for machine learning analysis
    
    Args:
        traffic_data: Raw traffic data
        
    Returns:
        DataFrame with extracted features
    """
    if traffic_data.empty:
        return pd.DataFrame()
    
    features = pd.DataFrame()
    
    # Time-based features
    if 'timestamp' in traffic_data.columns:
        traffic_data['timestamp'] = pd.to_datetime(traffic_data['timestamp'])
        features['hour'] = traffic_data['timestamp'].dt.hour
        features['day_of_week'] = traffic_data['timestamp'].dt.dayofweek
        features['minute'] = traffic_data['timestamp'].dt.minute
    
    # Source IP features
    if 'source_ip' in traffic_data.columns:
        # IP frequency
        ip_counts = traffic_data['source_ip'].value_counts()
        features['source_ip_frequency'] = traffic_data['source_ip'].map(ip_counts)
        
        # IP entropy (diversity measure)
        total_requests = len(traffic_data)
        features['source_ip_entropy'] = traffic_data['source_ip'].map(
            lambda ip: ip_counts[ip] / total_requests
        ).apply(lambda p: -p * np.log2(p) if p > 0 else 0)
    
    # Request size features
    if 'bytes' in traffic_data.columns:
        features['request_size'] = traffic_data['bytes']
        features['request_size_normalized'] = (
            traffic_data['bytes'] - traffic_data['bytes'].mean()
        ) / traffic_data['bytes'].std()
    
    # Request rate features (requests per minute)
    if 'timestamp' in traffic_data.columns:
        traffic_data_copy = traffic_data.copy()
        traffic_data_copy.set_index('timestamp', inplace=True)
        minute_counts = traffic_data_copy.resample('1T').size()
        
        # Map minute counts back to original data
        features['requests_per_minute'] = traffic_data['timestamp'].dt.floor('T').map(minute_counts)
    
    return features

def generate_attack_simulation_data(attack_type: str, duration_hours: int = 2, 
                                  intensity: int = 5) -> pd.DataFrame:
    """
    Generate simulated attack data for educational purposes
    
    Args:
        attack_type: Type of attack to simulate
        duration_hours: Duration of simulation in hours
        intensity: Attack intensity (1-10 scale)
        
    Returns:
        DataFrame with simulated attack data
    """
    start_time = datetime.now() - timedelta(hours=duration_hours)
    end_time = datetime.now()
    
    # Generate time series
    time_range = pd.date_range(start=start_time, end=end_time, freq='1T')
    
    # Base parameters
    base_requests_per_minute = 100
    attack_multiplier = intensity
    
    simulation_data = []
    
    for timestamp in time_range:
        # Calculate attack intensity over time
        time_factor = (timestamp - start_time).total_seconds() / 3600  # Hours since start
        
        if attack_type == 'escalating':
            current_multiplier = 1 + (attack_multiplier - 1) * (time_factor / duration_hours)
        elif attack_type == 'constant':
            current_multiplier = attack_multiplier
        elif attack_type == 'pulsing':
            pulse_factor = 1 + attack_multiplier * abs(np.sin(time_factor * np.pi))
            current_multiplier = pulse_factor
        else:
            current_multiplier = attack_multiplier
        
        requests_this_minute = int(base_requests_per_minute * current_multiplier)
        
        # Generate individual requests for this minute
        for i in range(requests_this_minute):
            # Generate source IPs based on attack type
            if attack_type in ['syn_flood', 'concentrated']:
                # Few source IPs with high volume
                source_ip = f"192.168.{np.random.randint(1, 5)}.{np.random.randint(1, 10)}"
            else:
                # Distributed sources
                source_ip = f"{np.random.randint(1, 255)}.{np.random.randint(1, 255)}.{np.random.randint(1, 255)}.{np.random.randint(1, 255)}"
            
            # Request size varies by attack type
            if attack_type == 'udp_flood':
                bytes_sent = np.random.randint(50, 200)  # Small packets
            elif attack_type == 'amplification':
                bytes_sent = np.random.randint(1000, 5000)  # Large responses
            else:
                bytes_sent = np.random.randint(200, 1500)  # Normal range
            
            simulation_data.append({
                'timestamp': timestamp + timedelta(seconds=i),
                'source_ip': source_ip,
                'bytes': bytes_sent,
                'attack_type': attack_type,
                'intensity': current_multiplier
            })
    
    return pd.DataFrame(simulation_data)

def validate_data_quality(data: pd.DataFrame) -> Dict[str, Any]:
    """
    Validate quality and completeness of traffic data
    
    Args:
        data: Traffic data to validate
        
    Returns:
        Data quality report
    """
    quality_report = {
        'total_records': len(data),
        'missing_values': {},
        'data_types': {},
        'anomalies': [],
        'quality_score': 0.0,
        'recommendations': []
    }
    
    if data.empty:
        quality_report['quality_score'] = 0.0
        quality_report['recommendations'].append('No data provided for analysis')
        return quality_report
    
    # Check for missing values
    for column in data.columns:
        missing_count = data[column].isnull().sum()
        missing_percentage = (missing_count / len(data)) * 100
        quality_report['missing_values'][column] = {
            'count': int(missing_count),
            'percentage': float(missing_percentage)
        }
    
    # Check data types
    for column in data.columns:
        quality_report['data_types'][column] = str(data[column].dtype)
    
    # Identify anomalies
    if 'timestamp' in data.columns:
        # Check for duplicate timestamps
        duplicate_timestamps = data['timestamp'].duplicated().sum()
        if duplicate_timestamps > 0:
            quality_report['anomalies'].append(f'Found {duplicate_timestamps} duplicate timestamps')
        
        # Check for time gaps
        if not data['timestamp'].isnull().all():
            time_diffs = pd.to_datetime(data['timestamp']).diff().dropna()
            large_gaps = time_diffs[time_diffs > timedelta(minutes=10)]
            if not large_gaps.empty:
                quality_report['anomalies'].append(f'Found {len(large_gaps)} large time gaps (>10 minutes)')
    
    if 'source_ip' in data.columns:
        # Check for invalid IP addresses
        invalid_ips = data[~data['source_ip'].str.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', na=False)]
        if not invalid_ips.empty:
            quality_report['anomalies'].append(f'Found {len(invalid_ips)} invalid IP addresses')
    
    # Calculate quality score
    missing_penalty = sum([mv['percentage'] for mv in quality_report['missing_values'].values()]) / len(data.columns)
    anomaly_penalty = len(quality_report['anomalies']) * 5  # 5% penalty per anomaly
    
    quality_score = max(0, 100 - missing_penalty - anomaly_penalty)
    quality_report['quality_score'] = quality_score
    
    # Generate recommendations
    if quality_score < 70:
        quality_report['recommendations'].append('Data quality is below acceptable threshold')
    
    if missing_penalty > 20:
        quality_report['recommendations'].append('High percentage of missing values detected')
    
    if len(quality_report['anomalies']) > 3:
        quality_report['recommendations'].append('Multiple data anomalies detected - review data source')
    
    if quality_score >= 90:
        quality_report['recommendations'].append('Data quality is excellent - proceed with analysis')
    
    return quality_report
