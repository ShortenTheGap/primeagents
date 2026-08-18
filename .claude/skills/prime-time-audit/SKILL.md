---
name: prime-time-audit
description: "Run the Prime CEO Time Audit as a guided interview: walk the user task-by-task through everything they spend time on, classify each task by Tier (Admin/Technician/Manager/Exec), Energy, and CDS (Cut/Delegate/Systemize), compute the full summarized analysis (hours by tier, by energy, by CDS, and total reclaimable hours), and deliver a detailed action plan with specific recommendations on which tasks to automate and how. Use whenever the user asks for a time audit, CEO time audit, XDS or CDS analysis, cut/delegate/systemize, asks where their time is going, what to delegate or get off their plate, what their next hire should be, or what to automate first. Also trigger when they paste a task list, brain dump, or transcript about their week, or upload a completed or partial Time_Audit_Template.xlsx for analysis."
license: MIT
metadata:
  author: prime-elite
  version: '2.0'
  source-form: https://docs.google.com/spreadsheets/d/1J66bj6ei1YxdKNAhGuivhmPsDYcmH6psY3lrXg1-BHY
---

# Prime CEO Time Audit

Interview the user about where their time actually goes, classify every task, compute the analysis, and deliver a detailed summary with concrete recommendations on which tasks to automate and how.

**Why this exercise exists (use this framing in summaries):** "Awareness creates its own momentum." The audit makes the user keenly aware of where their time goes so they can free it up through elimination, systems, and delegation — moving from reactive to proactive, into the CEO seat. Keep summaries warm, direct, and focused on freeing up time and creating space.

## Inputs this skill accepts

1. **Nothing** (the common case) → run the guided interview below.
2. **A brain dump, transcript, calendar export, or task list** → extract tasks and hours from it, then interview only for what's missing (usually Tier/Energy/CDS classifications).
3. **A partially or fully completed Time Audit workbook** → preserve everything already entered; interview only for gaps; skip to analysis when complete.

The user's answers and source material are the only source of truth. **Never invent tasks or hours.** If the user asks you to estimate hours, estimate conservatively and mark them as estimates in the summary.

## Phase 1 — The Interview

### Step A: Brain dump the task list first

Before classifying anything, get the complete task list. Ask:

> **"List out all of the specific tasks that you are currently spending your time on."**

Prompt them to think through their whole week: mornings, client/delivery work, sales, marketing, admin, email, meetings, firefighting, evenings-and-weekends work. Keep asking "what else?" until they confirm the list is complete. Push vague entries toward specifics — "Weekly payroll run," not "admin stuff."

If they already provided a task list or transcript, extract the tasks and read the list back for confirmation instead.

### Step B: Classify each task, one at a time

Walk the list task by task. For each task, ask the questions below — **one task at a time, conversationally grouped** (hours + tier + energy together, then the CDS group). To keep momentum, you may propose your best-guess classification and let them confirm or correct it ("I'd call this Tier 1 - Admin, Takes My Energy, S+D — sound right?"). Their answer always wins.

**Hours:**
> "How many hours per week do you spend on this task?"

**Tier:**
> "What tier of work would you consider this task?
>
> **Tier 1 - Admin:** Simple and administrative work that an assistant could do, such as email management, research, etc.
> **Tier 2 - Technical:** Often the work to keep your business running day to day, including creating and delivering your product or service.
> **Tier 3 - Manager:** The work of managing the department and team.
> **Tier 4 - Exec:** The work of leading the business, including things like vision, strategy, partnerships."

**Energy:**
> "What impact does this task have on your energy?
>
> **Gives Me Energy:** You enjoy doing this task and it gives you energy.
> **Neutral:** This task neither gives you energy nor takes your energy.
> **Takes My Energy:** You don't enjoy doing this task and it takes your energy. You may often avoid or procrastinate on these tasks."

**CDS:**
> "What action do you need to get this task off your plate?
>
> **Cut:** This task is not necessary and you can simply stop doing it.
> **Delegate:** This task should not be on your plate and you should delegate it to a team member. This person may or may not be on your team yet.
> **Systemize:** You need to create or improve the system for this task.
> **Systemize & Delegate:** You need to create a system first before you can delegate it to a team member.
> **Nothing:** You don't need to do anything with this task. It is working fine as is."

