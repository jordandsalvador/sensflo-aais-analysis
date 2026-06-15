# Advisor AI Solutions — Notion Workspace Map

> **Purpose.** Canonical reference for the Advisor AI Solutions Notion workspace so any
> Claude session, skill, or automation can navigate it without re-discovering structure.
> Treat this as the source of truth for page/database IDs, schemas, conventions, and brand.
>
> **Last verified:** 2026-06-15 · **Owner:** Jordan Salvador (jordan@advisoraisolutions.com)
> **Maintainer note:** if you restructure the workspace, update this file in the same change.

---

## 0. How an agent should use this file

1. Need to **write a to-do** for the user from emails/meetings → use the **🤖 AI To-Dos** data
   source (`aa14f147-df0d-48c6-bf9c-3d896f72fb07`). This is what the `accountability-pm` skill
   drives. Dedupe on `Source ID`. See §4.
2. Need to **read pipeline / clients / projects state** → query the relevant data source in §3.
3. Need to **render or restyle pages** → follow the brand system in §5 and the banner pipeline in §6.
4. IDs come in two flavors — **container `database_id`** (the embed/page you open) and
   **`data_source_id`** (the underlying collection you query/alter). Tools that *query rows* or
   *alter schema* want the **data_source_id**; tools that create *views* want both.

---

## 1. Top-level hierarchy

```
🏠 Home (page 80ad53400caf4196a60b49600d290f76)
├── 💼 Sales (page 3697fd5427ba8177a18dc2eccf361367)
│   ├── 🎯 Leads (db)
│   └── 🗣️ Discovery and Growth Plan Calls (db)
├── 🎙️ Podcast (page 3697fd5427ba81edba6dc4e073bb4298)
│   ├── 🧲 Podcast Pipeline (db)
│   ├── 🎧 Podcast Episodes (db)
│   └── 📝 Call Transcripts (db)
├── 🎨 Brand & Templates (page 3697fd5427ba81249a8ce8e9d6e5c91b)
│   ├── 🎨 Brand Guidelines (page dabcf932d6c748b2a0700945599d44cd)
│   └── [ARCHIVED] Podcast & Sales HQ (page c2682ca3b4a84a1bb8110c58f7d46498)
├── 🗓️ Tasks (db)            ← master task DB
├── 🎯 Today (db)            ← linked view-container of Tasks
├── 📅 This Week (db)        ← linked view-container of Tasks
├── 🤖 AI To-Dos (db)        ← skill-driven; see §4
├── 🤝 Clients (db)
├── 📌 Projects (db)
├── 📥 Conversation Inbox (db)
└── ✅ Done Log (db)
```

`Home` parent page lives under workspace root page **"Home"** ancestor; its own parent is the
top-level page tree (`80ad...` has no ancestor in fetches → it is the workspace landing page).

---

## 2. Pages (quick ID table)

| Page | ID | Notes |
|---|---|---|
| 🏠 Home | `80ad53400caf4196a60b49600d290f76` | Landing hub. Rebuilt 2026-05-23. |
| 💼 Sales | `3697fd5427ba8177a18dc2eccf361367` | Sub-hub. |
| 🎙️ Podcast | `3697fd5427ba81edba6dc4e073bb4298` | Sub-hub. |
| 🎨 Brand & Templates | `3697fd5427ba81249a8ce8e9d6e5c91b` | Sub-hub. |
| 🎨 Brand Guidelines | `dabcf932d6c748b2a0700945599d44cd` | Color/voice spec. |
| [ARCHIVED] Podcast & Sales HQ | `c2682ca3b4a84a1bb8110c58f7d46498` | Legacy hub, content redirects to Home. |

---

## 3. Databases

Each row: **container `database_id`** = the page you open/embed; **`data_source_id`** = the
collection you query/alter. Where one DB has multiple containers (Tasks), they share one
data source.

