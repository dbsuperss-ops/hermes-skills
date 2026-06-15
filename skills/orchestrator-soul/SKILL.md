---
name: orchestrator-soul
description: "Apply Orchestrator Mode SOUL.md — Hermes becomes a pure orchestrator, delegating all coding/planning to Codex CLI, Claude Code CLI, and AntiGravity CLI"
version: 1.0.0
author: dbsuperss
---

# Orchestrator Mode SOUL.md

This skill tells Hermes to stop doing any work itself and instead act as a pure orchestrator.

## How to apply

```bash
# 1. Install this skill
hermes skills install https://raw.githubusercontent.com/dbsuperss-ops/hermes-skills/main/skills/orchestrator-soul/SKILL.md

# 2. View the SOUL.md content and copy it to your profile
skill_view(name="orchestrator-soul", file_path="references/soul.md")

# 3. Replace your profile's SOUL.md with the content above
nano ~/.hermes/profiles/work/SOUL.md   # or ~/.hermes/SOUL.md
```

Then restart Hermes or start a new session.