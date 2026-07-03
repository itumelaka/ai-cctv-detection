from fastapi import APIRouter, HTTPException
from app.camera_registry import get_camera_by_id
from app.monitor import run_person_monitor_check, run_person_monitor_check_for_camera

router = APIRouter(
    prefix="/monitor",
    tags=["Monitor"]
)


@router.get("/person/check")
def person_monitor_check():
    try:
        return run_person_monitor_check()

    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Person monitor check failed: {error}")


@router.get("/{camera_id}/person/check")
def person_monitor_check_by_camera(camera_id: str):
    try:
        camera = get_camera_by_id(camera_id)
        return run_person_monitor_check_for_camera(camera)

    except KeyError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Person monitor check failed: {error}")