### 🗓️ Tasks — master task list
- data_source_id: `b3bc9e6e-53d7-4d1f-9efe-60f4b7481524`
- containers: `b0bfe62b4887432ba0b41473c856a687` (🗓️ Tasks) · `09bcff94167440cdbe3330cb0eb31cf0` (🎯 Today) · `7ed23348e97a4e15b974f4428fa7525e` (📅 This Week)
- key props: `Task`(title) · `Status`(status: Not started/Blocked/In progress/Waiting/Done) · `Priority`(select: P0/P1/P2/P3) · `Due`(date) · `Assignee`(person) · `Tags`(multi: Ops/Sales/Product/Engineering) · `Client`(rel→Clients) · `Project`(rel→Projects) · `Notes`
- views (on `b0bfe62b…`): `📋 All tasks` · `🚦 Board` (group Status) · `📆 Calendar` (by Due) · `🔥 High priority` (P0/P1)
- Today/This Week containers filter `Assignee = me` + relative-date `Due`. (Notion's view-DSL can't express `@me`/`today`, so these stay as their own containers.)

### 🎯 Leads — sales pipeline
- data_source_id: `dc642d44-73d1-4305-b847-314c6e890666`
- container: `b68afae31ad94d5d885c37e9a3c5964d` (under 💼 Sales)
- key props: `Lead`(title) · `Company` · `Contact name` · `Email` · `Phone` · `Stage`(status: New→Contacted→Discovery scheduled→Discovery done→Proposal created→Proposal in consideration→Won/Lost) · `Lead source`(multi) · `Follow-up`(date) · `Next step` · `Client (if won)`(rel→Clients) · `Project`(rel→Projects)
- views: `📋 All leads` · `🚦 Pipeline` (board by Stage) · `📆 Follow-ups` (calendar)

### 🤝 Clients — book of business
- data_source_id: `5f271c2c-c609-4258-b484-9e749c7865c6`
- container: `29a6b313e696433ead58a4481e2b5afb`
- key props: `Client`(title) · `Stage`(select: Lead/Discovery/Proposal/Negotiation/Won/Lost) · `Status`(status: Inactive) · `Industry`(select: Sustainable Construction/Engineering (AEC)/GreenTech/ConTech/Other) · `Primary contact` · `Email`/`Phone`/`Website` · `Lead`(rel) · `Projects`(rel) · `Tasks`(rel) · `Follow-up`(date)
- views: `📋 All clients` · `🚦 By Stage` (board) · `🏷️ By Industry` (board)
- has a `New client` page template.

### 📌 Projects — delivery tracker
- data_source_id: `f6508b5b-fd31-4645-adfe-906fecb561d5`
- container: `a3e68e36c002410fbcd6b0e809fa9efc`
- key props: `Project`(title) · `Status`(status: Not started/In progress/Done) · `Health`(select: Green/Yellow/Red) · `Priority`(P0–P3) · `Client`(rel) · `Lead`(rel) · `Tasks`(rel) · `Owner`(person) · `Start`/`Target end`/`Milestone date`(dates) · `Next milestone`
- views: `📋 All projects` · `🚦 By Health` (board) · `📆 Timeline` (Start→Target end)
- has a `New project` page template.

### 🗣️ Discovery and Growth Plan Calls
- data_source_id: `dff6a6f8-2a9a-46b2-9082-23c0c3f1bc2c`
- container: `8912a60b876840e79af287a3dd114d59` (under 💼 Sales)
- key props: `Call`(title) · `Call Date`(date) · `Outcome`(select: Qualified/Nurture/Not a fit) · `Lead (Podcast Pipeline)`(rel→Podcast Pipeline) · `Transcript` · `Notes` · `Next steps` · `Zoom Recording Link`(url) · `Growth Plan PDF`(file) · `Growth Plan Microsite`(url)

