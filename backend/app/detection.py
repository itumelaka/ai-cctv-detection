from functools import lru_cache
import cv2
from ultralytics import YOLO
from app.camera import capture_frame, capture_frame_for_camera
from app.config import settings

MODEL_NAME = "yolov8n.pt"
PERSON_CLASS_NAME = "person"


@lru_cache(maxsize=1)
def get_model():
    return YOLO(MODEL_NAME)


def detect_objects(frame, class_name_filter: str | None = None):
    model = get_model()

    results = model.predict(
        source=frame,
        conf=settings.yolo_confidence,
        verbose=False,
        device="cpu"
    )

    detections = []

    if results and len(results) > 0:
        result = results[0]
        names = result.names

        for box in result.boxes:
            class_id = int(box.cls[0].item())
            class_name = names.get(class_id, str(class_id))

            if class_name_filter and class_name != class_name_filter:
                continue

            confidence = float(box.conf[0].item())
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            detections.append({
                "class_id": class_id,
                "class_name": class_name,
                "confidence": round(confidence, 4),
                "box": {
                    "x1": round(float(x1), 2),
                    "y1": round(float(y1), 2),
                    "x2": round(float(x2), 2),
                    "y2": round(float(y2), 2)
                }
            })

    return detections


def _build_detection_response(frame, detections, camera_info: dict | None = None, filter_name: str | None = None):
    height, width = frame.shape[:2]

    response = {
        "status": "ok",
        "model": MODEL_NAME,
        "confidence_threshold": settings.yolo_confidence,
        "camera": {
            "frame_width": width,
            "frame_height": height
        },
        "detections_count": len(detections),
        "detections": detections
    }

    if filter_name:
        response["filter"] = filter_name

    if filter_name == PERSON_CLASS_NAME:
        response["person_detected"] = len(detections) > 0

    if camera_info:
        response["camera"].update({
            "id": camera_info.get("id"),
            "name": camera_info.get("name"),
            "host": camera_info.get("host"),
            "channel": camera_info.get("channel")
        })

    return response


def run_yolo_detection() -> dict:
    frame = capture_frame()
    detections = detect_objects(frame)
    return _build_detection_response(frame, detections)


def run_person_detection() -> dict:
    frame = capture_frame()
    detections = detect_objects(frame, class_name_filter=PERSON_CLASS_NAME)
    return _build_detection_response(frame, detections, filter_name=PERSON_CLASS_NAME)


def run_person_detection_for_camera(camera: dict) -> dict:
    frame = capture_frame_for_camera(camera)
    detections = detect_objects(frame, class_name_filter=PERSON_CLASS_NAME)
    return _build_detection_response(
        frame,
        detections,
        camera_info=camera,
        filter_name=PERSON_CLASS_NAME
    )


def _draw_detections(frame, detections):
    for detection in detections:
        box = detection["box"]
        class_name = detection["class_name"]
        confidence = detection["confidence"]

        x1 = int(box["x1"])
        y1 = int(box["y1"])
        x2 = int(box["x2"])
        y2 = int(box["y2"])

        label = f"{class_name} {confidence:.2f}"

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            frame,
            label,
            (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2
        )

    return frame


def _encode_jpeg(frame) -> bytes:
    success, buffer = cv2.imencode(".jpg", frame)

    if not success:
        raise RuntimeError("Failed to encode frame as JPEG.")

    return buffer.tobytes()


def run_yolo_snapshot_jpeg() -> bytes:
    frame = capture_frame()
    detections = detect_objects(frame)
    frame = _draw_detections(frame, detections)
    return _encode_jpeg(frame)


def run_person_snapshot_jpeg() -> bytes:
    frame = capture_frame()
    detections = detect_objects(frame, class_name_filter=PERSON_CLASS_NAME)
    frame = _draw_detections(frame, detections)
    return _encode_jpeg(frame)


def run_person_snapshot_jpeg_for_camera(camera: dict) -> bytes:
    frame = capture_frame_for_camera(camera)
    detections = detect_objects(frame, class_name_filter=PERSON_CLASS_NAME)
    frame = _draw_detections(frame, detections)
    return _encode_jpeg(frame)
