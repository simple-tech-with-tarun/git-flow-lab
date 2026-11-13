from incident_tracker.models import Incident
from incident_tracker.storage import JSONStorage


class IncidentTracker:
    def __init__(self, storage: JSONStorage | None = None):
        self._incidents: dict[str, Incident] = {}
        self._storage = storage

        if self._storage is not None:
            self._incidents = {
                incident.id: incident for incident in self._storage.load()
            }

    def _save(self) -> None:
        if self._storage is not None:
            self._storage.save(self.list_incidents())

    def create_incident(
        self,
        title: str,
        description: str,
        severity: str,
        priority: str,
    ) -> Incident:
        incident = Incident.create(
            title=title,
            description=description,
            severity=severity,
            priority=priority,
        )

        self._incidents[incident.id] = incident
        self._save()
        return incident

    def list_incidents(self) -> list[Incident]:
        return list(self._incidents.values())

    def get_incident(self, incident_id: str) -> Incident:
        try:
            return self._incidents[incident_id]
        except KeyError:
            raise KeyError(f"Incident not found: {incident_id}") from None

    def update_incident_status(self, incident_id: str, new_status: str) -> Incident:
        incident = self.get_incident(incident_id)
        incident.update_status(new_status)
        self._save()
        return incident

    def filter_incidents(
        self,
        severity: str | None = None,
        priority: str | None = None,
        status: str | None = None,
    ) -> list[Incident]:
        incidents = self.list_incidents()

        if severity is not None:
            severity = severity.lower()
            incidents = [
                incident for incident in incidents if incident.severity == severity
            ]

        if priority is not None:
            priority = priority.upper()
            incidents = [
                incident for incident in incidents if incident.priority == priority
            ]

        if status is not None:
            status = status.lower()
            incidents = [
                incident for incident in incidents if incident.status == status
            ]

        return incidents
