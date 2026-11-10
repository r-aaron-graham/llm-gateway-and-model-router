import unittest
from fastapi.testclient import TestClient
from main import app

class GatewayTests(unittest.TestCase):
    def test_local_generation_and_unknown_provider(self):
        with TestClient(app) as client:
            self.assertIn("local", client.get("/providers").json())
            response = client.post("/generate", json={"prompt": "abc", "provider": "local"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["completion"], "[LOCAL RESPONSE] cba")
            self.assertEqual(client.post("/generate", json={"prompt": "abc", "provider": "missing"}).status_code, 404)
