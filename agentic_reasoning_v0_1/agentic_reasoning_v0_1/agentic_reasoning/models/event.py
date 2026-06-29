from datetime import datetime, timezone
from pydantic import BaseModel, Field


class LedgerEvent(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    event_type: str
    payload: dict
