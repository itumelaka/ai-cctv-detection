import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = REPO_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.face_enrollment import (  # noqa: E402
    enroll_lbph_from_csv,
    generate_draft_csv,
    write_csv_template,
)


def _print_result(result: dict) -> None:
    print(json.dumps(result, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Manage approved local face enrollment CSV files and OpenCV/LBPH batch enrollment. "
            "No paid API or cloud face recognition is used."
        )
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    template_parser = subparsers.add_parser("template", help="Write a placeholder CSV template.")
    template_parser.add_argument("--output", required=True, help="CSV template output path.")

    draft_parser = subparsers.add_parser("draft", help="Generate a review draft CSV from local images.")
    draft_parser.add_argument("--source-dir", required=True, help="Local approved-reference image folder.")
    draft_parser.add_argument("--output", required=True, help="Draft CSV output path.")
    draft_parser.add_argument(
        "--label-from",
        choices=["parent", "filename", "folder"],
        default="parent",
        help="How to draft labels before human review.",
    )
    draft_parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Only scan the top-level source folder.",
    )

    batch_parser = subparsers.add_parser("batch-enroll", help="Enroll approved CSV rows with local OpenCV/LBPH.")
    batch_parser.add_argument("--csv", required=True, help="Reviewed enrollment CSV path.")
    batch_parser.add_argument("--reject-report", required=True, help="JSON report path for rejects and summary.")

    args = parser.parse_args()

    try:
        if args.command == "template":
            _print_result(write_csv_template(Path(args.output)))
            return 0

        if args.command == "draft":
            _print_result(
                generate_draft_csv(
                    Path(args.source_dir),
                    Path(args.output),
                    recursive=not args.no_recursive,
                    label_from=args.label_from,
                )
            )
            return 0

        if args.command == "batch-enroll":
            result = enroll_lbph_from_csv(Path(args.csv), Path(args.reject_report))
            _print_result(result)
            return 0 if result["accepted_count"] > 0 else 3
    except Exception as error:
        print(f"ERROR: {error}")
        return 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
