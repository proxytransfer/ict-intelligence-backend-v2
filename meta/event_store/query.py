from typing import List, Optional
from meta.contracts.event import Event
from .store import EventStore

class EventQuery:
    def __init__(self, store: EventStore):
        self.store = store

    def get_events_in_window(self, start_ts, end_ts) -> List[Event]:
        return [e for e in self.store.get_all() if start_ts <= e.timestamp <= end_ts]

    def get_latest_by_type(self, stype: str) -> Optional[Event]:
        events = self.store.query_by_semantic_type(stype)
        return max(events, key=lambda e: e.timestamp) if events else None
