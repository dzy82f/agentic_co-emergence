import hashlib
import re
from agentic_co_emergence.models.models import SemanticEvent, SemanticEventType

class SemanticGraphEngine:
    """
    Promotes organisational memory into a semantic graph.
    Edges are richer than raw memory links:
    - question -> claim = answered_by
    - claim -> assumption = depends_on
    - challenge -> claim = challenges
    - agreement -> claim = supports
    - uncertainty -> question = raises
    """
    def update_graph(self, memory_space_id, memory_projection, semantic_projection):
        events=[]
        for oid,obj in memory_projection.objects.items():
            concepts=self._concepts(obj["text"])
            if oid not in semantic_projection.nodes and not self._node_created(oid,events):
                events.append(SemanticEvent(memory_space_id,SemanticEventType.SEMANTIC_NODE_CREATED,oid,{"kind":obj["kind"],"text":obj["text"],"confidence":obj.get("confidence",.5),"mentions":obj.get("mentions",1),"sessions":obj.get("sessions",[]),"concepts":concepts}))
            else:
                events.append(SemanticEvent(memory_space_id,SemanticEventType.SEMANTIC_NODE_REINFORCED,oid,{"confidence":obj.get("confidence",.5),"mentions":obj.get("mentions",1),"sessions":obj.get("sessions",[])}))
        # Preserve explicit memory links
        for link in memory_projection.links:
            eid=self._edge_id(link.get("from"),link.get("to"),link.get("relation"))
            if eid not in semantic_projection.edges and not self._edge_created(eid,events):
                events.append(SemanticEvent(memory_space_id,SemanticEventType.SEMANTIC_EDGE_CREATED,eid,{"from":link.get("from"),"to":link.get("to"),"relation":link.get("relation"),"source":"memory_link","sessions":[link.get("session_id")] if link.get("session_id") else [],"weight":1}))
            else:
                events.append(SemanticEvent(memory_space_id,SemanticEventType.SEMANTIC_EDGE_REINFORCED,eid,{"weight":1}))
        # Infer semantic edges
        events.extend(self._infer_edges(memory_space_id, memory_projection, semantic_projection, events))
        events.extend(self._clusters(memory_space_id, memory_projection, semantic_projection, events))
        return events

    def _infer_edges(self, space, memory, semantic, batch):
        ev=[]
        objects=list(memory.objects.values())
        claims=[o for o in objects if o["kind"]=="claim"]
        questions=[o for o in objects if o["kind"]=="question"]
        assumptions=[o for o in objects if o["kind"]=="assumption"]
        uncertainties=[o for o in objects if o["kind"]=="uncertainty"]
        for q in questions:
            target=self._best_overlap(q,claims)
            if target: ev += self._edge(space,q["id"],target["id"],"answered_by","inferred",semantic,batch+ev)
        for c in claims:
            target=self._best_overlap(c,assumptions)
            if target: ev += self._edge(space,c["id"],target["id"],"depends_on","inferred",semantic,batch+ev)
        for u in uncertainties:
            target=self._best_overlap(u,questions)
            if target: ev += self._edge(space,u["id"],target["id"],"raises","inferred",semantic,batch+ev)
        return ev

    def _clusters(self, space, memory, semantic, batch):
        ev=[]
        concept_map={}
        for obj in memory.objects.values():
            for c in self._concepts(obj["text"]):
                concept_map.setdefault(c,[]).append(obj["id"])
        for concept, node_ids in concept_map.items():
            if len(node_ids) >= 2:
                cid="cluster-"+hashlib.sha1(concept.encode()).hexdigest()[:10]
                if cid not in semantic.clusters and not any(e.semantic_id==cid for e in batch+ev):
                    ev.append(SemanticEvent(space,SemanticEventType.SEMANTIC_CLUSTER_CREATED,cid,{"concept":concept,"node_ids":node_ids,"size":len(node_ids)}))
        return ev

    def _edge(self,space,src,dst,rel,source,semantic,batch):
        eid=self._edge_id(src,dst,rel)
        if eid not in semantic.edges and not self._edge_created(eid,batch):
            return [SemanticEvent(space,SemanticEventType.SEMANTIC_EDGE_CREATED,eid,{"from":src,"to":dst,"relation":rel,"source":source,"sessions":[],"weight":1})]
        return [SemanticEvent(space,SemanticEventType.SEMANTIC_EDGE_REINFORCED,eid,{"weight":1})]

    def _best_overlap(self,source,candidates):
        s=set(self._concepts(source["text"]))
        best=None; score=0
        for c in candidates:
            overlap=len(s & set(self._concepts(c["text"])))
            if overlap>score:
                best=c; score=overlap
        return best if score>0 else (candidates[0] if candidates else None)

    def _concepts(self,text):
        stop={"the","a","an","and","or","of","to","in","by","when","what","would","with","as","we","are","is","be","than","inside","one","rather","not","yet","how","if","that","this","from","must","can","should"}
        words=re.findall(r"[a-zA-Z][a-zA-Z\-]+",text.lower())
        return sorted({w for w in words if len(w)>4 and w not in stop})[:12]

    def _node_created(self,oid,events): return any(e.semantic_id==oid and e.event_type==SemanticEventType.SEMANTIC_NODE_CREATED for e in events)
    def _edge_created(self,eid,events): return any(e.semantic_id==eid and e.event_type==SemanticEventType.SEMANTIC_EDGE_CREATED for e in events)
    def _edge_id(self,src,dst,rel): return "edge-"+hashlib.sha1(f"{src}:{rel}:{dst}".encode()).hexdigest()[:14]
