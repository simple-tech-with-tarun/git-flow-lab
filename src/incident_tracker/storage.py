import json
from pathlib import Path

from incident_tracker.models import Incident


class JSONStorage:
    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)

    def save(self, incidents: list[Incident]) -> None:
        data = [
            {
                "title": incident.title,
                "description": incident.description,
                "severity": incident.severity,
                "priority": incident.priority,
                "id": incident.id,
                "status": incident.status,
                "created_at": incident.created_at,
            }
            for incident in incidents
        ]

        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load(self) -> list[Incident]:
        if not self.file_path.exists():
            return []

        with self.file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return [Incident(**item) for item in data]
