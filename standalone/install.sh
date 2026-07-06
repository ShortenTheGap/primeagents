#!/usr/bin/env bash
# Installer for the standalone loop-maker skill (Claude Code).
# Copies the skill into ~/.claude/skills/loop-maker/ and makes its scripts
# executable. Safe to re-run: it backs up any existing install first.
set -euo pipefail

# Resolve the directory this script lives in (so it works from anywhere).
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SRC="$SRC_DIR/loop-maker"

DEST_ROOT="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
DEST="$DEST_ROOT/loop-maker"

if [ ! -d "$SKILL_SRC" ]; then
  echo "✗ Can't find the skill folder next to this installer ($SKILL_SRC)." >&2
  echo "  Unzip the whole bundle and run ./install.sh from inside it." >&2
  exit 1
fi

echo "Installing loop-maker → $DEST"
mkdir -p "$DEST_ROOT"

# Back up an existing install so nothing is lost.
if [ -e "$DEST" ]; then
  STAMP="$(date +%Y%m%d-%H%M%S)"
  BAK="$DEST.backup-$STAMP"
  echo "  • Existing install found — backing it up to $BAK"
  mv "$DEST" "$BAK"
fi

# Copy the skill.
cp -R "$SKILL_SRC" "$DEST"

# Make the helper scripts executable (zip transport can drop the +x bit).
find "$DEST/scripts" -type f \( -name '*.sh' -o -name '*.py' \) -exec chmod +x {} + 2>/dev/null || true

echo
echo "✓ Installed. The skill is now at: $DEST"
echo
echo "Next steps:"
echo "  1. Open (or restart) Claude Code so it picks up the new skill."
echo "  2. Say:  make a loop that <your recurring task>"
echo "     (or just /loop-maker) — it'll walk you through 7 questions and scaffold it."
echo "  3. To RUN a scaffolded loop, see the loop's TRIGGER.md and the skill's"
echo "     references/host-claude-code.md (/loop, /schedule, cron, or manual)."
echo
echo "Note: this standalone build has no runtime — you run loops yourself, and"
echo "any loop with irreversible (send/publish/spend/delete) gates must stay"
echo "interactive, never behind an unattended runner."
