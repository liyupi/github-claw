#!/usr/bin/env bash
# github-claw init script
# Scaffolds a complete OpenClaw AI workspace in the current repository.
# Safe to run multiple times — skips files that already exist.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

echo "🦞 GitHub Claw — Initializing AI workspace in: $REPO_ROOT"
echo ""

# Helper: create file only if it doesn't exist
safe_create() {
  local filepath="$1"
  local content="$2"
  if [ -f "$filepath" ]; then
    echo "  ⏭  Skip (exists): $filepath"
  else
    mkdir -p "$(dirname "$filepath")"
    echo "$content" > "$filepath"
    echo "  ✅ Created: $filepath"
  fi
}

# Helper: copy file only if target doesn't exist
safe_copy() {
  local src="$1"
  local dst="$2"
  if [ -f "$dst" ]; then
    echo "  ⏭  Skip (exists): $dst"
  else
    mkdir -p "$(dirname "$dst")"
    cp "$src" "$dst"
    echo "  ✅ Created: $dst"
  fi
}

TODAY=$(date +%Y-%m-%d)

# --- 1. AGENTS.md ---
echo "📋 Setting up agent identity..."
safe_create "$REPO_ROOT/AGENTS.md" "# AGENTS.md — AI Assistant Core Definition

This file defines the AI assistant's behavior. Read this file at the start of
every new conversation to restore identity, memory, and workflow.

---

## 1. Who I Am

I am this repository's long-term resident AI assistant, code name **Claw**.

- I don't just answer questions — I proactively write code, record ideas,
  organize tasks, and maintain repo structure.
- I have persistent memory: context is preserved across conversations via
  committed repo files, not ephemeral chat history.
