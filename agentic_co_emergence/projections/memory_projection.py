from agentic_co_emergence.models.models import MemoryEventType, MemoryProjection

class MemoryProjector:
    def from_events(self, memory_space_id, events):
        p = MemoryProjection(memory_space_id=memory_space_id)
        for e in events:
            et, d, oid = e.event_type, e.payload, e.memory_object_id
            if et == MemoryEventType.MEMORY_OBJECT_CREATED:
                p.objects[oid]={"id":oid,"kind":d["kind"],"text":d["text"],"sessions":list(d.get("sessions",[])),"confidence":d.get("confidence",.5),"mentions":d.get("mentions",1),"status":d.get("status","active")}
            elif et == MemoryEventType.MEMORY_OBJECT_REINFORCED and oid in p.objects:
                obj=p.objects[oid]; obj["mentions"]=obj.get("mentions",1)+d.get("mentions",1)
                for sid in d.get("sessions", []):
                    if sid not in obj["sessions"]: obj["sessions"].append(sid)
            elif et == MemoryEventType.MEMORY_CONFIDENCE_UPDATED and oid in p.objects: p.objects[oid]["confidence"]=d["confidence"]
            elif et == MemoryEventType.MEMORY_LINK_CREATED: p.links.append(d)
            elif et == MemoryEventType.MEMORY_SESSION_INDEXED:
                if d["session_id"] not in p.indexed_sessions: p.indexed_sessions.append(d["session_id"])
        return p
