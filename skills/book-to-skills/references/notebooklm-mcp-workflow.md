# NotebookLM MCP Workflow

## Goal

Use NotebookLM MCP as the primary execution interface for transforming a single book into a reusable skill bundle.

## Execution Model

- One book maps to one notebook.
- Extraction is multi-stage and serial by default.
- Each stage produces structured output for the next stage.
- Strong claims require evidence; weak claims are downgraded.

## Stage Flow

### Stage 1: Prepare Notebook

- Create or reuse a notebook named after the book.
- Add the book source or extracted text.
- Record `BookBrief`.

Suggested MCP tools:

- `mcp__notebooklm-mcp__notebook_create`
- `mcp__notebooklm-mcp__source_add`
- `mcp__notebooklm-mcp__notebook_get`

### Stage 2: Book Mapping

- Ask for the high-level structure of the book.
- Identify main chapters, recurring themes, and core claims.
- Produce input for the `Book Profiler`.

Suggested MCP tool:

- `mcp__notebooklm-mcp__notebook_query`

### Stage 3: Author Thinking Extraction

- Ask how the author frames problems.
- Capture recurring analysis dimensions, decision heuristics, and sequencing habits.
- Produce input for the `Author Thinking Analyst`.

### Stage 4: Methodology Mining

- Ask for explicit and implicit methods.
- Merge repeated advice into reusable modules.
- Convert outputs into `MethodCard` candidates.

### Stage 5: Scenario Routing

- Ask where each method applies.
- Identify trigger conditions, failure modes, and anti-patterns.
- Produce input for the `Scenario Router`.

### Stage 6: Conflict Check and Synthesis

- Remove duplicates.
- Resolve method overlaps and dependencies.
- Flag unsupported claims.
- Prepare the final bundle for `Skill Packager / QA`.

## Evidence Rules

- Preserve references to chapters, source snippets, or other traceable evidence.
- Do not upgrade inferred patterns into facts without evidence notes.
- If NotebookLM returns vague or generic language, re-ask with narrower scope.

## Serial-First Rule

Even if the design includes multiple subagents, first version should execute stage by stage:

1. Map the book.
2. Extract the author's thinking style.
3. Mine methods.
4. Route methods to scenarios.
5. Package and verify.

This keeps the workflow debuggable and easier to validate inside Claude Code or OpenClaw.
