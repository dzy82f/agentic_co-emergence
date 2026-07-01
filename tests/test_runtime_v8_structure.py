from pathlib import Path

from agentic_co_emergence.core.adsn_validator import ADSNValidator
from agentic_co_emergence.core.policy_loader import PolicyLoader
from agentic_co_emergence.core.prompt_compiler import PromptCompiler
from agentic_co_emergence.core.prompt_builder import PromptBuilder
from agentic_co_emergence.core.runtime_controller import RuntimeController
from agentic_co_emergence.personas.persona_manager import PersonaManager


def test_packaged_protocols_exist():
    protocol_dir = Path("agentic_co_emergence/protocols")
    assert (protocol_dir / "constitution.md").exists()
    assert (protocol_dir / "adsn_protocol.md").exists()
    assert (protocol_dir / "review_protocol.md").exists()


def test_packaged_personas_exist():
    persona_dir = Path("agentic_co_emergence/personas")
    assert (persona_dir / "Tenzing.md").exists()
    assert (persona_dir / "Harry.md").exists()


def test_default_loaders_use_packaged_resources():
    policy = PolicyLoader().load()
    assert "state_protocols" in policy
    assert "Tenzing" in PersonaManager().load("Tenzing")


def test_adsn_rejects_self_handoff():
    policy = PolicyLoader().load()
    validator = ADSNValidator(policy)
    ok, reason = validator.validate_handoff("Tenzing", "Tenzing", ["Tenzing", "Joan"])
    assert not ok


def test_prompt_types_exist():
    assert PromptCompiler is not None
    assert PromptBuilder is not None


def test_runtime_controller_type_exists():
    assert RuntimeController is not None
