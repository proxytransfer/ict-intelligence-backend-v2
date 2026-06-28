import json
from pathlib import Path
from meta.contracts.event import Event

class EventStore:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.log_file = self.base_path / "events.jsonl"

    def append(self, event: Event):
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(event.__dict__, default=str) + "\n")

    def get_all(self) -> list[Event]:
        events = []
        if self.log_file.exists():
            with open(self.log_file) as f:
                for line in f:
                    data = json.loads(line)
                    events.append(Event(**data))
        return events

    def query_by_semantic_type(self, stype: str) -> list[Event]:
        return [e for e in self.get_all() if e.semantic_type == stype]
