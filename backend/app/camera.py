import os
import time
import cv2
from app.config import settings

def _open_rtsp_stream():
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"
    cap = cv2.VideoCapture(settings.rtsp_url, cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    return cap


def _read_frame_with_retry(cap, max_attempts: int = 30):
    last_frame = None

    for _ in range(max_attempts):
        ok, frame = cap.read()

        if ok and frame is not None:
            last_frame = frame
            break

        time.sleep(0.1)

    return last_frame


def test_rtsp_connection() -> dict:
    if not settings.cctv_host or not settings.cctv_username or not settings.cctv_password:
        return {
            "status": "failed",
            "message": "CCTV configuration is incomplete. Check backend/.env.",
            "camera_host": settings.cctv_host,
            "channel": settings.cctv_channel,
            "rtsp_url": settings.masked_rtsp_url
        }

    cap = _open_rtsp_stream()

    if not cap.isOpened():
        cap.release()
        return {
            "status": "failed",
            "message": "Cannot open RTSP stream.",
            "camera_host": settings.cctv_host,
            "channel": settings.cctv_channel,
            "rtsp_url": settings.masked_rtsp_url
        }

    frame = _read_frame_with_retry(cap)
    cap.release()

    if frame is None:
        return {
            "status": "failed",
            "message": "RTSP stream opened but cannot read frame after retries.",
            "camera_host": settings.cctv_host,
            "channel": settings.cctv_channel,
            "rtsp_url": settings.masked_rtsp_url
        }

    height, width = frame.shape[:2]

    return {
        "status": "connected",
        "message": "RTSP stream is reachable.",
        "camera_host": settings.cctv_host,
        "channel": settings.cctv_channel,
        "frame_width": width,
        "frame_height": height,
        "rtsp_url": settings.masked_rtsp_url
    }


def capture_snapshot_jpeg() -> bytes:
    if not settings.cctv_host or not settings.cctv_username or not settings.cctv_password:
        raise RuntimeError("CCTV configuration is incomplete. Check backend/.env.")

    cap = _open_rtsp_stream()

    if not cap.isOpened():
        cap.release()
        raise RuntimeError("Cannot open RTSP stream.")

    frame = _read_frame_with_retry(cap)
    cap.release()

    if frame is None:
        raise RuntimeError("RTSP stream opened but cannot read frame after retries.")

    success, buffer = cv2.imencode(".jpg", frame)

    if not success:
        raise RuntimeError("Failed to encode CCTV frame as JPEG.")

    return buffer.tobytes()
