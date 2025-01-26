from sqlalchemy import create_engine
from app.models import Base


engine = create_engine("sqlite:///event_trigger.db")
Base.metadata.create_all(bind=engine)
print("Database tables created successfully.")
