from meta.ontology.registry import OntologyRegistry
from meta.contracts.event import Event

class ConflictPolicy:
    def __init__(self, registry: OntologyRegistry):
        self.registry = registry

    def resolve(self, events: list[Event]) -> list[Event]:
        # Identifica eventos conflitantes usando a ontologia
        resolved_events = []
        for event in events:
            is_conflicting = False
            for existing_event in resolved_events:
                if self.registry.check_conflicts(event.semantic_type, existing_event.semantic_type):
                    is_conflicting = True
                    break
            if not is_conflicting:
                resolved_events.append(event)
        return resolved_events
