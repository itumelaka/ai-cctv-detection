import json
from pathlib import Path
from typing import Any
from urllib.parse import quote
from app.config import settings

BASE_DIR = Path(__file__).resolve().parents[1]
CAMERAS_CONFIG_FILE = BASE_DIR / "config" / "cameras.json"


def load_cameras() -> list[dict[str, Any]]:
    if not CAMERAS_CONFIG_FILE.exists():
        return []

    with CAMERAS_CONFIG_FILE.open("r", encoding="utf-8") as file:
        cameras = json.load(file)

    return cameras


def list_enabled_cameras() -> list[dict[str, Any]]:
    return [
        camera for camera in load_cameras()
        if camera.get("enabled", True)
    ]


def get_camera_by_id(camera_id: str) -> dict[str, Any]:
    for camera in load_cameras():
        if camera.get("id") == camera_id:
            return camera

    raise KeyError(f"Camera not found: {camera_id}")


def _camera_channel(camera: dict[str, Any], channel_override: str | None = None) -> str:
    return str(channel_override or camera.get("channel", "102"))


def build_rtsp_url(
    camera: dict[str, Any],
    channel_override: str | None = None,
) -> str:
    username = quote(settings.cctv_username, safe="")
    password = quote(settings.cctv_password, safe="")

    host = camera["host"]
    port = camera.get("port", 554)
    channel = _camera_channel(camera, channel_override=channel_override)

    return (
        f"rtsp://{username}:{password}"
        f"@{host}:{port}"
        f"/Streaming/Channels/{channel}"
    )


def build_masked_rtsp_url(
    camera: dict[str, Any],
    channel_override: str | None = None,
) -> str:
    username = quote(settings.cctv_username, safe="")

    host = camera["host"]
    port = camera.get("port", 554)
    channel = _camera_channel(camera, channel_override=channel_override)

    return (
        f"rtsp://{username}:********"
        f"@{host}:{port}"
        f"/Streaming/Channels/{channel}"
    )
