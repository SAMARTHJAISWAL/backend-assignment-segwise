"""Create the database tables (the API also does this on startup).

Run from the repo root:  python -m scripts.init_db
"""
from app.config import settings
from app.utils.db import init_db

if __name__ == "__main__":
    init_db()
    print(f"Database tables created at {settings.DATABASE_URL}")
