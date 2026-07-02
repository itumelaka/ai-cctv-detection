from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from app.camera import test_rtsp_connection, capture_snapshot_jpeg

router = APIRouter(
    prefix="/cameras",
    tags=["Cameras"]
)

@router.get("/test")
def test_camera():
    return test_rtsp_connection()


@router.get("/snapshot")
def camera_snapshot():
    try:
        image_bytes = capture_snapshot_jpeg()
        return Response(
            content=image_bytes,
            media_type="image/jpeg"
        )
    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        )
