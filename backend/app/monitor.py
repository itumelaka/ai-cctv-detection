from app.events import evaluate_person_event, evaluate_person_event_for_camera


def _build_monitor_response(event: dict, camera_id: str | None = None) -> dict:
    if event["person_detected"]:
        action = "attention_required"
        next_step = "Review evidence image and consider alert notification."
    else:
        action = "no_action"
        next_step = "Continue monitoring."

    response = {
        "status": "ok",
        "monitor": "person",
        "action": action,
        "next_step": next_step,
        "event": event
    }

    if camera_id:
        response["camera_id"] = camera_id

    return response


def run_person_monitor_check() -> dict:
    event = evaluate_person_event()
    return _build_monitor_response(event)


def run_person_monitor_check_for_camera(camera: dict) -> dict:
    event = evaluate_person_event_for_camera(camera)
    return _build_monitor_response(event, camera_id=camera.get("id"))
