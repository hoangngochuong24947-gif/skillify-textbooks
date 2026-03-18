from __future__ import annotations

import argparse
from pathlib import Path

from skillify_runtime import finalize_generated_skill


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Finalize a generated skill directory into installable skill layout.")
    parser.add_argument("--skill-dir", required=True, help="Generated skill directory.")
    parser.add_argument("--legacy-output-dir", help="Optional legacy output directory containing 00-05 markdown files.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    result = finalize_generated_skill(
        Path(args.skill_dir),
        legacy_output_dir=Path(args.legacy_output_dir) if args.legacy_output_dir else None,
    )
    print(result["skill_dir"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
