from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#Sets SQLite as the database engine, file-based database ///, and sets file name
DATABASE_URL = "sqlite:///./network.db"

#Create_engine is the bridge that connects the database(database_url)
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} #Allows FAST API's use of multiple threads/async
)

#When SessionLocal is called, a session connects to database
SessionLocal = sessionmaker(
    autocommit=False, #So that changes are not saved w/o session.commit()
    autoflush=False, #prevents SQLAlchemy from auto writing pending changes
    bind=engine #attaches the engine from above when SessionLocal() is called
)

#Creates a Base class for all SQLAlchemy models to inherit from. Models will be recognized as tables.
Base = declarative_base()

def get_db(): #Acts as the gateway between FastAPI and database
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

