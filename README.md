# LLM gateway and model router

A FastAPI endpoint with a registry of provider adapters. The local provider
returns a deterministic reversed prompt so the HTTP flow can be demonstrated
without credentials. The registry is loaded from `providers/__init__.py`.

## Run the example

```bash
python -m pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000
curl -X POST http://127.0.0.1:8000/generate -H "Content-Type: application/json" -d '{"prompt":"abc","provider":"local"}'
```

Expected JSON contains `"provider":"local"` and
`"completion":"[LOCAL RESPONSE] cba"`. `GET /providers` lists adapters.
An unknown provider returns HTTP 404.

The OpenAI adapter makes an external request when an API key is configured.
Only the local adapter is covered by the reviewer smoke test. Provider
selection uses the request field or `DEFAULT_PROVIDER`. Cost optimization,
fallbacks, and retries are potential extensions.

## Verify

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

To add an adapter, subclass `providers.base.BaseProvider` and register it
in `providers/__init__.py`.
