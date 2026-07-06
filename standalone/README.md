# loop-maker (standalone for Claude Code)

Design and scaffold **self-running, self-verifying agent loops** — right inside
Claude Code, no Prime Agent Desk required.

A loop is a task your agent runs on its own, over and over, until a goal is met —
then stops. This skill interviews you (7 short questions), then scaffolds a
self-contained loop folder with its own logic, a **separate verifier** (a script
with a pass/fail exit code), an external state file, human gates, a trigger, and a
hard budget.

> **What you get vs. what the Desk adds.** This standalone build is the *design +
> scaffold* half. It does **not** include a runtime that auto-runs loops on a
> schedule, enforces budgets, and pauses at gates — that's the Prime Agent Desk
> feature. Standalone, **you run the loop yourself** with Claude Code's built-in
> tools (below), and the budget/gates are conventions you enforce.

---

## Install

1. Unzip this bundle.
2. From inside the unzipped folder, run:

   ```bash
   ./install.sh
   ```

   It copies the skill to `~/.claude/skills/loop-maker/` (backing up any existing
   install) and makes the helper scripts executable.
3. Open or restart Claude Code.

Uninstall: delete `~/.claude/skills/loop-maker/`.

Requirements: Claude Code. `python3` and `bash` are used by optional helper
scripts (a progress display and the scaffold linter); the skill degrades
gracefully to a manual checklist if `python3` is absent.

---

## Make a loop

In Claude Code, just say:

```
make a loop that checks my downloads folder every 30 min and files new invoices
```

or run `/loop-maker`. It first asks whether you truly want a *recurring* loop
(vs. a one-off), then walks the 7 questions — Goal, Trigger, Discovery, Action,
Verification, State, Human gates — and writes a folder:

```
loops/<name>/
  SKILL.md         # the loop's logic (read-only each run)
  STATE.md         # its memory between runs (read + written)
  verifier.sh      # the SEPARATE pass/fail check (exit 0 = done/ok, 1 = iterate)
  HUMAN-GATES.md   # gates + the machine-readable budget block
  TRIGGER.md       # run-until-done or interval
  work/            # scratch space
```

Then it runs a linter over the scaffold so the loop meets the bar before you run
it.

---

## Run a loop (three ways)

This build has no runtime, so you choose how it repeats. Full detail in
`~/.claude/skills/loop-maker/references/host-claude-code.md`; the short version:

| You want… | Use | Notes |
|---|---|---|
| Repeat while your session is open | **`/loop <interval> run one iteration of the loops/<name> loop`** | Stops when you close the session. |
| Scheduled cold-start ("every morning") | **`/schedule`**, or OS **cron** + `claude -p "run one iteration of the loops/<name> loop, honoring HUMAN-GATES.md"` | The agent wakes with no memory — that's why state lives on disk. |
| Just one pass now | Say **"run one iteration of the loops/<name> loop"** | Manual, always available. |

> **Verify slash-command syntax against current Claude Code docs** — `/loop` and
> `/schedule` availability and flags are host-specific and can change.

**Two safety rules with no runtime:**
1. **Budget = your runner's cap.** Nothing auto-stops the loop. Put a hard
   iteration cap in your runner that matches `max_iterations`. Each iteration can
   cost ~150k–200k tokens once your project context is large — set caps low.
2. **Gates stay interactive.** Never run a loop with irreversible (send / publish
   / spend / delete) gates under an unattended runner — it can't approve. Keep a
   human present.

---

## Later: moving to Prime Agent Desk

The `loop-trigger` and `loop-budget` blocks this skill writes are exactly what the
Desk's Loop Runtime reads — so a loop you scaffold here runs there **unchanged**,
and there the runtime enforces the budget and pauses at gates for you.

---

## License & credits

MIT. Adapted from the open-source [`loop-maker`](https://github.com/EricTechPro/loop-maker)
skill (MIT, EricTechPro) with the goal-contract rigor and self-linting idea from
[`qiaomu-goal-meta-skill`](https://github.com/joeseesun/qiaomu-goal-meta-skill)
(MIT, 向阳乔木). See `loop-maker/LICENSE`.
