---
name: loop-maker
description: >
  Designs and scaffolds a self-running, self-verifying agent loop from a
  7-question blueprint, for Prime Agent Desk. Primary trigger: "loop", "make a
  loop", or "set up a loop" — also: automate a recurring task, schedule an
  agent, run unattended, monitor a condition, triage a queue, poll on a cadence,
  or turn any manual workflow self-running — even if you never say the word
  "loop". Walks through elicit → survey → select → scaffold,
  producing a self-contained loop folder with a separate verifier, an external
  state file, human gates, a trigger, and a hard budget.
---

# loop-maker

A 4-phase wizard that turns any "I want this to run by itself" intent into a
deployable, auditable agent loop **inside Prime Agent Desk**. The output is
concrete: a `loops/<name>/` folder with the loop's logic, a separate verifier
program, a state file, human gates, a trigger definition, and a budget. Nothing
runs until the blueprint is approved.

> Adapted from the open-source `loop-maker` skill (MIT, EricTechPro) for the
> Prime Agent Desk host, with the goal-contract rigor and self-linting idea from
> `qiaomu-goal-meta-skill` (MIT, 向阳乔木). See `LICENSE`.

---

## The one rule

> **Durable knowledge → the loop's `SKILL.md` (read-only each run).
> Changing state → `STATE.md` (read+written each run).**

The loop's `SKILL.md` is loaded fresh each time the loop fires. It must never
accumulate knowledge between runs — it only carries the logic. Everything that
evolves (progress counters, last-seen timestamps, iteration results, queue
position) lives in `STATE.md`, which the loop reads and writes. Mutable state in
a `SKILL.md` is the anti-pattern: it silently disappears the moment the next run
reloads the skill from disk.

---

## Where loops run (read this first — the host matters)

Prime Agent Desk runs the agent **locally, on the student's own Claude login,
only while the desk app is open and the laptop is awake.** That shapes what a
loop can promise:

- There is **no wake-from-sleep scheduler.** A loop only advances while the app
  is running. "Every morning at 8am" is not honourable here; "every 15 minutes
  while the desk is open" and "run until done, then stop" are.
- A running loop spends **the student's own tokens.** Every loop therefore needs
  a hard budget (max iterations / tokens / minutes). This is non-negotiable.
- The **Loop Runtime** (the part of the desk that actually executes loops on a
  cadence, enforces the budget, and pauses for approval) may not be installed
  yet. If it is not, this skill still *designs and scaffolds* the loop, and you
  (the agent) can run iterations manually when the student asks — but say
  plainly that it will not run on its own until the Loop Runtime ships.

See `references/host-prime-agent-desk.md` for how each abstract step (schedule,
sub-agent dispatch, file I/O, verifier execution) maps onto the desk.

---

## Process: 4 phases

```
elicit  →  survey  →  select  →  scaffold
```

Work through these phases in order. At the start of each phase, print the
breadcrumb (optional — `python3` may not be present; if it errors, just say the
phase name):

```
python3 scripts/loop_progress.py breadcrumb <phase>
```

Create one todo item per phase and check it off before moving to the next. Do
not scaffold until the blueprint is approved.

---

## Phase 1 — Elicit (7 questions, one at a time)

### Gate 0 — loop, or just do it once? (ask this ONE line first)

**Stop before the wizard.** The Loop Runtime now actually *runs* loops, so do
not launch the full 7-question elicitation on every stray "automate this". Before
Q1, ask exactly one line and wait:

> **Do you want this to run repeatedly on its own (a loop), or should I just do
> it once now?**

Only proceed into the 7 questions if the student confirms they want a recurring /
self-running loop. If they just want the task done once, **do it now and stop** —
no wizard, no scaffold, no loop folder.

### Detect-first rule

Before asking anything, silently probe the environment so you don't ask what you
can already see:

- Is the agentHome a git repo with a remote? (`git remote -v`) — usually not.
- Is there already a `loops/` folder, and a loop with this name?
- Does the goal overlap an existing skill in `.claude/skills/`?

For any question the environment answers, print `(detected: <value>)` and skip
asking — this lowers `<total>` in the progress bar. Show what you detected so the
student can correct it.

### Asking the questions

Print a progress bar before each question you actually ask (optional, as above):

```
python3 scripts/loop_progress.py bar <n> <total>
```

`<n>` is the question number (counting only un-detected ones), `<total>` is how
many remain un-detected at elicit start. Ask one question, wait for the answer,
then move to the next.

### The 7 questions

