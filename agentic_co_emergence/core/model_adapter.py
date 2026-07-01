"""
ChatGPTAdapter for Tychevia Runtime v6.

This replaces the old LocalEchoModelAdapter.

Requirements:
    pip install openai python-dotenv

Environment:
    OPENAI_API_KEY=...
    TYCHEVIA_MODEL=gpt-5.5          # optional
    TYCHEVIA_TEMPERATURE=0.7        # optional

The adapter uses the OpenAI Responses API via the official openai Python SDK.
"""

from __future__ import annotations

import os
from typing import Optional

try:
    from dotenv import load_dotenv
except ImportError:  # python-dotenv is helpful but not mandatory
    load_dotenv = None

try:
    from openai import OpenAI
except ImportError:  # allows structure tests without optional API dependency
    OpenAI = None

MODEL_CAPABILITIES = {
    "gpt-5.5": {"supports_temperature": False},
    "gpt-5": {"supports_temperature": False},
    "gpt-4.1": {"supports_temperature": True},
    "gpt-4o": {"supports_temperature": True},
}


class ChatGPTAdapter:
    """
    Adapter boundary between the Tychevia Runtime and OpenAI.

    The Runtime should not know about OpenAI-specific details. It sends a prompt
    and receives text. Everything else remains governed by Tychevia.
    """

    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        temperature: Optional[float] = None,
    ):
        if load_dotenv:
            load_dotenv()

        self.model = model or os.getenv("TYCHEVIA_MODEL", "gpt-5.5")
        self.temperature = (
            temperature
            if temperature is not None
            else float(os.getenv("TYCHEVIA_TEMPERATURE", "0.7"))
        )

        if OpenAI is None:
            raise ImportError("openai is required to instantiate ChatGPTAdapter. Install with: pip install openai")
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def call(self, prompt, projection):
        """
        Return a model response as plain text.

        The prompt already contains the active Tychevia state, permitted
        protocols, current speaker, and output rules. This method does not
        decide what is legal. It only asks the model to propose output.
        """

        instructions = self._instructions_for_projection(projection)

        caps = MODEL_CAPABILITIES.get(self.model, {"supports_temperature": False})

        kwargs = {
            "model": self.model,
            "instructions": instructions,
            "input": prompt,
        }

        if caps.get("supports_temperature"):
            kwargs["temperature"] = self.temperature

        response = self.client.responses.create(**kwargs)

        text = getattr(response, "output_text", None)
        if text:
            return text.strip()

        # Defensive fallback for SDK/API response-shape changes.
        try:
            return response.output[0].content[0].text.strip()
        except Exception as exc:
            raise RuntimeError(
                "Could not extract text from OpenAI response. "
                "Inspect the raw response object for SDK/API changes."
            ) from exc

    def _instructions_for_projection(self, projection) -> str:
        if projection.current_speaker:
            speaker_line = (
                f"You are writing only as {projection.current_speaker}. "
                f"Begin exactly with '{projection.current_speaker}:' when in DISCUSSION."
            )
        else:
            speaker_line = "Follow the current Tychevia runtime state exactly."

        return f"""
You are participating in a governed Tychevia Runtime session.

The runtime, not you, owns:
- state transitions
- speaker selection
- round counting
- synthesis permission
- review permission
- archival state

Your task is only to produce the next legal candidate output for the current state.

{speaker_line}

Never synthesise unless the prompt says synthesis is allowed.
Never invoke review unless the prompt says review is allowed.
Never skip the required HANDOFF line during DISCUSSION.
Do not explain the runtime machinery.
""".strip()
