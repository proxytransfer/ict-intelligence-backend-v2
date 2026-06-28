from typing import List, Dict, Any

class ExecutionPolicy:
    def __init__(self, order: List[str]):
        self.required_order = order

    def allow_execution(self, layer_name: str, executed_layers: List[str]) -> bool:
        if layer_name not in self.required_order:
            return False
        idx = self.required_order.index(layer_name)
        # Todas as camadas anteriores devem ter sido executadas
        return all(l in executed_layers for l in self.required_order[:idx])
