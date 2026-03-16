"""
Entry point for the LLM gateway service.  This file defines the FastAPI application
and configures the provider registry and routing logic.

Run the server with:

    uvicorn main:app --reload
"""

from __future__ import annotations

import asyncio
import os
from typing import Optional, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from providers import get_provider, list_providers


class GenerateRequest(BaseModel):
    """Schema for a text generation request."""

    prompt: str = Field(..., description="The prompt to send to the language model")
    provider: Optional[str] = Field(
        None,
        description="Optional provider name.  If omitted, the default provider is used."
    )


class GenerateResponse(BaseModel):
    """Schema for the generation response."""

    provider: str
    completion: str


app = FastAPI(title="LLM Gateway", version="0.1.0")

# Allow CORS for simple local experiments.  In production you should restrict this.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/providers", response_model=Dict[str, str])
def providers() -> Dict[str, str]:
    """Return a mapping of available providers to human‑readable names."""
    return {name: provider.description for name, provider in list_providers().items()}


@app.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest) -> GenerateResponse:
    """Generate text using the specified provider."""
    provider_name = req.provider or os.environ.get("DEFAULT_PROVIDER", "local")
    provider = get_provider(provider_name)
    if provider is None:
        raise HTTPException(status_code=404, detail=f"Provider '{provider_name}' not found")

    try:
        completion = await provider.generate(req.prompt)
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Provider timed out")
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Provider error: {exc}")

    return GenerateResponse(provider=provider_name, completion=completion)