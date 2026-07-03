from app.events import evaluate_person_event


def run_person_monitor_check() -> dict:
    event = evaluate_person_event()

    if event["person_detected"]:
        action = "attention_required"
        next_step = "Review evidence image and consider alert notification."
    else:
        action = "no_action"
        next_step = "Continue monitoring."

    return {
        "status": "ok",
        "monitor": "person",
        "action": action,
        "next_step": next_step,
        "event": event
    }
