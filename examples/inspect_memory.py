from agentic_co_emergence.storage.event_store import MemoryEventStore
from agentic_co_emergence.projections.memory_projection import MemoryProjector
from agentic_co_emergence.storage.memory_query import MemoryQuery
MEMORY_SPACE_ID="tychevia-organisational-memory"
p=MemoryProjector().from_events(MEMORY_SPACE_ID,MemoryEventStore(MEMORY_SPACE_ID).load())
print("INDEXED SESSIONS")
for sid in p.indexed_sessions: print(f"- {sid}")
print("\nTOP MEMORY OBJECTS")
for o in MemoryQuery(p).top(20):
    print(f"- {o['id']} | {o['kind']} | confidence={o['confidence']} | mentions={o['mentions']} | sessions={len(o['sessions'])}\n  {o['text']}")
