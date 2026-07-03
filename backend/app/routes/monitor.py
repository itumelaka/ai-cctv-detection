from fastapi import APIRouter, HTTPException
from app.camera_registry import get_camera_by_id
from app.monitor import (
    run_person_monitor_check,
    run_person_monitor_check_for_camera,
    run_person_monitor_check_all,
    run_person_monitor_summary,
)

router = APIRouter(
    prefix="/monitor",
    tags=["Monitor"]
)


@router.get("/person/check")
def monitor_person_check():
    return run_person_monitor_check()


@router.get("/person/check-all")
def monitor_person_check_all():
    return run_person_monitor_check_all()


@router.get("/person/summary")
def monitor_person_summary():
    return run_person_monitor_summary()


@router.get("/{camera_id}/person/check")
def monitor_person_check_by_camera(camera_id: str):
    try:
        camera = get_camera_by_id(camera_id)
        return run_person_monitor_check_for_camera(camera)

    except KeyError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
