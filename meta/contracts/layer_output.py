from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

@dataclass
class LayerOutput:
    id: str
    timestamp: datetime
    layer_name: str
    semantic_type: str
    confidence: float
    valid: bool
    evidence: List[str] = field(default_factory=list)
    payload: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
