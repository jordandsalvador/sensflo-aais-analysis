# accountability-pm

Autonomous accountability + project-manager skill for Claude Code. Scans Gmail, Fathom, and Zoom on a twice-daily schedule, extracts action items, and writes them to Notion, Google Calendar (as Free events with a 7:30 AM MST reminder), a Gmail draft digest, and a local markdown file. Also supports a manual "Riverside" mode where you paste a transcript.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | The actual skill prompt Claude follows. |
| `config.example.json` | Template for the per-user config. Copy to `config.json`. |
| `hooks/should-run.sh` | SessionStart hook gate — fires the skill once per Morning/EOD window. |

## Install as a user skill

```bash
# Copy the skill to your user skills directory.
cp -r .claude/skills/accountability-pm ~/.claude/skills/

# Seed an empty config (the skill will auto-detect identity on first run).
cp ~/.claude/skills/accountability-pm/config.example.json \
   ~/.claude/skills/accountability-pm/config.json
```

## Wire up the twice-daily SessionStart hook

Add this to `~/.claude/settings.json` (merge into your existing `hooks` block):

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

How it works: the hook checks the current America/Denver hour and the cached "last window" file. If the current window (Morning before 14:00, EOD after) hasn't been run yet today, it prints a one-line instruction telling Claude to invoke the skill. Otherwise it stays silent and the session proceeds normally.

> If you want a true cron-style trigger that fires even when no session is open, run `claude -p "/accountability-pm"` from cron at 08:00 and 17:00 America/Denver. The SessionStart hook gives you the same effect as long as you open Claude Code at least once per window.

## Required MCP servers

The skill calls tools from these MCP servers (all already connected in this environment):

- **Gmail** — read inbox threads, create digest drafts
- **Fathom** — list meetings, fetch summaries/transcripts
- **Zoom** — list recordings, fetch transcripts
- **Notion** — search/create database, query rows for dedupe, create pages
- **Google Calendar** — create transparent events with reminders

## Usage

| What you say | What happens |
|---|---|
| `/accountability-pm` (or "run the PM skill") | Scan mode. Pulls new data since last run, writes new to-dos. |
| "Process this Riverside transcript: <paste>" | Riverside mode. Same extraction, source tagged as `Riverside`. |
| "What's on my plate today?" / "Show outstanding to-dos" | Review mode. Read-only Notion query, grouped summary. |

## What gets created

- **Notion** — one DB named `AI To-Dos` (created on first run if missing) with rows including `Task`, `Owner`, `Due Date`, `Source`, `Source Link`, `Source ID`, `Status`, `Priority`, `Confidence`, `Notes`.
- **Google Calendar** — a 15-min timed event at 07:30 America/Denver on the due date, marked **Free** (`transparency: transparent`), with a popup reminder at event start. Title prefixed `[PM]`.
- **Gmail draft** — one digest per run titled `PM digest — YYYY-MM-DD Morning|EOD`, addressed to yourself. Not sent.
- **Local markdown** — appended to `~/todos/YYYY-MM-DD.md`.

## Dedupe

Every row carries a deterministic `Source ID` like `gmail:<thread_id>:<task_hash>`. Re-runs check this id before writing, so running twice in the same window (or across days for the same email) won't create duplicates.

## Identity

On first run, the skill calls Fathom's `get_identity` to learn your name + email and caches it in `config.json`. That identity is used to decide which action items belong to "Me" vs. another person you need to follow up with.
