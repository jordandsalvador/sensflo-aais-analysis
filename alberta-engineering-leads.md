# Alberta Engineering Firms — No/Weak-Website Lead Research

> Reference doc for future Claude sessions and skills. Companion to `ab-engineering-no-website-leads.csv` (same directory).
> Last updated: 2026-05-25.

## Purpose

B2B sales-prospecting research for a web-services agency (Advisor AI Solutions / SensFlo).
Goal: identify Alberta engineering firms with **no website, broken, or outdated websites**, then find
the **decision-maker** (owner / president / founder / responsible P.Eng.) and any publicly available
contact info for outreach.

The originating request was "scan Calgary, Alberta for engineering firms without a website," which then
expanded to "scrape the contacts of the decision makers" for a supplied list of 20 firms (mix of Calgary,
Edmonton, Red Deer, Fort McMurray, and small-town AB).

## Method & hard constraints (important for future sessions)

- **Directory sites block automated fetch.** `yellowpages.ca`, `yellowpages.net`, `bbb.org`, `cossd.com`,
  `listingsca.com`, and `cea.ca` all return **HTTP 403** to `WebFetch`. Do not waste calls fetching them.
- **`WebSearch` is biased toward firms that HAVE websites** (search engines rank them higher), so it is the
  wrong tool for enumerating website-less firms. It IS useful for finding named principals once you have a
  firm name.
- **Best sources that DO work:** LinkedIn public snippets, company team/about pages (when not 403),
  Canadian corporate registry / OpenCorporates, ACEC/APEGA references, news/press releases, chamber pages.
- **APEGA permit-holder / responsible-member directory** requires interactive search and was not directly
  accessible via fetch.
- **No personal emails were fabricated.** Public sources mostly expose generic inboxes (`info@`, contact
  forms). Personal addresses are masked behind ZoomInfo/RocketReach. Inferred patterns (e.g. `mbroks@`,
  `james.marr@`) are explicitly marked **unconfirmed**.
- **The "right" tool for true city-wide scanning** is the Google Places API (`Nearby Search` +
  `Place Details` with a `website` field; missing field = lead). Not implemented — needs a user-supplied
  API key. Est. cost ~$10–25 to cover Calgary's engineering universe.

## Results summary

- 20 firms researched, split across 3 parallel research agents.
- **~15 firms** have strong, named decision-makers (High confidence).
- **Binnie & Valard:** corporate execs found, but no Calgary/local office lead published.
- **3 unresolved:** TDI (Edmonton), Basin Engineering Services, Projex Technologies.

### Verification flags (act on these before outreach)

- **OpenCycle Technologies** — *likely NOT a no-website lead.* `opencycle.ai` is a live rebrand of Patching
  Associates (server responds; 403 to bots only). Recommend removing from the target list.
- **GeoMetrix Group Engineering** — *name/discipline mismatch.* The public firm by that legal name is an
  **Edmonton structural/bridge** shop at `geometrixgroup.ca` (Wayne Stewart, ~10 staff), NOT the
  geotechnical `geometrix.ca` ~17-staff firm in the source list. Confirm intended target.
- **Projex Technologies** — *likely defunct.* Acquired by Ausenco (Jul 2013), `projex.ca` dead. Verify it
  still operates before any outreach.
- **TDI (Edmonton)** — not verifiable; conflated with TDi Systems (Calgary) and TDI Engineering LLC (Texas).
- **Basin Engineering Services** — 4+ unrelated "Basin" firms; no named leader surfaced.

## Decision-maker contacts

