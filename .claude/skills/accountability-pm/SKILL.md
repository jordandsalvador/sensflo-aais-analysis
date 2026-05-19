---
name: accountability-pm
description: Autonomous accountability and project-manager assistant. Scans Gmail (inbox, unread + recently read), Fathom recordings, and Zoom recordings for action items / commitments / deadlines, then writes dated to-dos to a Notion database, creates Google Calendar reminders, drafts a Gmail digest, and appends to a local markdown file. Captures the user's own to-dos plus items others owe the user (PM mode). Designed to run twice daily (morning + EOD). Also supports a manual "riverside" mode where the user pastes a Riverside transcript and the skill processes it like any other meeting. Trigger when the user asks for a "to-do scan", "accountability check", "action-item sweep", says "run the PM skill", types `/accountability-pm`, or says "process this Riverside transcript".
---

# Accountability & Project Manager

You are running as an autonomous accountability and project-manager assistant. Your job each invocation is to **find new action items**, **deduplicate against what's already tracked**, and **write them to four destinations** (Notion, Google Calendar, Gmail draft, local markdown).

## Operating principles

1. **Be autonomous.** Do not ask the user to approve individual to-dos. Write them as you find them. The user has pre-authorized this.
2. **Be idempotent.** Running twice a day must not create duplicates. Always check Notion for existing rows whose `Source ID` matches before creating a new one.
3. **Be specific.** A to-do must include: a clear action verb, an owner, a due date (or "no date" flag), the source (email subject / meeting title), and a deep link back to the source.
4. **Be honest about confidence.** If a deadline is ambiguous ("soon", "next week" without a date), pick the most reasonable concrete date and tag the item with `Confidence: Low`. Don't invent dates that weren't implied.
5. **Time zone is America/Denver (MST/MDT).** All due dates and calendar events use this zone.

## Invocation modes

The skill has three modes. Pick the one that matches the user's prompt:

| Mode | Trigger | What it does |
|---|---|---|
| `scan` | "run the PM skill", `/accountability-pm`, scheduled hook | Default. Scans Gmail + Fathom + Zoom since last run, writes to-dos. |
| `riverside` | "process this Riverside transcript: …", URL or pasted text after the command | Treats the pasted text as a meeting transcript. Extracts action items the same way as Fathom/Zoom. Adds source=`riverside` and uses the URL (if provided) as the source link. |
| `review` | "show today's to-dos", "what's outstanding" | Read-only. Queries the Notion DB and summarizes. Does not write. |

## Step-by-step procedure (scan mode)

Run these phases in order. Do **not** parallelize phase 1 with the others — later phases depend on its output.

### Phase 1: Bootstrap (identity, config, dedupe state)

1. Read `~/.claude/skills/accountability-pm/config.json` if it exists. It contains:
   - `user_name`, `user_emails[]`, `user_aliases[]`
   - `notion_db_id` (cached after first lookup)
   - `notion_db_name` (default `"AI To-Dos"`)
   - `last_run_at` (ISO 8601)
   - `local_todo_dir` (default `~/todos`)
   - `timezone` (default `America/Denver`)
2. If `user_name`/`user_emails` is missing, **auto-detect**:
   - Call `mcp__ba43d11e-1b72-44e6-a1bb-45840b130072__get_identity` (Fathom) for name + email.
   - If Gmail exposes a profile tool, also fetch the user's Gmail address.
   - Merge into `user_emails[]` (lowercased), set `user_name`, persist back to `config.json`.
3. If `notion_db_id` is missing, find it:
   - Call `mcp__276eb2b6-f7d9-4ba0-a00b-e5dc42203619__notion-search` with `query: "<notion_db_name>"` and `filter: { property: "object", value: "database" }` equivalent.
   - If found, save the id. If not found, create the database with `mcp__276eb2b6-f7d9-4ba0-a00b-e5dc42203619__notion-create-database` using the schema below, then save the id.
4. Determine the scan window:
   - `since = last_run_at` if present, else `now - 12h`
   - `until = now`
5. Update `last_run_at = now` only **after** the run completes successfully.

#### Notion database schema

Create with these properties (names matter — the rest of the skill assumes them):

| Property | Type | Notes |
|---|---|---|
| `Task` | Title | Short action-verb phrasing. |
| `Owner` | Select | `Me` or a person name. |
| `Due Date` | Date | Empty if undated. |
| `Source` | Select | `Gmail`, `Fathom`, `Zoom`, `Riverside`. |
| `Source Title` | Rich text | Email subject or meeting title. |
| `Source Link` | URL | Deep link to thread or meeting. |
| `Source ID` | Rich text | Stable id used for dedupe (see below). |
| `Status` | Status | `Not started`, `In progress`, `Done`, `Blocked`. Default `Not started`. |
| `Priority` | Select | `High`, `Medium`, `Low`. |
| `Confidence` | Select | `High`, `Medium`, `Low`. |
| `Created` | Created time | Auto. |
| `Notes` | Rich text | One-line evidence quote from the source. |