### 📥 Conversation Inbox — capture & process
- data_source_id: `c02e8cb6-40c0-46be-b2a9-4e1523ba1e3a`
- container: `3aad5e5784474461aa6805bb8e251bbf`
- key props: `Title`(title) · `Raw (paste here)`(text) · `Processing`(status: Inbox/Needs cleanup/In progress/Processed/Archived) · `Type`(select) · `Source`(select: Fathom/Zoom/Google Meet/Phone/Email/Other) · `Conversation date` · `Lead / Company`(rel) · `Client`(rel) · `Project`(rel) · `Tags`(multi) · `Opportunity / Outcome` · `Next step`
- views: `Inbox` (to-do) · `All` · **`Drop a conversation`** (form_editor — paste transcripts/emails here).

### ✅ Done Log — completed work
- data_source_id: `448eb5e4-18e5-48c6-aceb-90528ccbfa8e`
- container: `c911734ea8904735a33ebc7f9201757b`
- key props: `Done`(title) · `Completed`(date) · `Type`(select: Task/Client work/Project work/Lead / prospect/Ops) · `Client`/`Project`/`Lead`/`Task`(rels) · `Notes`
- views: `Inbox (quick add)` · `By Type` (board) · `Calendar`

### 🧲 Podcast Pipeline — guest funnel
- data_source_id: `ef556975-426b-48df-8724-aa94e97a1e2e`
- container: `e67828546125402b8a39e1b5a2f4891d` (under 🎙️ Podcast)
- key props: `Name`(title) · `Company` · `Email` · `LinkedIn`(url) · `Stage`(status: Prospecting/Cold emailed/Replied/Booked on show/Recorded/Discovery booked/Client/Not pursuing) · `Source`(select: Cold email/Referral/Inbound) · `Cold Email Date`/`Show Record Date`/`Discovery Call Date`(dates) · `Owner`(person) · `Zoom Link`
- views: `🚦 Pipeline` (board by Stage)

### 🎧 Podcast Episodes
- data_source_id: `e63c148b-36eb-4b2f-9dd3-4d31feea80fd`
- container: `a6791da33a9a4002b69c6129c4332a7e` (under 🎙️ Podcast)
- key props: `Episode`(title) · `Status`(status: Planned/Scheduled/Recorded/Editing/Published) · `Guest Name` · `Guest (Pipeline)`(rel→Podcast Pipeline) · `Record Date`/`Publish Date`(dates) · `Episode Link`(url) · `Transcript`
- views: `Episodes` (table) · `Recording Calendar`

### 📝 Call Transcripts — structured meeting library
- data_source_id: `3ace8df9-0b64-49a8-9a5c-715edb89763a`
- container: `bd38cac7d5af41c1b1a0d141d6fde661` (under 🎙️ Podcast)
- key props: `Title`(title) · `Date` · `Source`(select: Fathom/Zoom/Riverside) · `Source ID`(text, dedupe) · `Source Account` · `Participants` · `Duration (min)`(number) · `Summary` · `Action Items` · `Transcript` · `GHL Contact`(url)
- views: `📋 All transcripts`
- Note: complements Conversation Inbox. Inbox = ad-hoc capture w/ processing workflow; Call
  Transcripts = durable, source-ID-deduped meeting record.

---

## 4. 🤖 AI To-Dos — the accountability-pm skill target

**This is the database the `accountability-pm` skill reads/writes. Do not rename its props.**

- data_source_id: `aa14f147-df0d-48c6-bf9c-3d896f72fb07`
- container: `c027cd40b5c145ec99718cb24dc32fad`
- parent page: 🏠 Home

