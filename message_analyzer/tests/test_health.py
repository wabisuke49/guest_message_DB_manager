"""Tests for the service health endpoint."""

import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app


class HealthCheckTests(unittest.TestCase):
    def test_health_check_returns_ok(self) -> None:
        with patch("main.initialize_database") as initialize_database:
            with TestClient(app) as client:
                response = client.get("/health")

        initialize_database.assert_called_once_with()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
