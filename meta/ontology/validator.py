from .registry import OntologyRegistry, ConceptSpec

class OntologyValidator:
    def __init__(self, registry: OntologyRegistry):
        self.registry = registry

    def validate_concept_instance(self, concept_name: str, payload: dict) -> bool:
        spec = self.registry.get(concept_name)
        if not spec:
            return False
        # Verificar campos obrigatórios de acordo com o spec
        required_fields = ["timestamp", "value", "state"]
        for f in required_fields:
            if f not in payload:
                return False
        return True

    def check_conflicts(self, concept_a: str, concept_b: str) -> bool:
        """Retorna True se houver conflito declarado entre A e B."""
        spec_a = self.registry.get(concept_a)
        if spec_a and concept_b in spec_a.invalidates:
            return True
        spec_b = self.registry.get(concept_b)
        if spec_b and concept_a in spec_b.invalidates:
            return True
        return False
