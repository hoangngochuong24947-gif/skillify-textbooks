# Output Schemas

## Standard Generated Skill Directory

Every generated book skill should end in a standard skill directory, not a loose `output/` bundle.

```text
skills/<book-slug>/
├── SKILL.md
├── book-brief.yaml
├── workflow.yaml
├── skill-bundle-manifest.yaml
├── references/
├── queries/
└── logs/
```

## Core Files

### `SKILL.md`

Required skill entry point with:

- YAML frontmatter using only `name` and `description`
- overview of when to use the generated book skill
- links to `references/` and `queries/`
- a short workflow summary that points to `workflow.yaml`

### `book-brief.yaml`

```yaml
{
  "title": "string",
  "author": "string",
  "domain": "string",
  "audience": "string",
  "goal": "string",
  "language": "zh | en"
}
```

### `workflow.yaml`

```yaml
{
  "version": "1.0.0",
  "book": {},
  "execution_mode": "auto_parallel | manual_batch | sequential_fallback",
  "stages": [],
  "wait_policy": {
    "poll_interval_seconds": 5,
    "timeout_seconds": 300,
    "max_retries": 3,
    "side_tasks": []
  },
  "artifacts": {},
  "logging": {}
}
```

Required top-level fields:

- `version`
- `book`
- `execution_mode`
- `stages`
- `wait_policy`
- `artifacts`
- `logging`

## Reference Documents

`references/` contains the staged markdown outputs:

- `00-overview.md`
- `01-author-thinking.md`
- `02-method-catalog.md`
- `03-scenario-router.md`
- `04-subagent-playbooks.md`
- `05-master-skill-spec.md`

These remain the support material behind the generated `SKILL.md`.

## Query Packs

`queries/pack-*.yaml` stores the staged NotebookLM prompt contracts.

Schema:

```yaml
{
  "filename": "string",
  "stage": "string",
  "objective": "string",
  "questions": ["string"],
  "evidence_rule": "string",
  "expected_output": "string"
}
```

## Logs

`logs/` is runtime-only support material and may be gitignored.

### `logs/checkpoint.json`

```yaml
{
  "stage": "string | null",
  "status": "not_started | running | done | failed | timeout",
  "attempts": 0,
  "completed_side_tasks": ["string"],
  "last_updated": "ISO-8601 timestamp"
}
```

### `logs/run-*.jsonl`

Each event line contains:

```json
{
  "timestamp": "ISO-8601 timestamp",
  "stage": "string",
  "action": "string",
  "status": "string",
  "notebook_id": "string | null",
  "query_pack": "string | null",
  "output_file": "string | null",
  "message": "string"
}
```

Required event keys:

- `timestamp`
- `stage`
- `action`
- `status`
- `notebook_id`
- `query_pack`
- `output_file`
- `message`

## Skill Bundle Manifest

`skill-bundle-manifest.yaml` is written during finalization.

```yaml
{
  "source_book": "string",
  "master_skill_name": "string",
  "included_methods": ["string"],
  "generated_docs": ["string"],
  "platform_notes": ["string"]
}
```

## Compatibility Rule

Legacy `output/00-05*.md` folders are supported as migration input, but they are not the final target shape. Finalized skills must place those documents under `references/`.

## Quality Gates

- `SKILL.md` exists
- `workflow.yaml` exists and parses as YAML/JSON-compatible YAML
- `references/00-05*.md` exist
- `queries/pack-*.yaml` exist
- `logs/` is optional for commit validation but must be supported by the runtime
