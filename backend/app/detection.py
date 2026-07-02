from functools import lru_cache
from ultralytics import YOLO
from app.camera import capture_frame

MODEL_NAME = "yolov8n.pt"


@lru_cache(maxsize=1)
def get_model():
    return YOLO(MODEL_NAME)


def run_yolo_detection() -> dict:
    frame = capture_frame()
    height, width = frame.shape[:2]

    model = get_model()

    results = model.predict(
        source=frame,
        conf=0.35,
        verbose=False,
        device="cpu"
    )

    detections = []

    if results and len(results) > 0:
        result = results[0]
        names = result.names

        for box in result.boxes:
            class_id = int(box.cls[0].item())
            confidence = float(box.conf[0].item())
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            detections.append({
                "class_id": class_id,
                "class_name": names.get(class_id, str(class_id)),
                "confidence": round(confidence, 4),
                "box": {
                    "x1": round(float(x1), 2),
                    "y1": round(float(y1), 2),
                    "x2": round(float(x2), 2),
                    "y2": round(float(y2), 2)
                }
            })

    return {
        "status": "ok",
        "model": MODEL_NAME,
        "camera": {
            "frame_width": width,
            "frame_height": height
        },
        "detections_count": len(detections),
        "detections": detections
    }
