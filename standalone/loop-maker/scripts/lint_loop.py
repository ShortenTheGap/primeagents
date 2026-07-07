#!/usr/bin/env python3
"""Deterministic quality gate for a scaffolded loop folder.

loop-maker preaches "a program checks the work, not the model's opinion" — so it
holds its OWN output to the same bar. Point this at a `loops/<name>/` folder and
it fails (exit 1) if the scaffold has unfilled placeholders, a missing or empty
budget/trigger contract, vague verification, or infinite-retry language.

Usage: lint_loop.py <loops/name dir>
Exit:  0 = clean · 1 = problems found · 2 = misuse
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_FILES = ["SKILL.md", "STATE.md", "verifier.sh", "HUMAN-GATES.md", "TRIGGER.md"]

# Unfilled markers — unambiguous "you forgot to substitute this".
PLACEHOLDER_PATTERNS = [
    (r"\{\{[^}]+\}\}", "unsubstituted template placeholder {{...}}"),
    (r"\bTODO\b", "TODO left in"),
    (r"\bTBD\b", "TBD left in"),
    (r"\bFIXME\b", "FIXME left in"),
    (r"待补充|待定", "unfilled placeholder (待补充/待定)"),
]

# Vague / unbounded language that defeats a verifiable loop.
DANGEROUS_VAGUE = [
    r"make sure it works",
    r"edit anything",
    r"change whatever",
    r"keep trying",
    r"until it (looks|seems|feels) (good|right|done)",
    r"随便改",
    r"一直尝试",
    r"直到满意",
]

# A verification/verifier should name concrete evidence, not a vibe.
EVIDENCE = re.compile(
    r"\b(run|exit|grep|test|build|lint|check|verify|exists?|non-empty|count|file|path|"
    r"status|0|1|screenshot|log|artifact|url|api|diff|output)\b",
    re.IGNORECASE,
)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def lint(loop_dir: Path) -> list[str]:
    errors: list[str] = []

    # 1. required files present
    present = {}
    for name in REQUIRED_FILES:
        p = loop_dir / name
        if not p.is_file():
            errors.append(f"missing required file: {name}")
        else:
            present[name] = read(p)

    # 2. verifier executable + not a trivial stub
    verifier = loop_dir / "verifier.sh"
    if verifier.is_file():
        import os

        if not os.access(verifier, os.X_OK):
            errors.append("verifier.sh is not executable (chmod +x)")
        body = present.get("verifier.sh", "")
        non_comment = [l for l in body.splitlines() if l.strip() and not l.strip().startswith("#")]
        if len(non_comment) <= 2 or re.search(r"^\s*exit\s+0\s*$", body, re.MULTILINE) and len(non_comment) <= 3:
            errors.append("verifier.sh looks like a stub (no real predicate) — it must actually check the result")

    # 3. no unfilled placeholders anywhere in the scaffold
    for name, text in present.items():
        for pattern, label in PLACEHOLDER_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                errors.append(f"{name}: {label}")

    # 4. no vague / infinite-retry language
    for name, text in present.items():
        for pattern in DANGEROUS_VAGUE:
            if re.search(pattern, text, re.IGNORECASE):
                errors.append(f"{name}: vague/unbounded instruction matched `{pattern}`")

    # 5. machine-readable budget — at least one real numeric limit
    gates = present.get("HUMAN-GATES.md", "")
    budget = re.search(r"```loop-budget\s*(.*?)```", gates, re.DOTALL)
    if not budget:
        errors.append("HUMAN-GATES.md: missing ```loop-budget``` block")
    else:
        nums = re.findall(r"^\s*(max_iterations|max_tokens|max_minutes)\s*:\s*(\d+)\s*$", budget.group(1), re.MULTILINE)
        if not nums:
            errors.append("HUMAN-GATES.md: loop-budget has no concrete numeric limit (need ≥1 of max_iterations/max_tokens/max_minutes)")

    # 6. machine-readable trigger — valid mode
    trigger = present.get("TRIGGER.md", "")
    tb = re.search(r"```loop-trigger\s*(.*?)```", trigger, re.DOTALL)
    if not tb:
        errors.append("TRIGGER.md: missing ```loop-trigger``` block")
    else:
        mode = re.search(r"^\s*mode\s*:\s*(run-until-done|interval)\s*$", tb.group(1), re.MULTILINE)
        if not mode:
            errors.append("TRIGGER.md: loop-trigger mode must be `run-until-done` or `interval`")
        elif mode.group(1) == "interval" and not re.search(r"^\s*interval_minutes\s*:\s*\d+\s*$", tb.group(1), re.MULTILINE):
            errors.append("TRIGGER.md: interval mode needs a numeric interval_minutes")

    # 7. gates present (at least the two unconditional ones)
    if gates and not re.search(r"\bG1\b", gates):
        errors.append("HUMAN-GATES.md: no G1 (pre-run sign-off) gate")
    if gates and not re.search(r"\bG2\b", gates):
        errors.append("HUMAN-GATES.md: no G2 (verifier-anomaly) gate")

    # 8. verification names concrete evidence
    skill = present.get("SKILL.md", "")
    if skill and not EVIDENCE.search(skill):
        errors.append("SKILL.md: names no concrete verification evidence (commands, exit codes, file checks, counts)")

    # 9. the work/ scratch dir the scaffold is told to create must exist
    if not (loop_dir / "work").is_dir():
        errors.append("missing work/ scratch dir (scaffold must create it; add a .gitkeep so it survives sync)")

    # 10. optional ```loop-requires``` block — if present, every line must be a
    # valid `command:|env:|file: value` declaration, and it must not be empty (an
    # empty block means the requirements were neither filled in nor the section
    # deleted). Absent block = the loop needs nothing beyond the project = fine.
    rb = re.search(r"```loop-requires\s*(.*?)```", skill, re.DOTALL)
    if rb:
        lines = [l.strip() for l in rb.group(1).splitlines()]
        meaningful = [l for l in lines if l and not l.startswith("#") and not l.startswith("<!--")]
        if not meaningful:
            errors.append("SKILL.md: empty ```loop-requires``` block — list real requirements or delete the section")
        for l in meaningful:
            if not re.match(r"^(command|env|file)\s*:\s*\S", l):
                errors.append(f"SKILL.md: loop-requires line must be `command:|env:|file: <value>`, got `{l}`")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: lint_loop.py <loops/name dir>", file=sys.stderr)
        return 2
    loop_dir = Path(argv[1])
    if not loop_dir.is_dir():
        print(f"not a directory: {loop_dir}", file=sys.stderr)
        return 2
    errors = lint(loop_dir)
    if errors:
        for e in errors:
            print(f"✗ {e}", file=sys.stderr)
        print(f"\n{len(errors)} problem(s) — fix before declaring the loop scaffolded.", file=sys.stderr)
        return 1
    print(f"✓ loop lint passed: {loop_dir.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
