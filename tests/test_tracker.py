import pytest

from incident_tracker.tracker import IncidentTracker


def test_create_incident():
    tracker = IncidentTracker()

    incident = tracker.create_incident(
        title="Database outage",
        description="Production database is unavailable.",
        severity="critical",
        priority="P1",
    )

    assert incident.title == "Database outage"
    assert tracker.get_incident(incident.id) == incident


def test_list_incidents():
    tracker = IncidentTracker()

    tracker.create_incident("Incident 1", "Description 1", "low", "P4")
    tracker.create_incident("Incident 2", "Description 2", "high", "P1")

    incidents = tracker.list_incidents()

    assert len(incidents) == 2


def test_get_incident():
    tracker = IncidentTracker()

    created = tracker.create_incident(
        "Database outage", "Database unavailable", "critical", "P1"
    )

    retrieved = tracker.get_incident(created.id)

    assert retrieved == created


def test_get_nonexistent_incident():
    tracker = IncidentTracker()

    with pytest.raises(KeyError, match="Incident not found"):
        tracker.get_incident("nonexistent-id")
