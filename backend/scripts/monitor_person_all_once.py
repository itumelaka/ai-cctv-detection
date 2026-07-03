import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = PROJECT_ROOT / "backend"

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.monitor import run_person_monitor_check_all


def main():
    result = run_person_monitor_check_all()

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if result.get("failed_count", 0) > 0:
        return 1

    if result.get("attention_required_count", 0) > 0:
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
