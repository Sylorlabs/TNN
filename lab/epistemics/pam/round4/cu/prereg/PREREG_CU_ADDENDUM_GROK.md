# PREREG_CU_ADDENDUM_GROK — Grok PART B follow-up (second addendum)

**Source:** `~/workspace/tnn-lab/pam/round4/hypotheses/grok_pam_r4.md` PART B
("CONSCIOUS vs UNCONSCIOUS PAM"), committed as `8b6adcd1`.
**Status:** committed BEFORE any grok-driven measurement is run. The c/u
battery, its evidence, and VERDICT_CU.md are already frozen; this addendum
adds new measurements only.

## G0. Reconciliation principle (binding)

`PREREG_CU.md` + Correction C1 + Correction C2 already froze the CU decision
cutoffs (KB-CU-WORTH, KB-CU-JUDG, KB-CU-K8, KB-CU-ATTACKWIN, KB-CU-REPLAY,
KB-CU-LINEAR, KB-CU-INTROFLOOR, KB-CU-K6, KB-CU-K7). Those numbers are NOT
refit after seeing data. Grok's B.6 decision rule and its cutoffs (+10 pts,
2×, 128 B, 90%, second-half ≥5, 80% / 1.3×) are adopted as RECONCILIATION
INPUT: the new measurements are evaluated against grok's P-CON / P-UNC /
P-HYB criteria and reported, but where grok's cutoffs conflict with frozen
CU bars, the frozen CU bars stand for the program decision. Adopted below
are grok's probe DESIGNS and analyses: the ablation probe (B.3),
second-half-G (B.4), the count-only control (B.2), and the trigger-only
hybrid arm (B.4–B.6).

## G1. Architecture mapping (grok construct → CU instrument)

| Grok PART B | CU instrument | Note |
|---|---|---|
| DecRec (claim_id, rule_id, evidence_ids) | REC line: `lt\|id\|K\|outcome\|fired\|blocked\|` + 8 evidence fields | text form; same causal content |
| Cross-decision scanner (B.2 reader) | NONE | CU battery has no reader; both variants caught 100/100 attacks via the shared frozen core. Per grok B.2, consciousness without a reader is write amplification — reported as such, not hidden. |
| Laundering subset (GEN→EXT relabel) | 40 LAU rows (conf/prov-laundered, bar-failing) | all rejected by both variants in the frozen battery |
| Frozen wrong set (12 TMB-5 + 9 CC1) | 12 W rows + 9 CC1 pairs (18 P member rows) | Correction C2: frozen bar itself admits P5-2/P6-2 individually |
| Per-producer admit/reject counts | Per-class (C/W/P/A×atk) admit/reject counts | rows carry no producer field; class is the available grouping |
| Trigger-only (veto, divergence, promotion, type≠FACT, scanner hit, unstaked/provisional) | Veto → rejection (outcome 0); all other triggers have no CU-instrument counterpart → mapped to none | hybrid = RECs on rejections only (320 rows), outcome byte on admits |
| DecRec budget 128 B/admission | measured 64.23 B/admission (frozen) | exhibit excluded in both designs |

## G2. K1/K2 reconciliation

Grok B.6 rule 1 kills an arm that "false-admits on the frozen wrong set."
Literal application would kill both arms for P5-2/P6-2 — but Correction C2
established those two pass the FROZEN M1 BAR itself (conf=718≥705,
mrgF=6600≥3588); the instruments implement the bar correctly. Reconciled
K1 (binding): an arm is dead iff its wrong-set disposition DIFFERS FROM
THE FROZEN BAR'S OWN (W 0/12, P exactly P5-2/P6-2) — i.e. frozen
KB-CU-JUDG. Judgment delta between arms must be 0. K2: byte-identical
reruns required of all three arms (c, u, h). The hybrid arm uses the same
frozen core; only REC emission is trigger-gated.

## G3. Ablation probe (B.3) — operationalization (binding)

**Probe set** (130 rows): all 100 frozen-attack-tape rows (A-*) + all 30
frozen-wrong-set rows (12 W + 18 P). The "scanner marked mismatch-relevant"
subset is EMPTY (no scanner in CU instruments — documented, not silently
dropped). Attack-tape admissions in the frozen battery: 0 (all 100
rejected); wrong-set admissions: P5-2, P6-2.

**Cited evidence ids** (in id order = REC field order): conf, mrgF, strong,
agree, prov, prov_ok, decl_ok, auth — the 8 evidence fields of each
conscious REC.

**Removal semantics** (binding): re-run the pure gate (§2 mirror, already
verified 0 mismatches on all 1,232 rows) with the field ABSENT, fail-closed:
a check consuming an absent field cannot pass. Implemented as: conf→0,
mrgF→0, prov→2 (breaks 1≥prov), prov_ok→0, decl_ok→0, auth→2 (breaks 1≥auth),
strong→0, agree→0 (no consuming check; expect no flip). A cited id is
NECESSARY iff the decision bit flips vs the recorded outcome.

