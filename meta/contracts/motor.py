from abc import ABC, abstractmethod
from typing import Any, Dict, List
from .layer_output import LayerOutput

class MotorICT(ABC):
    """Interface para todos os motores especializados."""
    @abstractmethod
    def analyze(self, context: Dict[str, Any]) -> LayerOutput:
        """Executa a análise do conceito e retorna LayerOutput."""
        ...

    @abstractmethod
    def validate(self, output: LayerOutput) -> bool:
        """Valida a saída conforme regras ontológicas."""
        ...

    @abstractmethod
    def explain(self, output: LayerOutput) -> List[str]:
        """Explica em linguagem natural as conclusões."""
        ...

    @abstractmethod
    def metrics(self) -> Dict[str, float]:
        """Métricas de performance do motor."""
        ...

    @abstractmethod
    def audit(self, output: LayerOutput) -> Dict[str, Any]:
        """Gera trilha de auditoria detalhada."""
        ...
