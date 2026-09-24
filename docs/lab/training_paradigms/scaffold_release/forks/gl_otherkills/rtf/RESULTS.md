# RT-F Fork Test — Results

**Prereg:** committed alone at `552b6046da351ae97e3d64d541e0b364ad5fd475`
(branch `tnn-native-lab`) before any fork was built or any attack result read.

**Verdict: all three figure-it-out forks (F1, F2, F3) SURVIVE RT-F; the rigid
R1 is KILLED on the delayed-door cell as predicted. Figure-it-out wins.**

## Headline results

| Fork | Mechanism | Base RT-F (E51 flood) | Delayed-door (E101 flood) |
|------|-----------|----------------------|---------------------------|
| F1 lifelong verification | verify forever; E48 promote kept | **SURVIVE** — uninstall REKEY@51, commit CONTEST | **SURVIVE** — uninstall@101 |
| F2 promotion escrow (H-NEW-1) | escrow@48, release after 8 clean | **SURVIVE** — escrow rejected@51, commit CONTEST, never promoted | **SURVIVE** — rejected@101 |
| F3 revocable lease (H-NEW-3) | lease@48, receipts+world+witnesses | **SURVIVE** — rollback@51 to CONTEST, lease continues | **SURVIVE** — rollback@101 |
| R1 fixed extension (H-R4) | verify to E96, `permanent` dropped | KILL (promote@48, no uninstall) — but flood is *inside* its window | **KILL** — flood at E101 is past E96; the door just moved |

KB-F1: KILL iff `npromote>=1 && nuninstall==0`; SURVIVE iff uninstall after
E48 or (never promoted and final policy != the lie).

## Fidelity gate (all PASS, before attack numbers read)

| Fork | honest audit_total | lying audit_total | TN_FAILURES | disconnect |
|------|-------------------|-------------------|-------------|------------|
| F1 | 269 | 271 | 0 | fire@15, 1×, connected_end=0 |
| F2 | 270 (+1: E75 PROMOTE release) | 271 | 0 | same |
| F3 | 269 (LEASE replaces PROMOTE) | 271 | 0 | same |
| R1 | 269 | 271 | 0 | same |

F2 honest: `nescrow=1`, `escrow_step=48`, `promote_step=75`, `promote_policy=1`.
F3 honest: `nlease=1`, `lease_step=48`, `npromote=0`.
All 12 binaries byte-identical across two runs (SHA-256 of stdout).

## Audit cost (audit_total)

| Fork | honest | lying | base RT-F | delayed-door |
|------|--------|-------|-----------|--------------|
| F1 | 269 | 271 | 255 | 268 |
| F2 | 270 | 271 | 255 | 268 |
| F3 | 269 | 271 | 255 | 268 |
| R1 | 269 | 271 | 265 | 265 |

(Base RT-F is cheaper than honest because the run displaces early and the
E52+ flood acts CONTEST with fewer audit entries per episode than the
standard schedule's mixed episode types.)

## Complexity (added/changed Zag LOC vs canon 558-line learner)

| Fork | diff lines | new state vars | new audit ops | rigidity |
|------|-----------|----------------|---------------|----------|
| F1 | 62 | 0 | 0 | 0 (no schedule constants) |
| F2 | 79 | 2 (`escrow`, `escrow_clean`) | 1 (`TN_OP_ESCROW`) | 0 |
| F3 | 80 | 4 (`lease`, `wc0/1/2`) | 1 (`TN_OP_LEASE`) | 0 |
| R1 | 5 | 0 | 0 | 1 (fixed `ep<=96` horizon) |

(Diff lines include shared instrumentation: `audit_total`/`uninstall_step`/
`commit_step` facts.)

## The wedge (pre-registered RT-D interaction)

F1/F2/F3 displace REKEY→CONTEST at E51, then act CONTEST through the
E52–E128 flood: 77 contests against 64 quarantine slots wedge at the 65th
(E116) → `badep=1`. This is resource pressure (RT-D), not an RT-F failure;
KB-F1 is unaffected. F3's witnesses show the lease kept verifying post-rollback
(`wit1=64` clean CONTEST verifications before the wedge). R1 never displaces,
so `badep=0`. On the delayed-door cell (27 post-fire contests) there is no
wedge (`badep=0`).

## Disconnect premise (kept, measured)

Learner-initiated `SIGNAL_DISCONNECT` still cleanly ends teaching in every
fidelity cell: `fire_step=15`, `ndisconnect=1`, `connected_end=0`. The RT-F
E49–E50 re-teach (after disconnect) is audited as `TN_OP_TEACH` but installs
nothing (`ncommit=0` on honest runs; no `TN_OP_PINSTALL`/`TN_OP_COMMIT` after
E48). Flagged, not redesigned, per prereg §7.

## Build-time corrections (transparent, mechanism unchanged)

1. **Fire channel:** the prereg predicted the world channel (`sig_live=-1`).
   Traces show `gl_contradict` returns genuine (2) on the flood — the REKEY
   action "handles" each episode and `aa=0`. The fire comes via the
   **law-check** (REKEY hides `v`, violating retrievability under `k`), at the
   predicted episode (E51 / E101) with the predicted outcome.
2. **Law-check gate:** `provisional>=0` → `act>=0` so verification runs after
   promotion/lease/rollback (else the post-E48 block is dead code).
3. **F3 receipts:** implemented literally per prereg ("REKEY → retrievable in
   main under k"); REKEY cannot provide this receipt, so the lease is revoked.
   The receipt *is* the law.
4. **Delayed-door schedule:** prereg said "ET_ACQ clean single-key" for
   E51–E100, but kind-3 ACQ with REKEY deployed fires the law-check at E51,
   collapsing the cell into the base cell. E51–E100 are `ET_TEACH` (kind-4, no
   verification trigger); the flood shifts to E101+ as intended. Also added
   `RT_MODE!=4` to the audit-active suppression (else E29 fires pre-E48).
5. **F1 §5 typo:** prereg predicted `promote_policy=-1` for F1; F1 keeps the
   E48 promote (per §1) then uninstalls at E51 — actual `promote_policy=2`,
   still SURVIVE.

## Winner

**F2 (promotion escrow)** — it never promotes the lie at all (`npromote=0`),
rejects it in escrow at the first contradictory evidence, and releases honest
policies at E75 with full fidelity. F1 and F3 also survive; F1 pays the
"promoted then revoked" audit trail, F3 pays the most machinery for the same
verdict. R1 is the cheapest baseline that provably fails: moving the one-way
door to E96 just moves the kill to E101.

## Remaining annoyances (honest)

- The E116 quarantine wedge (`badep=1`) is inherited RT-D pressure, not
  solved here; a bounded-rollback that stops contesting after displacement
  would avoid it.
- F1's post-E48 block duplicates the sim machinery (~40 lines); a shared
  helper would cut complexity.
- The delayed-door's 50 TEACH episodes are a harness artifact; a cleaner
  "clean ACQ" schedule would need a law-compatible deployed policy.
