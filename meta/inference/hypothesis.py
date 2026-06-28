from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Hypothesis:
    id: str
    description: str
    supporting_events: List[str]
    confidence: float

@dataclass
class ValidationResult:
    hypothesis: Hypothesis
    passed: bool
    conflicts: List[str] = field(default_factory=list)
    notes: str = ""
