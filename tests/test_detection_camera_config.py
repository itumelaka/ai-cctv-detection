import sys
import types
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))


fake_dotenv = types.ModuleType("dotenv")
fake_dotenv.load_dotenv = lambda: None
sys.modules.setdefault("dotenv", fake_dotenv)

fake_cv2 = types.ModuleType("cv2")
fake_cv2.CAP_FFMPEG = 0
fake_cv2.CAP_PROP_BUFFERSIZE = 0
fake_cv2.IMWRITE_JPEG_QUALITY = 1
fake_cv2.VideoCapture = lambda *_args, **_kwargs: None
fake_cv2.FONT_HERSHEY_SIMPLEX = 0
sys.modules.setdefault("cv2", fake_cv2)

fake_ultralytics = types.ModuleType("ultralytics")
fake_ultralytics.YOLO = lambda *_args, **_kwargs: None
sys.modules.setdefault("ultralytics", fake_ultralytics)

from app import detection


class _Frame:
    def __init__(self, width, height):
        self.shape = (height, width, 3)


class DetectionCameraConfigTests(unittest.TestCase):
    def test_camera_person_threshold_overrides_global_default(self):
        self.assertEqual(
            detection._person_confidence_threshold(
                {"id": "makmal_cam_13", "person_confidence_threshold": 0.75}
            ),
            0.75,
        )

    def test_missing_camera_threshold_uses_global_default(self):
        self.assertEqual(
            detection._person_confidence_threshold({"id": "other_cam"}),
            detection.settings.person_confidence_threshold,
        )

    def test_scales_detection_boxes_for_high_resolution_evidence_frame(self):
        detections = [
            {
                "class_name": "person",
                "confidence": 0.91,
                "box": {"x1": 10, "y1": 20, "x2": 110, "y2": 220},
            }
        ]

        scaled = detection._scale_detections_for_frame(
            detections,
            source_frame=_Frame(width=640, height=360),
            target_frame=_Frame(width=1920, height=1080),
        )

        self.assertEqual(
            scaled[0]["box"],
            {"x1": 30.0, "y1": 60.0, "x2": 330.0, "y2": 660.0},
        )


if __name__ == "__main__":
    unittest.main()
