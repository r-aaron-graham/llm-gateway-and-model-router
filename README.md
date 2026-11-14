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

## Deployment verification

Build the reviewer container from the repository root.

```sh
docker build -t reviewer-smoke .
docker run --rm -p 127.0.0.1:8000:8000 reviewer-smoke
```

From another terminal, run `curl --fail http://127.0.0.1:8000/providers`. Expect HTTP 200. Stop the container with Ctrl+C when finished. Use the local provider for verification. Set provider credentials through the runtime environment only when deliberately enabling a live provider. Put access controls and rate limits in front of a shared deployment.

## Reproduce the CI dependency set

Use Python 3.12 on Linux. GitHub Actions and the Docker build apply `requirements.lock` as pip constraints. The file pins resolved runtime and test dependencies. For a local install, add `-c requirements.lock` to the install command above. Verify the installed packages with `python -m pip check`.

When updating dependencies, resolve the runtime and test requirements together in a clean Python 3.12 environment and rerun CI, including the container smoke test.
