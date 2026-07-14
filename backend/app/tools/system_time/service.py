"""Business logic for the system_time reference tool."""
from datetime import datetime, timezone

from app.tools.system_time.schemas import SystemTimeOutput


def get_current_time(requested_timezone: str = "UTC") -> SystemTimeOutput:
    if requested_timezone.upper() != "UTC":
        # A real tool would support more zones; this reference tool
        # deliberately stays minimal and just normalizes to UTC.
        requested_timezone = "UTC"
    now = datetime.now(timezone.utc)
    return SystemTimeOutput(iso_timestamp=now.isoformat(), timezone=requested_timezone)
