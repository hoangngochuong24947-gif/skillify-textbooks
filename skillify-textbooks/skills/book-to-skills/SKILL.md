---
name: book-to-skills
description: Use when the user wants to turn a book into reusable skills, methodology documents, or a book-derived thinking system for Claude Code, OpenClaw, or similar agent environments. Trigger on phrases like "从书生成skill" or "book to skill" or when user wants to extract methodologies from a book.
---

# Book to Skills

## Overview

Transform a book into reusable, evidence-based skills that an agent can actually call. This skill enforces systematic extraction—not summary generation—to produce a structured bundle including author thinking models, methodology cards, routing rules, and execution-ready Markdown outputs.

**Core principle:** Every conclusion must have evidence from the book. No guesswork, no relying on training data about the book.

## When to Use

**Use this skill when:**
- User says "帮我从《书名》生成skill"
- User wants to extract methodologies, frameworks, or thinking patterns from a book
- User needs a book-derived thinking system for agent environments
- User wants to convert book content into reusable MethodCards

**Do NOT use when:**
- User just wants a book summary or review
- User wants subjective interpretation without evidence
- The book has no clear methodology or framework

## Decision Flowchart

```dot
digraph usage_decision {
  "User mentions book + skill/methodology?" [shape=diamond];
  "User wants summary only?" [shape=diamond];
  "Book has extractable methods?" [shape=diamond];
  "Use book-to-skills" [shape=box,style=filled,fillcolor=lightgreen];
  "Refuse or redirect" [shape=box,style=filled,fillcolor=lightcoral];
  "Proceed with summary" [shape=box,style=filled,fillcolor=lightyellow];

  "User mentions book + skill/methodology?" -> "User wants summary only?" [label="yes"];
  "User wants summary only?" -> "Proceed with summary" [label="yes"];
  "User wants summary only?" -> "Book has extractable methods?" [label="no"];
  "Book has extractable methods?" -> "Use book-to-skills" [label="yes"];
  "Book has extractable methods?" -> "Refuse or redirect" [label="no"];
}
```

## Outcomes

This skill produces a structured bundle that helps an agent answer:

1. Should this book's thinking style be applied to the user's problem?
2. Which methodology modules from the book are relevant?
3. Which subagents should be assigned?
4. Which Markdown documents should be produced?

## Red Flags - STOP and Reassess

- **Thinking "I know this book"** → STOP. Use NotebookLM to query the actual content, not your training data.
- **Creating content without evidence** → STOP. Every MethodCard needs evidence references.
- **Skipping the five-stage query process** → STOP. This ensures systematic extraction.
- **Producing just a summary** → STOP. This skill creates executable skills, not summaries.

## Required Inputs

Collect or infer a minimal `BookBrief`:

```yaml
title: string
author: string
domain: string
audience: string
goal: string
language: zh | en
```

If some fields are missing, continue with reasonable assumptions and record them in the output.

## Default Workflow

1. **Create NotebookLM notebook** for the selected book
2. **Execute five-stage query packs** from [references/query-packs.md](references/query-packs.md)
3. **Build book map and author thinking model**
4. **Convert techniques into MethodCards** (see schema below)
5. **Route methods to problem types** and define combination rules
6. **Assign subagents** using [references/subagent-playbooks.md](references/subagent-playbooks.md)
7. **Package into Markdown output bundle** per [references/output-schemas.md](references/output-schemas.md)
8. **Prepare infographic structure** (optional) using [references/visual-infographic-spec.md](references/visual-infographic-spec.md)

## MethodCard Schema

Every extracted method must be documented as:

```yaml
name: string              # Method name
thesis: string            # Core claim/principle
triggers:                 # When to use this method
  - string
steps:                    # Executable steps
  - string
scenarios:                # Example applications
  - string
limits:                   # When NOT to use
  - string
evidence:                 # Book evidence references
  - "Chapter X, Section Y: specific quote or reference"
assigned_agents:          # Which subagents handle this
  - string
```

## Subagent System

Use the following fixed roles:

| Role | Primary Duty | Key Output |
|------|--------------|------------|
| `Book Profiler` | Build book map, structure, core issues | `00-overview.md` |
| `Author Thinking Analyst` | Extract author's judgment patterns | `01-author-thinking.md` |
| `Methodology Miner` | Convert scattered techniques to MethodCards | `02-method-catalog.md` |
| `Scenario Router` | Map methods to problem types | `03-scenario-router.md` |
| `Skill Packager / QA` | Compile skill spec and validate evidence | `04-subagent-playbooks.md`, `05-master-skill-spec.md` |

Read [references/subagent-playbooks.md](references/subagent-playbooks.md) before assigning work.

## Output Bundle

Produce these Markdown artifacts:

- `00-overview.md` - Book goals, structure, concept map, keywords
- `01-author-thinking.md` - Author's observation patterns, judgment framework
- `02-method-catalog.md` - All MethodCards, grouped by theme
- `03-scenario-router.md` - Problem-to-method mapping and combination rules
- `04-subagent-playbooks.md` - Subagent duties, inputs, outputs, handoffs
- `05-master-skill-spec.md` - Top-level skill logic, delegation, output rules

Schemas defined in [references/output-schemas.md](references/output-schemas.md).

## Operating Rules

| Rule | Violation Consequence |
|------|----------------------|
| **Use NotebookLM MCP as primary interface** | Risk using training data instead of actual book content |
| **Use staged, purpose-built prompts** | Open-ended chat leads to inconsistent extraction |
| **Every conclusion must have evidence** | Skills drift from book content, become unreliable |
| **Weak conclusions → mark as pending** | Publishing unverified methods damages skill quality |
| **First version: single book only** | Scope creep, unfinished multi-book mess |
| **Logical parallel, actual serial execution** | Race conditions, inconsistent state |

## Common Mistakes & Fixes

| Mistake | Why It Happens | Fix |
|---------|----------------|-----|
| Relying on training data about the book | Faster than reading | Force NotebookLM query first, every time |
| Creating generic summaries | Easier than structured extraction | Follow the five-stage query packs strictly |
| Missing evidence references | Forget to record during extraction | Add evidence field to every MethodCard template |
| Weak conclusions promoted | Want to appear complete | Mark as `pending_confirmation` instead |
| Skipping subagent assignments | Simpler to do it all yourself | Use fixed role system, delegate systematically |

## Reference Guide

- **NotebookLM workflow**: [references/notebooklm-mcp-workflow.md](references/notebooklm-mcp-workflow.md)
- **Question packs**: [references/query-packs.md](references/query-packs.md)
- **Subagent contracts**: [references/subagent-playbooks.md](references/subagent-playbooks.md)
- **Output schemas**: [references/output-schemas.md](references/output-schemas.md)
- **Infographic structure**: [references/visual-infographic-spec.md](references/visual-infographic-spec.md)

## Quick Reference: Default Prompt Shape

When invoked without detailed spec, assume the user wants:

- Structured extraction of the book's thinking system
- Methodology cards with evidence
- Routing logic for real user problems
- Master skill specification for Claude Code / OpenClaw execution

**Start with:** "I'll help you convert this book into reusable skills. First, let me set up the extraction workflow..."
