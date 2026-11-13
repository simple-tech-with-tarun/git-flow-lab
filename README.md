# Incident Tracker

A Python command-line application for managing operational incidents.

## Features

- Create and manage incidents.
- Track incident severity and priority.
- Update incident status.
- Filter and list incidents.
- Persist incident data in JSON format.

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

Application commands and usage instructions will be documented as features are implemented.