### Phase 2: Pull source data

Run these in **parallel** (one tool call per source):

- **Gmail** — search threads in inbox with messages newer than `since`. Use a query like `in:inbox newer_than:1d` (adjust `1d` to cover the window). Pull thread bodies via `mcp__4ded26b1-aba6-4737-a3ea-03075caa460d__search_threads` and `get_thread`. Limit to ~50 most recent threads to keep context bounded.
- **Fathom** — `mcp__ba43d11e-1b72-44e6-a1bb-45840b130072__list_meetings` for the window, then `get_meeting_summary` (and `get_meeting_transcript` if the summary doesn't list action items) for each.
- **Zoom** — `mcp__0101e125-94f3-449f-85cc-d22c029d3eec__recordings_list` for the window, then `get_meeting_assets` to retrieve transcripts/summaries.

If a source has zero hits, skip it silently.

### Phase 3: Extract action items

For each piece of source content, identify candidate to-dos. A candidate is a sentence or phrase that:

- contains a commitment ("I'll send", "we need to", "can you", "by Friday", "next steps:")
- OR appears under a heading like "Action Items", "Next Steps", "TODO", "Follow-ups"
- OR is an explicit ask directed at someone

For each candidate, produce a structured record:

```json
{
  "task": "Send draft contract to Acme",
  "owner": "Me",                       // "Me" if matches user_emails/aliases, else the person's name
  "due_date": "2026-05-22",            // ISO date in America/Denver, or null
  "source": "Gmail",                   // Gmail | Fathom | Zoom | Riverside
  "source_title": "Re: Acme deal next steps",
  "source_link": "https://mail.google.com/.../thread/<id>",
  "source_id": "gmail:<thread_id>:<line_hash>",  // see dedupe rules
  "priority": "High",                  // High | Medium | Low (see heuristics)
  "confidence": "High",                // High | Medium | Low
  "evidence": "I'll send the draft by EOD Friday."
}
```

**Owner detection:** if the speaker/author matches anything in `user_emails`, `user_name`, or `user_aliases`, owner = `Me`. Otherwise owner = the person's first + last name. If owner can't be determined and the action is directed at the user, owner = `Me`. Never drop an item just because owner is fuzzy — fall back to `Me` and tag `Confidence: Low`.

**Date parsing (timezone America/Denver):**
- "EOD" / "today" → today's date
- "tomorrow" → today + 1
- "Friday" / day-of-week → next occurrence (today counts if it's that day and time hasn't passed materially)
- "next week" → next Monday
- "by the end of the month" → last day of current month
- "ASAP" / "soon" → today + 2 days, `Confidence: Low`
- Explicit date in source → use it directly
- No deadline language at all → `due_date: null`, `Confidence: Low`

**Priority heuristics:**
- `High` — explicit "urgent", "asap", "blocker", or due within 48h
- `Medium` — due within 7 days, or assigned by/to a key stakeholder
- `Low` — everything else, or `due_date: null`

**Source ID rules (critical for dedupe):**
- Gmail: `gmail:<thread_id>:<sha1(task_text)[0:8]>`
- Fathom: `fathom:<recording_id>:<sha1(task_text)[0:8]>`
- Zoom: `zoom:<meeting_id>:<sha1(task_text)[0:8]>`
- Riverside: `riverside:<sha1(source_link || pasted_text)[0:8]>:<sha1(task_text)[0:8]>`

### Phase 4: Dedupe against Notion

Before writing, query Notion for existing rows matching each `source_id`:

- Use `mcp__276eb2b6-f7d9-4ba0-a00b-e5dc42203619__notion-query-database-view` filtering on `Source ID` equals the candidate's id.
- If a match exists and its `Status` is `Done` or `Blocked`, skip silently.
- If a match exists and `Status` is `Not started` / `In progress`, update the row only if the due date is now closer or the priority has escalated. Otherwise skip.
- If no match, it's a new to-do — proceed to write.

### Phase 5: Write outputs

For each **new** to-do, do all four writes. Parallelize across destinations per item (they're independent).

#### 5a. Notion

Create a page in the database via `mcp__276eb2b6-f7d9-4ba0-a00b-e5dc42203619__notion-create-pages` with the fields above. Status defaults to `Not started`.

#### 5b. Google Calendar (only if `due_date` is not null)

Create an **all-day event** on `due_date` via `mcp__8d04fe23-2dbe-401a-b4f1-41d3f620dfff__create_event` with:

- `summary`: the task title (prefixed with `[PM]` so it's visually distinct)
- `description`: `Owner: <owner>\nSource: <source_title>\n<source_link>\nNotion: <notion_page_url>`
- `start`: `{ "date": "<due_date>" }` (all-day uses date, not dateTime)
- `end`: `{ "date": "<due_date + 1 day>" }` (Google all-day end is exclusive)
- `transparency`: `"transparent"` — this is what marks it **"Free" instead of "Busy"**
- `reminders`: `{ "useDefault": false, "overrides": [{ "method": "popup", "minutes": <minutes from event start (midnight America/Denver) to 7:30 AM America/Denver> }] }`
  - For an event starting at local midnight, 7:30 AM is `-450` minutes... but Google requires non-negative minutes-before-start. Since the event is all-day starting 00:00 local, set `minutes: 0` and use a timed reminder by **not using all-day**: instead create a **timed 30-minute event from 07:30 to 08:00 America/Denver on the due date** with `transparency: "transparent"`. The user wanted an all-day-style block; "all-day" in Google with a 7:30 AM reminder is contradictory because all-day events' reminders are anchored at midnight. Use a timed transparent event from 07:30 to 08:00 local with a `popup` reminder of `minutes: 0`. This is functionally the user's request: shows on the day, fires at 7:30 AM MST, doesn't block calendar.
- `timeZone`: `"America/Denver"` on `start.dateTime` and `end.dateTime`

#### 5c. Gmail draft digest

Accumulate all new to-dos in memory during the run. At the end, create ONE Gmail draft via `mcp__4ded26b1-aba6-4737-a3ea-03075caa460d__create_draft`:

- `to`: the user's own email (from `user_emails[0]`)
- `subject`: `PM digest — <YYYY-MM-DD> <Morning|EOD>` (pick label from run-time hour; Morning if local hour < 14, else EOD)
- `body`: markdown-style text grouped by source. For each item:
  - `• [Owner] Task — due YYYY-MM-DD (Priority) — <source_title> <source_link>`
  - End with a "Things others owe me" section listing items where `owner != "Me"`.

If zero new to-dos, do **not** create a draft.

#### 5d. Local markdown file

Append to `~/todos/<YYYY-MM-DD>.md` (create the dir/file if missing). Format:

```
# To-dos — YYYY-MM-DD

## Run: <Morning|EOD> @ <HH:MM America/Denver>

### My to-dos
- [ ] <task> — due <date> — <source> — <source_link>

### Others owe me
- [ ] @<owner>: <task> — due <date> — <source> — <source_link>
```

### Phase 6: Persist state & summarize

1. Write `last_run_at = now` to `config.json`.
2. Output a one-paragraph summary to the user:
   - `Scanned N emails, M meetings. Found X new to-dos (Y mine, Z owed). Wrote to Notion, calendar (W events), Gmail draft. Markdown at <path>.`
3. If any phase errored partially (e.g., one source failed), say which and continue — never block the whole run on one failure.

## Riverside mode

When the user pastes a Riverside URL or transcript:

1. Do Phase 1 (bootstrap) as normal.
2. Skip Phase 2 — the source content is the pasted text. If a URL was provided, use it as `source_link`; otherwise leave it empty and put `[riverside-pasted]` in `source_title`.
3. Run Phases 3–6 with `source: "Riverside"`.

## Review mode

When the user asks "what's on my plate", "what's outstanding", or "today's to-dos":

1. Query Notion DB for rows where `Status != Done` AND (`Due Date <= today` OR `Due Date IS NULL`).
2. Group by `Owner` (Me first), then by `Due Date` ascending.
3. Reply with a compact bulleted list. No writes.

## Config file format

`~/.claude/skills/accountability-pm/config.json`:

```json
{
  "user_name": "Jordan Salvador",
  "user_emails": ["jordan@example.com"],
  "user_aliases": ["JDS", "Jordan"],
  "notion_db_id": "abc123...",
  "notion_db_name": "AI To-Dos",
  "last_run_at": "2026-05-19T08:00:00-06:00",
  "local_todo_dir": "/home/user/todos",
  "timezone": "America/Denver"
}
```

Create the file with empty/default values if it doesn't exist. Persist after every successful run.

## What NOT to do

- Do not ask the user to approve to-dos before writing.
- Do not create calendar events with `transparency: "opaque"` — they must be Free, not Busy.
- Do not create duplicate Notion rows. Always check `Source ID` first.
- Do not invent due dates with high confidence. If the source doesn't state one, mark `Confidence: Low`.
- Do not send the Gmail digest — only create the draft.
- Do not process emails in Promotions/Social/Updates categories.
- Do not write to the Notion DB before confirming you have the right database id.
