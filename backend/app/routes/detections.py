from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from app.camera import capture_frame
from app.detection import (
    run_yolo_detection,
    run_yolo_snapshot_jpeg,
    run_person_detection,
    run_person_snapshot_jpeg,
)

router = APIRouter(
    prefix="/detections",
    tags=["Detections"]
)


@router.get("/test")
def test_detection():
    try:
        frame = capture_frame()
        height, width = frame.shape[:2]

        return {
            "status": "ok",
            "message": "Dummy detection endpoint is working.",
            "camera": {
                "frame_width": width,
                "frame_height": height
            },
            "detections": []
        }

    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        )


@router.get("/yolo")
def yolo_detection():
    try:
        return run_yolo_detection()

    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        )
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"YOLO detection failed: {error}"
        )


@router.get("/yolo/snapshot")
def yolo_snapshot():
    try:
        image_bytes = run_yolo_snapshot_jpeg()

        return Response(
            content=image_bytes,
            media_type="image/jpeg"
        )

    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        )
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"YOLO snapshot failed: {error}"
        )


@router.get("/person")
def person_detection():
    try:
        return run_person_detection()

    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        )
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Person detection failed: {error}"
        )


@router.get("/person/snapshot")
def person_snapshot():
    try:
        image_bytes = run_person_snapshot_jpeg()

        return Response(
            content=image_bytes,
            media_type="image/jpeg"
        )

    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        )
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Person snapshot failed: {error}"
        )
