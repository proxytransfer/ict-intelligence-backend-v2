import networkx as nx

class KnowledgeQueryEngine:
    def __init__(self, graph: nx.DiGraph):
        self.graph = graph

    def get_causal_chain(self, start_node: str, end_node: str) -> list:
        """Retorna caminho mais curto de causas entre dois nós."""
        try:
            return nx.shortest_path(self.graph, source=start_node, target=end_node)
        except nx.NetworkXNoPath:
            return []

    def get_nodes_by_concept(self, concept: str) -> list:
        return [n for n, d in self.graph.nodes(data=True) if d.get('concept') == concept]
