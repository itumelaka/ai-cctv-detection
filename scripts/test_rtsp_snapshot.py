import os
from pathlib import Path
from urllib.parse import quote

import cv2
from dotenv import load_dotenv


def build_rtsp_url() -> str:
    host = os.getenv("CAMERA_HOST", "").strip()
    port = os.getenv("CAMERA_PORT", "554").strip()
    username = os.getenv("CAMERA_USERNAME", "").strip()
    password = os.getenv("CAMERA_PASSWORD", "").strip()
    channel = os.getenv("CAMERA_CHANNEL", "102").strip()

    if not host:
        raise ValueError("CAMERA_HOST is missing in .env")

    if not username:
        raise ValueError("CAMERA_USERNAME is missing in .env")

    if not password:
        raise ValueError("CAMERA_PASSWORD is missing in .env")

    safe_username = quote(username, safe="")
    safe_password = quote(password, safe="")

    return f"rtsp://{safe_username}:{safe_password}@{host}:{port}/Streaming/Channels/{channel}"


def main() -> None:
    load_dotenv()

    output_path = Path(os.getenv("SNAPSHOT_OUTPUT", "outputs/rtsp_test_snapshot.jpg"))
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rtsp_url = build_rtsp_url()

    print("Connecting to RTSP stream...")
    print("Camera host:", os.getenv("CAMERA_HOST"))
    print("Camera channel:", os.getenv("CAMERA_CHANNEL", "102"))

    cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)

    if not cap.isOpened():
        print("ERROR: Cannot open RTSP stream.")
        print("Check camera IP, port 554, username, password, and channel number.")
        return

    print("RTSP stream opened successfully.")

    ret, frame = cap.read()

    if not ret or frame is None:
        print("ERROR: Stream opened but cannot read frame.")
        cap.release()
        return

    height, width = frame.shape[:2]
    cv2.imwrite(str(output_path), frame)

    print("Frame captured successfully.")
    print(f"Frame size: {width}x{height}")
    print(f"Snapshot saved to: {output_path}")

    cap.release()


if __name__ == "__main__":
    main()
