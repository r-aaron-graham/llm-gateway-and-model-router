"""Provider that integrates with the OpenAI API.

This implementation is a stub that demonstrates how you could interact with a remote
language model provider using an HTTP client.  It requires an API key to be set via
the `OPENAI_API_KEY` environment variable.  The actual call is commented out
because this environment may not have network access.
"""

from __future__ import annotations

import os
from typing import ClassVar

import httpx

from .base import BaseProvider


class OpenAIProvider(BaseProvider):
    """Provider for the OpenAI completion API."""

    name: ClassVar[str] = "openai"
    description: ClassVar[str] = "OpenAI API provider"

    _api_key_env: ClassVar[str] = "OPENAI_API_KEY"
    _api_url: ClassVar[str] = "https://api.openai.com/v1/chat/completions"

    async def generate(self, prompt: str) -> str:
        api_key = os.getenv(self._api_key_env)
        if not api_key:
            return "OpenAI API key not configured"

        # Compose the payload for the chat completions endpoint.  See OpenAI docs for details.
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.0,
            "max_tokens": 100,
        }
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        # Use an asynchronous HTTP client to send the request.  This call is commented out
        # because outbound network access is not guaranteed.  Uncomment in a real environment.
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(self._api_url, json=payload, headers=headers)
                response.raise_for_status()
            except Exception as exc:  # noqa: BLE001
                return f"OpenAI API request failed: {exc}"

        # Parse the response JSON and return the generated message.  See OpenAI docs for structure.
        data = response.json()
        try:
            return data["choices"][0]["message"]["content"].strip()
        except Exception as exc:  # noqa: BLE001
            return f"Unexpected OpenAI response: {exc}"