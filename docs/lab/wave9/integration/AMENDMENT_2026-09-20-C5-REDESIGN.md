# Dated Amendment 2026-09-20 — C5 redesign: strict verdict gating as the default compose path

**Authority:** Micah's overnight-agentic authorization 2026-09-20; flagged for his retroactive
review in the morning. Required by `AMENDMENT_2026-09-20-BATTERY-REPAIR.md` §1
("no re-repair of a fired control without a new dated amendment").
**Status:** committed BEFORE implementation/re-run (pre-registration).

## §1. The finding

The repaired S10 battery (commit `5aa2fb13`) is VALID — six controls ALIVE — but C5 returned
**LEAKAGE**, a real architectural property, not an instrument failure: O4's composition path does
not enforce O2's verdict partitions (CONFIRMED / OPEN / REFUTED).

Operational-leakage analysis (`C5_OPERATIONAL_LEAKAGE_ANALYSIS.md`, independent scratch driver,
fidelity validated against committed telemetry): in the **intact** repaired-S10 run
(`c5_arm=0`), of **1,024** successful COMPOSE entries, **9 (0.9%)** had a backing claim
(`claim_cid` in `a1`) whose O2 verdict was **REFUTED at compose time** (3 each in DC-2/3/4, 0 in
DC-5). **All 9 were APPLYed** (served as live behavior) in the same episode. **Zero** were used
as CONSOLIDATE backing. Mechanism: a claim on the anchor slot is refuted in episode N's
section 2; episode N+1's compose still annotates it as backing, because the compose path never
reads the verdict. Qualifier (honest): `claim_cid` is an audit annotation, not a composer input —
this proves partition non-enforcement at the seam, not that refuted content shaped the vectors.

Architectural context (read from the sources, not assumed):

- O2's REFUTE is **terminal**: `impl/o2_eliminate.zag:101` — `if(old==O2_V_REFUTED){return O2_OK;}
  // terminal: elimination is final`. The architecture already chose absolute killing.
- Consolidation candidacy is **CONFIRMED-only**: `impl/loop.zag:191-193` (L2: `vv==4` →
  `seam3_consolidate`). Verdict-partition intent exists at belief-fixation.
- **Apply follows compose unconditionally**: `impl/loop.zag:140-144` — every `rc==0` compose is
  APPLYed. Compose-time is therefore the last checkable choke point before behavior.

## §2. The debate and its resolution

A three-position council debated (briefs committed alongside this amendment):
`position_a_verdict_brief.md` (strict-by-default), `position_b_verdict_brief.md`
(verdict-aware composition + quarantine), `position_c_verdict_brief.md` (red team).

