from fastapi import APIRouter
from app.camera import test_rtsp_connection

router = APIRouter(
    prefix="/cameras",
    tags=["Cameras"]
)

@router.get("/test")
def test_camera():
    return test_rtsp_connection()
