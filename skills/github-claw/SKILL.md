---
name: github-claw
description: >
  Turn any GitHub repository into an OpenClaw-style AI workspace — a persistent,
  self-evolving "crayfish" (小龙虾) system powered by GitHub Copilot. Installs an
  agent identity, file-based memory, skill management, GitHub Actions automation
  (daily digest, issue auto-reply, bug auto-assign to Copilot, PR review, Pages
  deploy), and a structured project scaffold. Use this skill whenever the user
  wants to set up an AI-driven workspace, create a Copilot-powered repo, build a
  self-maintaining GitHub project, or mentions "claw", "小龙虾", "AI workspace",
  "agent workspace", "Copilot workspace", or "OpenClaw".
---

# GitHub Claw — Turn GitHub into a Crayfish 🦞

Transform any GitHub repository into a persistent, self-evolving AI workspace
where GitHub Copilot acts as a long-term resident assistant (code name **Claw**).

## What This Skill Does

This skill scaffolds a complete AI workspace with seven integrated capabilities:

1. **Agent Identity & Persona** — `AGENTS.md` defines who Claw is, how it works, and its operating principles
2. **File-Based Memory** — `MEMORY.md` + `memory/` provide long-term context, daily logs, and task tracking
3. **Skill Discovery & Management** — `.agents/skills/` ecosystem for installing, managing, and reusing skills
4. **Scheduled Automation** — GitHub Actions workflows for daily AI news digest
5. **Issue Auto-Handling** — Auto-reply to new issues + auto-assign bugs to Copilot coding agent
6. **Pages Deployment** — Auto-deploy a `site/` directory to GitHub Pages on push
7. **Development Workflow** — Structured approach to coding, PR review, and project progression

## Quick Start

When a user asks to set up an OpenClaw workspace, follow this sequence:

### Step 1: Initialize the Workspace

Run the initialization script to scaffold all files:

```bash
bash skills/github-claw/scripts/init.sh
```

This creates the full directory structure. If the repo already has some of these
files, the script will skip them (no overwriting).

### Step 2: Configure Secrets

Tell the user to set up one GitHub repository secret:

- `COPILOT_ASSIGN_TOKEN` — A GitHub PAT with `issues:write` permission, required
  for the bug-auto-assign workflow to assign issues to `copilot-swe-agent[bot]`.

### Step 3: Personalize

After scaffolding, help the user customize:

- **`AGENTS.md`** — Change the agent name, language, or operating principles
- **`MEMORY.md`** — Add project-specific background and user preferences
- **Workflow schedules** — Adjust cron times in `.github/workflows/`

### Step 4: First Conversation

Tell the user to open a Copilot chat and say:

> 请读取 `AGENTS.md` 和 `MEMORY.md`，恢复你的身份和工作状态，然后开始工作。

---

## Capability Details

For detailed reference on each capability, read the corresponding file in
`references/` when needed:

| Capability | Reference File | When to Read |
|---|---|---|
| Agent identity, persona, operating rules | `references/agent-identity.md` | When customizing the agent's role or behavior |
| File-based memory system | `references/memory-system.md` | When setting up or troubleshooting memory |
| Skill discovery, install, management | `references/skill-management.md` | When adding or managing skills |
| GitHub Actions automation (all workflows) | `references/github-automation.md` | When customizing workflows or adding new ones |

## Workflow Templates

Pre-built GitHub Actions workflow files are in `assets/workflows/`:

| File | Purpose |
|---|---|
| `issue-handler.yml` | Auto-reply to new issues + assign bugs to Copilot |
| `ai-daily-digest.yml` | Daily AI news digest from GitHub + Hacker News |
| `deploy-pages.yml` | Auto-deploy `site/` to GitHub Pages |

These are copied into `.github/workflows/` by the init script.

## File Structure After Installation

```
your-repo/
├── AGENTS.md                          # Agent identity & rules
├── MEMORY.md                          # Long-term memory
├── README.md                          # Repo overview
├── memory/
│   ├── tasks.md                       # Task tracker
│   └── YYYY-MM-DD.md                  # Daily logs (created as needed)
├── .agents/
│   └── skills/
│       └── README.md                  # Skill registry
├── .github/
│   └── workflows/
│       ├── issue-handler.yml          # Issue automation
│       ├── ai-daily-digest.yml        # Daily digest
│       └── deploy-pages.yml           # Pages deploy
└── site/                              # (optional) Static site directory
```

## Design Principles

- **Files are memory** — All persistent state lives in committed files, not ephemeral chat
- **Read-first** — Every new conversation starts by reading `AGENTS.md` → `MEMORY.md` → latest daily log
- **Skills-first** — Check local `.agents/skills/` before building from scratch
- **Minimal change** — Only modify what the task requires
- **Lightweight** — Simple file structure, extend only when needed
- **Language-agnostic** — Works with any programming language or project type
