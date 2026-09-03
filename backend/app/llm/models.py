"""Logical MIDAS model names and selection policy."""

from enum import Enum

from app.llm.config import get_llm_settings


class MIDASModel(str, Enum):
    """Logical model aliases for future purpose-specific routing."""

    DEFAULT = "default"
    PORTFOLIO_QA = "portfolio_qa"
    SCENARIO_ANALYSIS = "scenario_analysis"
    DOCUMENT_IMPORT = "document_import"


# Future: map logical names to LiteLLM identifiers per use case.
_MODEL_POLICY: dict[MIDASModel, str] = {}


def resolve_litellm_model(logical: MIDASModel = MIDASModel.DEFAULT) -> str:
    """Resolve a logical MIDAS model name to a LiteLLM model identifier."""
    settings = get_llm_settings()
    if logical in _MODEL_POLICY:
        return _MODEL_POLICY[logical]
    return settings.default_model
