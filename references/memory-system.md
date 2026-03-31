# File-Based Memory System Reference

This document describes the persistent memory architecture used by GitHub Claw.

## Overview

GitHub Claw uses **committed files** as its memory, not ephemeral conversation
history. This means:

- Memory survives across sessions, devices, and even different AI providers
- Memory is version-controlled, auditable, and searchable
- Memory can be edited by both the human and the AI
- Memory has clear structure with different tiers for different lifespans

## Memory Architecture

```
your-repo/
├── MEMORY.md              # Long-term memory (persistent facts)
├── memory/
│   ├── tasks.md           # Task tracker (cross-session)
│   ├── 2026-03-30.md      # Daily log
│   ├── 2026-03-31.md      # Daily log
│   └── ...
```

## MEMORY.md — Long-Term Memory

This file stores information that should persist indefinitely:

- User preferences and working style
- Project background and goals
- Persistent agreements and conventions
- Important decision records with dates and rationale

### Template

```markdown
# MEMORY.md — Long-Term Memory

Read this file at the start of every new conversation. Update it when
important new information emerges.

---

## User & Project Background

- **Repository name**: your-repo
- **Purpose**: [description]
- **Initialization date**: YYYY-MM-DD
- **AI assistant code name**: Claw

---

## User Preferences

- [Primary language for communication]
- [Coding style preferences]
- [Tool preferences]

---

## Persistent Agreements

- [Convention 1]
- [Convention 2]

---

## Important Decision Record

| Date | Decision | Reason |
|---|---|---|
| YYYY-MM-DD | [what] | [why] |

---

*Last updated: YYYY-MM-DD*
```

## memory/tasks.md — Task Tracker

Cross-conversation task tracking with three states:

```markdown
# Task Tracker

Status: `[ ]` to-do | `[~]` in-progress | `[x]` done

---

## In Progress

- [~] **YYYY-MM-DD** Task description

---

## To-Do

- [ ] Task description

---

## Completed (Recent)

- [x] **YYYY-MM-DD** Task description

---

## Completed

- [x] **YYYY-MM-DD** Task description

---

*Last updated: YYYY-MM-DD*
```

## memory/YYYY-MM-DD.md — Daily Logs

Each day gets a log file capturing what happened:

```markdown
# YYYY-MM-DD Work Log

## Completed Tasks

### Task Name
- What was done
- Key details

## Decisions

- [Decision made and why]

## Notes

- [Anything worth remembering]
```

### Log Lifecycle

- Created on demand when work happens on a given day
- Logs older than 30 days may be archived or deleted
- Important information from old logs should be promoted to `MEMORY.md`

## Read-First Protocol

Every new conversation follows this sequence:

1. Read `AGENTS.md` — restore identity and operating rules
2. Read `MEMORY.md` — restore long-term context
3. Read latest `memory/YYYY-MM-DD.md` — understand recent work
4. Read `memory/tasks.md` — understand current priorities

This takes seconds and ensures the AI never starts from zero.

## Write-Promptly Protocol

Before ending a conversation:

1. Write today's work to `memory/YYYY-MM-DD.md`
2. Update task status in `memory/tasks.md`
3. If new persistent info emerged, append to `MEMORY.md`
4. Commit all changes
