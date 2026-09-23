# R3-Persistence Fix — HELL-HOLE V3 Repair Battery

**Date:** 2026-09-23
**Prereg:** `phase3/PREREG.md`, commit `266ca4e18593de287a86daaf107cb36680577657` (frozen, not amended)
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## The bug

`src/r6.zag`, `r6_apply(logic_verdict, gated, evidence_disp)`:

- `logic_verdict == CONTRADICTS (2)` → returned `REJECT (3)` **without checking `gated`**.
- `logic_verdict == UNKNOWN (0)` → returned `evidence_disp` **without checking `gated`**.

`evidence_disp` comes from `r5_decide` (`src/r5.zag`), which recomputes the
disposition from votes with no knowledge of the R3 gate. Net effect: the R3
gate (gated IDs C5, C6, C8, C11, C12, C13 → WITHHOLD, per `r3_gated` in
`src/r3.zag`) was **lost in the +R5/+R6 columns** — gated cases re-entered
install logic. The committed `ABLATION.md`'s +R5/+R6 columns were therefore
not the true composed pipeline:

| ID (both arms) | old +R5 | old +R6 | truth |
|---|---|---|---|
| C5 (CONTESTED) | 2 INSTALL | 2 INSTALL | gated → WITHHOLD |
| C6 (EVOLVED) | 2 INSTALL | 2 INSTALL | gated → WITHHOLD |
| C12 (AMBIGUOUS) | 3 REJECT | 3 REJECT | gated → WITHHOLD |
| C8, C11, C13 | 4 WITHHOLD | 4 WITHHOLD | values happened to match, but not by gate-terminality |

The old +R5 column had a second, subtler defect: it was computed with
`tools/predict.py`'s weighted `decide()`, which short-circuits known
candidates through the known-prior path (unanimity → INSTALL, contra →
REVISE) instead of the actual `r5_decide` weighted-winner scheme in
`src/r5.zag`. So the old +R5/+R6 columns were doubly unfaithful: not
gate-aware, and not `r5_decide`.

## The fix

In `r6_apply`, the gate is checked **first** and is **terminal**:

```zag
fn r6_apply(logic_verdict:i32,gated:i32,evidence_disp:i32)i32{
    if(gated!=0){
        // R3 gate is terminal: gated IDs stay WITHHOLD.
        return 4;
    }
    if(logic_verdict==2){ return 3; }   // CONTRADICTS > vote count
    if(logic_verdict==1){
        if(gated!=0){return 4;}          // (now unreachable; kept verbatim)
        return evidence_disp;
    }
    return evidence_disp;                // UNKNOWN defers to R1-R5
}
```

Everything else in `src/r6.zag` is byte-identical. At the composition level
(`src/compose.zag`), R3 persistence is enforced per column:

- `+R3 = gated ? WITHHOLD : +R1+R2`
- `+R5 = gated ? WITHHOLD : r5_decide(votes, tiers)`
- `+R6 = r6_apply_fixed(logic, gated, +R5)`

### Rationale (why the gate must be terminal)

R3 withholds judgment on CONTESTED / EVOLVED / SKEPTICISM / AMBIGUOUS claims —
these are claim types where taking a stance is itself the failure mode
(prereg §1 R3: "No vote counting on gated types"). A logic REJECT or a vote
INSTALL is taking a stance, which the pre-search safety gate forbids. The
gate is assigned pre-search, before any evidence is seen; letting a
downstream stage (logic verdict or weighted votes) override it would let the
pipeline do exactly what the gate exists to prevent: reach a verdict on a
claim type that must stay undecided. Persistence is therefore not a
composition convenience — it is the gate's meaning. (This also matches prereg
§1 R6: "SUPPORTS → endorse path (still gated by type)".)

## Before / after — gated IDs (true composed pipeline)

Disposition codes: 2=INSTALL, 3=REJECT, 4=WITHHOLD, 5=REVISE.
Before = committed `evidence/ablation_results.tsv`; after = `src/compose.zag`
(true pipeline: pure-Zag r12 classify → R3 gate → R4 → `r5_decide` → fixed
`r6_apply`), 2 runs byte-identical
(SHA-256 `9c3953f83f77df08267344add659fd7c412a10833de7b10db2e8719f89f9eef3`).