**Position A WINS.** Position B is rejected: strictly more complex while preventing less —
EXPLAIN-tagged composites are still served, multi-hop tag propagation is uncomputable in the
current seam signature (`o4_compose` takes `need_id`, no input list — B's own admission),
permanent taint (one wrong REFUTE poisons all downstream composites forever), and a much
larger trusted surface. Position C (red team) is rejected on substance; its pressure improved
this amendment. Rulings:

- (a) *The re-scope was never preregistered.* Answered: the verdict-partition re-scope went
  through the dated-amendment process with Micah's authorization. That process IS the
  preregistration mechanism; "never in the original prereg" describes every amendment.
- (b) *Composing ≠ believing; strict kills reductio / error explanation / steelman / pedagogy.*
  Answered: all four operate on **OPEN** claims pre-verdict or on **refutation evidence**
  (CONFIRMED). A's gate blocks only post-terminal-REFUTE composition — re-litigation, which
  the architecture's terminal REFUTE already forbids. Counterfactuals ("suppose H") go through
  O2's hypothesis path as new claims (new `cid`; terminality is per-claim).
  Explaining why H is wrong = composing the refutation (the evidence that killed it), which the
  gate permits; the verdict record + refutation evidence IS the account of the kill.
- (c) *Enforcement belongs at consolidation, not composition.* Answered: it is already there
  (CONFIRMED-only candidacy) and it is **insufficient** — the 9 operational leaks were
  applied/served, never consolidated. The gap is at compose/apply, and O3/O5 have no verdict
  plumbing to extend (C conceded this gap).
- (d) *The ledger already detects silent inclusion.* Answered: wave-6 attribution law —
  ledgers/checkers prove, they do not cause. Detection ≠ prevention; C5 is a prevention bar.
- (e) C's falsification trigger is **partially met**: 9 ledger-recorded REFUTED-backed
  composites in intact, unforced runs, all applied as live behavior. C's narrower trigger
  (reconfirmation / commit while REFUTED) is already prevented by terminal REFUTE +
  CONFIRMED-only consolidation; the serve-layer harm is what this amendment closes.

## §3. The design (Position A, as amended by the coordinator)

The strict verdict check becomes the **DEFAULT** in `seam4_compose`: every compose through the
seam refuses when the backing claim (`claim_cid > 0`) resolves to `O2_V_REFUTED` at compose time
via `o2_verdict`. No cfg flag; no exceptions in the default path.

- **Refusal semantics:** ledgered refusal (`LG_O4`/`LG_OP_COMPOSE`, `SEAM_REFUSED_PARTITION`,
  `need_id`, `claim_cid`), `trace.* = -1`, refusal return code. The caller treats it as abstain —
  refusals feed L1 (abstain → hypothesis), they do not starve it.
- **Coverage statement (exact, binding):** the gate checks the anchor's backing claim only.
  `claim_cid <= 0` (claim-less composes): permitted and ledgered; the checker verifies these are
  genuinely claim-less. Non-anchor input traces pulled by `o4_compose`: **not checked** — known
  residual, §6.1.
- **Flag changes:** `c5_strict` retired (folded into the default); `c5_arm` retained for
  test-arm construction only.
- **Why compose-time:** apply follows compose unconditionally; consolidation is already
  CONFIRMED-gated; compose-time is the last checkable choke point before behavior (§1).

## §4. The C5 bar (re-run, binding)

- Killed-only arm (`c5_arm=3`, default path): **0** successful composites. ≥1 → LEAKAGE → FAIL.
- Accepted-only (arm 1) and candidate-only (arm 2): **≥1** composite each — the gate must be
  discriminating, not destructive.
- Positive controls: synthetic REFUTED-backed compose via the default path refused 100% of runs
  (`c5_bite` shape); accepted/candidate arms flow.
- Calibration (battery-amendment §11 precedent): the instrument must fire on its broken variant
  and stay silent on the intact system, else the trial is re-blocked, not passed.

## §5. Capability non-regression (binding)

C2 ALIVE; all six stage gates PASS; P1–P10 clear; C7 repaired metric holds (897→897, no
collapse); C1/C3/C4/C6 ALIVE. `composites_ok` must not fall **>5%** vs the repaired-S10 intact
run on identical stage budgets (adopted from A's falsification criterion #2 as a bar).
**A fix that kills composition to save C5 is a failure: report FAIL, do not pass.**

## §6. Known limitations and tensions (not buried)

1. **Non-anchor input traces unchecked** (residual). Future probe: input-trace verdict audit
   once the seam can list compose inputs.
2. **O2-error amplification.** Terminal REFUTE + strict compose makes a wrongly-REFUTED claim's
   content permanently unusable — no appeal path exists. This is the architecture's terminal
   REFUTE made consistent, not a cost introduced by this gate. The fix is an O2
   appeal/re-adjudication mechanism: an explicitly separate future redesign, out of scope here.
   (Without the gate, O2's verdicts are advisory, which contradicts the architecture.)
3. **Verdict-flap races.** A claim CONFIRMED at scan but REFUTED at compose (or the reverse)
   yields refusal/abstain; the ledger records the verdict read at compose time, so flaps are
   visible in audit. Deterministic given ledger state.

## §7. Structural guard (new build-gate entry condition G0b)

Static check at build time: exactly **one** `o4_compose` call site in the source tree, inside
`seam4_compose`. Any direct call elsewhere fails the gate. (Answers "the guarantee is
conventional, not structural" — the seam's sole-entry status becomes a checked invariant.)

## §8. Re-run scope

**Full S10 curriculum** (8,920 episodes, frozen budgets), all seven controls, all ten probes,
defended-channel telemetry, paired byte-identical reruns, zero RNG, independent checker, full
RESULTS doc. Full scope because the gate sits on the compose path used by every stage —
capability non-regression must be demonstrated, not assumed.

## §9. S100 gate (explicit — no ambiguity this time)

S100 un-gates **iff ALL** of: (1) C5 bar §4 holds; (2) positive controls fire; (3) capability
non-regression §5 holds; (4) paired reruns byte-identical; (5) zero RNG in trial sources;
(6) independent checker passes. **Any failure → S100 stays gated**, and no further re-repair
of a fired control without a new dated amendment.

## §10. No-rescue rule

This amendment **strengthens** the guarantee: killed-only composites must be 0, and the intact
system currently fails that bar (9 observed). No bar is softened. The debate record
(A/B/C briefs + operational-leakage analysis) is committed with this amendment.

---
*End of amendment. Next: implementation → calibration → full S10 re-run → independent checker
→ verdict → commit. The re-run must not start before this amendment is committed.*
