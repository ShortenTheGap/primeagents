---
name: living-avatar
description: Mine customer interaction data (sales call transcripts, intake forms, onboarding forms, support threads, community posts, churn interviews) for verbatim customer language, then maintain a versioned Living Avatar document through a propose-and-approve loop with the business owner. Use this skill whenever the owner asks to run their weekly avatar review, update or build their customer avatar, analyze customer language, extract voice-of-customer data, find pain language or hooks in transcripts, or asks "what are my customers actually saying." Also use it when the owner uploads or points to sales calls, intake forms, or customer conversations and wants marketing insight from them, even if they never say the word "avatar."
---

# Living Avatar

You maintain a Living Avatar: a versioned document of the business owner's ideal customer, built entirely from verbatim customer language mined from real interactions. The avatar is not a persona invented in a brainstorm. It is a database of what customers actually said, with receipts.

The owner uses this document to write social content, email campaigns, webinar copy, pre-sales videos, and sales collateral in their customers' own words. Copy written in customer language outperforms copy written in founder language. Your job is to keep the supply of that language fresh, ranked, and sourced.

## Operating rules

These rules exist because violating any one of them destroys the value of the entire system.

1. **Verbatim only.** Every quote in the avatar is the customer's exact words. Never paraphrase, never summarize a quote, never "clean up" grammar. The moment customer language passes through your voice, it stops sounding like a human and stops working in copy. Light redaction of names and identifying details is allowed; rewording is not.
2. **Customer speech only.** Transcripts contain two speakers. The owner's words are contamination. Most stale avatars are stale precisely because they're full of how the founder describes the problem. Extract only what the customer or prospect said. If a transcript has no speaker labels, use context to separate the voices, and skip anything you can't attribute confidently.
3. **Every claim has receipts.** Every pattern in the avatar carries: 2 to 5 verbatim quotes, a count of distinct customers who expressed it, first-seen and last-seen dates, and source references. A claim without receipts gets deleted, not defended.
4. **The owner approves every change.** You propose, they decide. Never silently edit the avatar. The only exceptions: incrementing frequency counts and refreshing last-seen dates on already-approved patterns.
5. **One quote, one customer, one count.** The same customer saying the same thing on three calls is frequency 1, intensity 3. Distinct-customer count is what makes something a pattern. Note intensity separately when it's striking.

## Files you maintain

All files live in the owner's vault under `Avatar/`. Create the folder on first run.

- `Avatar/Living Avatar.md` — the current avatar. Structure defined in `assets/avatar-template.md` (read it before creating or editing the avatar).
- `Avatar/Quote Bank.md` — overflow verbatim quotes organized by theme, beyond the 2 to 5 shown per claim in the avatar. Copywriting raw material.
- `Avatar/Avatar Changelog.md` — one entry per approved change: date, what changed, why, evidence summary. This is the version history.
- `Avatar/Rejected Patterns.md` — patterns the owner declined, with date and their reason if given. Check this before every proposal so you never re-pitch a rejected pattern. If a rejected pattern later triples in frequency, you may raise it once more, and say explicitly that you're re-raising it and why.
- `Avatar/Scan Log.md` — after each run: date, sources scanned, quotes extracted, proposals made and their outcomes. This is how you know what's already been processed. Never re-extract from sources already logged.

## The two modes

Determine mode by checking whether `Avatar/Living Avatar.md` exists and has approved content.

### Bootstrap mode (first run, or avatar is empty/stale beyond use)

Most owners arrive with no avatar or one that's years old. The first run is the proof moment for this whole system, so go deep.

1. Inventory the vault and memory tools for every customer-language source you can find (see Source guide below). Tell the owner what you found and what looks missing: "I found 23 sales call transcripts and your onboarding forms, but no churn interviews. Anywhere else customer language lives?"
2. Extract and cluster across ALL history, not just recent data.
3. If an old avatar document exists anywhere in the vault, read it. Treat its claims as hypotheses to confirm or contradict with data, not as truth.
4. Draft a complete Avatar v1 using the template. Mark every claim with its evidence strength.
5. Walk the owner through it section by section for approval. Where the data contradicts what the owner believed (or what their old avatar said), say so directly. That contradiction is the most valuable finding of the bootstrap. Do not soften it.
6. Write the approved version, initialize the changelog with "v1.0 — Bootstrapped from N sources spanning [date range]," and log the scan.

### Weekly mode (avatar exists)

The weekly review is a ritual, not an interruption. One digest per week.

1. Read `Avatar/Scan Log.md` to find what's new since the last run. Scan only new or changed sources.
2. Extract and tag quotes (see Extraction guide).
3. Cluster new quotes into themes. Merge with running counts.
4. Diff against the current avatar. Every cluster lands in one of four buckets:
   - **Confirms** an existing claim → update frequency and last-seen silently.
   - **Contradicts** an existing claim → propose a change.
   - **New pattern** at or above threshold (3+ distinct customers) → propose an addition.
   - **Below threshold** → hold in the Quote Bank under "Emerging," say nothing yet.
5. Check for staleness: any avatar claim with zero mentions across the last 15+ interactions or 90+ days gets a retirement proposal. Retired claims move to a History section at the bottom of the avatar, never deleted, because markets cycle.
6. Deliver the weekly digest (format below).
7. Apply approved changes, update changelog, quote bank, and scan log.

If a week has no proposals, still deliver a short digest: what was scanned, top confirming quote of the week, and any emerging patterns being watched. The owner should never wonder whether the system is alive.

## Source guide

Ranked by copywriting value. When sources conflict, trust the higher tier.

**Tier 1 — unfiltered emotional language (weight heaviest):**
- Sales call transcripts, especially the first third. The answer to "what made you book this call" is the single highest-value text in the business.
- Pre-sales intake forms, open-ended fields only. Written before rapport, so zero performance.
- Objection moments anywhere in sales calls. Capture the exact hesitation phrasing.

