from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from app.camera import capture_frame
from app.camera_registry import get_camera_by_id
from app.detection import (
    run_yolo_detection,
    run_yolo_snapshot_jpeg,
    run_person_detection,
    run_person_snapshot_jpeg,
    run_person_detection_for_camera,
    run_person_snapshot_jpeg_for_camera,
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
        raise HTTPException(status_code=503, detail=str(error))


@router.get("/yolo")
def yolo_detection():
    try:
        return run_yolo_detection()

    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"YOLO detection failed: {error}")


@router.get("/yolo/snapshot")
def yolo_snapshot():
    try:
        image_bytes = run_yolo_snapshot_jpeg()
        return Response(content=image_bytes, media_type="image/jpeg")

    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"YOLO snapshot failed: {error}")


@router.get("/person")
def person_detection():
    try:
        return run_person_detection()

    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Person detection failed: {error}")


@router.get("/person/snapshot")
def person_snapshot():
    try:
        image_bytes = run_person_snapshot_jpeg()
        return Response(content=image_bytes, media_type="image/jpeg")

    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Person snapshot failed: {error}")


@router.get("/{camera_id}/person")
def person_detection_by_camera(camera_id: str):
    try:
        camera = get_camera_by_id(camera_id)
        return run_person_detection_for_camera(camera)

    except KeyError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Person detection failed: {error}")


@router.get("/{camera_id}/person/snapshot")
def person_snapshot_by_camera(camera_id: str):
    try:
        camera = get_camera_by_id(camera_id)
        image_bytes = run_person_snapshot_jpeg_for_camera(camera)
        return Response(content=image_bytes, media_type="image/jpeg")

    except KeyError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Person snapshot failed: {error}")
