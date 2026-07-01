from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

class RuntimeState(str, Enum):
    IDLE="IDLE"; STARTUP="STARTUP"; ISSUE_CAPTURE="ISSUE_CAPTURE"; ISSUE_FRAMING="ISSUE_FRAMING"
    DISCUSSION="DISCUSSION"; ROUND_CHECK="ROUND_CHECK"; SYNTHESIS="SYNTHESIS"; REVIEW="REVIEW"; ARCHIVE="ARCHIVE"

class GovernanceEventType(str, Enum):
    SESSION_STARTED="SESSION_STARTED"; ISSUE_CAPTURED="ISSUE_CAPTURED"; ISSUE_FRAMED="ISSUE_FRAMED"
    STATE_CHANGED="STATE_CHANGED"; DISCUSSION_STARTED="DISCUSSION_STARTED"; ROUND_STARTED="ROUND_STARTED"
    ROUND_COMPLETED="ROUND_COMPLETED"; MODEL_OUTPUT_ACCEPTED="MODEL_OUTPUT_ACCEPTED"; MODEL_OUTPUT_REJECTED="MODEL_OUTPUT_REJECTED"
    AGENT_TURN_ACCEPTED="AGENT_TURN_ACCEPTED"; SPEAKER_CHANGED="SPEAKER_CHANGED"
    SYNTHESIS_UNLOCKED="SYNTHESIS_UNLOCKED"; REVIEW_UNLOCKED="REVIEW_UNLOCKED"; SESSION_ARCHIVED="SESSION_ARCHIVED"

class ReasoningEventType(str, Enum):
    CLAIM_REGISTERED="CLAIM_REGISTERED"; QUESTION_REGISTERED="QUESTION_REGISTERED"; ASSUMPTION_REGISTERED="ASSUMPTION_REGISTERED"
    CHALLENGE_REGISTERED="CHALLENGE_REGISTERED"; AGREEMENT_REGISTERED="AGREEMENT_REGISTERED"; UNCERTAINTY_REGISTERED="UNCERTAINTY_REGISTERED"
    HANDOFF_RATIONALE_REGISTERED="HANDOFF_RATIONALE_REGISTERED"

class KnowledgeEventType(str, Enum):
    KNOWLEDGE_OBJECT_CREATED="KNOWLEDGE_OBJECT_CREATED"; KNOWLEDGE_OBJECT_REINFORCED="KNOWLEDGE_OBJECT_REINFORCED"
    KNOWLEDGE_LINK_CREATED="KNOWLEDGE_LINK_CREATED"; KNOWLEDGE_CONFIDENCE_UPDATED="KNOWLEDGE_CONFIDENCE_UPDATED"

class MemoryEventType(str, Enum):
    MEMORY_OBJECT_CREATED="MEMORY_OBJECT_CREATED"; MEMORY_OBJECT_REINFORCED="MEMORY_OBJECT_REINFORCED"
    MEMORY_LINK_CREATED="MEMORY_LINK_CREATED"; MEMORY_CONFIDENCE_UPDATED="MEMORY_CONFIDENCE_UPDATED"; MEMORY_SESSION_INDEXED="MEMORY_SESSION_INDEXED"

class SemanticEventType(str, Enum):
    SEMANTIC_NODE_CREATED="SEMANTIC_NODE_CREATED"; SEMANTIC_NODE_REINFORCED="SEMANTIC_NODE_REINFORCED"
    SEMANTIC_EDGE_CREATED="SEMANTIC_EDGE_CREATED"; SEMANTIC_EDGE_REINFORCED="SEMANTIC_EDGE_REINFORCED"
    SEMANTIC_CLUSTER_CREATED="SEMANTIC_CLUSTER_CREATED"

class TelemetryEventType(str, Enum):
    PROTOCOLS_LOADED="PROTOCOLS_LOADED"; PROMPT_BUILT="PROMPT_BUILT"; MODEL_OUTPUT_PROPOSED="MODEL_OUTPUT_PROPOSED"
    VALIDATION_PASSED="VALIDATION_PASSED"; VALIDATION_FAILED="VALIDATION_FAILED"; REASONING_EXTRACTED="REASONING_EXTRACTED"
    KNOWLEDGE_COMPILED="KNOWLEDGE_COMPILED"; MEMORY_UPDATED="MEMORY_UPDATED"; SEMANTIC_GRAPH_UPDATED="SEMANTIC_GRAPH_UPDATED"

@dataclass
class GovernanceEvent:
    session_id: str; event_type: GovernanceEventType; payload: Dict[str, Any]=field(default_factory=dict)
    event_id: str=field(default_factory=lambda: str(uuid4()))
    timestamp: str=field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    def to_dict(self): d=asdict(self); d["event_type"]=self.event_type.value; return d
    @classmethod
    def from_dict(cls, data): data=dict(data); data["event_type"]=GovernanceEventType(data["event_type"]); return cls(**data)

@dataclass
class ReasoningEvent:
    session_id: str; event_type: ReasoningEventType; speaker: Optional[str]; content: str
    source_governance_event_id: Optional[str]=None; payload: Dict[str, Any]=field(default_factory=dict)
    event_id: str=field(default_factory=lambda: str(uuid4()))
    timestamp: str=field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    def to_dict(self): d=asdict(self); d["event_type"]=self.event_type.value; return d
    @classmethod
    def from_dict(cls, data): data=dict(data); data["event_type"]=ReasoningEventType(data["event_type"]); return cls(**data)

