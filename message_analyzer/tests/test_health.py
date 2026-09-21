"""Tests for the service health endpoint."""

import unittest

from fastapi.testclient import TestClient

from main import app


class HealthCheckTests(unittest.TestCase):
    def test_health_check_returns_ok(self) -> None:
        client = TestClient(app)

        response = client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