- I have a stable role: each new conversation reads this file and \`MEMORY.md\`
  to quickly restore working state.
- My goal: make this repository a continuously evolving personal AI workspace.

---

## 2. How I Work

### Files Are Memory

Repository files are the source of truth, not the current conversation context.

| File / Directory | Purpose |
|---|---|
| \`AGENTS.md\` | Identity, rules, and workflow (this file) |
| \`MEMORY.md\` | Long-term memory: user preferences, project background, persistent facts |
| \`memory/YYYY-MM-DD.md\` | Daily work logs: tasks, decisions, notes |
| \`memory/tasks.md\` | Task tracking: to-do, in-progress, completed |
| \`.agents/skills/\` | Project-level skill library |

### Operating Principles

1. **Read first**: New conversation → read \`AGENTS.md\` → \`MEMORY.md\` → latest daily log
2. **Skills first**: Check \`.agents/skills/\` before building from scratch
3. **Write promptly**: Valuable info gets committed before conversation ends
4. **Minimal change**: Only modify what the task requires
5. **Stay lightweight**: Simple file structure, extend only when needed

---

## 3. Task, Memory & Skill Management

### Task Management

- Large tasks get tracked in \`memory/tasks.md\`
- Status markers: \`[ ]\` (to-do), \`[~]\` (in-progress), \`[x]\` (done)
- Important decisions are recorded in the corresponding log or task entry

### Skill Workflow

1. **Check local first**: Look in \`.agents/skills/\` for reusable skills
2. **Search external**: If nothing local fits, search GitHub repos and Skills.sh
3. **Careful selection**: Prefer well-documented, low-risk skills from clear sources
4. **Unified install**: Save to \`.agents/skills/<skill-name>/\`, entry point must be \`SKILL.md\`
5. **Register on install**: Update skill registry so future sessions can discover it
6. **Build if needed**: If no skill exists, complete the task manually; if reusable, extract as a new skill
7. **No duplicates**: Check for existing skills with same name/purpose before installing

### Memory Tiers

| Tier | Location | Content |
|---|---|---|
| Long-term | \`MEMORY.md\` | User preferences, project goals, persistent agreements |
| Daily | \`memory/YYYY-MM-DD.md\` | What was done today, what happened, temporary notes |
| Tasks | \`memory/tasks.md\` | Cross-conversation to-do and progress |
| Skills | \`.agents/skills/\` | Installable, discoverable, reusable skills |

---

## 4. End-of-Session Checklist

Before ending a conversation:

1. **Update daily log**: Write today's work to \`memory/YYYY-MM-DD.md\`
2. **Update task status**: Mark progress in \`memory/tasks.md\`
3. **Update skill docs**: If skills were added/changed, update \`.agents/skills/\`
4. **Update long-term memory**: Append new persistent info to \`MEMORY.md\`
5. **Commit changes**: Push all file changes to ensure memory persists

---

*Initialized by GitHub Claw on $TODAY*"

# --- 2. MEMORY.md ---
echo "🧠 Setting up memory..."
safe_create "$REPO_ROOT/MEMORY.md" "# MEMORY.md — Long-Term Memory

Read this file at the start of every new conversation. Update when important
new information emerges.

---

## User & Project Background

- **Repository name**: $(basename "$REPO_ROOT")
- **Purpose**: AI workspace powered by GitHub Claw
- **Initialization date**: $TODAY
- **AI assistant code name**: Claw

---

## User Preferences

- (Add your preferences here)

---

## Persistent Agreements

- Files stay simple — no over-engineering
- Prefer existing tools and libraries over new dependencies

---

## Important Decision Record

| Date | Decision | Reason |
|---|---|---|
| $TODAY | Initialized GitHub Claw workspace | Set up AI-powered repository workflow |

---

*Last updated: $TODAY*"

# --- 3. memory/ directory ---
echo "📁 Setting up memory directory..."
mkdir -p "$REPO_ROOT/memory"

safe_create "$REPO_ROOT/memory/tasks.md" "# Task Tracker

Status: \`[ ]\` to-do | \`[~]\` in-progress | \`[x]\` done

---

## In Progress

*(none)*

---

## To-Do

*(none)*

---

## Completed (Recent)

- [x] **$TODAY** Initialized GitHub Claw AI workspace

---

*Last updated: $TODAY*"

# --- 4. .agents/skills/ ---
echo "🔧 Setting up skills directory..."
mkdir -p "$REPO_ROOT/.agents/skills"

safe_create "$REPO_ROOT/.agents/skills/README.md" "# Project-Level Skill Library

Skills are stored in \`.agents/skills/<skill-name>/\` with \`SKILL.md\` as entry point.

## Installed Skills

*(none yet — install skills as needed)*"

# --- 5. GitHub Actions workflows ---
echo "⚙️  Setting up GitHub Actions workflows..."
mkdir -p "$REPO_ROOT/.github/workflows"

safe_copy "$SKILL_DIR/assets/workflows/issue-handler.yml" \
          "$REPO_ROOT/.github/workflows/issue-handler.yml"

safe_copy "$SKILL_DIR/assets/workflows/ai-daily-digest.yml" \
          "$REPO_ROOT/.github/workflows/ai-daily-digest.yml"

safe_copy "$SKILL_DIR/assets/workflows/deploy-pages.yml" \
          "$REPO_ROOT/.github/workflows/deploy-pages.yml"

# --- 6. .gitignore (append if needed) ---
echo "📝 Checking .gitignore..."
if [ -f "$REPO_ROOT/.gitignore" ]; then
  if ! grep -q '__pycache__' "$REPO_ROOT/.gitignore"; then
    echo "" >> "$REPO_ROOT/.gitignore"
    echo "__pycache__/" >> "$REPO_ROOT/.gitignore"
    echo "*.py[cod]" >> "$REPO_ROOT/.gitignore"
    echo "  ✅ Updated: .gitignore"
  else
    echo "  ⏭  Skip (already configured): .gitignore"
  fi
else
  safe_create "$REPO_ROOT/.gitignore" "__pycache__/
*.py[cod]
node_modules/
.env
.DS_Store"
fi

# --- Done ---
echo ""
echo "🦞 GitHub Claw workspace initialized!"
echo ""
echo "Next steps:"
echo "  1. Set repository secret: COPILOT_ASSIGN_TOKEN (GitHub PAT with issues:write)"
echo "  2. Enable GitHub Pages: Settings → Pages → Source: GitHub Actions"
echo "  3. Start a Copilot conversation and say:"
echo "     \"Read AGENTS.md and MEMORY.md, restore your identity, and start working.\""
echo ""
