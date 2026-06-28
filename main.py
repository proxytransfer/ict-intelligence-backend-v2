from fastapi import FastAPI
from meta.ontology.registry import OntologyRegistry
from meta.event_store.store import EventStore

app = FastAPI(title="ICT Market Intelligence Backend")

@app.get("/")
async def root():
    return {"status": "online", "project": "ICT Market Intelligence"}

@app.get("/health")
async def health():
    return {"status": "ok"}
