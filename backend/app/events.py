from datetime import datetime, timezone
from app.config import settings
from app.detection import (
    run_person_detection,
    run_person_detection_for_camera,
    run_person_snapshot_jpeg,
    run_person_snapshot_jpeg_for_camera,
)
from app.event_log import append_event_log, read_latest_event_logs, read_all_event_logs, save_evidence_image


def _build_person_event(detection_result: dict, snapshot_func, camera_context: dict | None = None) -> dict:
    detections_count = detection_result["detections_count"]
    person_detected = detection_result["person_detected"]
    timestamp = datetime.now(timezone.utc).isoformat()

    evidence_path = None

    if person_detected:
        event_type = "person_detected"
        severity = "medium"
        message = "Person detected in CCTV frame."

        image_bytes = snapshot_func()
        camera_id = camera_context.get("id") if camera_context else "default_camera"
        filename = f"person_detected_{camera_id}_{timestamp}.jpg"
        evidence_path = save_evidence_image(image_bytes, filename)
    else:
        event_type = "no_person"
        severity = "none"
        message = "No person detected in CCTV frame."

    camera_data = {
        "host": settings.cctv_host,
        "channel": settings.cctv_channel,
        "frame_width": detection_result["camera"]["frame_width"],
        "frame_height": detection_result["camera"]["frame_height"]
    }

    if camera_context:
        camera_data.update({
            "id": camera_context.get("id"),
            "name": camera_context.get("name"),
            "host": camera_context.get("host"),
            "channel": camera_context.get("channel")
        })

    event = {
        "status": "ok",
        "event_type": event_type,
        "severity": severity,
        "message": message,
        "timestamp": timestamp,
        "camera": camera_data,
        "person_detected": person_detected,
        "detections_count": detections_count,
        "detections": detection_result["detections"],
        "evidence_path": evidence_path
    }

    append_event_log(event)

    return event


def evaluate_person_event() -> dict:
    detection_result = run_person_detection()
    return _build_person_event(
        detection_result=detection_result,
        snapshot_func=run_person_snapshot_jpeg
    )


def evaluate_person_event_for_camera(camera: dict) -> dict:
    detection_result = run_person_detection_for_camera(camera)

    return _build_person_event(
        detection_result=detection_result,
        snapshot_func=lambda: run_person_snapshot_jpeg_for_camera(camera),
        camera_context=camera
    )


def get_latest_events(limit: int = 20) -> dict:
    if limit < 1:
        limit = 1

    if limit > 100:
        limit = 100

    events = read_latest_event_logs(limit=limit)

    return {
        "status": "ok",
        "limit": limit,
        "events_count": len(events),
        "events": events
    }


def get_event_stats() -> dict:
    events = read_all_event_logs()

    total_events = len(events)
    person_detected_count = 0
    no_person_count = 0
    evidence_count = 0

    for event in events:
        if event.get("person_detected") is True:
            person_detected_count += 1

        if event.get("event_type") == "no_person":
            no_person_count += 1

        if event.get("evidence_path"):
            evidence_count += 1

    latest_event = events[-1] if events else None

    return {
        "status": "ok",
        "total_events": total_events,
        "person_detected_count": person_detected_count,
        "no_person_count": no_person_count,
        "evidence_count": evidence_count,
        "latest_event": {
            "timestamp": latest_event.get("timestamp"),
            "event_type": latest_event.get("event_type"),
            "severity": latest_event.get("severity"),
            "person_detected": latest_event.get("person_detected")
        } if latest_event else None
    }
