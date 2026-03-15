# Installation Guide

## Quick Install

### Option 1: Direct Copy (Recommended for Claude Code Users)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/skillify-textbooks.git

# Copy skill to your Claude Code skills directory
cp -r skillify-textbooks/skills/book-to-skills ~/.claude/skills/

# Done! The skill will auto-trigger on book-related queries
```

### Option 2: Symbolic Link (For Development)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/skillify-textbooks.git
cd skillify-textbooks

# Create symbolic link for development
ln -s "$(pwd)/skills/book-to-skills" ~/.claude/skills/book-to-skills

# Now you can edit files and test immediately
```

## Verification

After installation, verify the skill is recognized:

```bash
# Check skill files exist
ls ~/.claude/skills/book-to-skills/

# Expected output:
# SKILL.md
# parallel-manifest.yaml
# AGENT_ORCHESTRATOR.md
# references/
```

## Usage

Once installed, simply ask in Claude Code:

```
"帮我从《思考，快与慢》生成一套技能"
"Convert 'Thinking, Fast and Slow' into a skill"
"把《金字塔原理》转成方法论技能"
```

The skill will automatically:
1. Parse your book reference
2. Set up NotebookLM workspace
3. Execute parallel agent extraction
4. Generate the skill bundle

## Requirements

- Claude Code or compatible agent environment
- NotebookLM MCP connection (for book processing)
- Git (for installation)

## Troubleshooting

### Skill not triggering?

Check that:
1. Files are in `~/.claude/skills/book-to-skills/`
2. `SKILL.md` has proper frontmatter (--- name/description ---)
3. Restart Claude Code after installation

### Parallel execution issues?

The skill supports three execution modes:
- `auto_parallel` (default): Automatically parallelizes independent agents
- `manual_batch`: User confirms each batch
- `sequential_fallback`: Runs all agents sequentially

To force sequential mode, add to your query:
```
"...使用串行模式执行"
```
