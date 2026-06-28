from meta.ontology.registry import OntologyRegistry, ConceptSpec
from .ir import Rule, Condition, SemanticIR

class SemanticCompiler:
    def __init__(self, registry: OntologyRegistry):
        self.registry = registry

    def compile(self) -> SemanticIR:
        rules = []
        for name, spec in self.registry.get_all().items():
            rule = self._spec_to_rule(spec)
            rules.append(rule)
        return SemanticIR(rules=rules)

    def _spec_to_rule(self, spec: ConceptSpec) -> Rule:
        # Converte requires em inputs, e conditions genéricas a partir de parâmetros
        conditions = []
        for param, default in spec.parameters.items():
            # Cria uma condição placeholder (será preenchida pelo motor)
            conditions.append(Condition(
                expression=f"{spec.name}.{param} >= threshold",
                evaluate=lambda ctx, p=param, d=default: ctx.get(p, d) >= d
            ))
        return Rule(
            name=spec.name,
            inputs=spec.requires.copy(),
            output=spec.name,
            conditions=conditions
        )
