# Host adapter — Prime Agent Desk

How the abstract actions used throughout `loop-maker` map onto the one host this
skill targets: **Prime Agent Desk** (the desktop app that runs the Claude Agent
SDK locally, in the student's `my-ai-team` agentHome, on their own Claude login).

The skill body describes actions in neutral language ("dispatch a sub-agent",
"read a file", "schedule a run"). This file resolves each to the desk.

---

## The host in one paragraph

The desk is a Tauri shell wrapping a local Node bridge that hosts the Agent SDK.
The agent (Sue) runs in the student's agentHome with `bypassPermissions` over
loopback only — it can read/write/run anything in that folder, but it is never
reachable from the network. There is no server, no cloud agent: **everything
happens on the student's machine, only while the app is open.**

---

## Action map

| Abstract action | On Prime Agent Desk |
|---|---|
| **Read / write a file** | Native `Read` / `Write` / `Edit` tools, or `Bash` for pipelines. Paths are relative to the agentHome. |
| **Run a shell command** | The `Bash` tool. Runs in the agentHome; shell state does not persist across calls — chain with `&&` or write a script. |
| **Dispatch a sub-agent** | The Agent SDK sub-agent / `Agent` tool. Used inside a single iteration (e.g. orchestrator–workers); the desk runs **one loop iteration at a time** (global concurrency cap = 1), so sub-agents parallelise *within* an iteration, not across iterations. |
| **Schedule / recurring run** | The desk **Loop Runtime**, via the `loop-trigger` block in `TRIGGER.md`. Two modes only: `run-until-done` and `interval` (every N minutes **while the app is open**). There is **no wake-from-sleep cron** — the laptop must be awake and the desk running. |
| **Run-until-condition** | `mode: run-until-done` in `TRIGGER.md`. The runtime iterates act → verify → update state until `verifier.sh` exits 0 (goal predicate holds) or the `loop-budget` trips. |
| **Verify an iteration** | `verifier.sh` in the loop folder, run by the runtime after each action. Exit 0 = holds, exit 1 = iterate. Missing / non-executable = treated as failure (fail-closed). |
| **Web search** | Only if the student has loaded a search MCP server (Connections). Not present by default — do not assume it; check `.claude/` / enabled connectors first, and design a non-search discovery path when it is absent. |
| **Approve an irreversible action** | The runtime **pauses** the loop at any gate listed in `HUMAN-GATES.md`, queues a pending-approval item, and waits — nothing irreversible runs unattended. |

---

## Hard limits of this host (design within them)

- **No background execution.** Close the app or sleep the laptop and the loop
  stops at the next iteration boundary. Interval loops resume scheduling on
  relaunch (a single coalesced catch-up tick, not a replayed backlog);
  run-until-done loops require an explicit restart.
- **Budget is the student's own token usage.** Always set a `loop-budget`. The
  runtime treats it as a hard stop, not a suggestion.
- **One iteration at a time** across all loops in the agentHome.
- **The Loop Runtime may not be installed yet.** When it is absent, this skill
  still designs and scaffolds the loop; the agent can run iterations manually on
  request, but the loop will not run on its own. Say so plainly.

---

## What NOT to wire in

Do not scaffold loops that depend on:

- A wake-from-sleep schedule, an inbound webhook, or any "while the laptop is
  closed" behaviour — the host cannot honour them.
- `crontab` / `launchd` / GitHub Actions schedules — the loop lives in the desk,
  not in the OS scheduler.
- Tools or connectors the student has not enabled — verify availability in
  Phase 2 (survey) before relying on them.
