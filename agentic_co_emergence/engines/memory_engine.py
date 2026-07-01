from agentic_co_emergence.models.models import MemoryEvent, MemoryEventType
class MemoryEngine:
    def update_memory(self, space, session_id, knowledge, memory):
        ev=[]
        for oid,obj in knowledge.objects.items():
            if oid not in memory.objects:
                ev.append(MemoryEvent(space,MemoryEventType.MEMORY_OBJECT_CREATED,oid,{"kind":obj["kind"],"text":obj["text"],"sessions":[session_id],"confidence":obj.get("confidence",.5),"mentions":obj.get("mentions",1),"status":obj.get("status","active")}))
            else:
                ev.append(MemoryEvent(space,MemoryEventType.MEMORY_OBJECT_REINFORCED,oid,{"sessions":[session_id],"mentions":obj.get("mentions",1)}))
                ev.append(MemoryEvent(space,MemoryEventType.MEMORY_CONFIDENCE_UPDATED,oid,{"confidence":min(.98,round(max(memory.objects[oid].get("confidence",.5),obj.get("confidence",.5))+.03,2))}))
        for link in knowledge.links: ev.append(MemoryEvent(space,MemoryEventType.MEMORY_LINK_CREATED,None,{**link,"session_id":session_id}))
        if session_id not in memory.indexed_sessions:
            ev.append(MemoryEvent(space,MemoryEventType.MEMORY_SESSION_INDEXED,None,{"session_id":session_id,"knowledge_objects_indexed":len(knowledge.objects),"knowledge_links_indexed":len(knowledge.links)}))
        return ev
