"""BaseProvider defines the interface that all providers must implement.

Providers encapsulate the logic for interacting with a specific language model backend.
Each provider must declare a `name` property and implement the asynchronous `generate`
method, which takes a prompt and returns a completion.
"""

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from typing import ClassVar


class BaseProvider(ABC):
    """Abstract base class for all providers."""

    #: Human‑readable description of the provider
    description: ClassVar[str] = "Base LLM provider"

    #: Unique name used to reference this provider via the API
    name: ClassVar[str] = "base"

    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """Generate a completion for the given prompt.

        Implementations should respect any provider‑specific configuration (e.g. API keys,
        engine selection) and must return a string containing the model's response.

        :param prompt: The input prompt to process
        :return: The generated text
        """
        raise NotImplementedError