# LLM Gateway and Model Router

This repository provides a **reference implementation** of an LLM gateway – a unified entry point for
serving large language model requests across multiple providers.  The goal is to abstract away
provider‑specific details and expose a single API for downstream applications.  Under the hood the
gateway can route requests to different engines (e.g. OpenAI, Anthropic, local models) based on
configuration, cost/latency constraints, or runtime parameters.  It also demonstrates how to add
basic guardrails such as retry logic, timeout handling, and provider fallbacks.

## Features

* FastAPI application exposing a `/generate` endpoint for text generation.
* Provider registry with a base interface and pluggable implementations.
* Sample `OpenAIProvider` and `LocalProvider` demonstrating how to integrate remote APIs and local models.
* Routing logic that selects a provider based on a query parameter or falls back to a default.
* Simple retry and timeout handling to improve robustness.
* Typed models using Pydantic for request and response validation.

## Getting started

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the API server locally:

```bash
uvicorn main:app --reload
```

3. Send a request via cURL or your favourite HTTP client:

```bash
curl -X POST http://localhost:8000/generate \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Write a haiku about modular data centres", "provider": "local"}'
```

### Environment variables

Some providers may require API keys or other credentials.  If you wish to enable the
`OpenAIProvider`, set the `OPENAI_API_KEY` environment variable before running the server.

```bash
export OPENAI_API_KEY=your-token
```

### Extending the gateway

To add a new provider, subclass `providers.base.BaseProvider` and implement the `generate` method.
Then register your provider in `providers.__init__.py`.  The gateway will automatically make it
available via the `/generate` endpoint.

## License

This project is provided for educational purposes and is not production‑ready.  You are free to
adapt, extend, or incorporate parts of it into your own projects under the MIT license.