# Skillify Textbooks

`skillify-textbooks` turns a book-processing skill prototype into a lightweight execution layer that can generate **standard installable skill directories**.

The project still keeps `skills/book-to-skills/` as the meta-skill and methodology source. The new scripts add the missing runtime layer for:

- creating a standard generated skill directory with `pathlib`
- polling NotebookLM-style stages with checkpoint recovery
- saving lightweight run logs and query packs
- finalizing `00-05` reference outputs into a top-level `SKILL.md`

## What Changed

Generated book outputs no longer stop at a loose `output/` folder. The target shape is now:

```text
skills/<book-slug>/
├── SKILL.md
├── book-brief.yaml
├── workflow.yaml
├── skill-bundle-manifest.yaml
├── references/
│   ├── 00-overview.md
│   ├── 01-author-thinking.md
│   ├── 02-method-catalog.md
│   ├── 03-scenario-router.md
│   ├── 04-subagent-playbooks.md
│   └── 05-master-skill-spec.md
├── queries/
│   ├── pack-01-book-mapping.yaml
│   ├── pack-02-author-thinking.yaml
│   ├── pack-03-methodology-mining.yaml
│   ├── pack-04-scenario-routing.yaml
│   └── pack-05-conflict-check.yaml
└── logs/
    ├── checkpoint.json
    └── run-*.jsonl
```

`logs/` stays optional at commit time, but the runtime writes to it during actual runs.

## Runtime Scripts

The new CLI layer lives under `scripts/`:

- `init_generated_skill.py`
  - reads a `BookBrief`
  - computes the slug
  - creates the standard skill directory
  - prewrites `workflow.yaml`, query packs, placeholders, and log bootstrap files
- `wait_notebooklm.py`
  - polls a stage status file through a file-based adapter
  - supports checkpoint recovery
  - runs lightweight side tasks while waiting
- `finalize_generated_skill.py`
  - imports legacy `output/` style markdown when needed
  - finalizes `SKILL.md`
  - writes `skill-bundle-manifest.yaml`

## Quick Start

### 1. Create the generated skill scaffold

```bash
python scripts/init_generated_skill.py \
  --skills-root skills \
  --title "Thinking, Fast and Slow" \
  --author "Daniel Kahneman" \
  --domain "Behavioral economics" \
  --audience "Agent builders" \
  --goal "Create a reusable book-derived skill" \
  --language en
```

### 2. Wait on a NotebookLM-style stage

Prepare a small status file such as:

```json
{
  "status": "running",
  "message": "NotebookLM is still processing the source.",
  "notebook_id": "demo-notebook"
}
```

Then run:

```bash
python scripts/wait_notebooklm.py \
  --skill-dir skills/thinking-fast-and-slow \
  --stage methodology-mining \
  --status-file tmp/notebook-status.json
```

### 3. Finalize the generated skill

```bash
python scripts/finalize_generated_skill.py \
  --skill-dir skills/thinking-fast-and-slow
```

If you already have legacy `00-05` files under an `output/` directory, you can import them:

```bash
python scripts/finalize_generated_skill.py \
  --skill-dir skills/corporate-finance \
  --legacy-output-dir skills/corporate-finance/output
```

## Repository Structure

- `skills/book-to-skills/`
  - the meta-skill and methodology references
- `skills/<book-slug>/`
  - generated book-specific skills in standard skill layout
- `scripts/`
  - lightweight runtime layer
- `tests/`
  - unit tests for init, wait, finalize, and legacy compatibility

## Testing

Run the standard library test suite:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Notes

- This is an optimization, not a rewrite of the core methodology.
- The wait loop is intentionally **polling + side tasks**, not a heavy async scheduler.
- `workflow.yaml` is stored as JSON-compatible YAML so it stays easy to parse without extra dependencies.
