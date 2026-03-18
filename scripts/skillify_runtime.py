from __future__ import annotations

import json
import re
import shutil
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha1
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence


REFERENCE_FILES = [
    "00-overview.md",
    "01-author-thinking.md",
    "02-method-catalog.md",
    "03-scenario-router.md",
    "04-subagent-playbooks.md",
    "05-master-skill-spec.md",
]

QUERY_PACKS = [
    {
        "filename": "pack-01-book-mapping.yaml",
        "stage": "book-mapping",
        "objective": "Build the book map, chapter progression, recurring themes, and core claims.",
        "questions": [
            "What is the high-level structure of the book?",
            "How do the chapters build on one another?",
            "Which themes recur across multiple chapters?",
        ],
        "evidence_rule": "Cite chapter or section evidence for every structural claim.",
        "expected_output": "references/00-overview.md",
    },
    {
        "filename": "pack-02-author-thinking.yaml",
        "stage": "author-thinking",
        "objective": "Extract how the author frames problems, sequences judgment, and chooses evidence.",
        "questions": [
            "How does the author usually define the problem before solving it?",
            "What recurring judgment dimensions or heuristics appear across the book?",
            "Which sequencing habits show up when the author explains decisions?",
        ],
        "evidence_rule": "Keep original terms when useful and attach chapter evidence.",
        "expected_output": "references/01-author-thinking.md",
    },
    {
        "filename": "pack-03-methodology-mining.yaml",
        "stage": "methodology-mining",
        "objective": "Extract explicit and implicit reusable methods and convert them into MethodCards.",
        "questions": [
            "Which named methods, models, or frameworks appear directly in the book?",
            "Which recurring but unnamed methods can be inferred from repeated patterns?",
            "For each method, what are the triggers, steps, limits, and scenarios?",
        ],
        "evidence_rule": "Every MethodCard must include traceable evidence and downgrade weak claims.",
        "expected_output": "references/02-method-catalog.md",
    },
    {
        "filename": "pack-04-scenario-routing.yaml",
        "stage": "scenario-routing",
        "objective": "Map user problem types to the methods that should be triggered.",
        "questions": [
            "For what kinds of user problems should each method be used?",
            "When should the method not be used or be combined with another method?",
            "What order should multiple methods be applied in?",
        ],
        "evidence_rule": "Routing decisions should be explainable from the book-derived methods.",
        "expected_output": "references/03-scenario-router.md",
    },
    {
        "filename": "pack-05-conflict-check.yaml",
        "stage": "conflict-check",
        "objective": "Resolve overlaps, identify unsupported claims, and prepare the final skill bundle.",
        "questions": [
            "Which methods overlap or conflict with one another?",
            "Which conclusions still need better evidence?",
            "What should be elevated into the final skill entry point versus left as support material?",
        ],
        "evidence_rule": "Mark anything weak as pending_confirmation instead of upgrading it to fact.",
        "expected_output": "references/04-subagent-playbooks.md and references/05-master-skill-spec.md",
    },
]

STAGE_REQUIREMENTS = {
    "book-mapping": [],
    "author-thinking": ["00-overview.md"],
    "methodology-mining": ["00-overview.md", "01-author-thinking.md"],
    "scenario-routing": ["02-method-catalog.md"],
    "conflict-check": ["00-overview.md", "01-author-thinking.md", "02-method-catalog.md", "03-scenario-router.md"],
}

DEFAULT_SIDE_TASKS = [
    "ensure_query_packs",
    "ensure_stage_placeholders",
    "initialize_logs",
    "validate_previous_outputs",
    "prepare_next_stage_prompts",
]


@dataclass
class BookBrief:
    title: str
    author: str
    domain: str
    audience: str
    goal: str
    language: str = "zh"

    @classmethod
    def from_mapping(cls, payload: dict[str, Any]) -> "BookBrief":
        return cls(
            title=str(payload.get("title", "")).strip(),
            author=str(payload.get("author", "")).strip(),
            domain=str(payload.get("domain", "")).strip(),
            audience=str(payload.get("audience", "")).strip(),
            goal=str(payload.get("goal", "")).strip(),
            language=str(payload.get("language", "zh")).strip() or "zh",
        )


