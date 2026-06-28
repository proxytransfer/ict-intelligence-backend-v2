from dataclasses import dataclass, field
from typing import List, Callable, Any

@dataclass
class Condition:
    expression: str  # e.g., "close > swing.high"
    evaluate: Callable[[dict], bool] = lambda _: True

@dataclass
class Rule:
    name: str
    inputs: List[str]
    output: str
    conditions: List[Condition] = field(default_factory=list)

@dataclass
class SemanticIR:
    rules: List[Rule]
    version: str = "1.0"
