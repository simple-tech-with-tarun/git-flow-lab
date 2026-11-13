import json

import pytest

from incident_tracker.models import Incident
from incident_tracker.storage import JSONStorage


def test_save_and_load_preserves_incident_data(tmp_path):
    file_path = tmp_path / "data" / "incidents.json"
    storage = JSONStorage(file_path)

    incident = Incident.create(
        title="API outage",
        description="Production API is unavailable",
        severity="critical",
        priority="P1",
    )

    storage.save([incident])
    loaded_incidents = storage.load()

    assert len(loaded_incidents) == 1
    assert loaded_incidents[0] == incident


def test_load_returns_empty_list_when_file_does_not_exist(tmp_path):
    storage = JSONStorage(tmp_path / "incidents.json")

    assert storage.load() == []


def test_save_creates_parent_directories(tmp_path):
    file_path = tmp_path / "nested" / "data" / "incidents.json"
    storage = JSONStorage(file_path)

    storage.save([])

    assert file_path.exists()
    assert json.loads(file_path.read_text(encoding="utf-8")) == []


def test_load_raises_error_for_malformed_json(tmp_path):
    file_path = tmp_path / "incidents.json"
    file_path.write_text("{invalid json", encoding="utf-8")
    storage = JSONStorage(file_path)

    with pytest.raises(json.JSONDecodeError):
        storage.load()


def test_load_raises_error_for_invalid_incident_data(tmp_path):
    file_path = tmp_path / "incidents.json"
    file_path.write_text(
        json.dumps([{"title": "API outage", "severity": "unknown"}]),
        encoding="utf-8",
    )
    storage = JSONStorage(file_path)

    with pytest.raises((TypeError, ValueError)):
        storage.load()
