from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_active_events():
    """
    Test retrieving active (non-archived) events.
    """
    response = client.get(
        "/events/?archived=false",
        headers={"X-API-KEY": "your-secure-secret-key-123456"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    print("Active events retrieved successfully:", response.json())

def test_get_archived_events():
    """
    Test retrieving archived events.
    """
    response = client.get(
        "/events/?archived=true",
        headers={"X-API-KEY": "your-secure-secret-key-123456"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    print("Archived events retrieved successfully:", response.json())

def test_archive_event():
    """
    Test archiving an event by ID.
    """
    event_id = 2  # Replace with an existing event ID
    response = client.put(
        f"/events/archive/{event_id}",
        headers={"X-API-KEY": "your-secure-secret-key-123456"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Event archived successfully"}
    print(f"Event {event_id} archived successfully.")
