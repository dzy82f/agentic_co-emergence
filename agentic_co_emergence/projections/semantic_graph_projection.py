from agentic_co_emergence.models.models import SemanticEventType, SemanticGraphProjection

class SemanticGraphProjector:
    def from_events(self, memory_space_id, events):
        p = SemanticGraphProjection(memory_space_id=memory_space_id)
        for e in events:
            et, d, sid = e.event_type, e.payload, e.semantic_id
            if et == SemanticEventType.SEMANTIC_NODE_CREATED:
                p.nodes[sid] = {"id": sid, "kind": d["kind"], "text": d["text"], "confidence": d.get("confidence", .5), "mentions": d.get("mentions", 1), "sessions": list(d.get("sessions", [])), "concepts": list(d.get("concepts", []))}
            elif et == SemanticEventType.SEMANTIC_NODE_REINFORCED and sid in p.nodes:
                node = p.nodes[sid]
                node["mentions"] += d.get("mentions", 1)
                node["confidence"] = max(node["confidence"], d.get("confidence", node["confidence"]))
                for sess in d.get("sessions", []):
                    if sess not in node["sessions"]: node["sessions"].append(sess)
            elif et == SemanticEventType.SEMANTIC_EDGE_CREATED:
                eid = sid
                p.edges[eid] = {"id": eid, **d, "weight": d.get("weight", 1)}
            elif et == SemanticEventType.SEMANTIC_EDGE_REINFORCED and sid in p.edges:
                p.edges[sid]["weight"] = p.edges[sid].get("weight", 1) + d.get("weight", 1)
            elif et == SemanticEventType.SEMANTIC_CLUSTER_CREATED:
                p.clusters[sid] = {"id": sid, **d}
        return p
