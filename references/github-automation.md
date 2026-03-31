# GitHub Actions Automation Reference

This document describes all GitHub Actions workflow templates included with
GitHub Claw.

## Overview

GitHub Claw includes three workflow templates that automate common repository
operations. All workflows use `actions/github-script@v7` for direct GitHub API
access without additional dependencies.

## Workflow 1: Issue Auto-Handler

**File**: `.github/workflows/issue-handler.yml`
**Template**: `assets/workflows/issue-handler.yml`

### Triggers

| Event | Condition | Action |
|---|---|---|
| `issues: opened` | Any new issue | Post welcome comment |
| `issues: labeled` | Label is `bug` | Assign to Copilot coding agent |

### Auto-Reply Behavior

When a new issue is opened, the workflow posts a comment:
- Greets the author by username
- Asks for environment info, reproduction steps, and expected vs actual behavior
- For feature requests, asks for use case and expected outcome
- Footer marks it as automated

### Bug Auto-Assignment

When an issue receives the `bug` label:
- Calls the GitHub API to assign `copilot-swe-agent[bot]`
- Uses `agent_assignment` parameter for Copilot coding agent integration
- Posts a confirmation comment on success
- Posts an error message (with details) on failure, so the user knows what went wrong

### Required Secret

- `COPILOT_ASSIGN_TOKEN` — GitHub PAT with `issues:write` scope. Required because
  the default `GITHUB_TOKEN` cannot assign the Copilot bot.

### Customization

| What | Where | How |
|---|---|---|
| Welcome message text | `auto-reply` job, `body` array | Edit the string array |
| Bug assignee | `assign-copilot-on-bug` job | Change `copilot-swe-agent[bot]` |
| Trigger label | Job `if` condition | Change `'bug'` to another label |
| Language | Comment strings | Translate as needed |

---

## Workflow 2: AI Daily Digest

**File**: `.github/workflows/ai-daily-digest.yml`
**Template**: `assets/workflows/ai-daily-digest.yml`

### What It Does

Runs daily on a schedule to collect AI technology news and create a GitHub Issue
with the digest. Three data sources:

1. **GitHub New AI Repos** — Searches for repos with `topic:artificial-intelligence`
   created in the past week with 50+ stars
2. **GitHub Active AI Repos** — Searches for repos mentioning AI/LLM/GPT keywords,
   pushed to in the past week, with 1000+ stars
3. **Hacker News** — Fetches top stories and filters for AI-related keywords
   (AI, LLM, GPT, OpenAI, Claude, Gemini, Anthropic, etc.)

### Schedule

Default: UTC 05:17 daily (Beijing 13:17). Change the cron expression to adjust.

### Output

Creates a GitHub Issue with label `daily-digest` containing:
- 🔥 AI tech hot topics from Hacker News (up to 10)
- 🌟 New AI projects from GitHub (up to 10)
- 🚀 Recently active AI projects from GitHub (up to 10)

### Customization

| What | Where | How |
|---|---|---|
| Schedule | `cron` field | Change cron expression |
| Keywords | `aiKeywords` regex | Add/remove terms |
| Star thresholds | Search queries | Change `stars:>50` / `stars:>1000` |
| Issue label | `labels` array | Change `daily-digest` |
| Language | Issue body strings | Translate headings and descriptions |

---

## Workflow 3: GitHub Pages Deploy

**File**: `.github/workflows/deploy-pages.yml`
**Template**: `assets/workflows/deploy-pages.yml`

### What It Does

Automatically deploys the `site/` directory to GitHub Pages whenever files in
that directory are pushed to the `main` branch.

### Triggers

- Push to `main` branch with changes in `site/**`
- Manual trigger via `workflow_dispatch`

### Prerequisites

The user must enable GitHub Pages in the repository settings:
1. Go to Settings → Pages
2. Set Source to "GitHub Actions"

### Customization

| What | Where | How |
|---|---|---|
| Source directory | `path` in upload step | Change `site` to another directory |
| Trigger branch | `branches` array | Change `main` to another branch |
| Trigger paths | `paths` array | Adjust file patterns |

---

## Adding New Workflows

When the user needs additional automation, follow this pattern:

1. Create the workflow file in `.github/workflows/`
2. Use `actions/github-script@v7` for GitHub API operations
3. Use `actions/checkout@v4` when repo content is needed
4. Wrap API calls in try/catch with user-facing error messages
5. Add a documentation comment at the top of the workflow
6. If the workflow needs special permissions, document the required secrets
