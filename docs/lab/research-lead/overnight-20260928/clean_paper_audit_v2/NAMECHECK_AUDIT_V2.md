# NAMECHECK_AUDIT_V2.md

Step 0 standing-rules name-check (2026-09-30 UTC), Clean-Paper v2 Governance Auditor.

Applicable standing rules:
1. Pure Zag red line (2026-09-23, extended by Micah 2026-09-30 to cover
   scratch/diagnostics/analysis): shell and git only, zero Python at every
   step. All claim sweeps, hash extraction, and byte checks via
   grep/sed/awk/git. No python3 invocation, not even for byte checks.
2. Shell-only byte checks (2026-09-30): use the shell-only
   check_no_dash.sh snippet for AUDIT_V2.md and NAMECHECK_AUDIT_V2.md.
3. Contaminated-paper ban: never read, stage, or commit
   TNN_RESEARCH_PAPER_20260929.md; verify only a zero diff.
4. Shared-branch discipline: explicit pathspecs on every git add/commit;
   run git status --porcelain immediately before each commit; on a live
   .git/index.lock, wait and retry, never remove it.

This audit introduces no new scientific claims. It is a governance check
of the v2 paper (89cf970ee) against the 53-claim ledger freeze (8837d2ee0).
