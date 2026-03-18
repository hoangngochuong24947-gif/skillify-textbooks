from __future__ import annotations

import argparse
from pathlib import Path

from skillify_runtime import DEFAULT_SIDE_TASKS, FileStatusAdapter, read_data_file, wait_for_completion


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Poll NotebookLM stage status while running lightweight local side tasks.")
    parser.add_argument("--skill-dir", required=True, help="Generated skill directory.")
    parser.add_argument("--stage", required=True, help="Stage identifier to monitor.")
    parser.add_argument("--status-file", required=True, help="JSON/YAML-like status file used by the file adapter.")
    parser.add_argument("--notebook-id", help="NotebookLM notebook id for logging.")
    parser.add_argument("--poll-interval", type=int, help="Override workflow poll interval.")
    parser.add_argument("--timeout", type=int, help="Override workflow timeout.")
    parser.add_argument("--max-retries", type=int, help="Override workflow max retries.")
    parser.add_argument("--side-task", action="append", dest="side_tasks", help="Optional side task override. Repeat to provide multiple values.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    skill_dir = Path(args.skill_dir)
    workflow = read_data_file(skill_dir / "workflow.yaml")
    wait_policy = workflow.get("wait_policy", {})
    result = wait_for_completion(
        skill_dir,
        stage=args.stage,
        adapter=FileStatusAdapter(Path(args.status_file)),
        poll_interval_seconds=args.poll_interval or int(wait_policy.get("poll_interval_seconds", 5)),
        timeout_seconds=args.timeout or int(wait_policy.get("timeout_seconds", 300)),
        max_retries=args.max_retries or int(wait_policy.get("max_retries", 3)),
        side_tasks=args.side_tasks or wait_policy.get("side_tasks", DEFAULT_SIDE_TASKS),
        notebook_id=args.notebook_id,
    )
    print(result["status"])
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