| Firm | City | Decision Maker | Title | Public Contact | Conf. |
|------|------|----------------|-------|----------------|-------|
| Akron Engineering Consultant's Group | Fort McMurray | Nayef Mahgoub, P.Eng., MBA | Owner / Managing Director | admin@akronengineering.com · (780) 750-9950 | High |
| Eagle Engineering Corp. | Bragg Creek | Kim Biddle | Founder / Owner / Principal | (403) 949-9116 | High |
| Hawk's Aerial and Technical Solutions | Calgary | Kyle Hawkings, P.Eng. | Owner / Director | info@hawkats.com · (587) 938-1301 | High |
| Hedgehog Technologies | Calgary (HQ Burnaby) | Michael Wrinch (Founder/Pres); Matthew Keeler (Calgary mgr) | Founder/President; Office Mgr | hedgehogtech.com team page | High |
| OpenCycle Technologies | Calgary | Justin Caskey, P.Eng. | Founder | info@patchingassociates.com · (403) 274-5882 | High |
| T2 Utility Engineers | Edmonton | Sinclair Slusariuc (Branch Mgr); Matt Bourgeois (Pres, Canada) | Branch Mgr; President | 1-855-222-8283 | High |
| TDI | Edmonton | Not found | — | — | Low |
| Steenhof Building Services Group | Calgary | Jack Steenhof (Founder); Andy Muzio (President) | Founder; President | info@steenhof.ca · (587) 287-1980 | High |
| GeoMetrix Group Engineering | Edmonton | Wayne Stewart, M.Eng., P.Eng. | Founder / President | info@geometrixgroup.ca · (780) 738-8808 | Medium |
| Aptus Engineering | Red Deer | Martin Broks, P.Eng. | President / CEO / Founder | info@aptuseng.ca · (403) 340-3022 | High |
| Sameng Inc. | Edmonton | David Yue (Pres); Gerry Samide (Founder); Mary Samide (CFO) | President; Founder; CFO | services@sameng.com · (780) 482-2557 | High |
| DES Engineering | Edmonton | Thomas Kyle, P.Eng. (Pres); Dan Hamilton (Mng Partner) | President; Managing Partner | info@deseng.ca · (780) 801-2700 | High |
| CVL Engineers | Edmonton | Michael Oleskiw (Pres); Wendy Oleskiw (co-principal) | President; Co-principal | info@cvl-eng.ca · (780) 982-8931 | High |
| Envirogeotech Consulting | Calgary / Medicine Hat | Chandra S. Acharya, P.Eng., PhD; Ranjeet Gaekwad | Principal Owner; President | contact@envirogeotech.com · (403) 487-4377 | Med-High |
| LEX3 Engineering | Calgary / Edmonton / Red Deer | Kris Jackson; Sean Brown; Trevor Baragar (all P.Eng.) | Principals | reception@lex3.ca · (403) 340-1117 | Medium |
| Binnie Consulting | Calgary (parent BC) | Richard Bush, P.Eng., MBA, PMP | President / CEO | askbinnie@binnie.com · (403) 930-1790 | High (CEO) / Low (local) |
| Banner Environmental Engineering | Diamond Valley / Calgary | James Marr | President & Chief Engineer | james.marr@banneree.com (unconfirmed) · (403) 933-4199 | High (name) / Med (email) |
| Basin Engineering Services | Calgary | Not found | — | (403) 260-5376 (ZoomInfo) | Low |
| Valard Construction LP | Calgary / Edmonton | Adam Budzinski (CEO); Carey Kostyk (Sr EVP); Dave Torgerson (COO) | Corporate execs | (403) 279-1003 | High (corp) / Low (local) |
| Projex Technologies | Calgary | Barry Brad (Pres/CEO); Philip Shuker (MD) | President/CEO; MD | none (defunct) | Medium |

Full data — including website status, niche, source URLs, and per-firm notes — lives in
**`ab-engineering-no-website-leads.csv`**.

## Suggested next steps

1. **Get verified personal emails:** run the collected names + domains through Hunter.io or Apollo. The CSV
   is structured for import.
2. **Resolve the 3 unverified firms** (TDI, Basin, Projex) via direct phone contact or registry lookup.
3. **Scale the scan properly:** build a Google Places API script (Nearby Search → Place Details, flag
   missing `website`) to enumerate the full Calgary engineering universe instead of working from a
   hand-supplied list. Needs a Google Maps API key.
4. **Drop OpenCycle** from the no-website target list; re-confirm GeoMetrix's intended entity.