**Faults.** (F1) cited id not necessary → unnecessary-citation fault.
(F2) a gate input whose removal flips the bit but which is NOT cited →
omission fault (structurally impossible here — REC cites the full input
vector — but checked, not assumed).

**Necessity agreement** (binding): zero-fault admits-in-probe /
admits-in-probe. Denominator = admitted rows in the probe set
(P5-2, P6-2, plus any attack-tape admits — 0 in the frozen battery).
Grok reconciliation bar: ≥90%. Rejected probe rows are fault-scanned and
reported, but excluded from the agreement ratio per grok's definition
(their fail-closed flip-tests are degenerate: removing any input from an
already-rejected row cannot flip it — documented here, not discovered
later).

**Secondary diagnostic** (preregistered, not part of agreement): on the 128
rejected probe rows, fail-OPEN removal (conf→99999, mrgF→999999, prov→0,
prov_ok→1, decl_ok→1, auth→0, strong/agree→1 — missing check passes).
The flipping set must equal the failing input(s) of the REC's cited
blocked_by rule. Report match rate: this verifies the record's causal
claim (blocked_by + the corrupted field on attack rows) independently of
the agreement ratio.

**No-modulus rule honored:** probe covers the full 130-row set, no sampling.

## G4. Laundering-G and count-only control (B.2, B.4)

**Laundering subset:** 40 LAU rows in tape order. H1 = LAU-0..LAU-19,
H2 = LAU-20..LAU-39. catch = rejected/40 (an attack is "caught" iff the
gate rejects it). G_full = catch_con − catch_unc in absolute POINTS;
G_H1, G_H2 likewise. Computed from frozen c_run1/u_run1 evidence (no new
runs needed) AND re-verified against the new h runs' shared core.

**Count-only control** (fair unconscious control, B.2): scorer-side replay
of u_run1.txt in tape order maintaining per-class admit/reject counts
(C, W, P, A-LAU, A-FORK, A-AUTH). The control's decisions are the
unconscious decisions (counts do not feed the frozen gate — structural,
verified by the instrument source). Report catch_control on LAU and
G_control = catch_con − catch_control. If G is reproduced by the control,
the gain was the counter, not the record (B.2).

## G5. Hybrid arm (trigger-only, B.4–B.6)

New instrument mode `h` in cu_pam.zag (NEW code, frozen c/u arms
untouched): identical frozen core; REC emitted iff outcome==0 (rejection =
veto analog, 320 rows); admits emit the outcome byte only. Summary labels
mode=hybrid. Build with the pinned toolchain `--no-zagd`; run 2× on the
frozen tape; require byte-identical reruns (K2). Metrics: cycles_h,
rec_bytes_h, entries_h (=320 expected), growth not applicable (admits
silent). Query diagnostic: run cu_query on h_run1 with cu_questions.txt;
report primary (20 admitted-C questions → expect NO_RECORD) and diagnostic
(5 W questions → expect answered) scores.

P-HYB evaluation (grok criteria, reconciliation input): hybrid captures
≥80% of the full-conscious laundering delta at ≤1.3× unconscious cycles.
Note preregistered: if the full-conscious delta is 0, the 80% clause is
degenerate (0/0) and the evaluation rests on the cost clause — reported
explicitly, not finessed.

## G6. Decision analysis (after measurement)

Evaluate and report, as reconciliation input (not program decision):
- **P-CON** (grok): G_full ≥ +10 pts AND cycles ≤ 2× AND bytes ≤ 128 B AND
  agreement ≥ 90% AND second-half G ≥ 5 AND count-control does not
  reproduce G.
- **P-UNC** (grok): G_full < 5 pts AND reconciled K1 green AND
  (agreement < 90% OR count-control reproduces the gain).
- **P-HYB** (grok): per G5.
Then state the ADOPTED DEFAULT, which follows the frozen CU bars
(KB-CU-WORTH already PASS → conscious worth its cost), QUALIFIED by
grok's threat-model dependence:
- **Benign model:** worth rests on introspection alone; report grok-strict
  necessity agreement alongside frozen citation-match quality (1.00).
- **Non-adaptive adversary:** report G (full + halves); with no reader in
  the instruments, records are write amplification for catch (B.2).
- **Adaptive adversary (reads rule ids):** report second-half G; note the
  ledger-as-spec surface (fired rule ids are deliberation-visible).

## G7. What this addendum does NOT change

No frozen bar, cutoff, threshold, or c/u instrument semantic is altered.
The hybrid mode is new code, not a modification of the frozen arms. No
frozen number is refit: the c/u evidence was scored before this addendum;
the ablation probe, G-halves, count-control, and hybrid runs are new,
independent measurements. DecRecs remain non-content (B.5 regress guard):
not eligible as EXT evidence, corroboration, or gap fillers.
