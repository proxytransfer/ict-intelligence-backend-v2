from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .motor import MotorICT

class Domain(ABC):
    """Agrupa motores, validadores e políticas de um domínio ICT."""
    name: str
    motors: List[MotorICT] = []
    policies: Dict[str, Any] = {}

    @abstractmethod
    def validate_domain(self, outputs: List[Any]) -> bool:
        """Valida consistência entre motores do domínio."""
        ...
