#!/usr/bin/env bash
set -euo pipefail

# Quick scan helper for file-first memory.
# Usage: ./scripts/agent_notes_scan.sh "keyword"

q=${1:-}
if [[ -z "${q}" ]]; then
  echo "Usage: $0 <keyword>" >&2
  exit 2
fi

rg -n --hidden --glob '!**/.git/**' "${q}" memory MEMORY.md playbooks templates || true