class FileStatusAdapter:
    def __init__(self, status_file: Path) -> None:
        self.status_file = Path(status_file)

    def get_status(self, stage: str) -> dict[str, Any]:
        payload = read_data_file(self.status_file)
        if stage in payload and isinstance(payload[stage], dict):
            return payload[stage]
        if payload.get("stage") == stage:
            return payload
        return {
            "status": payload.get("status", "pending"),
            "message": payload.get("message", f"No explicit status for stage '{stage}'."),
            "notebook_id": payload.get("notebook_id"),
        }


class SequenceStatusAdapter:
    def __init__(self, statuses: Sequence[dict[str, Any] | str]) -> None:
        self._statuses = list(statuses)
        self._index = 0

    def get_status(self, stage: str) -> dict[str, Any]:
        if not self._statuses:
            return {"status": "pending", "message": f"No status values configured for {stage}."}
        value = self._statuses[min(self._index, len(self._statuses) - 1)]
        if self._index < len(self._statuses) - 1:
            self._index += 1
        if isinstance(value, str):
            return {"status": value, "message": f"Sequence adapter reported '{value}' for {stage}."}
        return value


def now_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def slugify(value: str) -> str:
    normalized = value.lower().strip()
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_only).strip("-")
    if slug:
        return slug
    digest = sha1(value.encode("utf-8")).hexdigest()[:8]
    return f"book-skill-{digest}"


def skill_dir(skills_root: Path, book: BookBrief) -> Path:
    return Path(skills_root) / slugify(book.title)


def read_data_file(path: Path) -> dict[str, Any]:
    text = Path(path).read_text(encoding="utf-8").strip()
    if not text:
        return {}
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        payload = {}
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or ":" not in line:
                continue
            key, value = line.split(":", 1)
            payload[key.strip()] = value.strip().strip("'\"")
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain an object-like mapping.")
    return payload


