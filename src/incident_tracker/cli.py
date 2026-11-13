import argparse
import os
from pathlib import Path

from incident_tracker.models import (
    VALID_PRIORITIES,
    VALID_SEVERITIES,
    VALID_STATUSES,
    Incident,
)
from incident_tracker.storage import JSONStorage
from incident_tracker.tracker import IncidentTracker


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="incident-tracker",
        description="Command-line Incident Tracker",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    create_subparser = subparsers.add_parser(
        "create",
        help="Create a new incident",
    )
    create_subparser.add_argument("--title", required=True, help="Incident title")
    create_subparser.add_argument(
        "--description",
        required=True,
        help="Incident description",
    )

    create_subparser.add_argument(
        "--severity",
        required=True,
        choices=sorted(VALID_SEVERITIES),
        help="Incident severity",
    )
    create_subparser.add_argument(
        "--priority",
        required=True,
        choices=sorted(VALID_PRIORITIES),
        help="Incident priority",
    )

    subparsers.add_parser(
        "list",
        help="List all incidents",
    )

    show_parser = subparsers.add_parser(
        "show",
        help="Show details of an incident",
    )
    show_parser.add_argument(
        "incident_id",
        help="ID of the incident to display",
    )

    update_parser = subparsers.add_parser(
        "update-status",
        help="Update an incident's status",
    )
    update_parser.add_argument(
        "incident_id",
        help="ID of the incident to update",
    )
    update_parser.add_argument(
        "--status",
        required=True,
        choices=sorted(VALID_STATUSES),
        help="New incident status",
    )

    filter_parser = subparsers.add_parser(
        "filter",
        help="Filter incidents",
    )
    filter_parser.add_argument(
        "--severity",
        choices=sorted(VALID_SEVERITIES),
        help="Filter by severity",
    )
    filter_parser.add_argument(
        "--priority",
        choices=sorted(VALID_PRIORITIES),
        help="Filter by priority",
    )
    filter_parser.add_argument(
        "--status",
        choices=sorted(VALID_STATUSES),
        help="Filter by status",
    )

    return parser


def get_tracker() -> IncidentTracker:
    data_file = Path(os.environ.get("INCIDENT_TRACKER_DATA", "data/incidents.json"))

    return IncidentTracker(storage=JSONStorage(data_file))


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    tracker = get_tracker()

    if args.command == "create":
        try:
            incident = tracker.create_incident(
                title=args.title,
                description=args.description,
                severity=args.severity,
                priority=args.priority,
            )
            print("Incident created successfully.")
            display_incident(incident)
        except ValueError as error:
            parser.error(str(error))
    elif args.command == "list":
        incidents = tracker.list_incidents()
        display_incidents(incidents)
    elif args.command == "show":
        try:
            incident = tracker.get_incident(args.incident_id)
            display_incident(incident)
        except KeyError as error:
            parser.error(str(error))
    elif args.command == "update-status":
        try:
            incident = tracker.update_incident_status(
                incident_id=args.incident_id,
                new_status=args.status,
            )
            print("Incident status updated successfully.")
            display_incident(incident)
        except (KeyError, ValueError) as error:
            parser.error(str(error))
    elif args.command == "filter":
        incidents = tracker.filter_incidents(
            severity=args.severity,
            priority=args.priority,
            status=args.status,
        )
        display_incidents(incidents)


def display_incident(incident: Incident) -> None:
    print(f"ID:          {incident.id}")
    print(f"Title:       {incident.title}")
    print(f"Description: {incident.description}")
    print(f"Severity:    {incident.severity}")
    print(f"Priority:    {incident.priority}")
    print(f"Status:      {incident.status}")
    print(f"Created at:  {incident.created_at}")


def display_incidents(incidents: list[Incident]) -> None:
    if not incidents:
        print("No incidents found.")
        return

    for incident in incidents:
        print(
            f"{incident.id} | "
            f"{incident.title} | "
            f"{incident.severity} | "
            f"{incident.priority} | "
            f"{incident.status}"
        )


if __name__ == "__main__":
    main()
