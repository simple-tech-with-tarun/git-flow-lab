from incident_tracker.models import Incident


class IncidentTracker:
    def __init__(self):
        self._incidents: dict[str, Incident] = {}

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
        return incident

    def list_incidents(self) -> list[Incident]:
        return list(self._incidents.values())

    def get_incident(self, incident_id: str) -> Incident:
        try:
            return self._incidents[incident_id]
        except KeyError:
            raise KeyError(f"Incident not found: {incident_id}") from None
