from meta.ontology.registry import OntologyRegistry
from meta.contracts.layer_output import LayerOutput

class OntologyPolicy:
    def __init__(self, registry: OntologyRegistry):
        self.registry = registry

    def validate_output(self, output: LayerOutput) -> bool:
        concept = self.registry.get(output.semantic_type)
        if not concept:
            return False
        # Verifica se o output contém os campos esperados
        # (simplificado)
        return output.valid and output.confidence >= 0