| Property | Type | Values / notes |
|---|---|---|
| `Task` | title | Action-verb phrasing. |
| `Owner` | select | `Me`, `Bella Bethoney`, `Eden Silken`, `Mickey Pendergast`, `Kenneth Cottrell`, `Brian Hurst` (add new people as options before insert). |
| `Due Date` | date | Empty if undated. |
| `Source` | select | `Gmail`, `Fathom`, `Zoom`, `Riverside`. |
| `Source Title` | text | Email subject / meeting title. |
| `Source Link` | url | Deep link to source. |
| `Source ID` | text | **Dedupe key.** `gmail:<thread>:<sha1(task)[:8]>` etc. |
| `Status` | status | `Not started`/`In progress`/`Done`/`Blocked`. |
| `Priority` | select | `High`/`Medium`/`Low`. |
| `Confidence` | select | `High`/`Medium`/`Low`. |
| `Notes` | text | One-line evidence quote. Also appended to by the verify loop. |
| `Calendar Event ID` | text | Cached id of the `[PM]` reminder event written by Phase 5b. Read by the verify loop to delete the reminder when the to-do is auto-closed. |
| `Created` | created_time | Auto. |

**Views** (view IDs for direct query):
- `📋 All to-dos` — `43a2f1e4-9020-41fd-9df9-0d7a03d4df85`
- `🙋 Mine` — `3697fd54-27ba-81f9-a68f-000c17b8bb19` (Owner=Me, not Done)
- `👥 Others owe me` — `3697fd54-27ba-8115-94b2-000cac2e9360` (Owner≠Me, not Done)
- `📆 Calendar` — `3697fd54-27ba-811b-8bdb-000cd04e1ad9`
- `🚦 By Owner` — `3697fd54-27ba-81cd-ba46-000c7719d2b3`

**Skill config** lives at `~/.claude/skills/accountability-pm/config.json` (container-local,
not in repo). It caches `notion_db_id`, `notion_data_source_id` (= the IDs above),
`pm_calendar_id` (currently null → falls back to `jordan@advisoraisolutions.com` Google
Calendar), `user_emails`, `last_run_at`, `timezone: America/Denver`, and a `verify_loop`
block tuning the continuous-improvement loop.

**Continuous-improvement loop** (added 2026-06-15). The skill's SKILL.md defines a
**Phase 0: Verify-and-close** that runs before each scan and a **Phase 7: Lessons log**
that runs after. Phase 0 closes to-dos whose completion is already evidenced in Gmail
Sent or Google Calendar (calendar event w/ attendee+date match, or sent thread w/ subject
overlap to the named recipient), conservatively — fuzzy matches go to a `LIKELY DONE —
PLEASE CONFIRM` section of the digest instead of auto-closing. On auto-close, the cached
`Calendar Event ID` is used to delete the matching `[PM]` reminder. Each run appends to
`~/.claude/skills/accountability-pm/lessons.md`, and the next run reads the last ~5
blocks to dampen known false-positive probe patterns. Canonical skill source mirrored at
`.claude/skills/accountability-pm/` in this repo so it survives container resets.

---

## 5. Brand system

| Role | Color | Hex | Notion mapping |
|---|---|---|---|
| Primary (Navy) | Dark Navy | `#0B1F3A` | `blue_bg` callouts, `blue` text |
| Accent (Gold) | Gold | `#D4AF37` | `yellow_bg` callouts — **reserve for CTAs / key metrics** |
| Secondary (Teal) | Teal | `#1C6E71` | `green_bg` callouts — supporting highlights, nav |
| Neutral | — | — | `gray_bg` for informational notes |

- **Type:** Playfair Display (headings/hero), Inter (body/UI). Approximate in Notion with
  headings + consistent casing.
- **Voice:** clear · operator-level · confident · technical-but-approachable · results-oriented.
  Sound like someone who *runs* the system, not someone explaining it from outside.
- **Layout rules:** 1–2 callouts max per section, consistent section ordering, tight tables,
  short property names.
- Full spec: 🎨 Brand Guidelines page `dabcf932d6c748b2a0700945599d44cd`.

---

## 6. Cover banner pipeline

On-brand gradient banners (navy→teal base + gold glow) are used as page/database covers.

