# GitHub Claw 🦞

> Turn any GitHub repository into a self-evolving AI workspace powered by GitHub Copilot.

## What is GitHub Claw?

GitHub Claw is a **reusable agent skill** that transforms a GitHub repository into
a persistent, self-evolving AI workspace. It gives GitHub Copilot (or any compatible
AI coding agent) a stable identity, file-based memory, skill management, and
automated workflows — turning it from a one-shot Q&A tool into a long-term
collaborative partner.

## Capabilities

| Capability | Description |
|---|---|
| 🧠 **Agent Identity** | Persistent persona with operating principles via `AGENTS.md` |
| 📁 **File-Based Memory** | Long-term context, daily logs, task tracking via `MEMORY.md` + `memory/` |
| 🔧 **Skill Management** | Discover, install, and reuse skills in `.agents/skills/` |
| 📰 **Daily Digest** | Automated AI news from GitHub + Hacker News, posted as Issues |
| 🐛 **Issue Automation** | Auto-reply to new issues + auto-assign bugs to Copilot |
| 🚀 **Pages Deploy** | Auto-deploy `site/` to GitHub Pages on push |
| 💻 **Dev Workflow** | Structured approach to coding, review, and project progression |

## Skill Structure

```
github-claw/
├── SKILL.md                        # Skill entry point (YAML frontmatter + instructions)
├── README.md                       # This file
├── LICENSE                         # MIT license
├── references/
│   ├── agent-identity.md           # AGENTS.md template & customization guide
│   ├── memory-system.md            # File-based memory architecture
│   ├── skill-management.md         # Skill discovery/install/manage workflow
│   └── github-automation.md        # GitHub Actions workflow documentation
├── assets/workflows/
│   ├── issue-handler.yml           # Auto-reply + Copilot bug assignment
│   ├── ai-daily-digest.yml         # Daily AI news digest
│   └── deploy-pages.yml            # GitHub Pages auto-deploy
└── scripts/
    └── init.sh                     # One-command workspace initialization
```

## Installation

### Option A: Clone and init

```bash
# Clone this skill
git clone https://github.com/liyupi/github-claw.git /tmp/github-claw

# Copy to your repo
mkdir -p /path/to/your-repo/skills
cp -r /tmp/github-claw /path/to/your-repo/skills/github-claw

# Initialize your workspace
cd /path/to/your-repo
bash skills/github-claw/scripts/init.sh

# Clean up
rm -rf /tmp/github-claw
```

### Option B: Manual setup

Read `SKILL.md` and follow the Quick Start instructions to create files manually.

## Post-Installation Setup

1. **Set repository secret**: Go to Settings → Secrets → Actions, add
   `COPILOT_ASSIGN_TOKEN` with a GitHub PAT that has `issues:write` permission.

2. **Enable GitHub Pages** (optional): Go to Settings → Pages, set Source to
   "GitHub Actions".

3. **Start working**: Open a Copilot conversation and say:

   > Read `AGENTS.md` and `MEMORY.md`, restore your identity, and start working.

## After Initialization

Your repo will have these new files:

```
your-repo/
├── AGENTS.md                          # Agent identity & operating rules
├── MEMORY.md                          # Long-term memory
├── memory/
│   └── tasks.md                       # Task tracker
├── .agents/
│   └── skills/
│       └── README.md                  # Skill registry
├── .github/
│   └── workflows/
│       ├── issue-handler.yml          # Issue auto-reply + Copilot assignment
│       ├── ai-daily-digest.yml        # Daily AI news digest
│       └── deploy-pages.yml           # GitHub Pages auto-deploy
└── skills/
    └── github-claw/                   # This skill (kept for reference)
```

## Customization

- **Agent name**: Edit `AGENTS.md` section 1 (default: "Claw")
- **Language**: All templates default to English; translate as needed
- **Workflow schedule**: Edit cron expressions in `.github/workflows/`
- **Issue reply text**: Edit strings in `issue-handler.yml`
- **Digest keywords**: Edit the `aiKeywords` regex in `ai-daily-digest.yml`

## License

MIT
