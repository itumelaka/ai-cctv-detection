import os
import cv2
from app.config import settings

def test_rtsp_connection() -> dict:
    if not settings.cctv_host or not settings.cctv_username or not settings.cctv_password:
        return {
            "status": "failed",
            "message": "CCTV configuration is incomplete. Check backend/.env.",
            "camera_host": settings.cctv_host,
            "channel": settings.cctv_channel,
            "rtsp_url": settings.masked_rtsp_url
        }

    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"

    cap = cv2.VideoCapture(settings.rtsp_url, cv2.CAP_FFMPEG)

    if not cap.isOpened():
        cap.release()
        return {
            "status": "failed",
            "message": "Cannot open RTSP stream.",
            "camera_host": settings.cctv_host,
            "channel": settings.cctv_channel,
            "rtsp_url": settings.masked_rtsp_url
        }

    ok, frame = cap.read()
    cap.release()

    if not ok or frame is None:
        return {
            "status": "failed",
            "message": "RTSP stream opened but cannot read frame.",
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
