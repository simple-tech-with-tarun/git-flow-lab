import json

import pytest

from incident_tracker.cli import main


def test_create_incident(monkeypatch, tmp_path, capsys):
    data_file = tmp_path / "incidents.json"
    monkeypatch.setenv("INCIDENT_TRACKER_DATA", str(data_file))
    monkeypatch.setattr(
        "sys.argv",
        [
            "incident-tracker",
            "create",
            "--title",
            "API outage",
            "--description",
            "Production API is unavailable",
            "--severity",
            "critical",
            "--priority",
            "P1",
        ],
    )

    main()

    output = capsys.readouterr().out

    assert "Incident created successfully." in output
    assert "API outage" in output

    saved_incidents = json.loads(data_file.read_text(encoding="utf-8"))
    assert len(saved_incidents) == 1
    assert saved_incidents[0]["title"] == "API outage"


def test_list_incidents(monkeypatch, tmp_path, capsys):
    data_file = tmp_path / "incidents.json"
    monkeypatch.setenv("INCIDENT_TRACKER_DATA", str(data_file))

    data_file.write_text(
        json.dumps(
            [
                {
                    "title": "API outage",
                    "description": "Production API is unavailable",
                    "severity": "critical",
                    "priority": "P1",
                    "id": "incident-123",
                    "status": "open",
                    "created_at": "2026-11-14T00:00:00+00:00",
                }
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        ["incident-tracker", "list"],
    )

    main()

    output = capsys.readouterr().out

    assert "incident-123" in output
    assert "API outage" in output
    assert "critical" in output


def test_show_incident(monkeypatch, tmp_path, capsys):
    data_file = tmp_path / "incidents.json"
    monkeypatch.setenv("INCIDENT_TRACKER_DATA", str(data_file))

    data_file.write_text(
        json.dumps(
            [
                {
                    "title": "Database failure",
                    "description": "Primary database is unavailable",
                    "severity": "high",
                    "priority": "P1",
                    "id": "incident-456",
                    "status": "open",
                    "created_at": "2026-11-14T00:00:00+00:00",
                }
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        ["incident-tracker", "show", "incident-456"],
    )

    main()

    output = capsys.readouterr().out

    assert "incident-456" in output
    assert "Database failure" in output
    assert "Primary database is unavailable" in output
    assert "high" in output
    assert "P1" in output
    assert "open" in output


def test_update_incident_status(monkeypatch, tmp_path, capsys):
    data_file = tmp_path / "incidents.json"
    monkeypatch.setenv("INCIDENT_TRACKER_DATA", str(data_file))

    data_file.write_text(
        json.dumps(
            [
                {
                    "title": "Database failure",
                    "description": "Primary database is unavailable",
                    "severity": "high",
                    "priority": "P1",
                    "id": "incident-456",
                    "status": "open",
                    "created_at": "2026-11-14T00:00:00+00:00",
                }
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "incident-tracker",
            "update-status",
            "incident-456",
            "--status",
            "in_progress",
        ],
    )

    main()

    output = capsys.readouterr().out
    saved_incidents = json.loads(data_file.read_text(encoding="utf-8"))

    assert "Incident status updated successfully." in output
    assert "in_progress" in output
    assert saved_incidents[0]["status"] == "in_progress"


def test_filter_incidents(monkeypatch, tmp_path, capsys):
    data_file = tmp_path / "incidents.json"
    monkeypatch.setenv("INCIDENT_TRACKER_DATA", str(data_file))

    data_file.write_text(
        json.dumps(
            [
                {
                    "title": "API outage",
                    "description": "Production API is unavailable",
                    "severity": "critical",
                    "priority": "P1",
                    "id": "incident-123",
                    "status": "open",
                    "created_at": "2026-11-14T00:00:00+00:00",
                },
                {
                    "title": "Disk warning",
                    "description": "Disk usage reached 80 percent",
                    "severity": "medium",
                    "priority": "P2",
                    "id": "incident-456",
                    "status": "open",
                    "created_at": "2026-11-14T00:00:00+00:00",
                },
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "incident-tracker",
            "filter",
            "--severity",
            "critical",
            "--status",
            "open",
        ],
    )

    main()

    output = capsys.readouterr().out

    assert "incident-123" in output
    assert "API outage" in output
    assert "incident-456" not in output
    assert "Disk warning" not in output


def test_show_nonexistent_incident(monkeypatch, tmp_path, capsys):
    data_file = tmp_path / "incidents.json"
    monkeypatch.setenv("INCIDENT_TRACKER_DATA", str(data_file))

    monkeypatch.setattr(
        "sys.argv",
        ["incident-tracker", "show", "unknown-id"],
    )

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 2

    output = capsys.readouterr().err
    assert "Incident not found: unknown-id" in output


def test_update_incident_rejects_invalid_transition(
    monkeypatch,
    tmp_path,
    capsys,
):
    data_file = tmp_path / "incidents.json"
    monkeypatch.setenv("INCIDENT_TRACKER_DATA", str(data_file))

    data_file.write_text(
        json.dumps(
            [
                {
                    "title": "Database failure",
                    "description": "Primary database is unavailable",
                    "severity": "high",
                    "priority": "P1",
                    "id": "incident-456",
                    "status": "closed",
                    "created_at": "2026-11-14T00:00:00+00:00",
                }
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "incident-tracker",
            "update-status",
            "incident-456",
            "--status",
            "open",
        ],
    )

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 2

    output = capsys.readouterr().err
    assert "Cannot transition incident" in output


def test_create_incident_rejects_whitespace_title(
    monkeypatch,
    tmp_path,
    capsys,
):
    data_file = tmp_path / "incidents.json"
    monkeypatch.setenv("INCIDENT_TRACKER_DATA", str(data_file))

    monkeypatch.setattr(
        "sys.argv",
        [
            "incident-tracker",
            "create",
            "--title",
            "   ",
            "--description",
            "Production API is unavailable",
            "--severity",
            "critical",
            "--priority",
            "P1",
        ],
    )

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 2

    output = capsys.readouterr().err
    assert "title" in output.lower()
