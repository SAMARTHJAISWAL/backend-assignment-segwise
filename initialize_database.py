from app.models import Base
from app.utils.db import engine

# Create all tables in the database
Base.metadata.create_all(bind=engine)
print("Database initialized successfully!")
