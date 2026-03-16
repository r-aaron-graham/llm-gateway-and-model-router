"""Provider registry for the LLM gateway.

This module exposes functions to register providers and to look them up by name.  When new
providers are added, import and register them here.
"""

from __future__ import annotations

from typing import Dict, Type

from .base import BaseProvider  # noqa: F401
from .local_provider import LocalProvider  # noqa: F401
from .openai_provider import OpenAIProvider  # noqa: F401

# Internal registry mapping provider names to instances
_providers: Dict[str, BaseProvider] = {}


def _register_default_providers():
    """Register built‑in providers at startup."""
    for provider_cls in (LocalProvider, OpenAIProvider):
        provider = provider_cls()
        _providers[provider.name] = provider


def get_provider(name: str) -> BaseProvider | None:
    """Retrieve a provider by name, returning None if not found."""
    return _providers.get(name)


def list_providers() -> Dict[str, BaseProvider]:
    """Return all registered providers as a mapping."""
    return dict(_providers)


def register_provider(provider_cls: Type[BaseProvider]) -> None:
    """Register a provider class.  Useful for third‑party extensions."""
    provider = provider_cls()
    _providers[provider.name] = provider


# Initialize default providers when this module is imported
_register_default_providers()
