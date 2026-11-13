from datetime import datetime
from uuid import UUID

import pytest

from incident_tracker.models import Incident


def test_create_incident():
    incident = Incident.create(
        title="Database outage",
        description="Production database is unavailable.",
        severity="critical",
        priority="P1",
    )

    assert incident.title == "Database outage"
    assert incident.description == "Production database is unavailable."
    assert incident.severity == "critical"
    assert incident.priority == "P1"
    assert incident.status == "open"


def test_incident_has_unique_id():
    first = Incident.create("Incident 1", "Description 1", "low", "P4")
    second = Incident.create("Incident 2", "Description 2", "high", "P1")

    assert first.id != second.id
    UUID(first.id)
    UUID(second.id)


def test_incident_has_utc_timestamp():
    incident = Incident.create("Test incident", "Test description", "low", "P4")

    timestamp = datetime.fromisoformat(incident.created_at)

    assert timestamp.tzinfo is not None
    assert timestamp.utcoffset().total_seconds() == 0


def test_create_incident_normalizes_inputs():
    incident = Incident.create(
        title="  Database outage  ",
        description="  Database unavailable  ",
        severity="CRITICAL",
        priority="p1",
    )

    assert incident.title == "Database outage"
    assert incident.description == "Database unavailable"
    assert incident.severity == "critical"
    assert incident.priority == "P1"


@pytest.mark.parametrize("title", ["", "   "])
def test_empty_title_is_rejected(title):
    with pytest.raises(ValueError, match="title cannot be empty"):
        Incident.create(title, "Description", "high", "P1")


@pytest.mark.parametrize("description", ["", "   "])
def test_empty_description_is_rejected(description):
    with pytest.raises(ValueError, match="description cannot be empty"):
        Incident.create("Test incident", description, "high", "P1")


def test_invalid_severity_is_rejected():
    with pytest.raises(ValueError, match="Invalid severity"):
        Incident.create("Test incident", "Description", "urgent", "P1")


def test_invalid_priority_is_rejected():
    with pytest.raises(ValueError, match="Invalid priority"):
        Incident.create("Test incident", "Description", "high", "P5")


def test_update_status_successfully():
    incident = Incident.create("Test incident", "Description", "high", "P1")

    incident.update_status("in_progress")

    assert incident.status == "in_progress"


def test_update_status_normalizes_input():
    incident = Incident.create("Test incident", "Description", "high", "P1")

    incident.update_status("IN_PROGRESS")

    assert incident.status == "in_progress"


def test_update_status_rejects_invalid_status():
    incident = Incident.create("Test incident", "Description", "high", "P1")

    with pytest.raises(ValueError, match="Invalid status"):
        incident.update_status("pending")


def test_update_status_rejects_invalid_transition():
    incident = Incident.create("Test incident", "Description", "high", "P1")

    with pytest.raises(ValueError, match="Cannot transition"):
        incident.update_status("closed")


def test_closed_incident_cannot_change_status():
    incident = Incident.create("Test incident", "Description", "high", "P1")
    incident.update_status("resolved")
    incident.update_status("closed")

    with pytest.raises(ValueError, match="Cannot transition"):
        incident.update_status("open")


def test_invalid_status_is_rejected():
    with pytest.raises(ValueError, match="Invalid status"):
        Incident(
            title="Test incident",
            description="Description",
            severity="high",
            priority="P1",
            id="test-id",
            status="pending",
            created_at="2026-11-13T00:00:00+00:00",
        )
