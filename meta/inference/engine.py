from meta.ontology.registry import OntologyRegistry
from meta.event_store.store import EventStore
from meta.state_machine.narrative_fsm import NarrativeFSM
from meta.knowledge_graph.query_engine import KnowledgeQueryEngine
from .hypothesis import Hypothesis, ValidationResult

class InferenceEngine:
    def __init__(self, registry: OntologyRegistry, event_store: EventStore, fsm: NarrativeFSM, kg_query: KnowledgeQueryEngine):
        self.registry = registry
        self.event_store = event_store
        self.fsm = fsm
        self.kg_query = kg_query

    def run(self, latest_events: list) -> list[ValidationResult]:
        results = []
        for ev in latest_events:
            hyp = Hypothesis(
                id=f"hyp_{ev.id}",
                description=f"Event {ev.semantic_type} suggests narrative transition",
                supporting_events=[ev.id],
                confidence=ev.confidence
            )
            # Validar hipótese contra estado atual e ontologia
            valid = self.fsm.on_event(ev)
            conflicts = []
            if not valid:
                conflicts.append(f"Transition from {self.fsm.current_phase} not allowed by {ev.semantic_type}")
            results.append(ValidationResult(hypothesis=hyp, passed=valid, conflicts=conflicts))
        return results
