# LEDGER GOVERNANCE: consolidated summary for Micah

**Date:** 2026-10-03. **Status:** claim minting PAUSED (per f40fbeb11/C463). No live guard installed; all proposals are design/staging only.

## 1. What is broken

The ledger file (`canonical_ledger/CLAIM_LEDGER.md`) on `tnn-native-lab` currently **ends at C376**. Entries **C377-C410 (34 entries, 136 lines) are deleted** by commit `f20dddf0b` ("WATCHDOG: ledger C415", 08:12 UTC). A verified restore exists; it has not been executed.

The cause is worse than one bad commit. Between 07:45 and 08:12 UTC (27 minutes), **9 tail-wipe commits** (0 insertions, 96-136 deletions each) plus **1 empty mint commit** hit the ledger. 6 of the 9 wipes were committed by experiment workers that never intended to mint: a botched watchdog rewrite left the shared worktree/index with the tail deleted, and the next committer swept it in. Root cause (MINT-SCRIPT-FIX analysis, verified): **the "mint" is not an append, it is a C377-anchored tail rewrite**; when the tail reconstruction comes back empty, the rewrite becomes a wipe; nothing ever inspects the staged diff before commit. There is **no mint script**; the whole procedure is manual agent file-edits. Four "silent repair" mints (112-132 insertions) papered over earlier wipes by reconstructing tails from memory, masking the damage. This is the 4th identical failure class in ledger history; C411 (LIFETIME-META-2) was never written at all and exists only in a commit subject plus a staged entry. C412 and C415 entries were likewise never written.

Parallel to the damage: a numbering race. The watchdog minted C404-C454 in commit messages without touching the ledger while the canonical ledger held C404-C410 for other experiments. The watchdog conceded the canonical numbers; its displaced claims are homeless.

## 2. What is proposed (all proposals, no implementation)

| Doc | Proposal |
|---|---|
| LEDGER_RECONCILIATION.md (C457) | Canonical priority: C404-C410 stand. 6 displaced watchdog claims renumbered; 43 watchdog-only claims admitted; C417 probable-duplicate held for verification |
| STAGED_LEDGER_ENTRIES.md (C458) | Exact append text for **49 entries** (43 + 6). STAGING ONLY, not written. NOTE: its C455-C460 numbering is stale (see next) |
| COLLISION_RESOLUTION.md (C463) | Watchdog minted C455-C460 **after** the proposal cutoff. Recommends **Option A (revised)**: post-cutoff claims keep C455-C460; displaced block moves to **C461-C466**. Full write = **55 entries** + C417 decision |
| RESTORE_PLAN.md | Mechanical restore of C377-C410 from `860f009b5`; acceptance = SHA-256 `31431585...6bcdf972`, single pure-append hunk, explicit-pathspec commit |
| C411_INVESTIGATION.md | C411 fully reconstructible from commit subject + staged entry + `b5b4e003e` evidence |
| MINT_GUARD.md (+ mint_guard.sh, TIP) | Bash pre-commit gate: TIP-match, ins>0/del=0, byte-prefix pure-append, 4-line entry shape, no unstaged surprises. Retrospectively blocks all 9 wipes + empty commit. TIP initialized to restored state (SHA above, max 410) |
| WIREIN_PROPOSAL.md (GUARD-WIREIN) | **A now (procedural wire-in), B via D follow-up (ledger-conditional pre-commit hook)**; retires the tail rewrite; TIP as committed file; hook warn-and-pass degradation |
| TIP_COMMITTED_DESIGN.md (TIP-COMMITTED) | TIP is tracked, advanced atomically in the same commit; `--stage-tip` replaces `--advance-tip`; guard/hook read TIP from HEAD and index only |

## 3. Decisions Micah must make (deduplicated, 13)

**Numbering / admission (blocks the ledger write):**
1. **Collision resolution:** approve Option A (revised)? Displaced claims C404/C405/C406/C407/C409/C410-era -> **C461-C466** (NT1, LM1, GEN-STATEFIX, NT2, L3-INR-SEALED, GEN-STRESS); post-cutoff claims keep C455-C460 (INTEGRATION-B1B2, C11-REFIX, LEDGER-RECONCILE, LEDGER-WRITE, COGOPS-PERIOD, MA4-REDTEAM). Reject Option B (renumber the rule-followers), reject sub-numbering and canonical renumbering.
2. **Admit the 43 watchdog-only claims** (C411-C416, C418-C454) with staged caveats? C429 stays EXPLORATORY (stray python3, PROCESS-FAIL); C453 stays CONDITIONAL-PASS (2 python3 invocations disclosed, RX-K10 red team pending).
3. **C417 disposition:** verify against `cognitive_ops_compose/` lane, then mark SUPERSEDED-BY-C410 vs admit as distinct.
4. **Citation-hygiene file edits** (citation_hygiene/CITATION_UPDATES.md, composition_synthesis, gen_nm10 PREREG/REPORT): approve as separate follow-up task?

