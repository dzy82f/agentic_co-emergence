from pathlib import Path
from agentic_co_emergence.storage.conversation_history import ConversationHistory
from agentic_co_emergence.core.event_parser import EventParser
from agentic_co_emergence.personas.persona_manager import PersonaManager
from agentic_co_emergence.storage.event_store import GovernanceEventStore, ReasoningEventStore, KnowledgeEventStore, MemoryEventStore, SemanticEventStore
from agentic_co_emergence.engines.knowledge_engine import KnowledgeEngine
from agentic_co_emergence.projections.knowledge_projection import KnowledgeProjector
from agentic_co_emergence.engines.memory_engine import MemoryEngine
from agentic_co_emergence.projections.memory_projection import MemoryProjector
from agentic_co_emergence.core.model_adapter import ChatGPTAdapter
from agentic_co_emergence.models.models import RuntimeResult, TelemetryEvent, TelemetryEventType
from agentic_co_emergence.core.policy_loader import PolicyLoader
from agentic_co_emergence.core.prompt_builder import PromptBuilder
from agentic_co_emergence.core.prompt_compiler import PromptCompiler
from agentic_co_emergence.core.protocol_loader import ProtocolLoader
from agentic_co_emergence.engines.reasoning_engine import ReasoningEngine
from agentic_co_emergence.projections.reasoning_projection import ReasoningProjector
from agentic_co_emergence.engines.semantic_graph_engine import SemanticGraphEngine
from agentic_co_emergence.projections.semantic_graph_projection import SemanticGraphProjector
from agentic_co_emergence.projections.state_projection import StateProjection
from agentic_co_emergence.storage.telemetry_store import TelemetryStore
from agentic_co_emergence.core.transition_engine import TransitionEngine
from agentic_co_emergence.core.validator import Validator

