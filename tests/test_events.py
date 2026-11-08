from datetime import timedelta

from app.models import EventLog, Trigger
from app.services.scheduler import archive_old_events, cleanup_old_logs, execute_trigger
from app.utils.db import SessionLocal
from app.utils.time import utcnow


def _add_event(hours_ago: float, archived: bool = False, trigger_id: int = 0):
    with SessionLocal() as db:
        db.add(EventLog(trigger_id=trigger_id, details=f"{hours_ago}h", archived=archived,
                        timestamp=utcnow() - timedelta(hours=hours_ago)))
        db.commit()


def test_test_endpoint_logs_event(client):
    r = client.post("/test/", json={"hello": "world"})
    assert r.status_code == 200
    events = client.get("/events/").json()
    assert len(events) == 1
    assert "hello" in events[0]["details"]
    assert events[0]["archived"] is False


def test_events_pagination_newest_first(client):
    for h in (3, 2, 1):
        _add_event(hours_ago=h / 10)
    page1 = client.get("/events/?page=1&limit=2").json()
    page2 = client.get("/events/?page=2&limit=2").json()
    assert [e["details"] for e in page1] == ["0.1h", "0.2h"]
    assert [e["details"] for e in page2] == ["0.3h"]


def test_aggregate(client):
    client.post("/test/", json={})
    client.post("/test/", json={})
    assert client.get("/events/aggregate").json() == [{"trigger_id": 0, "count": 2}]


def test_retention_archives_then_deletes(client):
    _add_event(hours_ago=1)    # stays active
    _add_event(hours_ago=3)    # gets archived
    _add_event(hours_ago=50, archived=True)  # gets deleted

    assert archive_old_events() == 1
    assert cleanup_old_logs() == 1

    active = client.get("/events/?archived=false").json()
    archived = client.get("/events/?archived=true").json()
    assert [e["details"] for e in active] == ["1h"]
    assert [e["details"] for e in archived] == ["3h"]


def test_execute_trigger_logs_and_deactivates(client):
    with SessionLocal() as db:
        t = Trigger(name="t", type="scheduled", payload="p", schedule_time=utcnow())
        db.add(t)
        db.commit()
        trigger_id = t.id

    execute_trigger(trigger_id)

    with SessionLocal() as db:
        assert db.get(Trigger, trigger_id).is_active is False
        events = db.query(EventLog).filter_by(trigger_id=trigger_id).all()
        assert len(events) == 1 and "Payload: p" in events[0].details