**Conditional follow-ups** (only when applicable):
- If Delegate or Systemize & Delegate → **"Who will you delegate this to? It may be an existing team member, or a role that you need to hire."** (New Owner)
- If Systemize or Systemize & Delegate → **"What system will you create or improve to reduce the amount of time this task takes?"** (System to Create — if they don't know, propose one; that feeds the automation recommendations)

**Store exact data values** (the form's dropdowns and SUMIFs key off these strings verbatim):
- Tier: `1-Admin`, `2-Technician`, `3-Manager`, `4-Exec`
- Energy: `Gives Me Energy`, `Neutral`, `Takes My Energy` (blank allowed if they can't decide)
- CDS: `X` (Cut), `D` (Delegate), `S` (Systemize), `S+D`, `---` (nothing)
- New Owner: blank when CDS is `X` or `---`
- System to Create: only for `S` and `S+D`

### Step C: Sanity check

Total the hours. If the sum is under 25 or over 80 hours/week, read the total back and confirm before analyzing ("Your tasks add up to 94 hours/week — is that right, or are some of these overlapping?"). Also confirm any task list shorter than 8 tasks is genuinely complete.

## Phase 2 — Summarized Analysis (replicate the form's math)

Compute and present, mirroring the form's Summarized Analysis block:

1. **Total # Hours/Week** — sum of all task hours
2. **Total # Hours By Tier** — subtotals for 1-Admin, 2-Technician, 3-Manager, 4-Exec
3. **Total # Hours By Energy** — subtotals for Gives Me Energy, Neutral, Takes My Energy
4. **How to Get Things Off Your Plate** — subtotals by CDS: X, D, S, S+D
5. **Low-Hanging Fruit:**
   - Immediate Items to Cut = hours where CDS = `X`
   - Admin Hours to Delegate = hours where Tier = `1-Admin`
   - **Total Hours Saved = hours where (CDS = `X` OR Tier = `1-Admin`), counted once** — note: the template's own formula double-subtracts tasks that are both 1-Admin and X; report the corrected number and, if it differs from what their spreadsheet will show, say so in one line.
   - New Hours = Total − Total Hours Saved
6. **Top Tasks to Get Off Your Plate** — tasks where Tier = `1-Admin` OR Energy = `Takes My Energy`, sorted by hours descending (the form caps at 16; keep the top 16 by hours if more qualify)
7. **Tasks You Should Keep/Continue Doing** — tasks where Tier = `3-Manager` OR `4-Exec` OR Energy = `Gives Me Energy`

Present the analysis as clean tables with a short BLUF up top: total hours, hours reclaimable, and the single biggest time drain.

## Phase 3 — Automation Recommendations (the core deliverable)

For every task marked `S` or `S+D` (plus any `D` task that is clearly automatable), produce a specific recommendation — not "create an SOP" but what to actually build:

- **Task, hours/week, and what the system replaces**
- **Automation approach** — name the concrete mechanism: a template + checklist SOP, a scheduled AI-agent loop, an inbox rule + draft-reply agent, a form → CRM workflow, a recurring report generator, a calendar-booking flow, etc. Scope it to tools the user actually has — ask what their stack is (CRM, email, calendar, automation platform, AI tools) before prescribing, and never assume a specific product they haven't named.
- **Judgement level** — low-judgement + high-frequency + schedule-shaped tasks are the best automation candidates; high-judgement tasks get a system that assists rather than replaces
- **Estimated hours reclaimed** and a rough build effort (hours, not weeks)
- **Rank order** — sort by (hours saved × ease of build). The #1 item should be buildable this week.

Then draft the **Action Plan** (mirrors the form's Step 2 tab):
- **Most Valuable Activities** (up to 5, with ideal % of time summing to 100%) — pulled from 4-Exec and Gives-Me-Energy tasks
- **First 3 Systems to Create** (each marked Create or Update) — the highest-hours S and S+D tasks
- **Next 3 Positions to Hire** — cluster D and S+D tasks by the role that would own them; the first hire absorbs the largest block of delegated hours

Frame the action plan as a draft for the user to react to, and close with the #1 recommended automation as a ready-to-build brief (what it does, trigger, inputs, outputs, tools) they can hand to whoever builds their automations.

## Phase 4 — Deliverables

Ask which format they want, or default to **chat analysis + interactive HTML**:

### Interactive HTML audit (default)

`assets/time_audit.html` — a Prime-branded single-file web app: full task table with dropdowns, live "hours you can reclaim" counter, auto-computed analysis, off-your-plate and keep lists, Step 2 action plan, local autosave, JSON export.

**Always copy assets to the working directory first** — never edit them in place, never rebuild from scratch; their formatting is the deliverable's brand.

To prefill, replace the injection marker `/*__DATA__*/null/*__END__*/` with `/*__DATA__*/<json>/*__END__*/`:

```json
{
  "tasks": [{"task":"","hrs":0,"tier":"1-Admin","energy":"Takes My Energy","cds":"S+D","owner":"","system":""}],
  "mva": [{"a":"Activity","p":35}],
  "systems": [{"s":"System name","cu":"Create"}],
  "hires": [{"p":"Position","t":"Top tasks to delegate"}]
}
```

Tier/Energy/CDS strings must exactly match the allowed values (empty string = blank). `mva` percentages are whole numbers summing to 100. Inject only raw task rows — the page computes all analysis live. Name it `[Name] - CEO Time Audit.html`. After generating, validate the injected JSON with `json.loads` — a syntax error silently breaks the page.

### Excel workbook (on request)

`assets/Time_Audit_Template.xlsx` — the classic template. Fill with openpyxl:

1. **Rows 4–53, columns A–G** on the "Step 1 - XDS" tab. Dropdown validations already exist — write exact-match values only. New Owner blank for `X`/`---`; System to Create only for `S`/`S+D`.
2. **Rows 72 and 90 contain dead Google Sheets QUERY formulas** (`__xludf.DUMMYFUNCTION`) that do not work in Excel. Overwrite row 72 and row 90 with plain header strings (`Specific Task`, `Hours/Week`, `Tier`, `Energy`, `CDS`, `New Owner`, `System to Create`), then write the two filtered lists as **static values**: Off-Your-Plate list in rows 73–88 (max 16, sorted by hours desc), Keep list from row 91 down. Match surrounding formatting (Arial, no fill).
3. **Leave every other formula alone** — B54 total and the SUMIF blocks in rows 59–69 compute automatically once rows 4–53 are filled.
4. **Fill the "Step 2 - Actions (Example)" tab**: MVAs in B6:B10 with fractions in E6:E10 (0.3 = 30%, must sum to 1.0 — E11 checks), systems in B14:B16 with `Create`/`Update` in E14:E16, hires in B19:B21 with top tasks to delegate in C19:C21. Rename the tab to `Step 2 - Actions` (drop " (Example)") for delivery.
5. **Verify portably** (no external recalc scripts): reload the saved file with openpyxl and confirm every value you wrote is present, exact-match strings only, hours are numbers, and the two static lists match your computed analysis. State in the summary that the SUMIF totals compute on first open in Excel/Sheets.
6. Name it `[Name] - CEO Time Audit - [Month Year].xlsx`.

### Persist and re-audit

Save a dated summary (task table + analysis + recommendations) to `shared/time-audit-YYYY-MM-DD.md` in the working project. On a later run, if a previous summary exists, offer a **re-audit comparison**: hours then vs. now, which off-your-plate tasks actually came off, and hours genuinely reclaimed.

## Template quirks — do not "fix" silently

- The template contains typos ("Hours To Be Saves", "How to Ge Things", "Sytemize & Delegate"). The `Sytemize & Delegate` label sits next to the SUMIF keying off `S+D`, so it's cosmetic. Leave them — users know this document.
- The "New Hours" formula (B68) double-subtracts tasks that are both `1-Admin` and `X`. Leave the formula; report the corrected number in chat (Phase 2.5).
- Row 2 has a "WATCH THIS VIDEO FIRST" callout with no link. Leave it.
- Cells containing a single space are intentional placeholders — overwrite freely.
- XDS is the tab's name for the exercise; CDS is the classification column. Don't rename either.

## Guardrails

- Never invent tasks, hours, owners, or systems the user didn't state or approve.
- One task at a time in the interview — never dump all questions for all tasks at once.
- Exact string values in all data (`1-Admin`, `Gives Me Energy`, `S+D`, `---`, etc.).
- Estimates are marked as estimates. Blanks the user can't answer stay blank and get flagged in the summary.
- Ask about the user's actual tool stack before recommending automation tools — never assume a specific CRM, email platform, or automation product.
- BLUF summaries, warm but direct.
