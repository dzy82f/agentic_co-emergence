from agentic_co_emergence.models.models import KnowledgeEventType, KnowledgeProjection

class KnowledgeProjector:
    def from_events(self, session_id, events):
        p = KnowledgeProjection(session_id=session_id)
        for e in events:
            et, d, oid = e.event_type, e.payload, e.knowledge_object_id
            if et == KnowledgeEventType.KNOWLEDGE_OBJECT_CREATED:
                p.objects[oid] = {"id": oid, "kind": d["kind"], "text": d["text"], "speakers": list(d.get("speakers", [])), "source_reasoning_event_ids": list(d.get("source_reasoning_event_ids", [])), "confidence": d.get("confidence", .5), "status": d.get("status","active"), "mentions": d.get("mentions",1)}
            elif et == KnowledgeEventType.KNOWLEDGE_OBJECT_REINFORCED and oid in p.objects:
                obj=p.objects[oid]; obj["mentions"]=obj.get("mentions",1)+1
                for s in d.get("speakers", []):
                    if s not in obj["speakers"]: obj["speakers"].append(s)
                obj["source_reasoning_event_ids"].extend(d.get("source_reasoning_event_ids", []))
            elif et == KnowledgeEventType.KNOWLEDGE_CONFIDENCE_UPDATED and oid in p.objects: p.objects[oid]["confidence"]=d["confidence"]
            elif et == KnowledgeEventType.KNOWLEDGE_LINK_CREATED: p.links.append(d)
        return p
