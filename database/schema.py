"""
Database schema for DoS Attack Analysis Platform
Contains SQLAlchemy models for storing attack data, case studies, and educational content
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class CaseStudy(Base):
    __tablename__ = 'case_studies'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    target = Column(String, nullable=False)
    attack_type = Column(String, nullable=False)
    peak_traffic = Column(String)
    duration = Column(String)
    attack_vectors = Column(JSON)  # Store as JSON array
    impact = Column(JSON)  # Store impact details as JSON
    mitigation = Column(JSON)  # Store mitigation strategies as JSON
    lessons_learned = Column(JSON)  # Store lessons as JSON array
    technical_details = Column(JSON)  # Store technical details as JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AttackVector(Base):
    __tablename__ = 'attack_vectors'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(Text)
    technical_details = Column(JSON)
    mitigation_strategies = Column(JSON)
    difficulty_level = Column(String)
    impact_potential = Column(String)
    detection_methods = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class MitigationStrategy(Base):
    __tablename__ = 'mitigation_strategies'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(Text)
    implementation_steps = Column(JSON)
    effectiveness_rating = Column(Float)
    cost_level = Column(String)
    complexity = Column(String)
    applicable_attack_types = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class EducationalContent(Base):
    __tablename__ = 'educational_content'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content_type = Column(String, nullable=False)  # module, quiz, exercise
    category = Column(String)
    content_data = Column(JSON)  # Store content structure as JSON
    difficulty_level = Column(String)
    estimated_duration = Column(Integer)  # in minutes
    prerequisites = Column(JSON)
    learning_objectives = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserProgress(Base):
    __tablename__ = 'user_progress'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_session = Column(String, nullable=False)  # Session-based tracking
    content_id = Column(Integer, nullable=False)
    content_type = Column(String, nullable=False)
    completion_status = Column(String, default='started')  # started, in_progress, completed
    score = Column(Float)
    time_spent = Column(Integer)  # in seconds
    answers = Column(JSON)  # Store quiz answers or exercise results
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Database connection and session management
def get_database_url():
    """Get database URL from environment variables"""
    return os.getenv('DATABASE_URL', 'postgresql://localhost/dos_analysis')

def create_database_engine():
    """Create SQLAlchemy engine"""
    database_url = get_database_url()
    return create_engine(database_url, echo=False)

def create_session():
    """Create database session"""
    engine = create_database_engine()
    Session = sessionmaker(bind=engine)
    return Session()

def init_database():
    """Initialize database tables"""
    engine = create_database_engine()
    Base.metadata.create_all(engine)
    return engine