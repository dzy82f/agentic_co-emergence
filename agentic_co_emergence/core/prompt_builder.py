from agentic_co_emergence.models.models import RuntimeState

class PromptBuilder:
    def build(self, projection, protocols, persona_text: str = "", conversation_history: str = ""):
        issue = projection.issue.framed_question or projection.issue.raw_user_question or "[No issue captured]"
        protocol_block = "\n\n".join(f"## {name}\n{content}" for name, content in protocols.items())
        base = f"""TYCHEVIA LIVE PERSONA RUNTIME PROMPT

State: {projection.state.value}
Issue: {issue}
Round: {projection.current_round}
Completed rounds: {projection.completed_rounds}
Turns in current round: {projection.turns_in_current_round}
Current speaker: {projection.current_speaker}
Previous speaker: {projection.previous_speaker}
Synthesis allowed: {projection.synthesis_allowed}
Review allowed: {projection.review_allowed}

Active agents:
{", ".join(projection.active_agents)}

Active protocols:
{", ".join(protocols.keys())}

CURRENT PERSONA
{persona_text or "[No persona loaded for this state.]"}

RECENT DISCUSSION HISTORY
{conversation_history or "[No prior discussion turns.]"}

GENERAL RULES
- Obey the current state only.
- Do not invoke inactive protocols.
- Do not synthesise unless synthesis_allowed is true.
- Do not review unless review_allowed is true.
- Do not explain the runtime.
"""
        if projection.state == RuntimeState.DISCUSSION:
            base += f"""

DISCUSSION OUTPUT RULES
- Only {projection.current_speaker} may speak.
- Begin exactly with: {projection.current_speaker}:
- Make a distinct contribution from the persona above.
- Do not merely restate prior speakers.
- Include exactly one labelled reasoning line using one of:
  CLAIM:
  QUESTION:
  ASSUMPTION:
  CHALLENGE:
  AGREEMENT:
  UNCERTAINTY:
- End with exactly:
  HANDOFF: <agent name>
"""
        elif projection.state == RuntimeState.ISSUE_FRAMING:
            base += "\nISSUE FRAMING OUTPUT RULES\n- Frame the issue clearly.\n- Identify tensions, constraints and what success would look like.\n"
        elif projection.state == RuntimeState.ROUND_CHECK:
            base += "\nROUND CHECK OUTPUT RULES\n- Briefly acknowledge round completion.\n- Do not synthesise.\n- Do not review.\n"
        elif projection.state == RuntimeState.SYNTHESIS:
            base += "\nSYNTHESIS OUTPUT RULES\n- Produce a synthesis of the completed discussion.\n"
        elif projection.state == RuntimeState.REVIEW:
            base += "\nREVIEW OUTPUT RULES\n- Review the process and quality of the discussion.\n"
        else:
            base += "\nSTATE OUTPUT RULES\n- Produce the next legal runtime output for this state.\n"
        return base + "\n\nACTIVE PROTOCOL TEXT\n" + protocol_block