- **Source + generator:** `assets/notion/gen_banners.py` (pure Python stdlib — no deps).
  Edit palette/glow and re-run: `python3 assets/notion/gen_banners.py`.
- **Files:** `assets/notion/{home,sales,podcast,brand,exec,projects}.png` (1600×640).
- **Hosting:** referenced by **commit-SHA-pinned** raw URLs so they never break:
  `https://raw.githubusercontent.com/jordandsalvador/sensflo-aais-analysis/<SHA>/assets/notion/<name>.png`
  Current SHA: `5d9a722cdb2cb808c9e2ef3137d01726e41ead20`.
- **Why SHA-pinned:** Notion fetches/rehosts covers; pinning to a commit keeps the exact image
  even as the branch moves. After regenerating, commit, push, then re-point covers to the new SHA.
- **Cover → page mapping:**
  - `home` → Home
  - `sales` → Sales hub, Leads, Discovery Calls, Clients
  - `podcast` → Podcast hub, Podcast Pipeline, Episodes, Call Transcripts
  - `brand` → Brand & Templates hub
  - `exec` → Tasks, Today, This Week, AI To-Dos, Conversation Inbox, Done Log
  - `projects` → Projects
- **Set a cover via MCP:** `notion-update-page` with `command:"update_properties"`,
  `properties:{}` (no-op), and `cover:"<raw url>"`.
- **Constraint:** Notion supports only a top-of-page banner — no true "background behind a
  section." Smooth gradients are used so any crop (desktop/mobile) looks centered.

---

## 7. Integrations & connected accounts

The `accountability-pm` skill (and any session driving this workspace) reaches external systems
through the following MCP connections. Update this section whenever an account is swapped.

| System | Account | Notes |
|---|---|---|
| **Notion** | jordan@advisoraisolutions.com workspace | This doc lives in that workspace's data sources. |
| **Gmail** | `jordan@advisoraisolutions.com` (primary) · `jordandsalvador@hotmail.com` (alias) | Both addresses are listed in the skill's `user_emails` so PM mode correctly attributes "Me" vs others. |
| **Google Calendar** | `jordan@advisoraisolutions.com` | Also the `pm_calendar_fallback` when a dedicated `PM To-dos` calendar doesn't exist (`pm_calendar_id` currently null). |
| **Fathom** | `jordan@advisoraisolutions.com` (switched **2026-06-14** from `jordandsalvador@hotmail.com`) | New transcripts/action items will record this as `Source Account` going forward. The legacy hotmail transcript on the Jamie Pfeffer row is historical and intentionally left as-is. |
| **Zoom** | (unverified at last edit — check `get_meeting_assets` permissions on a recent call to confirm) | Used for cloud recordings + AI summaries. |

## 8. Archived / deleted (2026-05-23 reorg)

- **Legacy podcast "Tasks" DB** (data_source `ace96df5-1e73-41fe-af29-31a5355fbd68`,
  container `64982fa573ec4a7597cde2a9afe5075e`) — was empty; moved to Notion trash. The master
  🗓️ Tasks DB (`b3bc9e6e…`) is canonical.
- **Podcast & Sales HQ** hub page — superseded by Home; retitled `[ARCHIVED]`, content replaced
  with a redirect, parked under 🎨 Brand & Templates.

---

## 9. Conventions for future edits

- Database titles carry a leading emoji that matches the data source icon (🗓️ 🎯 🤝 📌 🗣️ 📥 ✅ 🤖 🧲 🎧 📝).
- View names are emoji-prefixed and action-oriented (`🚦 Board`, `📆 Calendar`, `🔥 High priority`, `📋 All …`).
- Notion view-DSL **cannot** express `@me` or relative dates (`today`, `one_week_from_now`) or
  multi-value `IN(...)` on status-type props. Use existing pre-built containers (Today/This Week)
  for those, or build the filter in the Notion UI.
- Keep this file updated whenever structure, IDs, schema, or the banner SHA changes.
