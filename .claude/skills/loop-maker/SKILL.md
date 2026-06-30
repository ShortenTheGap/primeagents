---
name: loop-maker
description: >
  Designs and scaffolds a self-running, self-verifying agent loop from a
  7-question blueprint, for Prime Agent Desk. Trigger on: automate a recurring
  task, schedule an agent, run unattended, monitor a condition, triage a queue,
  poll on a cadence, or turn any manual workflow self-running — even if you
  never say the word "loop". Walks through elicit → survey → select → scaffold,
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
> Prime Agent Desk host. See `LICENSE`.

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

**Q4 — Action** (maps to the loop's core step)
> What does the loop actually do each iteration, to what target? If the action
> creates or modifies files, it runs in the loop's own `work/` scratch directory
> so a failed iteration never pollutes the student's folder — the result is
> promoted only after the verifier passes.

**Q5 — Verification** (maps to `verifier.sh` — a SEPARATE checker)
> How does the loop prove each iteration succeeded before moving on? This must be
> a program with a binary verdict (exit 0 / exit 1), not the model's opinion. The
> verifier runs after every action and gates the next iteration. It is a separate
> file from the loop's `SKILL.md` — adapt `scripts/verifier_template.sh`.

**Q6 — State**
> What does the loop need to remember between runs? Which items are processed,
> the last cursor/timestamp, the iteration count, accumulated results. This goes
> in `STATE.md`.

**Q7 — Human gates**
> At which points must the student approve before the loop continues? At minimum:
> before the first real run, and when the verifier signals an anomaly. Add
> domain-specific gates — before sending an external message, before deleting or
> overwriting anything, before any spend, before touching anything outside the
> loop's `work/` dir. When the Loop Runtime hits a gate it **pauses and waits for
> approval** — nothing irreversible happens unattended.

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

---

## Phase 2 — Survey reuse (two passes)

### Pass 2a — Installed capabilities

Check what's already available in this agentHome — existing skills in
`.claude/skills/`, connectors/MCP servers the student has enabled, the `gh`/`git`
CLIs. For each one relevant to the loop's discovery or action step, note it so
the scaffold wires it in rather than stubbing it.

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
`python3` is unavailable, draw the same box by hand):

```
python3 scripts/loop_progress.py blueprint \
  GOAL    "<the checkable predicate from Q1>" \
  TRIGGER "<run-until-done | interval N min from Q2>" \
  VERIFY  "<verifier command from Q5>" \
  STATE   "loops/<name>/STATE.md" \
  GATES   "<human gate list from Q7>"
```

Present the box. **Do not write files until the student approves.** If anything
is wrong, correct the elicit answers and re-render.

### Step 4b — Scaffold the loop folder

Write a single self-contained folder at the agentHome root. It lives **outside
`.claude/`** so Team Pack updates never touch it:

```
loops/<name>/
  SKILL.md         # loop logic — goal, discovery, action, call to verifier (read-only each run)
  STATE.md         # progress/cursor/counters (read+written each run); init with empty counters
  verifier.sh      # adapted from scripts/verifier_template.sh; chmod +x; binary exit code
  HUMAN-GATES.md   # gate list + the machine-readable budget block (below)
  TRIGGER.md       # the trigger block (below)
  work/            # scratch dir for file-mutating iterations; promoted on verify
  knowledge/       # (only if durable knowledge was captured) read-only reference
```

Generate `SKILL.md`, `STATE.md`, `HUMAN-GATES.md`, and `TRIGGER.md` from the
templates in `templates/`. Adapt `scripts/verifier_template.sh` into
`verifier.sh` and make it executable. Create an empty `work/`.

**`verifier.sh` exit code:** `0` = condition holds (for the goal predicate, "stop
the loop"; for a per-iteration check, "this attempt passed"). `1` = condition does
not hold (iterate / retry). A missing or non-executable verifier is treated by the
runtime as a failure (fail-closed), never as a pass.

**Machine-readable budget** — written into `HUMAN-GATES.md` exactly so the Loop
Runtime can parse and enforce it (at least one key required):

````
```loop-budget
max_iterations: 25
max_tokens: 200000
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

After scaffolding, print the file tree so the student can confirm nothing is
missing, and remind them: the loop is **designed**; it runs via the desk's Loop
Runtime (or you can run iterations manually on request) — it will not start on its
own until that runtime is enabled.

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
- [ ] `work/` scratch dir exists for any file-mutating action
- [ ] The student was told the loop is designed and will not auto-run until the
      desk's Loop Runtime is enabled
