import os
import tempfile

# Configure the app before it is imported: throwaway SQLite file, no Redis, known key.
_db_dir = tempfile.mkdtemp()
os.environ["DATABASE_URL"] = f"sqlite:///{os.path.join(_db_dir, 'test.db')}"
os.environ["CACHE_ENABLED"] = "false"
os.environ["SECRET_API_KEY"] = "test-key"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
from app.models import Base  # noqa: E402
from app.utils.db import engine  # noqa: E402

API_KEY = {"X-API-KEY": "test-key"}


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    with TestClient(app) as c:  # runs lifespan: creates tables, starts scheduler
        yield c
