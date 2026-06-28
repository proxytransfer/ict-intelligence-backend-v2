from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class KnowledgeNode:
    id: str
    concept: str
    properties: Dict[str, Any]