**Q1 — Goal** (maps to the loop's exit predicate)
> What condition means the loop is done? State it as something a program could
> check — a file exists, a count reaches a target, a queue is empty, an endpoint
> returns 200. A vibe ("it looks good") won't work; a checkable predicate will.

**Q2 — Trigger** (maps to `TRIGGER.md`)
> How does the loop start each run? On this host there are exactly two honest
> options: **run-until-done** (it iterates back-to-back until the goal predicate
> holds, then stops) or **interval** (it fires every N minutes *while the desk is
> open*). There is no wake-from-sleep schedule. Pick one; if interval, pin N.

**Q3 — Discovery**
> What does the loop look at each run to decide what to do? Examples: a directory
> listing, a file's contents, an API response, a note in the vault. This
> determines what the loop reads at the start of each iteration.
>
> **Discovery-first for unfamiliar or regulated domains.** If the task touches a
> domain you don't actually know (medical, legal, financial, compliance, an
> unfamiliar codebase or data format), make the loop's first iterations
> **read-only discovery** — read the project docs, sample data, and existing
> scripts and write down working assumptions — before it acts. Don't invent
> domain facts; surface what's unknown.

**Q4 — Action** (maps to the loop's core step)
> What does the loop actually do each iteration, and **which paths does it
> write?** List those paths — they become the loop's **declared targets**: the
> only files/dirs it is allowed to create, modify, or delete. Two shapes are
> fine and often combine:
> - **Build a new artifact** — stage it in the loop's `work/` scratch dir, then
>   promote it into a declared target once the verifier passes. Use this when a
>   half-finished artifact must not be visible until it's verified.
> - **Edit an existing file in place** — e.g. flip a line in a tracker. The file
>   is a declared target; the verifier checks its *final* state directly. No
>   staging needed.
> Anything the loop writes outside its declared targets (and `work/`) is a gate
> (G3) — so naming the targets up front is what keeps the loop bounded.

**Q5 — Verification** (maps to `verifier.sh` — a SEPARATE checker)
> How does the loop prove each iteration succeeded before moving on? This must be
> a program with a binary verdict (exit 0 / exit 1), not the model's opinion. The
> verifier runs after every action and gates the next iteration. It is a separate
> file from the loop's `SKILL.md`.
>
> There are two distinct checks — keep them separate:
> - **Per-iteration check** — did *this* attempt reach its final state? The loop
>   passes the current item's identity in as **arguments** (e.g. the artifact path
>   it just wrote, plus an optional marker file + token). Worked example:
>   `scripts/verify_item_example.sh`. Call it as
>   `verifier.sh <artifact> [<marker_file> <marker_token>]`.
> - **Goal predicate** — may the whole loop stop now? (e.g. "zero items left").
>   Worked example: `scripts/verify_example.sh`.
>
> Adapt `scripts/verifier_template.sh` (generic wrapper) or the worked examples
> above into the loop's `verifier.sh`. Record the exact argument convention in the
> loop's `SKILL.md` so each iteration knows how to call it.
>
> **Vague words become checks, not the predicate.** "Polished", "professional",
> "high quality" aren't bad goals — they're bad *exit conditions*. Translate each
> into something concrete the verifier (or a bounded review) can check — a file
> exists, a count, a layout has no overlap, a screenshot review — plus a capped
> number of focused improvement rounds. Never let a subjective word BE the stop
> condition; the budget's `max_iterations` bounds the polishing.

**Q6 — State**
> What does the loop need to remember between runs? Which items are processed,
> the last cursor/timestamp, the iteration count, accumulated results. This goes
> in `STATE.md`.

**Q7 — Human gates**
> At which points must the student approve before the loop continues? At minimum:
> before the first real run, and when the verifier signals an anomaly. Add
> domain-specific gates — before sending an external message, before any spend,
> before deleting data that can't be recovered, and before writing anything
> **outside the loop's declared target paths** (Q4). When the Loop Runtime hits a
> gate it **pauses and waits for approval** — nothing irreversible happens
> unattended.
>
> **These pause for approval BY DEFAULT (the safe default — don't remove it
> lightly):** credentials / accounts / API keys · payments or anything that costs
> money · production data or destructive operations · legal / medical / financial
> judgements · copyrighted or licensed assets · publishing, deploying, or pushing
> to a shared branch · anything where ownership or direction is unclear. Low-risk
> uncertainty is NOT a pause — make a sensible assumption and note it; reserve
> pauses for the list above so the loop doesn't stall on trivia.
>
> **When the loop's whole value IS doing one of these on its own** (auto-send the
> completion summary, auto-post the drafts through a pre-approved pipeline, notify
> on anomaly), you don't have to choose between "pauses forever" and "no gate at
> all." Capture it as an **autonomous action** (below): the loop declares a
> *concrete, narrow* capability the student **consents to once at Start**, and the
> runtime then lets exactly that action run unattended (still capped by the
> budget). Keep it as tight as the value needs — a specific send tool or a
> specific command, to a bounded audience — never "can run any shell" or "can send
> to anyone." The student can also grant this ad-hoc from a live gate via **Approve
> every time**. Default to a gate; reach for an autonomous action only when
> unattended is the actual point.

