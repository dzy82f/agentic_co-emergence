import sys
from agentic_co_emergence.storage.event_store import SemanticEventStore
from agentic_co_emergence.projections.semantic_graph_projection import SemanticGraphProjector
from agentic_co_emergence.storage.semantic_graph_query import SemanticGraphQuery
MEMORY_SPACE_ID="tychevia-organisational-memory"
g=SemanticGraphProjector().from_events(MEMORY_SPACE_ID,SemanticEventStore(MEMORY_SPACE_ID).load())
node_id=sys.argv[1] if len(sys.argv)>1 else next(iter(g.nodes.keys()), None)
if not node_id:
    print("No semantic nodes found.")
else:
    for line in SemanticGraphQuery(g).trace(node_id):
        print(line)