**Tier 2 — transformation language:**
- Onboarding forms ("what does success look like" answers are promise language).
- Win moments in coaching or community calls, in the customer's own words.
- Support tickets and community threads. Confusion language reveals what marketing failed to explain.

**Tier 3 — behavioral and exit signal:**
- Churn interviews, cancellation notes, refund requests.
- Email replies to campaigns.
- Analytics: use only as context for weighting attention, never as a language source.

Testimonials and reviews are usable but discount them one tier; they're performed for an audience.

## Extraction guide

You are scanning for structures, not keywords. Extract a quote when it matches any of these, and tag it accordingly:

- **[PAIN]** First-person, present-tense problem language. "I'm drowning in," "I can't keep up with," "every time I try to," "I'm so tired of."
- **[TRIGGER]** The moment they decided to seek help. "The last straw was," "I knew something had to change when." These become hooks.
- **[FAILED-ALT]** What they tried before. "We hired a VA," "I bought a course." This is competitor positioning and the "why this is different" section.
- **[COST]** What the problem costs in their units: hours, deals, sleep, weekends, credibility, missed dinners. Specific beats abstract.
- **[IDENTITY]** Self-description. "I'm not a tech person," "I didn't build this business to be an email admin." Identity language in copy outperforms benefit language.
- **[DESIRE]** Desired-state language, especially non-obvious ones. Watch for wants that aren't "more revenue."
- **[OBJECTION]** The exact sentence of hesitation. "I've been burned by masterminds before." Not the category, the sentence.
- **[STICKY]** Metaphors and coined phrases. "My business runs me." Flag these individually; they become hooks, subject lines, and titles regardless of frequency.
- **[BUYING]** What tipped the decision. "I signed up because."

Tag every quote with: source file, date, customer identifier (anonymize to initials or a stable ID), lifecycle stage (pre-sale / onboarding / active / exit), and one or more structure tags.

A [STICKY] quote is the one exception to the 3-customer threshold: a single brilliant phrase goes straight into the digest as a hook candidate, clearly labeled as n=1.

## The weekly digest format

Deliver as a single message. Structure:

```
# Living Avatar Weekly — [date]

**Scanned:** [N sources: brief list]. **Extracted:** [N quotes from N distinct customers].

## Proposed changes ([N])

### 1. [UPDATE/ADD/RETIRE]: [one-line description]
Your avatar currently says: "[current claim, or 'nothing on this']"
Your customers are saying: [pattern in one line]
Evidence: [N] of the last [N] interactions.
> "[verbatim quote]" — [ID], [source type], [date]
> "[verbatim quote]" — [ID], [source type], [date]
> "[verbatim quote]" — [ID], [source type], [date]
**Approve, edit, or reject?**

## Confirmations (no action needed)
[1-2 lines: which existing claims got reinforced this week]

## Hook candidates
> "[sticky quote]" — worth testing as a hook or subject line.

## Watching (below threshold)
[Emerging patterns at 1-2 customers, one line each]

## Downstream check
[Only when a change was approved: which existing assets now use stale language.
"Your webinar reg page still leads with [old pain]. Want a rewrite queued?"]
```

Keep proposals to a maximum of 3 per week even if more qualify. Rank by evidence strength and copy value, hold the rest for next week. More than 3 decisions per week turns the ritual into homework and trains the owner to skim.

When presenting a contradiction between the avatar and the data, state it plainly. The owner needs the correction, not diplomacy. "Your avatar says the top pain is lack of time. Your last 15 calls say the pain is specifically follow-up falling through cracks. Those produce different copy."

## Handling owner responses

- **Approve** → apply exactly as proposed. Update avatar, changelog, quote bank.
- **Edit** → apply their edit to the claim language, but the evidence quotes stay verbatim. If their edit contradicts the evidence, apply it anyway and note the divergence in the changelog. It's their avatar.
- **Reject** → log in Rejected Patterns with their reason. Quotes stay in the Quote Bank under "Rejected" for reference.
- **Silence on a proposal** → carry it to next week's digest once, marked "carried over." After two weeks unanswered, move it to Rejected Patterns as "expired unanswered" and stop asking.

## Using the avatar downstream

When the owner (or another skill) asks for content, copy, or campaign help, read `Avatar/Living Avatar.md` first and write from its language. Pull exact phrases from the Quote Bank for hooks, subject lines, and openers. When you use avatar language in a deliverable, you don't need to cite sources in the copy itself; the receipts live in the avatar.

When an avatar change is approved, run the downstream check: search the vault for marketing assets (landing pages, email sequences, webinar scripts, bios, offers) that use the now-outdated language, and list them in the digest with an offer to update. This step is where avatar maintenance converts into revenue, so never skip it.

## Edge cases

- **Owner's business has obviously distinct customer segments:** this skill maintains ONE avatar. If clustering consistently produces two contradictory groups (different pains, different identity language), don't average them into mush. Raise it once: "Your data contains two distinct customers: [A] and [B]. This avatar tracks one. Which is the primary?" Track the primary; park the secondary's quotes in the Quote Bank under "Segment B."
- **Thin data (fewer than 10 total interactions):** run bootstrap anyway, mark every claim "provisional, n<3," and tell the owner the avatar will firm up as data accumulates. A provisional avatar built from 8 real interactions still beats an invented persona.
- **No customer data found at all:** don't invent an avatar. Tell the owner what to start capturing (record sales calls, add open-ended intake questions) and offer to draft the intake questions.
- **Sensitive content in sources:** customer names, health details, financials, and anything embarrassing get anonymized at extraction. Quotes keep their meaning, not their identifying details.
