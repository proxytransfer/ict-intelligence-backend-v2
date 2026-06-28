from meta.knowledge_graph.builder import KnowledgeGraphBuilder
from meta.contracts.event import Event
from .store import EventStore

class Projector:
    def __init__(self, event_store: EventStore, kg_builder: KnowledgeGraphBuilder):
        self.event_store = event_store
        self.kg_builder = kg_builder

    def rebuild_graph(self):
        events = self.event_store.get_all()
        self.kg_builder.reset()
        for ev in events:
            self.kg_builder.add_event(ev)
        return self.kg_builder.get_graph()