### Two additional captures (both required before scaffold)

**Durable knowledge:** Anything the loop must know that does NOT change between
runs — a style guide, a rubric, known-good examples, a schema? Put it in a
`knowledge/` file inside the loop folder and have the loop's `SKILL.md` point at
it (read-only). Do not inline changing data here.

**Budget / stop rule:** The maximum cost before the loop must halt even if the
goal is unmet — as a hard stop, not a suggestion. Capture at least one of:
`max_iterations`, `max_tokens`, `max_minutes`. A loop without a budget can run
forever and drain the student's usage. **If the student skips this, do not
scaffold — collect it first.**

**Set `max_iterations` as the primary dial.** In a real agent vault each
iteration reloads the whole context (CLAUDE.md + memory + skills) through cache,
so a single iteration typically costs **~150,000–200,000 tokens** — not the tiny
number an empty test loop suggests. Two consequences: (1) pick `max_iterations`
first (e.g. 5–25) — it's the only cap that can't overshoot, since it advances
only on a completed turn; (2) if you set `max_tokens`, make it a **generous
runaway backstop** (think millions, not hundreds of thousands), or it will trip
after one or two iterations before the loop can reach its goal. `max_tokens` and
`max_minutes` are checked at iteration boundaries, so either can overshoot by up
to one iteration's worth.

---

## Phase 2 — Survey reuse (two passes)

### Pass 2a — Installed capabilities (and a dependency probe)

Check what's already available in this agentHome — existing skills in
`.claude/skills/`, connectors/MCP servers the student has enabled, the `gh`/`git`
CLIs. For each one relevant to the loop's discovery or action step, note it so
the scaffold wires it in rather than stubbing it.

**Then probe what the loop needs but the student may not have set up.** For each
external dependency the action/verification steps imply — a CLI (`command -v jq`),
an API key or token (is the env var set?), an input file the loop reads — check
whether it's actually present *now*:

