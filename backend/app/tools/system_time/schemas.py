"""Input/output schemas for the system_time reference tool."""
from pydantic import BaseModel


class SystemTimeInput(BaseModel):
    timezone: str = "UTC"  # only UTC is actually supported in this reference tool


class SystemTimeOutput(BaseModel):
    iso_timestamp: str
    timezone: str
