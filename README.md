# Incident Tracker

A Python command-line application for managing operational incidents.

## Features

- Create and manage incidents.
- Track incident severity and priority.
- Update incident status with validated transitions.
- Filter and list incidents.
- Persist incident data in JSON format.

## Prerequisites

- Python 3.10 or later.
- pip package manager.

## Development Setup

### 1. Create a Virtual Environment

```powershell
python -m venv .venv
```

### 2. Activate the Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install the Project and Development Dependencies

```powershell
python -m pip install -e ".[dev]"
```

## Quality Checks

### Run Automated Tests

```powershell
python -m pytest
```

### Run Ruff Linting

```powershell
python -m ruff check .
```

### Check Code Formatting

```powershell
python -m ruff format --check .
```

## Application Usage

The application can be executed using Python's module invocation:

`python -m incident_tracker.cli`

### Create an Incident

```powershell
python -m incident_tracker.cli create --title "API outage" --description "API requests are failing" --severity critical --priority P1
```

### List All Incidents

```powershell
python -m incident_tracker.cli list
```

### Show Incident Details

Replace `<incident-id>` with the ID returned when creating an incident.

```powershell
python -m incident_tracker.cli show <incident-id>
```

### Update Incident Status

```powershell
python -m incident_tracker.cli update-status <incident-id> --status in_progress
```

Supported statuses:

- `open`
- `in_progress`
- `resolved`
- `closed`

Status transitions are validated by the application.

### Filter Incidents

Filter by severity, priority, status, or a combination of criteria.

```powershell
python -m incident_tracker.cli filter --severity critical
python -m incident_tracker.cli filter --priority P1
python -m incident_tracker.cli filter --status open
python -m incident_tracker.cli filter --severity critical --status open
```

### Severity and Priority Values

Supported severity levels:

- `low`
- `medium`
- `high`
- `critical`

Supported priorities:

- `P1`
- `P2`
- `P3`
- `P4`

### Data Storage

By default, incident data is stored in:

`data/incidents.json`

You can override the storage location using the `INCIDENT_TRACKER_DATA` environment variable.

```powershell
$env:INCIDENT_TRACKER_DATA = ".\data\test-incidents.json"
```

The application creates the required data directory and JSON file when needed.

Incident data is automatically loaded when the application starts and saved after incident creation or status updates.
