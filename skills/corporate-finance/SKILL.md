---
name: corporate-finance
description: Use when the user wants book-derived methods, decision rules, or analysis workflows from Corporate Finance in a reusable skill format.
---

# Corporate Finance Skill

## Overview

This generated skill packages the book-derived workflow for **Corporate Finance** into a standard skill directory. Use the reference documents for evidence-backed detail and the workflow file for staged execution.

## When to Use

- Use when the user explicitly wants methods, heuristics, or problem framing from **Corporate Finance**.
- Use when you need evidence-backed references instead of a generic summary.
- Do not use when the user only wants a simple review or summary.

## Quick Reference

- Author: Stephen A. Ross, Randolph W. Westerfield, Bradford D. Jordan
- Domain: Corporate finance
- Audience: Students and finance practitioners
- Goal: Create a reusable corporate finance decision skill
- Language: en

## Workflow

- Read `workflow.yaml` for the staged extraction contract.
- Use the `queries/` pack files as the default NotebookLM prompt set.
- Use `logs/` for lightweight run audit trails and checkpoint recovery.

## References

- [`00-overview.md`](references/00-overview.md)
- [`01-author-thinking.md`](references/01-author-thinking.md)
- [`02-method-catalog.md`](references/02-method-catalog.md)
- [`03-scenario-router.md`](references/03-scenario-router.md)
- [`04-subagent-playbooks.md`](references/04-subagent-playbooks.md)
- [`05-master-skill-spec.md`](references/05-master-skill-spec.md)

## Query Packs

- [`pack-01-book-mapping.yaml`](queries/pack-01-book-mapping.yaml)
- [`pack-02-author-thinking.yaml`](queries/pack-02-author-thinking.yaml)
- [`pack-03-methodology-mining.yaml`](queries/pack-03-methodology-mining.yaml)
- [`pack-04-scenario-routing.yaml`](queries/pack-04-scenario-routing.yaml)
- [`pack-05-conflict-check.yaml`](queries/pack-05-conflict-check.yaml)
