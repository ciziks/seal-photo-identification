import pytest
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from services.backend.src.database import get_db, SessionLocal, engine

def test_get_db():
    # Test that get_db function yields a database session and closes it after use
    db_generator = get_db()
    db_session = next(db_generator)
    
    # Check if the yielded object is an instance of Session
    assert isinstance(db_session, Session)
    
    # Close the session generator
    db_generator.close()
    
    # Check if the session is closed
    assert db_session.close

def test_session_local():
    # Test that SessionLocal creates a new session
    db_session = SessionLocal()
    
    # Check if the session is an instance of Session
    assert isinstance(db_session, Session)
    
    # Close the session
    db_session.close()
    
    # Check if the session is closed
    assert db_session.is_active

def test_engine_creation():    
    # Test that the engine is created correctly
    assert isinstance(engine, Engine)
    
    # Check if the engine URL is correct
    assert str(engine.url) == "sqlite:///./sealcenter.db"