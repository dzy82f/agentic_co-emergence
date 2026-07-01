import hashlib
from agentic_co_emergence.models.models import KnowledgeEvent, KnowledgeEventType, ReasoningEventType
class KnowledgeEngine:
    KIND_MAP={ReasoningEventType.CLAIM_REGISTERED:"claim",ReasoningEventType.QUESTION_REGISTERED:"question",ReasoningEventType.ASSUMPTION_REGISTERED:"assumption",ReasoningEventType.CHALLENGE_REGISTERED:"challenge",ReasoningEventType.AGREEMENT_REGISTERED:"agreement",ReasoningEventType.UNCERTAINTY_REGISTERED:"uncertainty"}
    def compile(self, reasoning_events, existing):
        events=[]
        for r in reasoning_events:
            kind=self.KIND_MAP.get(r.event_type)
            if not kind: continue
            oid=self._id(kind,r.content)
            batch_created=any(e.knowledge_object_id==oid and e.event_type==KnowledgeEventType.KNOWLEDGE_OBJECT_CREATED for e in events)
            if oid not in existing and not batch_created:
                events.append(KnowledgeEvent(r.session_id,KnowledgeEventType.KNOWLEDGE_OBJECT_CREATED,oid,{"kind":kind,"text":r.content,"speakers":[r.speaker] if r.speaker else [],"source_reasoning_event_ids":[r.event_id],"confidence":self._init(kind),"status":"active","mentions":1}))
            else:
                events.append(KnowledgeEvent(r.session_id,KnowledgeEventType.KNOWLEDGE_OBJECT_REINFORCED,oid,{"speakers":[r.speaker] if r.speaker else [],"source_reasoning_event_ids":[r.event_id]}))
                events.append(KnowledgeEvent(r.session_id,KnowledgeEventType.KNOWLEDGE_CONFIDENCE_UPDATED,oid,{"confidence":min(.95,round(float(existing.get(oid,{}).get("confidence",self._init(kind)))+.08,2))}))
            link=self._link(r,oid,existing)
            if link: events.append(link)
        return events
    def _id(self,kind,text): return f"{kind}-"+hashlib.sha1(f"{kind}:{' '.join(text.lower().split())}".encode()).hexdigest()[:12]
    def _init(self,kind): return {"claim":.50,"question":.80,"assumption":.45,"challenge":.60,"agreement":.55,"uncertainty":.70}.get(kind,.5)
    def _link(self,r,source,objects):
        kind=self.KIND_MAP.get(r.event_type)
        if kind not in {"challenge","agreement"}: return None
        claims=[o for o in objects.values() if o.get("kind")=="claim"]
        if not claims: return None
        target=claims[-1]
        return KnowledgeEvent(r.session_id,KnowledgeEventType.KNOWLEDGE_LINK_CREATED,source,{"from":source,"to":target["id"],"relation":"challenges" if kind=="challenge" else "supports","speaker":r.speaker,"source_reasoning_event_id":r.event_id})
