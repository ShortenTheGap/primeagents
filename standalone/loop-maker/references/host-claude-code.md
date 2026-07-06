# Host adapter — Claude Code (standalone)

How the abstract actions used throughout `loop-maker` map onto **Claude Code**
(the CLI/desktop agent), for members running the skill **without** Prime Agent
Desk's Loop Runtime.

The skill body describes actions in neutral language ("dispatch a sub-agent",
"read a file", "schedule a run"). This file resolves each to Claude Code, and —
crucially — spells out the **honest execution story**: there is no dedicated
runtime enforcing budgets and gates, so *you* (with a runner you choose) drive
the loop, and the gates/budget are conventions the agent honors plus the caps
your runner sets.

---

## The host in one paragraph

Claude Code runs the agent in your terminal (or desktop app) against the current
working directory. It can read/write files and run shell commands directly. It
has built-in ways to repeat a prompt — `/loop` (in-session, on an interval) and
`/schedule` / cron for scheduled, cold-start runs — but **none of them know
about `loop-budget` or `HUMAN-GATES.md`**. The scaffold this skill produces is
therefore *self-describing*: the loop's own `SKILL.md` tells the agent to read
state, act once, verify, write state, and **stop at any gate**. You point a
runner at it to make it repeat.

---

## Action map

| Abstract action | In Claude Code (standalone) |
|---|---|
| **Read / write a file** | Native `Read` / `Write` / `Edit` tools, or `Bash`. Paths are relative to the working directory you launched Claude Code in. |
| **Run a shell command** | The `Bash` tool. Shell state does not persist across calls — chain with `&&` or write a script. |
| **Dispatch a sub-agent** | The `Task` / `Agent` tool. Use inside one iteration (e.g. orchestrator–workers). Keep it to one loop iteration at a time unless you deliberately isolate workers (see Concurrency). |
| **Schedule / recurring run** | See **Runners** below — `/loop` for interval-while-open, `/schedule` or cron for scheduled cold-start, or manual. The `loop-trigger` block in `TRIGGER.md` records the *intent*; a runner enacts it. |
| **Run-until-condition** | `mode: run-until-done` in `TRIGGER.md`. Drive it with a shell loop that re-invokes the loop and stops when `verifier.sh` exits 0, or run iterations by hand until it holds. |
| **Verify an iteration** | `verifier.sh` in the loop folder, run after each action. Exit 0 = holds, exit 1 = iterate. Missing / non-executable = failure (fail-closed). This works identically everywhere — it's just a script. |
| **Web search** | Only if you have a search tool/MCP enabled. Don't assume it; design a non-search discovery path when it's absent. |
| **Approve an irreversible action** | There is **no runtime pause**. The loop's `SKILL.md` instructs the agent to **halt at each gate in `HUMAN-GATES.md`, write the reason to state, and wait for you** instead of acting. Honor it: keep gated actions in a human-in-the-loop session, not an unattended runner. |

---

## Runners — how to actually make it repeat

Pick the one that matches the loop's `TRIGGER.md` mode. **Verify the exact
command/flags against current Claude Code docs — slash-command syntax changes.**

### 1. `/loop` — interval, while the session is open
Best match for `mode: interval`. Runs a prompt/slash-command on a recurring
interval in your current session:

```
/loop <interval> run one iteration of the loops/<name> loop
```

- Advances only while the Claude Code session stays open (like the Desk's "while
  the app is open" ceiling).
- Have the invoked prompt read `STATE.md`, do ONE pass, run `verifier.sh`, write
  state, and **stop at any gate**. The budget's `max_iterations` is your backstop
  — tell it to stop once the ledger reaches that count.

### 2. `/schedule` or cron — scheduled, cold-start
Best match when you want true "every morning at 8am" behavior (which the Desk
cannot do). Two options:

- **`/schedule`** — Claude Code's scheduled cloud agents (a cron-style routine).
- **OS cron + headless Claude Code**, e.g.:
  ```
  */15 * * * * cd /path/to/project && claude -p "run one iteration of the loops/<name> loop, honoring HUMAN-GATES.md" >> loops/<name>/run.log 2>&1
  ```
  A cold-start runner is the real test of the skill's discipline: the agent has
  no memory of prior runs, so everything it needs must be on disk in `STATE.md`.
  **Do not put gated (irreversible) actions behind an unattended cron** — cron
  can't approve a gate. Keep gated loops interactive.

### 3. Manual — run one iteration on demand
Always available: in a session, say *"run one iteration of the loops/<name>
loop"*. The agent reads state + the loop's `SKILL.md`, does one pass, verifies,
and updates state. Nothing continues on its own.

### run-until-done as a shell loop
For `mode: run-until-done` without a session babysitter:

```
until ./loops/<name>/verifier.sh; do
  claude -p "run one iteration of the loops/<name> loop, honoring HUMAN-GATES.md"
done
```

Add your own iteration cap so a never-satisfied predicate can't spin forever —
mirror `max_iterations` from `HUMAN-GATES.md`.

---

## Budget & gates without a runtime — read this

The Desk's Loop Runtime *enforces* `loop-budget` and *pauses* at gates. Standalone,
**those are conventions, not walls.** To stay safe:

- **Budget:** your runner is the enforcer. Put a hard iteration cap in the runner
  itself (the `until … done` count, cron frequency, or `/loop` you stop manually)
  that matches `max_iterations`. Remember each iteration can cost ~150k–200k
  tokens once your project context is large — set caps low.
- **Gates:** never run a loop with gated (send / publish / spend / delete /
  outside-target) actions under an *unattended* runner. Run those interactively
  so you can approve. The scaffold already tells the agent to stop and ask; keep
  a human present to answer.

---

## What NOT to wire in

- Inbound webhooks or "while the laptop is closed" behavior with `/loop` (that's
  session-bound — use cron/`/schedule` for cold-start instead).
- Tools or connectors you haven't enabled — verify availability in Phase 2
  (survey) before relying on them.
- Unattended runners for any loop that has an irreversible gate.
