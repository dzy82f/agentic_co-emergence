from agentic_co_emergence.storage.conversation_history import ConversationHistory
from agentic_co_emergence.personas.persona_manager import PersonaManager
from agentic_co_emergence.core.semantic_feedback import SemanticFeedback


class PromptCompiler:
    """
    Compiles all active Tychevia context into one prompt.

    Inputs:
    - runtime projection
    - active protocols
    - current persona
    - recent discussion history
    - semantic memory feedback
    """

    def __init__(self, prompt_builder, governance_store, semantic_projection):
        self.prompt_builder = prompt_builder
        self.governance_store = governance_store
        self.semantic_projection = semantic_projection
        self.persona_manager = PersonaManager()

    def compile(self, projection, protocols):
        persona_text = self.persona_manager.load(projection.current_speaker)
        history_text = ConversationHistory(self.governance_store).recent_turns()
        semantic_text = SemanticFeedback(self.semantic_projection).build()

        base_prompt = self.prompt_builder.build(
            projection,
            protocols,
            persona_text,
            history_text,
        )

        return base_prompt + f"""

SEMANTIC MEMORY FEEDBACK
{semantic_text}

USE OF MEMORY
- Use memory as context, not as authority.
- Do not repeat remembered claims unless you develop, challenge, refine or apply them.
- Prefer unresolved tensions, contested claims and underexplored concepts.
"""
