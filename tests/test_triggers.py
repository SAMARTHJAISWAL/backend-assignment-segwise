from datetime import datetime, timedelta

from app.services.scheduler import scheduler
from tests.conftest import API_KEY


def test_root(client):
    assert client.get("/").status_code == 200


def test_triggers_require_api_key(client):
    assert client.get("/triggers/").status_code == 422  # header missing
    assert client.get("/triggers/", headers={"X-API-KEY": "wrong"}).status_code == 401


def test_create_and_list_api_trigger(client):
    r = client.post("/triggers/", json={"name": "Webhook", "type": "api", "payload": "hi"}, headers=API_KEY)
    assert r.status_code == 200
    created = r.json()
    assert created["name"] == "Webhook" and created["is_active"] is True

    listed = client.get("/triggers/", headers=API_KEY).json()
    assert [t["id"] for t in listed] == [created["id"]]


def test_invalid_type_rejected(client):
    r = client.post("/triggers/", json={"name": "x", "type": "cron"}, headers=API_KEY)
    assert r.status_code == 422


def test_scheduled_requires_time(client):
    r = client.post("/triggers/", json={"name": "x", "type": "scheduled"}, headers=API_KEY)
    assert r.status_code == 422


def test_scheduled_trigger_registers_job_and_delete_removes_it(client):
    when = (datetime.now() + timedelta(hours=1)).isoformat()
    r = client.post("/triggers/", json={"name": "Later", "type": "scheduled", "schedule_time": when}, headers=API_KEY)
    trigger_id = r.json()["id"]
    assert scheduler.get_job(f"trigger-{trigger_id}") is not None

    assert client.delete(f"/triggers/{trigger_id}", headers=API_KEY).status_code == 200
    assert scheduler.get_job(f"trigger-{trigger_id}") is None


def test_delete_missing_trigger_is_404(client):
    assert client.delete("/triggers/999", headers=API_KEY).status_code == 404
