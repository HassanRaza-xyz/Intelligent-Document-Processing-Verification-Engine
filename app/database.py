from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# We use SQLite for local development. 
SQLALCHEMY_DATABASE_URL = "sqlite:///./ezitech_documents.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get the DB session in our endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()