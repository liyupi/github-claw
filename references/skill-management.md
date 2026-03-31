# Skill Discovery, Installation & Management Reference

This document describes the skill ecosystem used by GitHub Claw.

## Overview

Skills are reusable capability packages that extend what the AI assistant can
do. They live in `.agents/skills/` and follow a standardized structure.

## Skill Structure

```
.agents/skills/
├── README.md                    # Skill registry (lists all installed skills)
├── skill-name/
│   ├── SKILL.md                 # Main entry point (required)
│   ├── scripts/                 # Executable scripts (optional)
│   ├── references/              # Reference docs (optional)
│   └── assets/                  # Templates, icons, etc. (optional)
```

### SKILL.md Requirements

Every skill must have a `SKILL.md` with:

1. **YAML frontmatter** with `name` and `description`
2. **Markdown body** with instructions for the AI

```markdown
---
name: my-skill
description: What this skill does and when to use it
---

# Skill Title

Instructions for the AI assistant...
```

### Skill Registry (README.md)

The `.agents/skills/README.md` tracks all installed skills:

```markdown
# Project-Level Skill Library

Skills are stored in `.agents/skills/<skill-name>/` with `SKILL.md` as entry point.

## Installed Skills

- `skill-name`: Brief description
  Entry: `.agents/skills/skill-name/SKILL.md`
```

## Skill Workflow

### 1. Check Local First

Before building anything from scratch, check `.agents/skills/` for existing skills
that can be reused or composed.

### 2. Search External

If no local skill fits, search:
- GitHub open source repositories
- Skills.sh marketplace
- The `anthropics/skills` reference repository

### 3. Evaluate Before Installing

Prefer skills that are:
- From clear, reputable sources
- Well-structured with complete documentation
- Low-risk (no suspicious scripts or network calls)

### 4. Install

```bash
# Create skill directory
mkdir -p .agents/skills/<skill-name>

# Copy or create SKILL.md and supporting files
# ...

# Update the registry
# Add entry to .agents/skills/README.md
```

### 5. Register

After installing, immediately update `.agents/skills/README.md` with:
- Skill name and brief description
- Entry point path
- Source (if from external repo)
- Any notes about API keys or dependencies

### 6. Build If Needed

If no existing skill fits, complete the task manually. If the result is
reusable, extract it as a new skill for future sessions.

### 7. Avoid Duplicates

Before installing, check for existing skills with the same name or purpose.
Keep directory naming clear and structure clean.

## External Skill Tracking

When installing skills from external sources, track provenance in a
`skills-lock.json` at the repo root:

```json
{
  "version": 1,
  "skills": {
    "skill-name": {
      "source": "org/repo",
      "sourceType": "github",
      "computedHash": "sha256..."
    }
  }
}
```

This enables auditing which skills came from where and detecting if upstream
versions have changed.
