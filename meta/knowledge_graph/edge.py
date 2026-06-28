from dataclasses import dataclass

@dataclass
class KnowledgeEdge:
    source: str
    target: str
    relation: str  # 'causes', 'confirms', 'invalidates', 'precedes'