@dataclass
class KnowledgeEvent:
    session_id: str; event_type: KnowledgeEventType; knowledge_object_id: Optional[str]=None; payload: Dict[str, Any]=field(default_factory=dict)
    event_id: str=field(default_factory=lambda: str(uuid4()))
    timestamp: str=field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    def to_dict(self): d=asdict(self); d["event_type"]=self.event_type.value; return d
    @classmethod
    def from_dict(cls, data): data=dict(data); data["event_type"]=KnowledgeEventType(data["event_type"]); return cls(**data)

@dataclass
class MemoryEvent:
    memory_space_id: str; event_type: MemoryEventType; memory_object_id: Optional[str]=None; payload: Dict[str, Any]=field(default_factory=dict)
    event_id: str=field(default_factory=lambda: str(uuid4()))
    timestamp: str=field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    def to_dict(self): d=asdict(self); d["event_type"]=self.event_type.value; return d
    @classmethod
    def from_dict(cls, data): data=dict(data); data["event_type"]=MemoryEventType(data["event_type"]); return cls(**data)

@dataclass
class SemanticEvent:
    memory_space_id: str; event_type: SemanticEventType; semantic_id: Optional[str]=None; payload: Dict[str, Any]=field(default_factory=dict)
    event_id: str=field(default_factory=lambda: str(uuid4()))
    timestamp: str=field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    def to_dict(self): d=asdict(self); d["event_type"]=self.event_type.value; return d
    @classmethod
    def from_dict(cls, data): data=dict(data); data["event_type"]=SemanticEventType(data["event_type"]); return cls(**data)

@dataclass
class TelemetryEvent:
    session_id: str; event_type: TelemetryEventType; payload: Dict[str, Any]=field(default_factory=dict)
    event_id: str=field(default_factory=lambda: str(uuid4()))
    timestamp: str=field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    def to_dict(self): d=asdict(self); d["event_type"]=self.event_type.value; return d

@dataclass
class Issue:
    raw_user_question: str=""; working_title: str=""; framed_question: str=""; domain: str=""; constraints: List[str]=field(default_factory=list); status: str="empty"

@dataclass
class RuntimeProjection:
    session_id: str; state: RuntimeState=RuntimeState.IDLE; issue: Issue=field(default_factory=Issue)
    current_speaker: Optional[str]=None; previous_speaker: Optional[str]=None
    current_round: int=0; turns_in_current_round: int=0; total_turns: int=0; completed_rounds: int=0; minimum_rounds: int=3
    synthesis_allowed: bool=False; review_allowed: bool=False; facilitator_silent: bool=True; handoff_required: bool=True
    active_agents: List[str]=field(default_factory=lambda:["Tenzing","Aletheia","Joan","Alison","Lyla","Ada","Sael","Synaia","Harry"])
    governance_event_count: int=0; violations: List[Dict[str, Any]]=field(default_factory=list)
    def to_dict(self): d=asdict(self); d["state"]=self.state.value; return d

@dataclass
class ReasoningProjection:
    session_id: str
    claims: List[Dict[str, Any]]=field(default_factory=list); questions: List[Dict[str, Any]]=field(default_factory=list)
    assumptions: List[Dict[str, Any]]=field(default_factory=list); challenges: List[Dict[str, Any]]=field(default_factory=list)
    agreements: List[Dict[str, Any]]=field(default_factory=list); uncertainties: List[Dict[str, Any]]=field(default_factory=list)
    handoff_rationales: List[Dict[str, Any]]=field(default_factory=list)
    def to_dict(self): return asdict(self)

@dataclass
class KnowledgeProjection:
    session_id: str; objects: Dict[str, Dict[str, Any]]=field(default_factory=dict); links: List[Dict[str, Any]]=field(default_factory=list)
    def to_dict(self): return asdict(self)

@dataclass
class MemoryProjection:
    memory_space_id: str; objects: Dict[str, Dict[str, Any]]=field(default_factory=dict); links: List[Dict[str, Any]]=field(default_factory=list); indexed_sessions: List[str]=field(default_factory=list)
    def to_dict(self): return asdict(self)

@dataclass
class SemanticGraphProjection:
    memory_space_id: str; nodes: Dict[str, Dict[str, Any]]=field(default_factory=dict); edges: Dict[str, Dict[str, Any]]=field(default_factory=dict); clusters: Dict[str, Dict[str, Any]]=field(default_factory=dict)
    def to_dict(self): return asdict(self)

@dataclass
class ProposedModelEvent:
    speaker: Optional[str]; content: str; handoff_to: Optional[str]=None; attempted_synthesis: bool=False; attempted_review: bool=False; raw_text: str=""

@dataclass
class ValidationResult:
    ok: bool; reason: str=""

@dataclass
class RuntimeResult:
    status: str
    projection: Dict[str, Any]; reasoning_projection: Dict[str, Any]; knowledge_projection: Dict[str, Any]; memory_projection: Dict[str, Any]; semantic_projection: Dict[str, Any]
    governance_events: List[Dict[str, Any]]; reasoning_events: List[Dict[str, Any]]; knowledge_events: List[Dict[str, Any]]; memory_events: List[Dict[str, Any]]; semantic_events: List[Dict[str, Any]]; telemetry_events: List[Dict[str, Any]]
    output: Optional[str]=None; reason: Optional[str]=None
