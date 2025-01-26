from sqlalchemy import create_engine
from models import Base  # Adjust import based on your project structure

engine = create_engine("sqlite:///event_trigger.db")
Base.metadata.create_all(bind=engine)
print("Database tables created successfully.")
