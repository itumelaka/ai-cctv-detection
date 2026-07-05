from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from app.events import (
    evaluate_person_event,
    get_latest_dashboard_events,
    get_latest_events,
    get_event_stats,
)
from app.event_log import get_evidence_image_path
from app.event_reviews import get_review, list_reviews, upsert_review

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.get("/person")
def person_event():
    try:
        return evaluate_person_event()

    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        )
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Person event evaluation failed: {error}"
        )


@router.get("/logs")
def event_logs(limit: int = Query(default=20, ge=1, le=100)):
    try:
        return get_latest_events(limit=limit)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Reading event logs failed: {error}"
        )


@router.get("/latest-with-reviews")
def event_logs_with_reviews(limit: int = Query(default=20, ge=1, le=100)):
    try:
        return get_latest_dashboard_events(limit=limit)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Reading event logs with reviews failed: {error}"
        )


@router.get("/stats")
def event_stats():
    try:
        return get_event_stats()

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Reading event stats failed: {error}"
        )


@router.get("/reviews")
def event_reviews():
    try:
        return list_reviews()

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Reading event reviews failed: {error}"
        )


@router.get("/reviews/{event_id}")
def event_review(event_id: str):
    try:
        return {
            "status": "ok",
            "review": get_review(event_id)
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Reading event review failed: {error}"
        )


def _update_event_review(event_id: str, payload: dict):
    try:
        review = upsert_review(
            event_id=event_id,
            review_status=payload.get("review_status", "unreviewed"),
            note=payload.get("note", ""),
            reviewed_by=payload.get("reviewed_by", ""),
        )

        return {
            "status": "ok",
            "review": review
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Updating event review failed: {error}"
        )


@router.put("/reviews/{event_id}")
def put_event_review(event_id: str, payload: dict):
    return _update_event_review(event_id, payload)


@router.post("/reviews/{event_id}")
def post_event_review(event_id: str, payload: dict):
    return _update_event_review(event_id, payload)


@router.get("/evidence/{filename}")
def evidence_image(filename: str):
    try:
        file_path = get_evidence_image_path(filename)

        return FileResponse(
            path=file_path,
            media_type="image/jpeg",
            filename=file_path.name
        )

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Reading evidence image failed: {error}"
        )
