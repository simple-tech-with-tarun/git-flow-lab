from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

VALID_SEVERITIES = {"low", "medium", "high", "critical"}
VALID_PRIORITIES = {"P1", "P2", "P3", "P4"}
VALID_STATUSES = {"open", "in_progress", "resolved", "closed"}

VALID_STATUS_TRANSITIONS = {
    "open": {"in_progress", "resolved"},
    "in_progress": {"open", "resolved"},
    "resolved": {"in_progress", "closed"},
    "closed": set(),
}


@dataclass
class Incident:
    title: str
    description: str
    severity: str
    priority: str
    id: str
    status: str
    created_at: str

    def __post_init__(self):
        if not self.title.strip():
            raise ValueError("Incident title cannot be empty.")

        if not self.description.strip():
            raise ValueError("Incident description cannot be empty.")

        if self.severity not in VALID_SEVERITIES:
            raise ValueError(
                f"Invalid severity. Choose from: {', '.join(sorted(VALID_SEVERITIES))}"
            )

        if self.priority not in VALID_PRIORITIES:
            raise ValueError(
                f"Invalid priority. Choose from: {', '.join(sorted(VALID_PRIORITIES))}"
            )
        if self.status not in VALID_STATUSES:
            raise ValueError(
                f"Invalid status. Choose from: {', '.join(sorted(VALID_STATUSES))}"
            )

    def update_status(self, new_status: str) -> None:
        new_status = new_status.lower()

        if new_status not in VALID_STATUSES:
            raise ValueError(
                f"Invalid status. Choose from: {', '.join(sorted(VALID_STATUSES))}"
            )

        if new_status not in VALID_STATUS_TRANSITIONS[self.status]:
            raise ValueError(
                f"Cannot transition incident from '{self.status}' to '{new_status}'."
            )

        self.status = new_status

    @classmethod
    def create(
        cls,
        title: str,
        description: str,
        severity: str,
        priority: str,
    ) -> "Incident":
        return cls(
            title=title.strip(),
            description=description.strip(),
            severity=severity.lower(),
            priority=priority.upper(),
            id=str(uuid4()),
            status="open",
            created_at=datetime.now(timezone.utc).isoformat(),
        )
