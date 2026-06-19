from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# creates a local file named 'swarm_rescue.db' 
DATABASE_URL = "sqlite:///./swarm_rescue.db"

# Engine configuration for SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Session factory allows us to talk to the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that our database tables will inherit from
Base = declarative_base()

# Helper dependency to get a clean DB connection for requests
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()