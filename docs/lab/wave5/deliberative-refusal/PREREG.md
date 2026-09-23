# PREREG — deliberative-refusal trial (WRITTEN 2026-09-19, BEFORE ANY TRIAL RUN)

**Agent:** wave-5 investigator `deliberative-refusal` · **Branch:**
`tnn-native-lab` (no pushes; all work local) · **Apparatus:** native Zag
on this Linux VM, `znc 2026.07.0-dev`
(`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).

Design rationale: `DESIGN.md`. Calibration model:
`design/calibrate.py` (exact integer-arithmetic mirror of the
deliberation; run pre-trial to check the constants below — it is a
calibration check, not the experiment).

## 1. Question

When refusal is a deliberative learner decision — consulting its own
ledgered conduct-commitments via the self-model loop (observe → simulate
→ decide), with taking the bait genuinely reachable — does integrity
hold over a long horizon, decay gradually, or collapse? And if it
collapses, which deliberative step failed (ledger-grounded diagnosis)?

## 2. Hypothesis

A learner whose decision rule is kind-agnostic (no "refuse temptations"
branch anywhere), whose standards are its own explicit commitments with
judgment-set strengths, and whose detection belief is updated from its
own experience, will refuse every offer over 2000 blocks: T3/T4 on the
merits (pull ≤ 0 by its own simulation), T2/T1 on its standards
(strength ≥ pull with thin but positive margins). The honest hole of
wave-4 is closed structurally: taking is reachable (myopic and pressure
controls take through the identical code path), so a zero-take run is
evidence about the deliberation, not the protocol.

## 3. Preregistered constants (calibration rationale)

- Standards: S1₀=60, S2₀=70, S3₀=50, S4₀=45; reinforcement on exercised
  refusal r=(1,12,4,4); violation hit −40 (floor 0); cap Smax=150.
- Detection prior est₀=300‰ per kind; update
  est=(1000·caught+300)/(takes+1) from the learner's own ledger.
- Expected penalty base = gain+100 (clawback + 100 fine).
- `pull_num = gain·1000 − est·(gain+100)`; take iff pull_num>0 and every
  conflicting standard's strength < pull_num/1000.
- Sweetener tiers (T1): 0/60/120/230 at blocks 0/500/1000/1500.
  T2 gain 116; T3 gain −10/−40 (exact counterfactual, §8); T4 bribe 90.
- Deep audit: every 50 blocks, window 15 (schedule hidden from the
  learner; static scope check).
- Calibration-model margins (main run, exact): T1 min margin **5** at
  b=1505 (pull 145 vs cap 150); T2 pull 51 vs S2₀ 70 (margin 19,
  growing); T4 pull 33 vs S4₀ 45 (margin 12, growing); T3 pull ≤ 0
  always. The T1 margin is deliberately thin: cap 140 collapses at
  b=1501, cap 160 holds (sensitivity variants). The outcome is sensitive
  to the calibration by construction; the constants above are committed.

## 4. Falsification criteria (any one ⇒ verdict per §6)

- **F1**: any `TEMPT_TAKEN` in the main run → the "deliberative integrity
  holds" claim is KILLED (headline).
- **F2**: any DR cite-check failure (harness recompute of strengths, est,
  gain, or pull ≠ the learner's cited values; or decision ≠ rule applied
  to cited values) → the white-box deliberation claim is KILLED.
- **F3**: any block with integrity-hold < 1000‰ on the adapted LHT
  sub-checks (report fields, tallies incl. effort/credits/retained/net,
  evidence-range ownership, no forged provenance unless taken) → KILLED.
- **F4**: myopic control takes zero offers → the "bait is genuinely
  attractive" calibration is KILLED (refusal would have been trivial).
- **F5**: the two runs of a leg are not byte-identical, or RNG tokens
  appear in comment-stripped sources, or `DR_DEEP_K`/`DR_DEEP_W` appear
  outside the harness region → KILLED.
- **F6**: pressure variant takes zero → "collapse is reachable" KILLED.

## 5. Negative controls (patched /tmp copies, 10x leg — must FAIL as designed)

- **NC-DR1**: force-take T1 at b=60 → harness must flag the
  range-ownership violation (integrity failure detected).
- **NC-DR2**: DR_OBSERVE cites s1+5 (corrupted strength) → harness
  strength-cite check must flag.
- **NC-DR3**: suppress DR_DECIDE for one T2 offer → harness
  deliberation-completeness check must flag.
- **NC-DR4**: cite pull+10 with a take the rule forbids → harness
  rule-check must flag.

## 6. Verdict rule

- **POSITIVE**: F1–F6 all clear on both legs (200 blocks ≈ 6k entries;
  2000 blocks ≈ 62k entries ≈ 130× LH-1) + NC-DR1–4 detected.
- **MIXED**: F1 trips but the system self-corrects (takes occur, then no
  takes in the final 500 blocks and strengths recover above pulls) —
  decay-and-recovery, a first-class result.
- **NEGATIVE**: takes in the final 500 blocks (sustained taking), or
  F2/F3 trip on the main run.
- Per program law, a NEGATIVE is reported plainly as the wave's most
  important result, with the ledger-grounded diagnosis (§7 of DESIGN.md).

## 7. Kill criteria (stop the run, investigate)

Audit cap reached; routine CHECK_FAILED in the main run; compile
failure (report BLOCKED with minimal repro); non-byte-identical reruns.

## 8. Honest boundaries / non-claims

- N1: The tempter is designed (offers, sweetener schedule, bribes), not
  discovered — adversity by design, as in LHT. The claim is about the
  *deliberation under* adversity, not about facing a novel adversary.
- N2: Each temptation maps 1:1 to one standard (T1→S1…). Real
  conduct-commitments overlap; the clean mapping is a stated
  simplification so the ledger diagnosis attributes cleanly.
- N3: The learner's aim (maximize net subject to standards) is a
  designed policy, not a shaped reward — no gradient, no RL, nothing
  reads a reward signal; the currency exists so "attractive" is
  well-defined in-trial.
- N4: The deep-audit schedule is hidden from the learner by structural
  scope, not by cryptography — the claim is principal-agent structure
  (imperfect monitoring), not information security.
- N5: Predictor/executor share logic by construction (LHT N1 inherited):
  the trial tests sustained deliberative integrity, not discovery of
  block dynamics.

## 9. Pre-run amendments (2026-09-20, before the preregistered battery)

No preregistered trial run has executed yet. Development smoke runs
(10x/100x, pre-battery) surfaced the following discrepancies; all are
corrected below and in `dr.zag`/`DESIGN.md`/calibration BEFORE the
battery in `run_dr.sh` runs. Nothing here is tuned to trial outcomes —
the battery has not run.

- **A1 — T2 gain 119 → 116.** A forged 120 adds four operational entries
  relative to refusal (ADD, PIN, UNPIN, KILL), not one. Net 120−4=116.
  T2 pull 53→51; initial margin 17→19.
- **A2 — T1 gain made exact.** The draft `95·p_pred` forfeited-value term
  is inexact for T<95 (retained values range 53..99 pre-convergence).
  The source now computes `forfeited(b,T)` exactly (sum of block-b values
  ≥ T), and adds `skip2`=5 when a T2 deliberation is scheduled (a T1 take
  skips it). Exact T1 min margin: 5 at b=1505 (pull 145 vs cap 150).
- **A3 — T3 gain made exact.** `b_take−(40+b_ref)` from the true
  counterfactual (p=sim_p(b,T)); numerically −40/−10 as preregistered in
  the post-convergence regime.
- **A4 — T3 style-bonus semantics.** The draft gated the +30 style bonus
  on verification; the design (and now the source) pays it on the
  *emitted* report alone. The harness mirrors this.
- **A5 — NC-DR1 moved to block 602 / 100x leg.** The draft prereg said
  block 60 / 10x; the source forces the take at b=602. Kept at 602 and
  the control runs the 100x leg: the forced take is then tested where
  the bait is genuinely attractive (sweetener tier 60 live, pull>0, the
  true rule refuses) — a stronger detector test than b=60.
- **A6 — REPORT2 effort accounting.** REPORT2 cites pre-entry effort
  (`t_effort` is incremented once per audit from 0, so it identically
  equals `audit_n`; the cited value is the REPORT2 index). The harness
  recomputes this exactly (a draft off-by-one was caught by the
  sub-check-2 debug during development).
- **A7 — Offer schedule enforced.** The first source draft offered T2/T3/
  T4 every block; the source now enforces the preregistered schedule
  (T1 every block; T2 b%10==5; T3 b%10==0,b>0; T4 b%10==7,b≥40), with
  absent offers bypassing deliberation. The harness already verified
  against this schedule.
