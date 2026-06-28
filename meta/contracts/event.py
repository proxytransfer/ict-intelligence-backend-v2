from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict

@dataclass
class Event:
    id: str
    timestamp: datetime
    source: str               # camada ou motor
    semantic_type: str        # ex: "MSS", "Sweep"
    payload: Dict[str, Any]
    confidence: float
    valid: bool
    metadata: Dict[str, Any] = field(default_factory=dict)
