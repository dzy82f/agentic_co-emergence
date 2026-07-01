from agentic_co_emergence.storage.event_store import SemanticEventStore
from agentic_co_emergence.projections.semantic_graph_projection import SemanticGraphProjector
from agentic_co_emergence.storage.semantic_graph_query import SemanticGraphQuery

MEMORY_SPACE_ID="tychevia-organisational-memory"
g=SemanticGraphProjector().from_events(MEMORY_SPACE_ID,SemanticEventStore(MEMORY_SPACE_ID).load())
q=SemanticGraphQuery(g)

print("SEMANTIC NODES")
for node in g.nodes.values():
    print(f"- {node['id']} | {node['kind']} | confidence={node['confidence']} | mentions={node['mentions']}")
    print(f"  concepts={', '.join(node.get('concepts', []))}")
    print(f"  {node['text']}")

print("\nSEMANTIC EDGES")
for edge in g.edges.values():
    print(f"- {edge['from']} --{edge['relation']}--> {edge['to']} | weight={edge.get('weight')} | source={edge.get('source')}")

print("\nCLUSTERS")
for cluster in q.clusters():
    print(f"- {cluster['id']} | {cluster['concept']} | size={cluster['size']}")
