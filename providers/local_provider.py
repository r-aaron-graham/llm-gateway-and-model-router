"""A simple provider that generates deterministic responses without calling external services.

This provider is intended for demonstration purposes and local development.  It uses a
very simple heuristic to produce a response and does not rely on any third‑party APIs.
"""

from __future__ import annotations

from typing import ClassVar

from .base import BaseProvider


class LocalProvider(BaseProvider):
    """Local provider returning canned responses for demonstration."""

    name: ClassVar[str] = "local"
    description: ClassVar[str] = "Local mock model that echoes prompts"

    async def generate(self, prompt: str) -> str:
        # A naive implementation that echoes the prompt and adds a suffix.  In a real
        # application you could load a local Hugging Face model here.
        return f"[LOCAL RESPONSE] {prompt[::-1]}"