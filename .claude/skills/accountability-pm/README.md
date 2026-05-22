# accountability-pm

Autonomous accountability + project-manager skill for Claude Code. Scans Gmail, Fathom, and Zoom on a twice-daily schedule, extracts action items, and writes them to Notion, Google Calendar (on a dedicated "PM To-dos" secondary calendar with a 7:30 AM MST popup), a Gmail draft digest, and a local markdown file. Also supports a manual "Riverside" mode where you paste a transcript.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | The actual skill prompt Claude follows. |
| `config.example.json` | Template for the per-user config. Copy to `config.json`. |
| `hooks/should-run.sh` | SessionStart hook gate — fires the skill once per Morning/EOD window (local-Claude path only). |

## Install as a user skill

```bash
cp -r .claude/skills/accountability-pm ~/.claude/skills/
cp ~/.claude/skills/accountability-pm/config.example.json \
   ~/.claude/skills/accountability-pm/config.json
```

## Recommended trigger: Claude Code on the web "Routines" (cloud cron)

Cloud-based, fires regardless of whether your laptop is awake or open. Two routines, one per window.

1. Create a "PM To-dos" calendar in Google Calendar first (Settings → Add calendar → Create new → name it `PM To-dos`). Run the skill once interactively to bootstrap; it will pick up the calendar id and save it to `config.json`.
2. Open https://claude.ai/code/routines → **New routine**.
3. Configure two routines:

### Routine A — Morning

| Field | Value |
|---|---|
| Name | `accountability-pm — Morning` |
| Schedule | Daily at **08:00** in your local timezone (presets: Daily) |
| Repositories | This repo (so the skill at `.claude/skills/accountability-pm/` is on disk) |
| Environment | The environment that has Notion, Gmail, Google Calendar, Fathom, Zoom MCP connectors authenticated |
| Model | Opus or Sonnet (the skill is fairly demanding on synthesis quality) |
| Prompt | (paste the block below) |

```text
Run the accountability-pm skill in scan mode. The full procedure is in
`.claude/skills/accountability-pm/SKILL.md` — read it, then execute. Use
the config at `.claude/skills/accountability-pm/config.json` for db ids
and emails; if `last_run_at` is missing, scan the last 12 hours. Do all
four writes (Notion, Calendar, Gmail draft, markdown). At the end, commit
any new files under `todos/` and `config.json` updates to this branch
and push.
```

### Routine B — EOD

Same as Morning, but:
- Name: `accountability-pm — EOD`
- Schedule: Daily at **17:00** local

### Custom cron (optional)

The web UI gives you Daily / Weekdays presets. For weekdays-only, pick the **Weekdays** preset. For a non-standard time (e.g. 07:30), use the CLI: `claude` → `/schedule update <routine-id>` and enter a custom cron expression. Minimum interval is 1 hour.

### Notes on cloud routines

- **Stateless containers.** Each routine run starts in a fresh container with the repo cloned. `config.json` must be in the repo (or committed back at end of run) for state like `last_run_at` to persist. The skill auto-falls-back to a 12h window when state is absent — that's fine for twice-daily runs.
- **MCP authentication carries.** Connector auth is per-account, so the routine inherits your Notion / Gmail / Calendar / Fathom / Zoom credentials automatically. If a connector token expires, the routine logs the error and continues with the remaining sources.
- **Local markdown lives in the container.** To keep a record across runs, the routine should commit `todos/<date>.md` back to the repo (the prompt above asks for this).

## Alternative trigger: local Claude Code with a SessionStart hook

Use this if you want runs to fire whenever you open Claude Code locally (requires laptop awake + Claude running). Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/skills/accountability-pm/hooks/should-run.sh"
          }
        ]
      }
    ]
  }
}
```

The hook checks the current America/Denver hour and a cached "last window" file. If the current Morning (< 14:00) or EOD (>= 14:00) window hasn't been run yet today, it prints a one-line instruction telling Claude to invoke the skill.

## Required MCP servers

- **Gmail** — read inbox threads, create digest drafts
- **Fathom** — list meetings, fetch summaries/transcripts
- **Zoom** — list recordings, fetch transcripts
- **Notion** — search/create database, query rows for dedupe, create pages
- **Google Calendar** — create events on the `PM To-dos` secondary calendar

## Usage

| What you say | What happens |
|---|---|
| `/accountability-pm` (or "run the PM skill") | Scan mode. Pulls new data since last run, writes new to-dos. |
| "Process this Riverside transcript: <paste>" | Riverside mode. Same extraction, source tagged as `Riverside`. |
| "What's on my plate today?" / "Show outstanding to-dos" | Review mode. Read-only Notion query, grouped summary. |

## What gets created

- **Notion** — one DB named `AI To-Dos` (created on first run if missing) with rows including `Task`, `Owner`, `Due Date`, `Source`, `Source Link`, `Source ID`, `Status`, `Priority`, `Confidence`, `Notes`.
- **Google Calendar** — a 30-min timed event from 07:30–08:00 America/Denver on the due date on the `PM To-dos` secondary calendar (you control its Free/Busy contribution at the calendar level). Same-day items after 07:30 fire at `now + 5min` instead so the popup actually triggers. Overdue carry-overs get an `[OVERDUE]` prefix and a same-day popup. Title prefixed `[PM]`.
- **Gmail draft** — one digest per run titled `PM digest — YYYY-MM-DD Morning|EOD`, addressed to yourself. Sections: scan stats, MY TO-DOS, THINGS OTHERS OWE ME, CARRY-OVER (due today / overdue prior-run items), LINKS. Not sent.
- **Local markdown** — appended to `~/todos/YYYY-MM-DD.md`.

## Dedupe

Every row carries a deterministic `Source ID` like `gmail:<thread_id>:<task_hash>`. Re-runs check this id before writing, so running twice in the same window (or across days for the same email) won't create duplicates.

## Identity

On first run, the skill calls Fathom's `get_identity` to learn your name + email and caches it in `config.json`. If Fathom is unavailable, set `user_name` and `user_emails` manually in `config.json`. Identity is used to decide which action items belong to "Me" vs. another person you need to follow up with.