**Repair sequencing:**
5. **Execute the f20dddf0b restore** per RESTORE_PLAN.md before any ledger write (guard fails closed on damaged HEAD; reconciliation's canonical-priority premise requires C377-C410 present).
6. **Freeze watchdog claim minting** until the full ledger write lands (target block has shifted twice already).
7. Who performs the ledger write (worker on approval, or parent)? And whether the staged text is re-checked against live HEAD immediately before appending.

**Guard wire-in:**
8. **Approve Option A procedural wire-in** (guard as tracked script, mandatory mint step, bare-commit ban restated).
9. **Approve or defer Option B hook** (pre-commit via `core.hooksPath`, ledger-conditional fast path, with worker unblock procedure). Only B stops the six experiment-worker propagation wipes.
10. **TIP refinement (WIREIN+TICOMMITTED shared):** TIP as committed file advanced atomically in the guarded commit (recommended) vs working-tree TIP with post-commit `--advance-tip`.
11. **Hook degradation rule** for worktrees predating the guard lane: warn-and-pass (recommended) vs fail-closed.
12. **Confirm retirement of the tail-rewrite mint**: pure appends only; all tail repairs go through restore mode.
13. **Dash-hygiene gap:** entries C402/C406/C407/C410 contain em-dash bytes despite the "No em dashes were used in this entry (verified)" trailer. Enforce, fix the trailer, or drop the claim? (Guard warns only, does not block.)

**Minor (can ride with wire-in):** `--advance-tip` removed outright vs deprecated-alias error; TIP-bearing commit same-as-wire-in vs separate governance commit; designate the canonical location of the watchdog mint instructions.

## 4. Recommended sequencing

1. **D1-4 (numbering decisions) first.** Nothing can be staged correctly until the final numbers are fixed. Note STAGED_LEDGER_ENTRIES.md needs mechanical edits for Option A (C455-C460 -> C461-C466 renumber, renumbering-record rewrite, 6 new C455-C460 entries drafted, internal refs C421->C465, C447->C466) before approval means anything.
2. **Execute the restore (D5)** and verify SHA. Commit with explicit pathspec; verify C377 and C410 each appear exactly once.
3. **Wire in the guard (D8-13)**: commit lane files (guard, TIP, design docs), amend script per TIP-committed design, install six-step mint procedure; hook (if approved) only after restore + tracked files are in.
4. **Freeze minting (D6)** remains in force through this sequence.
5. **Append the 55 staged entries** + renumbering record in collision-resolve section 5 order (C411-C454, then C455-C460, then C461-C466), guarded, one commit.
6. **Citation-hygiene file edits (D4)** as a separate task.
7. **Re-run mint_guard.sh `--claim` on the next real mint** as the first production guard pass; unpause only after step 5 lands.

**Why this order:** the guard fails closed on the damaged HEAD, so restore must precede wire-in; minting must stay frozen until numbers are final or the race re-opens; staging text is stale until D1 is decided, so approving it as written would re-collide.

## 5. State of the ledger if all this lands

- Canonical C1-C410 intact (C361-C368 carry their documented duplicate pairs; both entries stand, never rewrite history).
- +43 watchdog-only claims (C411-C416, C418-C454; C429 EXPLORATORY, C453 CONDITIONAL-PASS).
- +6 post-cutoff claims at C455-C460; +6 displaced claims at C461-C466; C417 per decision.
- Guard wired: every future ledger commit must pass mint_guard.sh (procedural + optional hook), TIP committed atomically, tail-rewrite retired.

---

**Sources:** `ledger_reconcile/LEDGER_RECONCILIATION.md`, `ledger_write/STAGED_LEDGER_ENTRIES.md`, `ledger_collision_resolve/COLLISION_RESOLUTION.md`, `ledger_restore/RESTORE_PLAN.md`, `c411_investigate/C411_INVESTIGATION.md`, `mint_guard/MINT_GUARD.md` + `mint_guard.sh` + `TIP`, `guard_wirein/WIREIN_PROPOSAL.md`, `tip_committed/TIP_COMMITTED_DESIGN.md`, plus `ledger_resolution/C361-C368_DUPLICATES.md` for precedent.