def write_json_yaml(path: Path, payload: dict[str, Any] | list[Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def ensure_standard_structure(target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for name in ("references", "queries", "logs"):
        (target / name).mkdir(parents=True, exist_ok=True)


def placeholder_reference_text(filename: str, book: BookBrief) -> str:
    title_map = {
        "00-overview.md": "Book Overview",
        "01-author-thinking.md": "Author Thinking",
        "02-method-catalog.md": "Method Catalog",
        "03-scenario-router.md": "Scenario Router",
        "04-subagent-playbooks.md": "Subagent Playbooks",
        "05-master-skill-spec.md": "Master Skill Spec",
    }
    heading = title_map.get(filename, filename)
    return (
        f"# {heading}\n\n"
        f"- Source book: {book.title}\n"
        f"- Author: {book.author}\n"
        f"- Status: placeholder\n"
        f"- Next action: fill this document from the matching NotebookLM query stage.\n"
    )


def workflow_payload(book: BookBrief, skill_root: Path) -> dict[str, Any]:
    references = [f"references/{name}" for name in REFERENCE_FILES]
    stage_specs = [
        {
            "id": "prepare-notebook",
            "kind": "setup",
            "outputs": [],
            "notes": "Create or reuse the NotebookLM notebook and import the book source.",
        }
    ]
    for query in QUERY_PACKS:
        stage_specs.append(
            {
                "id": query["stage"],
                "kind": "query-pack",
                "query_pack": f"queries/{query['filename']}",
                "outputs": [query["expected_output"]],
            }
        )
    return {
        "version": "1.0.0",
        "book": asdict(book),
        "execution_mode": "auto_parallel",
        "stages": stage_specs,
        "wait_policy": {
            "poll_interval_seconds": 5,
            "timeout_seconds": 300,
            "max_retries": 3,
            "side_tasks": DEFAULT_SIDE_TASKS,
        },
        "artifacts": {
            "skill_root": str(skill_root.as_posix()),
            "references": references,
            "queries": [f"queries/{item['filename']}" for item in QUERY_PACKS],
            "bundle_manifest": "skill-bundle-manifest.yaml",
        },
        "logging": {
            "event_stream": "logs/run-*.jsonl",
            "checkpoint": "logs/checkpoint.json",
            "level": "lightweight",
        },
    }


def init_generated_skill(book: BookBrief, skills_root: Path, force: bool = False) -> Path:
    target = skill_dir(skills_root, book)
    if target.exists() and any(target.iterdir()) and not force:
        raise FileExistsError(f"{target} already exists. Use --force to overwrite placeholders.")
    ensure_standard_structure(target)
    write_json_yaml(target / "book-brief.yaml", asdict(book))
    write_json_yaml(target / "workflow.yaml", workflow_payload(book, target))
    for query in QUERY_PACKS:
        write_json_yaml(target / "queries" / query["filename"], query)
    for filename in REFERENCE_FILES:
        reference_path = target / "references" / filename
        if force or not reference_path.exists():
            reference_path.write_text(placeholder_reference_text(filename, book), encoding="utf-8")
    checkpoint_path = target / "logs" / "checkpoint.json"
    if force or not checkpoint_path.exists():
        write_json_yaml(
            checkpoint_path,
            {
                "stage": None,
                "status": "not_started",
                "attempts": 0,
                "completed_side_tasks": [],
                "last_updated": now_timestamp(),
            },
        )
    ensure_run_log(target)
    return target


def ensure_run_log(target: Path, run_name: str | None = None) -> Path:
    logs_dir = Path(target) / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / f"run-{run_name or run_id()}.jsonl"
    if not log_path.exists():
        log_path.write_text("", encoding="utf-8")
    return log_path


def load_checkpoint(target: Path) -> dict[str, Any]:
    checkpoint = Path(target) / "logs" / "checkpoint.json"
    if checkpoint.exists():
        return read_data_file(checkpoint)
    return {
        "stage": None,
        "status": "not_started",
        "attempts": 0,
        "completed_side_tasks": [],
        "last_updated": now_timestamp(),
    }


def save_checkpoint(target: Path, checkpoint: dict[str, Any]) -> None:
    checkpoint["last_updated"] = now_timestamp()
    write_json_yaml(Path(target) / "logs" / "checkpoint.json", checkpoint)


def append_log_event(
    target: Path,
    log_path: Path,
    *,
    stage: str,
    action: str,
    status: str,
    notebook_id: str | None = None,
    query_pack: str | None = None,
    output_file: str | None = None,
    message: str = "",
) -> None:
    event = {
        "timestamp": now_timestamp(),
        "stage": stage,
        "action": action,
        "status": status,
        "notebook_id": notebook_id,
        "query_pack": query_pack,
        "output_file": output_file,
        "message": message,
    }
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def stage_query_pack(stage: str) -> str | None:
    for query in QUERY_PACKS:
        if query["stage"] == stage:
            return query["filename"]
    return None


def run_side_task(target: Path, stage: str, task_name: str) -> str:
    if task_name == "ensure_query_packs":
        for query in QUERY_PACKS:
            query_path = target / "queries" / query["filename"]
            if not query_path.exists():
                write_json_yaml(query_path, query)
        return "Query packs ensured."
    if task_name == "ensure_stage_placeholders":
        book = BookBrief.from_mapping(read_data_file(target / "book-brief.yaml"))
        for filename in REFERENCE_FILES:
            reference_path = target / "references" / filename
            if not reference_path.exists():
                reference_path.write_text(placeholder_reference_text(filename, book), encoding="utf-8")
        return "Reference placeholders ensured."
    if task_name == "initialize_logs":
        ensure_run_log(target)
        if not (target / "logs" / "checkpoint.json").exists():
            save_checkpoint(target, load_checkpoint(target))
        return "Logs initialized."
    if task_name == "validate_previous_outputs":
        missing = []
        for filename in STAGE_REQUIREMENTS.get(stage, []):
            file_path = target / "references" / filename
            if not file_path.exists():
                missing.append(filename)
        if missing:
            return f"Missing prerequisite outputs: {', '.join(missing)}."
        return "Previous outputs validated."
    if task_name == "prepare_next_stage_prompts":
        pack_name = stage_query_pack(stage)
        if pack_name is None:
            return "No query pack associated with this stage."
        query = read_data_file(target / "queries" / pack_name)
        query.setdefault("prepared_at", now_timestamp())
        write_json_yaml(target / "queries" / pack_name, query)
        return f"Prepared {pack_name}."
    raise ValueError(f"Unknown side task: {task_name}")


def normalize_status(raw: str | None) -> str:
    value = str(raw or "pending").strip().lower()
    aliases = {
        "complete": "done",
        "completed": "done",
        "ready": "done",
        "success": "done",
        "processing": "running",
        "in_progress": "running",
    }
    return aliases.get(value, value)


def wait_for_completion(
    target: Path,
    *,
    stage: str,
    adapter: Any,
    poll_interval_seconds: int,
    timeout_seconds: int,
    max_retries: int,
    side_tasks: Iterable[str] | None = None,
    notebook_id: str | None = None,
    sleep_fn: Callable[[float], None] = time.sleep,
    monotonic_fn: Callable[[], float] = time.monotonic,
) -> dict[str, Any]:
    target = Path(target)
    ensure_standard_structure(target)
    log_path = ensure_run_log(target)
    checkpoint = load_checkpoint(target)
    checkpoint["stage"] = stage
    completed_tasks = set(checkpoint.get("completed_side_tasks", []))
    retries = int(checkpoint.get("attempts", 0))
    side_task_names = list(side_tasks or DEFAULT_SIDE_TASKS)
    start_time = monotonic_fn()
    append_log_event(target, log_path, stage=stage, action="wait_start", status="running", notebook_id=notebook_id, message="Wait loop started.")
    while True:
        elapsed = monotonic_fn() - start_time
        if elapsed > timeout_seconds:
            checkpoint["status"] = "timeout"
            checkpoint["attempts"] = retries
            checkpoint["completed_side_tasks"] = sorted(completed_tasks)
            save_checkpoint(target, checkpoint)
            append_log_event(target, log_path, stage=stage, action="wait_timeout", status="timeout", notebook_id=notebook_id, message=f"Timed out after {timeout_seconds} seconds.")
            return {"ok": False, "status": "timeout", "log_path": str(log_path)}

        status_payload = adapter.get_status(stage)
        current_status = normalize_status(status_payload.get("status"))
        notebook_id = notebook_id or status_payload.get("notebook_id")
        message = str(status_payload.get("message", "")).strip()
        checkpoint["status"] = current_status
        checkpoint["notebook_id"] = notebook_id

        append_log_event(
            target,
            log_path,
            stage=stage,
            action="status_poll",
            status=current_status,
            notebook_id=notebook_id,
            query_pack=stage_query_pack(stage),
            message=message or f"Polled stage '{stage}'.",
        )

        if current_status == "done":
            checkpoint["completed_side_tasks"] = sorted(completed_tasks)
            checkpoint["attempts"] = retries
            save_checkpoint(target, checkpoint)
            append_log_event(target, log_path, stage=stage, action="wait_complete", status="done", notebook_id=notebook_id, message="Stage completed.")
            return {"ok": True, "status": "done", "log_path": str(log_path)}

        if current_status in {"failed", "error"}:
            retries += 1
            checkpoint["attempts"] = retries
            if retries > max_retries:
                checkpoint["completed_side_tasks"] = sorted(completed_tasks)
                save_checkpoint(target, checkpoint)
                append_log_event(target, log_path, stage=stage, action="wait_failed", status="failed", notebook_id=notebook_id, message=message or "Maximum retries exceeded.")
                return {"ok": False, "status": "failed", "log_path": str(log_path)}
            append_log_event(target, log_path, stage=stage, action="retry_scheduled", status="retrying", notebook_id=notebook_id, message=f"Retry {retries} of {max_retries}.")

        for task_name in side_task_names:
            if task_name in completed_tasks:
                continue
            task_message = run_side_task(target, stage, task_name)
            completed_tasks.add(task_name)
            append_log_event(
                target,
                log_path,
                stage=stage,
                action=task_name,
                status="ok",
                notebook_id=notebook_id,
                query_pack=stage_query_pack(stage),
                message=task_message,
            )
        checkpoint["completed_side_tasks"] = sorted(completed_tasks)
        checkpoint["attempts"] = retries
        save_checkpoint(target, checkpoint)
        sleep_fn(poll_interval_seconds)


def import_legacy_output(target: Path, legacy_output_dir: Path) -> list[str]:
    copied = []
    legacy_path = Path(legacy_output_dir)
    if not legacy_path.exists():
        return copied
    references_dir = Path(target) / "references"
    references_dir.mkdir(parents=True, exist_ok=True)
    for filename in REFERENCE_FILES:
        source = legacy_path / filename
        if source.exists():
            shutil.copyfile(source, references_dir / filename)
            copied.append(filename)
    return copied


def render_skill_markdown(book: BookBrief, target: Path) -> str:
    slug = target.name
    references = "\n".join(f"- [`{name}`](references/{name})" for name in REFERENCE_FILES)
    query_refs = "\n".join(f"- [`{item['filename']}`](queries/{item['filename']})" for item in QUERY_PACKS)
    return (
        "---\n"
        f"name: {slug}\n"
        f"description: Use when the user wants book-derived methods, decision rules, or analysis workflows from {book.title} in a reusable skill format.\n"
        "---\n\n"
        f"# {book.title} Skill\n\n"
        "## Overview\n\n"
        f"This generated skill packages the book-derived workflow for **{book.title}** into a standard skill directory. "
        "Use the reference documents for evidence-backed detail and the workflow file for staged execution.\n\n"
        "## When to Use\n\n"
        f"- Use when the user explicitly wants methods, heuristics, or problem framing from **{book.title}**.\n"
        "- Use when you need evidence-backed references instead of a generic summary.\n"
        "- Do not use when the user only wants a simple review or summary.\n\n"
        "## Quick Reference\n\n"
        f"- Author: {book.author}\n"
        f"- Domain: {book.domain}\n"
        f"- Audience: {book.audience}\n"
        f"- Goal: {book.goal}\n"
        f"- Language: {book.language}\n\n"
        "## Workflow\n\n"
        "- Read `workflow.yaml` for the staged extraction contract.\n"
        "- Use the `queries/` pack files as the default NotebookLM prompt set.\n"
        "- Use `logs/` for lightweight run audit trails and checkpoint recovery.\n\n"
        "## References\n\n"
        f"{references}\n\n"
        "## Query Packs\n\n"
        f"{query_refs}\n"
    )


def finalize_generated_skill(target: Path, legacy_output_dir: Path | None = None) -> dict[str, Any]:
    target = Path(target)
    if legacy_output_dir is not None:
        import_legacy_output(target, legacy_output_dir)
    book_payload = read_data_file(target / "book-brief.yaml")
    if not book_payload and (target / "workflow.yaml").exists():
        workflow = read_data_file(target / "workflow.yaml")
        book_payload = workflow.get("book", {})
    book = BookBrief.from_mapping(book_payload)
    ensure_standard_structure(target)
    for query in QUERY_PACKS:
        query_path = target / "queries" / query["filename"]
        if not query_path.exists():
            write_json_yaml(query_path, query)
    for filename in REFERENCE_FILES:
        ref_path = target / "references" / filename
        if not ref_path.exists():
            ref_path.write_text(placeholder_reference_text(filename, book), encoding="utf-8")
    skill_text = render_skill_markdown(book, target)
    (target / "SKILL.md").write_text(skill_text, encoding="utf-8")
    write_json_yaml(
        target / "skill-bundle-manifest.yaml",
        {
            "source_book": book.title,
            "master_skill_name": target.name,
            "included_methods": ["references/02-method-catalog.md"],
            "generated_docs": [f"references/{name}" for name in REFERENCE_FILES] + ["SKILL.md", "workflow.yaml"],
            "platform_notes": [
                "Generated by skillify-textbooks runtime",
                "logs/ is optional and may remain gitignored",
            ],
        },
    )
    return {"ok": True, "skill_dir": str(target)}
