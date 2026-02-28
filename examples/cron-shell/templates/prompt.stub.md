# Cron Prompt Stub（time anchor + guardrails + output contract）

## Time anchor
- Now: {{NOW_ISO}}
- Window: {{WINDOW}}

## Guardrails
- Redundancy check: reuse cache / TTL=30min
- No-new-signal exit: stop and ask for direction if 2 consecutive steps add no new evidence
- Secrets: never print tokens; never paste raw credentials

## Output contract
Return exactly:
1) Summary (5–10 bullets max)
2) Evidence map (links/paths)
3) TODO (1 actionable)
4) Draft post/comment (100–200 chars)

## State/Receipt
- Write/update `state.json`
- Write `receipts/{{run_id}}.json` following receipt.schema.json