class RuntimeController:
    def __init__(self, session_id, storage_dir: str | Path="runtime_data", policy_path: str | Path | None=None):
        self.session_id=session_id; self.storage_dir=Path(storage_dir); self.policy=PolicyLoader(policy_path).load()
        self.memory_space_id=self.policy.get("memory_space_id","tychevia-organisational-memory")
        self.governance_store=GovernanceEventStore(session_id,self.storage_dir/"governance_events")
        self.reasoning_store=ReasoningEventStore(session_id,self.storage_dir/"reasoning_events")
        self.knowledge_store=KnowledgeEventStore(session_id,self.storage_dir/"knowledge_events")
        self.memory_store=MemoryEventStore(self.memory_space_id,self.storage_dir/"memory_events")
        self.semantic_store=SemanticEventStore(self.memory_space_id,self.storage_dir/"semantic_events")
        self.telemetry_store=TelemetryStore(session_id,self.storage_dir/"telemetry")
        self.projector=StateProjection(self.policy); self.reasoning_projector=ReasoningProjector(); self.knowledge_projector=KnowledgeProjector(); self.memory_projector=MemoryProjector(); self.semantic_projector=SemanticGraphProjector()
        self.protocol_loader=ProtocolLoader(self.policy); self.persona_manager=PersonaManager(); self.prompt_builder=PromptBuilder(); self.model_adapter=ChatGPTAdapter(); self.parser=EventParser(); self.validator=Validator(self.policy); self.transition_engine=TransitionEngine(self.policy)
        self.reasoning_engine=ReasoningEngine(); self.knowledge_engine=KnowledgeEngine(); self.memory_engine=MemoryEngine(); self.semantic_engine=SemanticGraphEngine()

    def run_next_step(self,user_input=None):
        ge=[]; re=[]; ke=[]; me=[]; se=[]; te=[]
        p=self._project()
        if user_input:
            ev=self.transition_engine.events_for_user_input(p,user_input); self.governance_store.append_many(ev); ge.extend(ev); p=self._project()
        protocols=self.protocol_loader.load_for_state(p)
        te.append(TelemetryEvent(self.session_id,TelemetryEventType.PROTOCOLS_LOADED,{"protocols":list(protocols.keys()),"state":p.state.value}))
        prompt=PromptCompiler(self.prompt_builder, self.governance_store, self._project_semantic()).compile(p, protocols); te.append(TelemetryEvent(self.session_id,TelemetryEventType.PROMPT_BUILT,{"state":p.state.value,"length":len(prompt)}))
        raw=self.model_adapter.call(prompt,p); te.append(TelemetryEvent(self.session_id,TelemetryEventType.MODEL_OUTPUT_PROPOSED,{"content":raw,"state":p.state.value}))
        proposed=self.parser.parse_model_output(raw,p); val=self.validator.validate(proposed,p)
        if not val.ok:
            te.append(TelemetryEvent(self.session_id,TelemetryEventType.VALIDATION_FAILED,{"reason":val.reason,"state":p.state.value}))
            rej=self.transition_engine.event_for_rejected_output(p,proposed,val.reason); self.governance_store.append(rej); ge.append(rej); self.telemetry_store.append_many(te)
            return self._result("rejected",raw,val.reason,ge,re,ke,me,se,te)
        te.append(TelemetryEvent(self.session_id,TelemetryEventType.VALIDATION_PASSED,{"state":p.state.value}))
        accepted=self.transition_engine.events_for_accepted_output(p,proposed); self.governance_store.append_many(accepted); ge.extend(accepted)
        for ev in accepted:
            extracted=self.reasoning_engine.extract_from_governance_event(ev)
            if extracted: self.reasoning_store.append_many(extracted); re.extend(extracted)
        te.append(TelemetryEvent(self.session_id,TelemetryEventType.REASONING_EXTRACTED,{"count":len(re)}))
        if re:
            kev=self.knowledge_engine.compile(re,self._project_knowledge().objects); self.knowledge_store.append_many(kev); ke.extend(kev)
        te.append(TelemetryEvent(self.session_id,TelemetryEventType.KNOWLEDGE_COMPILED,{"count":len(ke)}))
        if self._project().state.value=="ARCHIVE":
            mev=self.memory_engine.update_memory(self.memory_space_id,self.session_id,self._project_knowledge(),self._project_memory()); self.memory_store.append_many(mev); me.extend(mev)
            sev=self.semantic_engine.update_graph(self.memory_space_id,self._project_memory(),self._project_semantic()); self.semantic_store.append_many(sev); se.extend(sev)
        te.append(TelemetryEvent(self.session_id,TelemetryEventType.MEMORY_UPDATED,{"count":len(me)}))
        te.append(TelemetryEvent(self.session_id,TelemetryEventType.SEMANTIC_GRAPH_UPDATED,{"count":len(se)}))
        self.telemetry_store.append_many(te)
        return self._result("accepted",raw,None,ge,re,ke,me,se,te)

    def _result(self,status,output,reason,ge,re,ke,me,se,te):
        return RuntimeResult(status,self._project().to_dict(),self._project_reasoning().to_dict(),self._project_knowledge().to_dict(),self._project_memory().to_dict(),self._project_semantic().to_dict(),[e.to_dict() for e in ge],[e.to_dict() for e in re],[e.to_dict() for e in ke],[e.to_dict() for e in me],[e.to_dict() for e in se],[e.to_dict() for e in te],output,reason)

    def _project(self): return self.projector.from_events(self.session_id,self.governance_store.load())
    def _project_reasoning(self): return self.reasoning_projector.from_events(self.session_id,self.reasoning_store.load())
    def _project_knowledge(self): return self.knowledge_projector.from_events(self.session_id,self.knowledge_store.load())
    def _project_memory(self): return self.memory_projector.from_events(self.memory_space_id,self.memory_store.load())
    def _project_semantic(self): return self.semantic_projector.from_events(self.memory_space_id,self.semantic_store.load())
    def reset_session(self): self.governance_store.reset(); self.reasoning_store.reset(); self.knowledge_store.reset(); self.telemetry_store.reset()
    def reset_memory(self): self.memory_store.reset(); self.semantic_store.reset()
