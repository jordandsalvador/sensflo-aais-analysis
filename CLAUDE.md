# Advisor AI Solutions — Operator HQ Reference

> **Purpose of this file.** A shared reference for any Claude session or skill working on
> Advisor AI Solutions (AAIS) business operations. It maps the existing Notion "Operator HQ"
> system, the connected integrations, and the target weekly accountability / project-manager
> workflow. Read this first before building automations so you compose with what already exists
> instead of duplicating it.
>
> Owner: jordan@advisoraisolutions.com · Last verified: 2026-05-25

---

## 1. Business context

Advisor AI Solutions runs an operator system summarized as:
**Cold email → recorded → discovery → growth plan → client.** "Run the system; the system runs
the business." Sub-hubs: **Sales**, **Podcast**, **Brand & Templates**.

The single weekly accountability anchor is **"Today's Top 3 Outcomes"** on the Notion **Home**
page, edited every Monday.

---

## 2. Connected integrations

These capabilities are available via MCP in AAIS Claude sessions (server IDs are session-specific
UUIDs — match by capability, not by ID):

| Capability | Use for |
|---|---|
| **Notion** | The Operator HQ system of record (see §3). Read/write pages, query databases, meeting notes. |
| **Fathom** | Meeting transcripts + summaries (read-only). Discovery/sales call source. |
| **Zoom** | Recordings list + assets/transcripts. |
| **Gmail** | Search threads, draft replies, labels. Follow-up source + outbound drafts. |
| **Google Calendar** | List/create/update events. |
| **Calendly** | Availability, event types, booking links. |
| **Google Drive** | Read/search/create files. |
| **Gamma** | Generate presentations/docs/webpages. |
| **Canva** | Generate/export designs. |
| **GitHub** | This repo only: `jordandsalvador/sensflo-aais-analysis`. |

**Not connected (needed but absent):**
- **GoHighLevel (GHL)** — no MCP tool in-session. To touch GHL, add a connected GHL integration
  or a REST API token, then call the GHL API from a script.

---

## 3. Notion Operator HQ map

Canonical hub: **Home** — `80ad53400caf4196a60b49600d290f76`

| Area | Page / DB ID | Data source (collection) | Role |
|---|---|---|---|
| Home (anchor) | `80ad53400caf4196a60b49600d290f76` | — | Top 3 outcomes, daily snapshot, navigation |
| 🎯 Today | `09bcff94167440cdbe3330cb0eb31cf0` | — | Today's items |
| 📅 This Week | `7ed23348e97a4e15b974f4428fa7525e` | — | Week view |
| 🤖 AI To-Dos | `c027cd40b5c145ec99718cb24dc32fad` | `aa14f147-df0d-48c6-bf9c-3d896f72fb07` | Auto-captured action items. Views: 🙋 Mine · 👥 Others owe me |
| 🤝 Clients | `29a6b313e696433ead58a4481e2b5afb` | `5f271c2c-c609-4258-b484-9e749c7865c6` | Active book of business by stage/industry |
| 📌 Projects | `a3e68e36c002410fbcd6b0e809fa9efc` | `f6508b5b-fd31-4645-adfe-906fecb561d5` | Delivery tracker, board by health |
| 🗓️ Tasks | `b0bfe62b4887432ba0b41473c856a687` | `b3bc9e6e-53d7-4d1f-9efe-60f4b7481524` | Master backlog |
| 📥 Conversation Inbox | `3aad5e5784474461aa6805bb8e251bbf` | `c02e8cb6-40c0-46be-b2a9-4e1523ba1e3a` | Raw transcripts/emails/notes to process |
| ✅ Done Log | `c911734ea8904735a33ebc7f9201757b` | `448eb5e4-18e5-48c6-aceb-90528ccbfa8e` | Completed work |

Sub-hubs: **Sales** `3697fd5427ba8177a18dc2eccf361367` · **Podcast** `3697fd5427ba81edba6dc4e073bb4298`
· **Brand & Templates** `3697fd5427ba81249a8ce8e9d6e5c91b` (contains the voice/tone spec).

> Verify a database's schema with the Notion `fetch` tool on its `collection://` ID before
> writing rows — property names/options may evolve.

---

## 4. Existing automation

An **"accountability skill"** already auto-populates **🤖 AI To-Dos** ~2×/day from
**Gmail · Fathom · Zoom · Riverside** transcripts, splitting items into **🙋 Mine** and
**👥 Others owe me**. It also performs periodic cleanup (observed: items "auto-closed by reorg
sweep"). Compose new work on top of this — do not rebuild capture from scratch.

---

## 5. Target workflow — weekly meeting scan + accountability + project manager

The intended unified loop (a "weekly scan" layer on top of the daily capture):

1. **Scan** — pull the week's meetings (Fathom transcripts + Zoom recordings) and new Gmail
   threads since the last run.
2. **Extract** — decisions, commitments, action items → tag owner (Mine vs Others owe me),
   due date, and linked Client/Project.
3. **Reconcile** — upsert into 🤖 AI To-Dos; update 📌 Projects health; add 🗓️ Tasks; move
   finished work to ✅ Done Log; close stale items.
4. **PM layer** — flag overdue items, stalled projects, and "others owe me" follow-ups;
   sanity-check the week against Today's Top 3.
5. **Push out** — draft follow-up emails in Gmail; sync clients/opportunities/tasks to **GHL**
   (pending connection — see §2).
6. **Report** — post a weekly accountability digest (Notion and/or email).

Scheduling: run the weekly scan via `/loop` (e.g., Monday morning) while the existing
~2×/day daily capture continues.

---

## 6. Open items / decisions pending

- **GHL integration** — not connected. Need a token or connected integration, plus the sync
  scope (contacts? opportunities/pipeline? tasks?) and the target sub-account/location.
- **`saviorsaver88`** — referenced by the owner as a skill/tool to tie in, but not found in
  this environment or Notion. Identify what/where it is (existing skill, separate repo, or a
  GHL location) before composing with it.
- **Proposed name for the unified orchestrator:** "AAIS Operator" skill (scan → accountability
  → PM → GHL → digest). Not yet built.

---

## 7. Conventions

- **Voice & tone:** clear, operator-level, confident, technical-but-approachable,
  results-oriented. Full spec lives in the Brand & Templates hub.
- **Source of truth is Notion Home** — if something isn't on the calendar / in the system,
  treat it as not happening.
- **Development branch for business-optimization work:** `claude/business-optimization-GvKme`.
