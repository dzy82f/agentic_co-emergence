import sys
from agentic_co_emergence.storage.event_store import MemoryEventStore
from agentic_co_emergence.projections.memory_projection import MemoryProjector
from agentic_co_emergence.storage.memory_query import MemoryQuery
MEMORY_SPACE_ID="tychevia-organisational-memory"
query=" ".join(sys.argv[1:]) or "governance"
p=MemoryProjector().from_events(MEMORY_SPACE_ID,MemoryEventStore(MEMORY_SPACE_ID).load())
print(f"QUERY: {query}")
for o in MemoryQuery(p).search(query):
    print(f"- {o['id']} | {o['kind']} | confidence={o['confidence']} | mentions={o['mentions']}\n  {o['text']}")
