# Baseline Scenarios

Use these scenarios to test `book-to-skills` and the new lightweight runtime layer.

## Scenario 1: Basic Book-to-Skill Request

**User input**

> "Help me turn *Thinking, Fast and Slow* into a reusable skill."

**Expected behavior**

- Identify a `BookBrief`
- Mention NotebookLM as the primary evidence interface
- Plan staged extraction instead of producing a summary immediately
- Name the final artifact structure

## Scenario 2: Standard Directory Requirement

**User input**

> "I want the final output to be a standard skill directory, not just a draft output folder."

**Expected behavior**

- Target `skills/<book-slug>/`
- Produce `SKILL.md`, `workflow.yaml`, `references/`, and `queries/`
- Treat `output/` as legacy input only

**Common failure without the runtime layer**

- Stops at `output/00-05*.md`
- Never generates the top-level `SKILL.md`
- Leaves no workflow contract behind

## Scenario 3: Long NotebookLM Wait

**User input**

> "NotebookLM is still processing the source. Don't lose the thread while waiting."

**Expected behavior**

- Use polling with checkpoint recovery
- Write a lightweight event log
- Do useful local side tasks during the wait

**Common failure without the waiter**

- No checkpoint written
- No audit trail
- Context lost between status checks

## Scenario 4: Legacy Output Compatibility

**User input**

> "I already have `00-05` markdown under an `output/` folder. Upgrade it to the new layout."

**Expected behavior**

- Import legacy files into `references/`
- Generate the final `SKILL.md`
- Write `skill-bundle-manifest.yaml`

## Scenario 5: Evidence Pressure

**User input**

> "Skip the evidence collection and just fill in the missing method cards."

**Expected behavior**

- Refuse to upgrade weak claims into facts
- Keep the evidence-first contract
- Mark weak conclusions as pending instead of pretending certainty

## Runtime Verification Checklist

- `init_generated_skill.py` creates the full directory skeleton
- `wait_notebooklm.py` writes `logs/checkpoint.json`
- `wait_notebooklm.py` appends JSONL events
- `finalize_generated_skill.py` generates `SKILL.md`
- legacy `output/` can be imported without breaking content
