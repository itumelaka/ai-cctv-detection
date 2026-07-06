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

    def test_tv_dashboard_contains_hd_first_single_camera_live_controls(self):
        dashboard_ui = DASHBOARD_UI_PATH.read_text(encoding="utf-8")

        self.assertIn('let selectedLiveQuality = "hd"', dashboard_ui)
        self.assertIn('id="qualityHdButton"', dashboard_ui)
        self.assertIn('id="qualityStandardButton"', dashboard_ui)
        self.assertIn('id="snapshotButton"', dashboard_ui)
        self.assertIn('id="fullscreenLiveButton"', dashboard_ui)
        self.assertIn("Reconnecting", dashboard_ui)
        self.assertIn("snapshot.jpg?quality=", dashboard_ui)
        self.assertIn("selected camera only", dashboard_ui)
        self.assertNotIn("13-camera", dashboard_ui)


if __name__ == "__main__":
    unittest.main()
