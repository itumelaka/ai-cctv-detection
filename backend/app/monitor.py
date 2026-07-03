from app.camera_registry import list_enabled_cameras
from app.events import evaluate_person_event, evaluate_person_event_for_camera


def run_person_monitor_check() -> dict:
    event = evaluate_person_event()

    if event.get("person_detected"):
        action = "attention_required"
        next_step = "Review evidence image and consider alert notification."
    else:
        action = "no_action"
        next_step = "No person detected. Continue monitoring."

    return {
        "status": "ok",
        "monitor": "person",
        "action": action,
        "next_step": next_step,
        "event": event
    }


def run_person_monitor_check_for_camera(camera: dict) -> dict:
    event = evaluate_person_event_for_camera(camera)

    if event.get("person_detected"):
        action = "attention_required"
        next_step = "Review evidence image and consider alert notification."
    else:
        action = "no_action"
        next_step = "No person detected. Continue monitoring."

    return {
        "status": "ok",
        "monitor": "person",
        "action": action,
        "next_step": next_step,
        "event": event,
        "camera_id": camera.get("id")
    }


def run_person_monitor_check_all() -> dict:
    cameras = list_enabled_cameras()
    results = []

    for camera in cameras:
        try:
            result = run_person_monitor_check_for_camera(camera)
        except Exception as error:
            result = {
                "status": "failed",
                "monitor": "person",
                "action": "error",
                "next_step": "Review camera configuration or RTSP connection.",
                "camera_id": camera.get("id"),
                "camera_name": camera.get("name"),
                "camera_host": camera.get("host"),
                "channel": camera.get("channel"),
                "error": str(error)
            }

        results.append(result)

    attention_required_count = len([
        item for item in results
        if item.get("action") == "attention_required"
    ])

    failed_count = len([
        item for item in results
        if item.get("status") == "failed"
    ])

    no_action_count = len([
        item for item in results
        if item.get("action") == "no_action"
    ])

    return {
        "status": "ok",
        "monitor": "person",
        "mode": "check_all",
        "enabled_cameras_count": len(cameras),
        "attention_required_count": attention_required_count,
        "no_action_count": no_action_count,
        "failed_count": failed_count,
        "results": results
    }
