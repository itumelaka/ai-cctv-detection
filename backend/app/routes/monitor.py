from fastapi import APIRouter, HTTPException
from app.monitor import run_person_monitor_check

router = APIRouter(
    prefix="/monitor",
    tags=["Monitor"]
)


@router.get("/person/check")
def person_monitor_check():
    try:
        return run_person_monitor_check()

    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        )
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Person monitor check failed: {error}"
        )
