"""Robolytics Python SDK.

Generated from buf.build/beaglabs/robolytics.

Usage:
    import os
    from robolytics import Client, MissionStatus

    client = Client(
        client_id=os.environ["CHAVETA_CLIENT_ID"],
        client_secret=os.environ["CHAVETA_CLIENT_SECRET"],
    )

    client.scenario_started("warehouse-nav-v2", domain="warehouse")
    client.mission_completed("warehouse-nav-v2", MissionStatus.SUCCESS,
        {"collision_rate": 0.02, "route_completion_pct": 98.5})
"""

from __future__ import annotations

import time
import uuid
from typing import Optional, Dict

import httpx

# The generated protobuf types from buf:
# In production, these would be compiled from the .proto files.
# The .pyi stubs provide type hints but runtime types come from protobuf.
try:
    from .gen import event_pb2 as pb
except ImportError:
    pb = None  # type: ignore


class MissionStatus:
    UNSPECIFIED = 0
    SUCCESS = 1
    FAILURE = 2
    TIMEOUT = 3
    INTERVENTION = 4


class Client:
    """Robolytics client for sending events to the Chaveta ingest API."""

    def __init__(
        self,
        base_url: str = "https://chaveta.beaglabs.com",
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        access_token: Optional[str] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self._client_id = client_id
        self._client_secret = client_secret
        self._access_token = access_token
        self._http = httpx.Client(timeout=30.0)

    def _token(self) -> str:
        if self._access_token:
            return self._access_token
        if not self._client_id or not self._client_secret:
            raise ValueError("Provide client_id/client_secret or access_token")
        resp = self._http.post(
            f"{self.base_url}/api/auth/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": self._client_id,
                "client_secret": self._client_secret,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        self._access_token = data["access_token"]
        return self._access_token

    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self._token()}"}

    def _send(self, event: dict) -> dict:
        resp = self._http.post(
            f"{self.base_url}/api/v1/ingest",
            headers={**self._headers(), "Content-Type": "application/json"},
            json=event,
        )
        resp.raise_for_status()
        return resp.json()

    def _event_id(self) -> str:
        return str(uuid.uuid4())

    def _ts(self) -> int:
        return int(time.time() * 1_000_000_000)

    def scenario_started(
        self,
        scenario_id: str,
        *,
        domain: str = "",
        scenario_name: str = "",
        software_version: str = "",
        seed: str = "",
        repo: str = "",
        **params: str,
    ) -> dict:
        """Send a ScenarioStarted event."""
        event: dict = {
            "eventId": self._event_id(),
            "timestampNs": self._ts(),
            "source": "python-sdk",
            "sourceVersion": "1.0.0",
            "scenarioStarted": {
                "scenarioId": scenario_id,
                "scenarioName": scenario_name,
                "domain": domain,
                "softwareVersion": software_version,
                "seed": seed,
                "repo": repo,
                "params": params,
            },
        }
        return self._send(event)

    def mission_completed(
        self,
        scenario_id: str,
        status: int = MissionStatus.SUCCESS,
        metrics: Optional[Dict[str, float]] = None,
        *,
        mission_id: str = "",
        software_version: str = "",
    ) -> dict:
        """Send a MissionCompleted event with arbitrary metrics."""
        event: dict = {
            "eventId": self._event_id(),
            "timestampNs": self._ts(),
            "source": "python-sdk",
            "sourceVersion": "1.0.0",
            "missionCompleted": {
                "scenarioId": scenario_id,
                "missionId": mission_id,
                "status": status,
                "metrics": metrics or {},
                "softwareVersion": software_version,
            },
        }
        return self._send(event)

    def obstacle_encountered(
        self,
        scenario_id: str,
        obstacle_class: str,
        *,
        collision: bool = False,
        relative_speed: float = 0.0,
        mission_id: str = "",
        step: int = 0,
        video_r2_key: str = "",
    ) -> dict:
        """Send an ObstacleEncountered event."""
        event: dict = {
            "eventId": self._event_id(),
            "timestampNs": self._ts(),
            "source": "python-sdk",
            "sourceVersion": "1.0.0",
            "obstacleEncountered": {
                "scenarioId": scenario_id,
                "missionId": mission_id,
                "step": step,
                "obstacleClass": obstacle_class,
                "collision": collision,
                "relativeSpeed": relative_speed,
                "videoR2Key": video_r2_key,
            },
        }
        return self._send(event)

    def object_identified(
        self,
        scenario_id: str,
        class_name: str,
        *,
        confidence: float = 0.0,
        mission_id: str = "",
    ) -> dict:
        """Send an ObjectIdentified event."""
        event: dict = {
            "eventId": self._event_id(),
            "timestampNs": self._ts(),
            "source": "python-sdk",
            "sourceVersion": "1.0.0",
            "objectIdentified": {
                "scenarioId": scenario_id,
                "missionId": mission_id,
                "className": class_name,
                "confidence": confidence,
            },
        }
        return self._send(event)
