from agency_swarm import Agent, ModelSettings
from agency_swarm.tools import IPythonInterpreter
from openai.types.shared import Reasoning
from pathlib import Path

from config import get_default_model, is_openai_provider
from virtual_assistant.tools.ReadFile import ReadFile
from virtual_assistant.tools.WriteFile import WriteFile

_INSTRUCTIONS_PATH = Path(__file__).parent / "instructions.md"


def create_alignment_qa_agent() -> Agent:
    return Agent(
        name="Proposal Alignment QA Agent",
        description="Checks that proposal deck, proposal, quote, and internal scope all sell the same strategy and packages.",
        instructions=_INSTRUCTIONS_PATH.read_text(encoding="utf-8"),
        tools=[IPythonInterpreter, ReadFile, WriteFile],
        model=get_default_model(),
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="medium", summary="auto") if is_openai_provider() else None,
            verbosity="medium" if is_openai_provider() else None,
        ),
    )
