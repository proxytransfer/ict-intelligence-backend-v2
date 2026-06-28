from meta.state_machine.narrative_state import NarrativePhase
from meta.ontology.registry import OntologyRegistry

class StateValidator:
    def __init__(self, registry: OntologyRegistry):
        self.registry = registry

    def is_valid_transition(self, from_phase: NarrativePhase, to_phase: NarrativePhase, concept: str) -> bool:
        # Validar se o conceito realmente pode causar essa transição (consultar ontologia)
        spec = self.registry.get(concept)
        if not spec:
            return False
        # Simplificação: se o conceito produz algo que se alinha com a fase seguinte
        return True  # A implementação real checaria regras ontológicas
