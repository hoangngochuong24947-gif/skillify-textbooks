from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from skillify_runtime import (  # noqa: E402
    BookBrief,
    REFERENCE_FILES,
    SequenceStatusAdapter,
    finalize_generated_skill,
    init_generated_skill,
    load_checkpoint,
    wait_for_completion,
    write_json_yaml,
)


class SkillifyRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.skills_root = self.root / "skills"
        self.book = BookBrief(
            title="Thinking, Fast and Slow",
            author="Daniel Kahneman",
            domain="Behavioral economics",
            audience="Agent builders",
            goal="Create a reusable book-derived skill",
            language="en",
        )

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_init_generated_skill_creates_standard_layout(self) -> None:
        skill_dir = init_generated_skill(self.book, self.skills_root)
        self.assertTrue((skill_dir / "SKILL.md").exists() is False)
        self.assertTrue((skill_dir / "workflow.yaml").exists())
        self.assertTrue((skill_dir / "book-brief.yaml").exists())
        self.assertTrue((skill_dir / "references").is_dir())
        self.assertTrue((skill_dir / "queries").is_dir())
        self.assertTrue((skill_dir / "logs").is_dir())
        for filename in REFERENCE_FILES:
            self.assertTrue((skill_dir / "references" / filename).exists(), filename)
        self.assertTrue((skill_dir / "queries" / "pack-01-book-mapping.yaml").exists())
        self.assertTrue((skill_dir / "logs" / "checkpoint.json").exists())

    def test_wait_for_completion_runs_side_tasks_and_updates_checkpoint(self) -> None:
        skill_dir = init_generated_skill(self.book, self.skills_root)
        result = wait_for_completion(
            skill_dir,
            stage="methodology-mining",
            adapter=SequenceStatusAdapter(["pending", "running", "done"]),
            poll_interval_seconds=0,
            timeout_seconds=30,
            max_retries=1,
            sleep_fn=lambda _: None,
        )
        self.assertTrue(result["ok"])
        checkpoint = load_checkpoint(skill_dir)
        self.assertEqual(checkpoint["stage"], "methodology-mining")
        self.assertEqual(checkpoint["status"], "done")
        self.assertIn("ensure_query_packs", checkpoint["completed_side_tasks"])
        log_file = Path(result["log_path"])
        log_lines = [json.loads(line) for line in log_file.read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertTrue(any(item["action"] == "wait_complete" for item in log_lines))

    def test_wait_for_completion_uses_existing_checkpoint(self) -> None:
        skill_dir = init_generated_skill(self.book, self.skills_root)
        write_json_yaml(
            skill_dir / "logs" / "checkpoint.json",
            {
                "stage": "book-mapping",
                "status": "running",
                "attempts": 2,
                "completed_side_tasks": ["initialize_logs"],
            },
        )
        result = wait_for_completion(
            skill_dir,
            stage="book-mapping",
            adapter=SequenceStatusAdapter(["done"]),
            poll_interval_seconds=0,
            timeout_seconds=30,
            max_retries=3,
            sleep_fn=lambda _: None,
        )
        self.assertTrue(result["ok"])
        checkpoint = load_checkpoint(skill_dir)
        self.assertEqual(checkpoint["attempts"], 2)
        self.assertEqual(checkpoint["status"], "done")

    def test_finalize_generated_skill_imports_legacy_output(self) -> None:
        skill_dir = init_generated_skill(self.book, self.skills_root)
        legacy_output = self.root / "legacy-output"
        legacy_output.mkdir(parents=True, exist_ok=True)
        for filename in REFERENCE_FILES:
            (legacy_output / filename).write_text(f"# Legacy {filename}\n", encoding="utf-8")
        result = finalize_generated_skill(skill_dir, legacy_output_dir=legacy_output)
        self.assertTrue(result["ok"])
        self.assertTrue((skill_dir / "SKILL.md").exists())
        self.assertTrue((skill_dir / "skill-bundle-manifest.yaml").exists())
        for filename in REFERENCE_FILES:
            reference_text = (skill_dir / "references" / filename).read_text(encoding="utf-8")
            self.assertIn("Legacy", reference_text)


if __name__ == "__main__":
    unittest.main()
