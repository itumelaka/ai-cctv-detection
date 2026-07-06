import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DASHBOARD_UI_PATH = ROOT_DIR / "backend" / "app" / "routes" / "dashboard_ui.py"


class DashboardIdentityAssignmentUiTests(unittest.TestCase):
    def test_dashboard_ui_contains_identity_assignment_flow_without_training(self):
        dashboard_ui = DASHBOARD_UI_PATH.read_text(encoding="utf-8")

        self.assertIn("Assign Identity", dashboard_ui)
        self.assertIn("/faces/enrollment/identity-assignment", dashboard_ui)
        self.assertIn("assigned_label", dashboard_ui)
        self.assertIn("approved_for_training", dashboard_ui)
        self.assertIn("canAssignIdentity(event)", dashboard_ui)
        self.assertIn("personTargetsFromEvent(event)", dashboard_ui)
        self.assertIn("person_rank", dashboard_ui)
        self.assertIn("person_confidence", dashboard_ui)
        self.assertIn("person_bbox", dashboard_ui)
        self.assertIn("person_target_label", dashboard_ui)
        self.assertIn("identity_person_target", dashboard_ui)
        self.assertIn("event?.person_detections", dashboard_ui)
        self.assertIn("PERSON ${rank}", dashboard_ui)
        self.assertIn("targetCount > 1", dashboard_ui)
        self.assertNotIn("batch-enroll", dashboard_ui)
        self.assertNotIn("enroll_lbph_from_csv", dashboard_ui)

    def test_tv_dashboard_contains_webrtc_smooth_mjpeg_fallback_and_hd_snapshot_controls(self):
        dashboard_ui = DASHBOARD_UI_PATH.read_text(encoding="utf-8")

        self.assertIn('let selectedLiveMode = "webrtc"', dashboard_ui)
        self.assertIn('let selectedLiveQuality = "standard"', dashboard_ui)
        self.assertIn('id="modeWebrtcButton"', dashboard_ui)
        self.assertIn('id="modeMjpegButton"', dashboard_ui)
        self.assertIn("WebRTC Smooth", dashboard_ui)
        self.assertIn("MJPEG Fallback", dashboard_ui)
        self.assertIn("mediamtxWebrtcUrl(camera.camera_id)", dashboard_ui)
        self.assertIn("window.location.hostname", dashboard_ui)
        self.assertIn(":8889", dashboard_ui)
        self.assertIn('id="qualitySmoothButton"', dashboard_ui)
        self.assertIn('id="qualityHdButton"', dashboard_ui)
        self.assertIn("Smooth Live", dashboard_ui)
        self.assertIn("HD Live", dashboard_ui)
        self.assertIn('id="snapshotButton"', dashboard_ui)
        self.assertIn('id="fullscreenLiveButton"', dashboard_ui)
        self.assertIn("Reconnecting", dashboard_ui)
        self.assertIn("snapshot.jpg?quality=hd", dashboard_ui)
        self.assertIn("Snapshot: HD", dashboard_ui)
        self.assertIn("Evidence/Crops: HD when available", dashboard_ui)
        self.assertIn("selected camera only", dashboard_ui)
        self.assertNotIn("13-camera", dashboard_ui)
        self.assertNotIn("rtsp" + "://", dashboard_ui)
        self.assertNotIn("CCTV" + "_PASSWORD", dashboard_ui)
        self.assertNotIn("TELEGRAM" + "_BOT_TOKEN", dashboard_ui)
        self.assertNotIn("http://192.168.1.254:8889", dashboard_ui)


if __name__ == "__main__":
    unittest.main()
