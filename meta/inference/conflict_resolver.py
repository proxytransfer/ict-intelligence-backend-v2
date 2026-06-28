from meta.ontology.registry import OntologyRegistry
from meta.contracts.event import Event

class ConflictResolver:
    def __init__(self, registry: OntologyRegistry):
        self.registry = registry

    def resolve(self, events: list[Event]) -> list[Event]:
        # Elimina eventos conflitantes mantendo o de maior confiança
        resolved = []
        for i, ev in enumerate(events):
            keep = True
            for j, ev2 in enumerate(events):
                if i >= j: continue
                if self._conflict(ev, ev2):
                    if ev2.confidence > ev.confidence:
                        keep = False
                        break
            if keep:
                resolved.append(ev)
        return resolved

    def _conflict(self, ev1: Event, ev2: Event) -> bool:
        # Checa se conceitos se invalidam mutuamente
        c1 = self.registry.get(ev1.semantic_type)
        c2 = self.registry.get(ev2.semantic_type)
        if c1 and c2:
            return (ev2.semantic_type in c1.invalidates) or (ev1.semantic_type in c2.invalidates)
        return False
