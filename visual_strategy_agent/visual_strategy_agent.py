from agency_swarm import Agent, ModelSettings
from agency_swarm.tools import IPythonInterpreter, WebSearchTool
from openai.types.shared import Reasoning
from pathlib import Path

from config import get_default_model, is_openai_provider
from virtual_assistant.tools.ReadFile import ReadFile
from virtual_assistant.tools.WriteFile import WriteFile

_INSTRUCTIONS_PATH = Path(__file__).parent / "instructions.md"


def create_visual_strategy_agent() -> Agent:
    return Agent(
        name="Visual Strategy Agent",
        description=(
            "Creates proposal visuals, diagrams, strategy maps, roadmap graphics, "
            "buyer journeys, competitor gap matrices, and deck-ready visual concepts."
        ),
        instructions=_INSTRUCTIONS_PATH.read_text(encoding="utf-8"),
        tools=[WebSearchTool(search_context_size="medium"), IPythonInterpreter, ReadFile, WriteFile],
        model=get_default_model(),
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="medium", summary="auto") if is_openai_provider() else None,
            verbosity="medium" if is_openai_provider() else None,
            response_include=["web_search_call.action.sources"] if is_openai_provider() else None,
        ),
        conversation_starters=[
            "Create proposal visuals for a website growth proposal.",
            "Design a competitor gap matrix and roadmap graphic.",
            "Turn this strategy into deck-ready visual concepts.",
        ],
    )
