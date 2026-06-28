import os
import yaml
from typing import Dict, Any, List
from pathlib import Path

class ConceptSpec:
    def __init__(self, data: dict):
        self.name: str = data['concept']
        self.category: str = data['category']
        self.description: str = data.get('description', '')
        self.requires: List[str] = data.get('requires', [])
        self.produces: List[str] = data.get('produces', [])
        self.invalidates: List[str] = data.get('invalidates', [])
        self.confirms: List[str] = data.get('confirms', [])
        self.states: List[str] = data.get('states', [])
        self.parameters: Dict = data.get('parameters', {})
        self.confidence_range: List[int] = data.get('confidence_range', [0, 100])

class OntologyRegistry:
    def __init__(self, concepts_dir: str):
        self.concepts_dir = Path(concepts_dir)
        self.concepts: Dict[str, ConceptSpec] = {}
        self.load_all()

    def load_all(self):
        for file in self.concepts_dir.glob("*.yaml"):
            with open(file, 'r') as f:
                data = yaml.safe_load(f)
                concept = ConceptSpec(data)
                self.concepts[concept.name] = concept

    def get(self, name: str) -> ConceptSpec:
        return self.concepts.get(name)

    def validate_dependencies(self) -> List[str]:
        errors = []
        for name, spec in self.concepts.items():
            for req in spec.requires:
                if req not in self.concepts:
                    errors.append(f"{name} requires unknown concept '{req}'")
        return errors

    def get_all(self) -> Dict[str, ConceptSpec]:
        return self.concepts
