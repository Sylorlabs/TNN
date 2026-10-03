# Step 0 Name-Check: Ledger Cycle 8 Append

Date: 2026-09-30. Worker: Canonical Ledger Append Worker (cycle 8).

## Standing rules identified before any ledger work

1. **Pure Zag rule:** everything in pure Zag; no Python, C, or other languages. Shell may sequence processes and perform approved checks only. This cycle's work is pure markdown ledger text; no computation needed.
2. **Contaminated paper:** `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md` must remain untouched (zero diff verified before and after).
3. **Owned paths:** only the two ledger files:
   - `docs/lab/research-lead/overnight-20260928/canonical_ledger/CLAIM_LEDGER.md`
   - `docs/lab/research-lead/overnight-20260928/canonical_ledger/CANONICAL_STATE.md`
   plus this NAMECHECK.md in `docs/lab/research-lead/overnight-20260928/ledger_cycle8/`.
4. **Commit with explicit pathspecs** for exactly those three paths. Inspect status before committing.
5. **No em dashes** in any loop documentation. Shell-only dash check.
6. **Preserve all existing claims.** Append only. Never modify a prior entry.
7. **Do not inflate:** prereg/design/analysis results are not SURVIVES. Mark statuses honestly.
8. Never remove a live `.git/index.lock`; wait and retry.

## Pre-work verification

- Ledger at 77 claims (C77 at e6222f94b). CLAIM_LEDGER.md: 1658 lines. CANONICAL_STATE.md: 781 lines.
- All 18 result commits verified present in git log (905586a3b through 396895595).
- No Python invoked in this task.
