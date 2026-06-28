import networkx as nx
from meta.contracts.event import Event
from .node import KnowledgeNode
from .edge import KnowledgeEdge

class KnowledgeGraphBuilder:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_event(self, event: Event):
        node = KnowledgeNode(
            id=event.id,
            concept=event.semantic_type,
            properties=event.payload
        )
        self.graph.add_node(node.id, concept=node.concept, **node.properties)

    def add_relation(self, edge: KnowledgeEdge):
        self.graph.add_edge(edge.source, edge.target, relation=edge.relation)

    def reset(self):
        self.graph.clear()

    def get_graph(self) -> nx.DiGraph:
        return self.graph