- If it **is** present, good — wire it in.
- If it is **not**, do NOT silently stub it. Record it as a **declared
  requirement** (kind `command` / `env` / `file`) for the `loop-requires` block
  (Phase 4), and tell the student plainly: *"this loop needs X, which isn't set up
  yet — here's how to set it up."* The Loop Runtime will re-check these before
  every run and hold the loop in a "needs setup" state (naming what's missing)
  rather than letting it start and fail mid-run. Declaring the requirement is what
  turns an opaque runtime error into a clear, fixable message.

### Pass 2b — Skill bank search

Dispatch a search sub-agent over `references/skill-bank/`. It reads each entry and
returns any skill that overlaps the loop's goal, trigger, or action. Anything
found is a reuse candidate — extend it, don't duplicate it.

---

## Phase 3 — Select the simplest pattern

Default: **ReAct + deterministic verifier** unless the brief clearly calls for
something else. Load only the reference file for the chosen pattern.

| Pattern | When to use | Reference file |
|---|---|---|
| **ReAct + deterministic verifier** (DEFAULT) | One workstream, "done" is a program-checkable predicate | `references/pattern-react-deterministic-verifier.md` |
| Evaluator–optimizer | Criteria need judgement, not just a script | `references/pattern-evaluator-optimizer.md` |
| Orchestrator–workers | Work genuinely parallelizes into independent subtasks | `references/pattern-orchestrator-workers.md` |
| Ralph | Want a crude baseline / teaching loop | `references/pattern-ralph.md` |

On this host the Loop Runtime executes **one iteration at a time** (a global
concurrency cap of 1), so orchestrator–workers parallelism is logical, not truly
concurrent — the workers are dispatched as sub-agents within a single iteration.

State the chosen pattern and a one-line rationale before Phase 4.

---

## Phase 4 — Emit blueprint, then scaffold

### Step 4a — Blueprint approval contract

Before writing any files, render the filled blueprint (optional helper; if
`python3` is unavailable, present the same fields as a plain labelled list —
GOAL / TRIGGER / VERIFY / STATE / GATES — the content is what matters, not the
box):

```
python3 scripts/loop_progress.py blueprint \
  GOAL    "<the checkable predicate from Q1>" \
  TRIGGER "<run-until-done | interval N min from Q2>" \
  VERIFY  "<verifier command from Q5>" \
  STATE   "loops/<name>/STATE.md" \
  GATES   "<human gate list from Q7>"
```

Present the box. **Do not write files until the student approves.** If anything
is wrong, correct the elicit answers and re-render. (If the loop is being
designed non-interactively — the caller has already supplied every answer and an
explicit go-ahead — treat that as the approval and proceed; never invent an
approval that wasn't given.)

### Step 4b — Scaffold the loop folder

Write a single self-contained folder at the agentHome root. It lives **outside
`.claude/`** so Team Pack updates never touch it:

```
loops/<name>/
  SKILL.md         # loop logic + the declared target paths + the verifier call convention (read-only each run)
  STATE.md         # progress/cursor/counters (read+written each run); init with empty counters
  verifier.sh      # adapted from scripts/verifier_template.sh or a worked example; chmod +x; binary exit code
  HUMAN-GATES.md   # gate list + the machine-readable budget block (below)
  TRIGGER.md       # the trigger block (below)
  work/            # optional scratch for NEW artifacts (promote into a declared target on verify)
  knowledge/       # (only if durable knowledge was captured) read-only reference
```

Generate `SKILL.md`, `STATE.md`, `HUMAN-GATES.md`, and `TRIGGER.md` from the
templates in `templates/`. Adapt `scripts/verifier_template.sh` (or
`scripts/verify_item_example.sh` / `scripts/verify_example.sh`) into `verifier.sh`
and make it executable.

Record the loop's **declared target paths** (from Q4) in its `SKILL.md`, and
create what the loop needs up front: `work/`, and any output target it writes
(e.g. an output directory). Drop an empty `.gitkeep` into each empty dir so it
survives git/packaging/sync (otherwise empty dirs silently vanish in transport).
If the loop *reads* an input that doesn't exist yet (e.g. a tracker file the
student is expected to provide), say so plainly rather than letting the loop fail
on its first run.

**`verifier.sh` exit code:** `0` = condition holds (for the goal predicate, "stop
the loop"; for a per-iteration check, "this attempt passed"). `1` = condition does
not hold (iterate / retry). A missing or non-executable verifier is treated by the
runtime as a failure (fail-closed), never as a pass.

**Machine-readable budget** — written into `HUMAN-GATES.md` exactly so the Loop
Runtime can parse and enforce it. **Keep only the keys you're setting and delete
the rest; at least one is required** (the example shows all three). Lead with
`max_iterations`; size `max_tokens` as a generous backstop (each real-vault
iteration ≈ 150k–200k tokens — see the budget rule in Phase 1):

````
```loop-budget
max_iterations: 25
max_tokens: 5000000
max_minutes: 60
```
````

**Machine-readable trigger** — written into `TRIGGER.md`:

````
```loop-trigger
mode: run-until-done
```
````

or

````
```loop-trigger
mode: interval
interval_minutes: 15
```
````

**Machine-readable requirements (optional)** — written into the loop's `SKILL.md`
as a ```` ```loop-requires ```` block, from the unmet dependencies found in the
Phase 2a probe. The Loop Runtime checks these before every run and holds the loop
in a **"needs setup"** state (naming what's missing) instead of failing mid-run.
One declaration per line; **delete the block entirely if the loop needs nothing
beyond the vault and the student's Claude login** (do not leave it empty):

````
```loop-requires
command: gh
env: OPENAI_API_KEY
file: ~/Documents/tracker.md
```
````

- `command: <name>` — a CLI that must be on PATH.
- `env: <VAR>` — an env var / API key that must be set and non-empty.
- `file: <path>` — an input file that must exist (relative → agent folder; `~` = home).

Only declare things the loop genuinely can't run without — a missing requirement
stops the loop, so don't gate it on nice-to-haves.

**Machine-readable autonomous actions (optional)** — written into the loop's
`SKILL.md` as a ```` ```loop-allow ```` block, ONLY when the loop must take an
otherwise-gated action (send/post/publish/push) **unattended** to be worth
running (Q7). Each line is a *concrete* rule — never a fuzzy class — so the
student can see exactly what they're consenting to at Start:

````
```loop-allow
tool: mcp__claude_ai_Gmail__send_message
bash: gh pr create
```
````

- `tool: <exact tool name>` — auto-allow this one tool (e.g. the specific send
  tool the loop's action step actually uses; look it up, don't guess).
- `bash: <command prefix>` — auto-allow a shell command that STARTS WITH this
  literal prefix (the runtime still blocks `;`/`|`/`$()` so the prefix can't be
  used to smuggle a second command). Make the prefix as specific as possible.

The runtime honors these ONLY after the student clicks **Allow & start** once
(consent is bound to the exact rules — change the block and it re-asks). Keep the
list minimal and narrow: prefer one exact `tool:` over a broad `bash:` prefix,
and never declare `bash: curl` / a bare interpreter / a Write tool (writes stay
bounded by Targets regardless). **If the loop needs no unattended action, omit
this block** — the default gate is the safe choice.

### Step 4c — Lint the scaffold (a program checks it, not your judgement)

loop-maker holds its own output to the bar it demands of loops. After writing the
folder, run the deterministic linter and fix everything it flags before declaring
the loop done:

```
python3 scripts/lint_loop.py loops/<name>/
```

It fails on unfilled `{{placeholders}}`, a missing/empty budget or trigger block,
a stub or non-executable verifier, missing gates, a malformed or empty
`loop-requires`/`loop-allow` block (or a too-broad autonomy grant), and vague or
infinite-retry language ("make sure it works", "keep trying", "edit anything").
If `python3` is
unavailable, walk the Output-discipline checklist below by hand instead.

Then print the file tree so the student can confirm nothing is missing, and remind
them: the loop is **designed**; it runs via the desk's Loop Runtime (or you can
run iterations manually on request) — it will not start on its own until that
runtime is enabled.

---

## State backend

This host is single-machine, single-writer, so state is always a plain markdown
file the loop reads and writes:

```
loops/<name>/STATE.md
```

(Generated from `templates/STATE.md.tmpl`; initialise with the current timestamp
and empty counters.) There is no parallel/worktree backend on this host.

---

## Human gates + budget: non-negotiable

A loop without human gates can act in ways no one intended. A loop without a
budget can drain the student's usage. Both are required before a loop is
considered scaffolded.

- **Gates** appear in `HUMAN-GATES.md`. At minimum: one gate before the first
  live run, one gate if the verifier signals an anomaly. The runtime pauses at
  every gate and waits for approval — nothing irreversible runs unattended.
- **Budget** appears in `HUMAN-GATES.md` as the `loop-budget` block — a hard
  stop. At least one of max_iterations / max_tokens / max_minutes.

Do not declare the loop done if either is missing. If the student skipped Q7 or
the budget, surface it now and collect it before writing files.

---

## Output discipline checklist

Before handing off the scaffolded loop, verify all of the following. If any item
is missing, fix it before declaring done.

- [ ] All 7 questions answered (Goal · Trigger · Discovery · Action ·
      Verification · State · Human gates) and recorded in the blueprint
- [ ] Loop folder is at `loops/<name>/` (outside `.claude/`), self-contained
- [ ] Separate `verifier.sh` exists, is executable, and has a binary exit code
- [ ] `STATE.md` exists with initial timestamp + empty counters
- [ ] `HUMAN-GATES.md` has at least one pre-run gate and one anomaly gate
- [ ] `HUMAN-GATES.md` has a `loop-budget` block with at least one hard limit
- [ ] `TRIGGER.md` has a `loop-trigger` block (`run-until-done` or `interval`)
- [ ] The loop's declared target paths are recorded in its `SKILL.md`, `work/`
      exists, and any output target the loop writes has been created
- [ ] Any external dependency the loop needs but the student hasn't set up is
      declared in a `loop-requires` block (or the block is deleted because the
      loop needs nothing beyond the vault) — and the student was told what to set up
- [ ] If (and only if) the loop must take a send/post/publish action unattended,
      it's declared as a narrow `loop-allow` rule (specific `tool:`/`bash:` prefix,
      not a broad grant) — otherwise no block, and the action stays gated
- [ ] The verifier's argument convention is documented in the loop's `SKILL.md`
- [ ] The student was told the loop is designed and will not auto-run until the
      desk's Loop Runtime is enabled
- [ ] `python3 scripts/lint_loop.py loops/<name>/` passes — no placeholders, no
      vague/infinite-retry language, budget + trigger blocks valid (or the
      equivalent manual check if python3 is unavailable)
