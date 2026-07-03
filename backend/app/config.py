import os
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()


class Settings:
    app_name: str = os.getenv("APP_NAME", "ITU AI CCTV Backend")
    app_env: str = os.getenv("APP_ENV", "development")

    cctv_host: str = os.getenv("CCTV_HOST", "")
    cctv_port: int = int(os.getenv("CCTV_PORT", "554"))
    cctv_username: str = os.getenv("CCTV_USERNAME", "")
    cctv_password: str = os.getenv("CCTV_PASSWORD", "")
    cctv_channel: str = os.getenv("CCTV_CHANNEL", "101")

    yolo_confidence: float = float(os.getenv("YOLO_CONFIDENCE", "0.35"))
    person_event_cooldown_seconds: int = int(os.getenv("PERSON_EVENT_COOLDOWN_SECONDS", "300"))

    @property
    def rtsp_url(self) -> str:
        username = quote(self.cctv_username, safe="")
        password = quote(self.cctv_password, safe="")

        return (
            f"rtsp://{username}:{password}"
            f"@{self.cctv_host}:{self.cctv_port}"
            f"/Streaming/Channels/{self.cctv_channel}"
        )

    @property
    def masked_rtsp_url(self) -> str:
        username = quote(self.cctv_username, safe="")
        return (
            f"rtsp://{username}:********"
            f"@{self.cctv_host}:{self.cctv_port}"
            f"/Streaming/Channels/{self.cctv_channel}"
        )


settings = Settings()
