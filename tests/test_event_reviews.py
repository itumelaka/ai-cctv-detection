import sys
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app import event_reviews


class EventReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_dir = event_reviews.REVIEWS_DIR
        self.original_file = event_reviews.REVIEWS_FILE
        event_reviews.REVIEWS_DIR = Path(self.temp_dir.name)
        event_reviews.REVIEWS_FILE = Path(self.temp_dir.name) / "event_reviews.json"

    def tearDown(self):
        event_reviews.REVIEWS_DIR = self.original_dir
        event_reviews.REVIEWS_FILE = self.original_file
        self.temp_dir.cleanup()

    def test_event_review_id_prefers_evidence_filename(self):
        review_id = event_reviews.event_review_id({
            "evidence_path": "backend/data/evidence/person_detected_cam_1.jpg"
        })

        self.assertEqual(review_id, "person_detected_cam_1.jpg")

    def test_upsert_and_get_review(self):
        review = event_reviews.upsert_review(
            event_id="event-1",
            review_status="false_positive",
            note="Static object",
            reviewed_by="tester",
        )

        self.assertEqual(review["review_status"], "false_positive")
        self.assertEqual(review["note"], "Static object")
        self.assertEqual(review["reviewed_by"], "tester")
        self.assertEqual(
            event_reviews.get_review("event-1")["review_status"],
            "false_positive",
        )

    def test_invalid_review_status_raises_value_error(self):
        with self.assertRaises(ValueError):
            event_reviews.upsert_review("event-1", "not_a_status")


if __name__ == "__main__":
    unittest.main()
