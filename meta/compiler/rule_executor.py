from typing import Dict, Any
from .ir import Rule, SemanticIR
from meta.contracts.layer_output import LayerOutput

class RuleExecutor:
    def __init__(self, ir: SemanticIR):
        self.ir = ir

    def execute(self, rule_name: str, context: Dict[str, Any]) -> LayerOutput:
        rule = next((r for r in self.ir.rules if r.name == rule_name), None)
        if not rule:
            raise ValueError(f"Rule {rule_name} not found")
        valid = all(cond.evaluate(context) for cond in rule.conditions)
        return LayerOutput(
            id=f"{rule_name}_{context.get('timestamp')}",
            timestamp=context.get('timestamp'),
            layer_name="RuleExecutor",
            semantic_type=rule.output,
            confidence=1.0 if valid else 0.0,
            valid=valid,
            evidence=[f"Rule {rule_name} executed"]
        )
