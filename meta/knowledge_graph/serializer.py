import networkx as nx

class GraphSerializer:
    def to_json(self, graph: nx.DiGraph):
        nodes = [{"id": n, **d} for n, d in graph.nodes(data=True)]
        edges = [{"source": u, "target": v, **d} for u, v, d in graph.edges(data=True)]
        return {"nodes": nodes, "edges": edges}
