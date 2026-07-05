import json
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
REVIEWS_DIR = DATA_DIR / "event-reviews"
REVIEWS_FILE = REVIEWS_DIR / "event_reviews.json"
VALID_REVIEW_STATUSES = {
    "unreviewed",
    "reviewed",
    "valid",
    "false_positive",
    "ignored",
    "needs_follow_up",
}


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def event_review_id(event: dict) -> str:
    event_id = event.get("event_id")

    if event_id:
        return str(event_id)

    evidence_filename = event.get("evidence_filename")

    if evidence_filename:
        return Path(evidence_filename).name

    evidence_path = event.get("evidence_path")

    if evidence_path:
        return Path(evidence_path).name

    camera = event.get("camera") or {}
    camera_id = camera.get("id") or event.get("camera_id") or "unknown_camera"
    timestamp = event.get("timestamp") or "unknown_timestamp"
    event_type = event.get("event_type") or "unknown_event"

    return f"{camera_id}_{event_type}_{timestamp}"


def _ensure_review_dir() -> None:
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)


def read_reviews() -> dict:
    if not REVIEWS_FILE.exists():
        return {}

    try:
        with REVIEWS_FILE.open("r", encoding="utf-8") as file:
            reviews = json.load(file)
    except json.JSONDecodeError:
        return {}

    if not isinstance(reviews, dict):
        return {}

    return reviews


def write_reviews(reviews: dict) -> None:
    _ensure_review_dir()

    with REVIEWS_FILE.open("w", encoding="utf-8") as file:
        json.dump(reviews, file, indent=2, sort_keys=True)
        file.write("\n")


def default_review(event_id: str) -> dict:
    return {
        "event_id": event_id,
        "review_status": "unreviewed",
        "note": "",
        "reviewed_by": "",
        "reviewed_at": None,
        "updated_at": None,
    }


def get_review(event_id: str) -> dict:
    reviews = read_reviews()
    return reviews.get(event_id, default_review(event_id))


def list_reviews() -> dict:
    return {
        "status": "ok",
        "reviews_count": len(read_reviews()),
        "reviews": read_reviews(),
        "valid_statuses": sorted(VALID_REVIEW_STATUSES),
    }


def upsert_review(
    event_id: str,
    review_status: str,
    note: str = "",
    reviewed_by: str = "",
) -> dict:
    if review_status not in VALID_REVIEW_STATUSES:
        raise ValueError(
            "Invalid review_status. Expected one of: "
            + ", ".join(sorted(VALID_REVIEW_STATUSES))
        )

    reviews = read_reviews()
    existing = reviews.get(event_id, default_review(event_id))
    timestamp = _utc_timestamp()

    review = {
        **existing,
        "event_id": event_id,
        "review_status": review_status,
        "note": note or "",
        "reviewed_by": reviewed_by or "",
        "reviewed_at": timestamp if review_status != "unreviewed" else None,
        "updated_at": timestamp,
    }

    reviews[event_id] = review
    write_reviews(reviews)
    return review


def with_review(event: dict) -> dict:
    event_with_review = event.copy()
    review_id = event_review_id(event_with_review)
    event_with_review["review_id"] = review_id
    event_with_review["review"] = get_review(review_id)
    return event_with_review
