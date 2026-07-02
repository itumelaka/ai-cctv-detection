from fastapi import APIRouter, HTTPException
from app.camera import capture_frame

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
