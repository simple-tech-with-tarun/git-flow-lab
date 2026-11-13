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


def test_update_incident_status():
    tracker = IncidentTracker()

    incident = tracker.create_incident(
        "Database outage", "Database unavailable", "critical", "P1"
    )

    updated = tracker.update_incident_status(incident.id, "in_progress")

    assert updated.status == "in_progress"
    assert tracker.get_incident(incident.id).status == "in_progress"


def test_update_status_for_nonexistent_incident():
    tracker = IncidentTracker()

    with pytest.raises(KeyError, match="Incident not found"):
        tracker.update_incident_status("nonexistent-id", "in_progress")


def test_tracker_rejects_invalid_status_transition():
    tracker = IncidentTracker()

    incident = tracker.create_incident(
        "Database outage", "Database unavailable", "critical", "P1"
    )

    with pytest.raises(ValueError, match="Cannot transition"):
        tracker.update_incident_status(incident.id, "closed")


def test_filter_incidents_by_severity():
    tracker = IncidentTracker()

    tracker.create_incident("Incident 1", "Description 1", "critical", "P1")
    tracker.create_incident("Incident 2", "Description 2", "low", "P4")
    tracker.create_incident("Incident 3", "Description 3", "critical", "P2")

    incidents = tracker.filter_incidents(severity="critical")

    assert len(incidents) == 2
    assert all(incident.severity == "critical" for incident in incidents)


def test_filter_incidents_by_priority():
    tracker = IncidentTracker()

    tracker.create_incident("Incident 1", "Description 1", "critical", "P1")
    tracker.create_incident("Incident 2", "Description 2", "low", "P4")

    incidents = tracker.filter_incidents(priority="P1")

    assert len(incidents) == 1
    assert incidents[0].priority == "P1"


def test_filter_incidents_by_status():
    tracker = IncidentTracker()

    first = tracker.create_incident("Incident 1", "Description 1", "critical", "P1")
    tracker.create_incident("Incident 2", "Description 2", "low", "P4")

    tracker.update_incident_status(first.id, "in_progress")

    incidents = tracker.filter_incidents(status="in_progress")

    assert len(incidents) == 1
    assert incidents[0].id == first.id


def test_filter_incidents_with_multiple_criteria():
    tracker = IncidentTracker()

    first = tracker.create_incident("Incident 1", "Description 1", "critical", "P1")
    tracker.create_incident("Incident 2", "Description 2", "critical", "P2")
    tracker.create_incident("Incident 3", "Description 3", "low", "P1")

    tracker.update_incident_status(first.id, "in_progress")

    incidents = tracker.filter_incidents(
        severity="critical",
        priority="P1",
        status="in_progress",
    )

    assert len(incidents) == 1
    assert incidents[0].id == first.id


def test_filter_incidents_without_criteria():
    tracker = IncidentTracker()

    tracker.create_incident("Incident 1", "Description 1", "critical", "P1")
    tracker.create_incident("Incident 2", "Description 2", "low", "P4")

    assert len(tracker.filter_incidents()) == 2