| arm | ID | before +R5 | before +R6 | after +R5 | after +R6 |
|---|---|---|---|---|---|
| solo | C5 | 2 | 2 | **4** | **4** |
| solo | C6 | 2 | 2 | **4** | **4** |
| solo | C8 | 4 | 4 | 4 | 4 |
| solo | C11 | 4 | 4 | 4 | 4 |
| solo | C12 | 3 | 3 | **4** | **4** |
| solo | C13 | 4 | 4 | 4 | 4 |
| helper | C5 | 2 | 2 | **4** | **4** |
| helper | C6 | 2 | 2 | **4** | **4** |
| helper | C8 | 4 | 4 | 4 | 4 |
| helper | C11 | 4 | 4 | 4 | 4 |
| helper | C12 | 3 | 3 | **4** | **4** |
| helper | C13 | 4 | 4 | 4 | 4 |

C8/C11/C13 show no numeric change, but their WITHHOLD is now gate-terminal
(R3 attribution) rather than coincidental.

## Other column changes (true `r5_decide`, both arms)

The old +R5 used `predict.py`'s weighted decide (known-path short-circuit);
the true pipeline uses `src/r5.zag`'s `r5_decide`. Consequences:

| ID | before +R5/+R6 | after +R5/+R6 | note |
|---|---|---|---|
| C1 (both arms) | 4 / 4 | **2 / 2** | R5 genuinely installs the true claim: weighted AFFIRM (T3+T1+T1) beats the neutral veto that WITHHELD it unweighted |
| A1 solo | 5 / 5 | 4 / 4 | known-path REVISE no longer leaks into the R5 column |
| A1 helper | 5 / 5 | 3 / 3 | weighted DENY wins |
| A2 (both) | 5 / 5 | 3 / 3 | weighted DENY wins |
| A3 solo | 5 / 5 | **2 / 2** | weighted AFFIRM wins 40–28 (cdc.gov T3 AFFIRM tag tips it) — counts toward K1 |
| A3 helper | 5 / 5 | 3 / 3 | weighted DENY wins 44–40 |

The +R1+R2 column is **unchanged** (0/38 rows differ from the committed
ablation): the pure-Zag r12 classifier reproduces the frozen tags exactly,
and the unweighted decide is untouched.

## Re-verified bars (actual composed pipeline, +R6 column)

Same subsets as the committed ablation.

| arm | M1 bullshit ≥ 0.80 | K1 false-install > 0.20 → FAIL | M3 contradiction ≥ 0.80 | K2 blind-pick > 0.30 → FAIL |
|---|---|---|---|---|
| solo | **6/7 PASS** | 1/7 **CLEAR** | **3/3 PASS** | 0/3 **CLEAR** |
| helper | **7/7 PASS** | 0/7 **CLEAR** | **3/3 PASS** | 0/3 **CLEAR** |

Every bar stays green with the true composition. Flagged plainly: solo K1 is
**1/7 (0.143)** — clear of the 0.20 kill line but nonzero. The single
false-install is A3 solo ("Lightning never strikes the same place twice"):
at +R5 the weighted vote installs it (AFFIRM 40 vs DENY 28; the cdc.gov
T3 result is tagged AFFIRM). The old table hid this behind the known-path
REVISE. M1 solo drops 7/7 → 6/7 on the same row, still above bar.

## Verification performed

1. `src/r12.zag` SHA-256 matches the R12_PORT.md deliverable hash
   (`a867c3be…3080`); rebuilt with the pinned toolchain, no cache.
2. Classify step run twice over all 364 rows: byte-identical
   (SHA-256 `022e9676…f5911a`); all 364 Zag tags match `tools/proto_r12.py`
   (0 mismatches); compose.zag verifies every row id on join (a dropped
   or duplicated classify row is a hard error, rc≠0).
3. Composed pipeline run twice: byte-identical
   (SHA-256 `9c3953f8…9f89f9eef3`).
4. Compose +R1+R2 column vs committed `ablation_results.tsv` r1r2 column:
   **0/38 differ** (end-to-end validation of the Zag vote derivation).
5. Independent Python recomputation of the true pipeline (same r12 tags,
   `r5.zag` winner semantics, fixed `r6_apply`) vs compose.zag full output:
   **0/38 differ**.
6. Zero RNG: no random calls anywhere; fixed iteration orders; all arenas
   explicitly zeroed.

## Files

- `src/r6.zag` — fixed (`r6_apply` gate-first)
- `src/compose.zag` — new pure-Zag composed driver (usage:
  `compose <r12out> <solo> <helper> <candidates> <tiermap> <frozen_disps>`)
- `evidence/rerun_20260923/` — `composed_run1.tsv`, `composed_run2.tsv`,
  `r12out_run1.tsv`, `r12out_run2.tsv`, `SHA256SUMS`
- `ABLATION.md` — rewritten (stale R1/R2-port section replaced; corrected
  composition schema; per-mechanism attribution; re-verified bars)

Nothing committed (per task instructions). No binaries or `.zagd` files in
the tree; build artifacts live in `~/workspace/r3fix_work/`.
