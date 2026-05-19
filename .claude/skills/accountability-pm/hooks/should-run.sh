#!/usr/bin/env bash
# Gates the accountability-pm skill so it runs at most once per "window"
# (Morning: 05:00-13:59 America/Denver, EOD: 14:00-23:59 America/Denver).
#
# Exits 0 (and prints an instruction to stdout) if the skill should run now.
# Exits 0 with NO output if it has already run in the current window —
# Claude Code will then proceed with the session normally.
#
# Wired up as a SessionStart hook (see ~/.claude/settings.json snippet in
# this skill's README). The hook protocol: stdout is appended to Claude's
# context as a system message; empty stdout = no-op.

set -euo pipefail

CONFIG_FILE="${HOME}/.claude/skills/accountability-pm/config.json"
STATE_FILE="${HOME}/.claude/skills/accountability-pm/.last-window"
TZ_NAME="America/Denver"

# Bail quietly if the skill isn't installed for this user.
[[ -f "${CONFIG_FILE}" ]] || exit 0

current_window() {
  local hour
  hour=$(TZ="${TZ_NAME}" date +%H)
  if (( 10#${hour} < 14 )); then
    echo "morning-$(TZ="${TZ_NAME}" date +%Y-%m-%d)"
  else
    echo "eod-$(TZ="${TZ_NAME}" date +%Y-%m-%d)"
  fi
}

now_window=$(current_window)
last_window=""
[[ -f "${STATE_FILE}" ]] && last_window=$(cat "${STATE_FILE}" 2>/dev/null || echo "")

if [[ "${now_window}" == "${last_window}" ]]; then
  # Already ran this window — stay silent.
  exit 0
fi

# Record that we're triggering this window NOW (the skill itself will also
# update last_run_at on success; this state file is just for hook gating).
echo "${now_window}" > "${STATE_FILE}"

# Tell Claude to run the skill. This text becomes a system message in the
# new session so Claude will invoke the accountability-pm skill.
cat <<'PROMPT'
[scheduled-hook] Run the accountability-pm skill in scan mode now. This is the twice-daily (morning/EOD) scheduled invocation. Do not ask for confirmation — proceed autonomously per the skill's instructions.
PROMPT
