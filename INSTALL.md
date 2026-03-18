# Installation Guide

## Requirements

- Python 3.10+
- A NotebookLM-compatible workflow outside the repository
- An agent environment that can use the generated skill directories

This repository does not bundle a live NotebookLM client. The runtime is designed to stay lightweight and adapter-friendly.

## Install for Development

```bash
git clone https://github.com/YOUR_USERNAME/skillify-textbooks.git
cd skillify-textbooks
```

## Verify the Runtime Layer

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Generate a Standard Skill Directory

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

Expected output:

```text
skills/thinking-fast-and-slow/
```

## Poll a Stage While NotebookLM Works

```bash
python scripts/wait_notebooklm.py \
  --skill-dir skills/thinking-fast-and-slow \
  --stage methodology-mining \
  --status-file tmp/notebook-status.json
```

The waiter will:

- poll the stage status
- keep a checkpoint under `logs/checkpoint.json`
- append lightweight audit events to `logs/run-*.jsonl`
- fill in any missing query pack or placeholder artifacts

## Finalize the Skill

```bash
python scripts/finalize_generated_skill.py \
  --skill-dir skills/thinking-fast-and-slow
```

If you are upgrading an older sample that still has `output/00-05*.md`:

```bash
python scripts/finalize_generated_skill.py \
  --skill-dir skills/corporate-finance \
  --legacy-output-dir skills/corporate-finance/output
```

## Result

After finalization, the generated directory is directly usable as a standard skill folder:

- `SKILL.md`
- `workflow.yaml`
- `references/`
- `queries/`
- `logs/`

`logs/` remains optional for commit hygiene and is allowed to stay ignored by git.
