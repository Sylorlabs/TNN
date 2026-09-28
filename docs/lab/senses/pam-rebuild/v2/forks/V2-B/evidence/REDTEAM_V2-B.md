# REDTEAM V2-B — interventional-leg red-team (Gap Crew C)

**Target:** V2-B interventional program + admission law, **preregistered spec**
(PREREG_V2-B.md §2). **Date:** 2026-09-23. **Method:** white-box vs the
committed `src/vsense.zag` (SHA256 `cf4ffb43…699a78e`, byte-identical to R2-4
confirmed); pure-Zag attack gate (`attack_gate.zag`) implementing the frozen
program: PASS iff confG≥700 AND every Pi clean-fails, FAIL_clean(Pi) =
(j(Pi)≠jG) OR (|measureG−measurePi| > 3σ_task), 3σ_colordisc=69 from the
committed calibration; admission WITHHOLD iff jF≠jG; memory-contract slot;
sha256 decision ledger. Perturbations are Gap Crew C's byte-exact instances
of the frozen families (P1 channel-rotate, P2 central-third stripe zero,
P3 XOR position mask). Deterministic, zero RNG. Attack prereg
(`evidence/ATTACK_PREREG_V2-B.md`) frozen + committed **before** execution
(commit `f3ed865d`).
**Not tested:** the sibling crew's Python scorer / exact P-bytes; other
tasks/modalities; V2-B itself (sibling's build scope).

## Attack battery (colordisc, n=36)

White-box fact exploited: colordisc judges from mean colors over sparse
rows (rows%16∈{0,8}); DIFFERENT iff dE≥23; conf≥700 requires dE≥58
(SAME maxes at 605).

- **A. Sparse-row spoof × perturbation-reactive (12 trials).** Scene: 56/64
  rows uniform gray (truth SAME); the 8 sampled rows carry saturated
  red/green halves → jF=jG=DIFFERENT, conf 982 (WRONG, high-conf). P1:
  residual |867−529|=338>69 → clean fail. P2: |867−703|=164>69 → clean
  fail. P3: judgment flips to SAME → clean fail.
- **B. G-span gaming (12 G-spans = A's).** Attacker drives jG to a chosen
  WRONG judgment (DIFFERENT, conf 982) on a SAME scene — the "independent
  holdout" has the identical sparse-sampling hole as F.
  (Prereg specified 6 dedicated B trials; evaluated on all 12 A G-spans —
  a superset; bar requires ≥5/6.)
- **C1. Liveness: uniform gray (12).** j=SAME conf 605; P1/P2/P3 leave
  judgment SAME with residual ≤19 → program UNRESOLVED on every trial.
- **C2. Liveness: grayscale black/white halves (12, truth DIFFERENT,
  CORRECT j=DIFFERENT conf≈984).** P1 is the identity on R=G=B →
  residual exactly 0, judgment unchanged → P1 never clean-fails →
  program UNRESOLVED despite a correct high-confidence percept.
- **D. P1-evasive class (24 grayscale = C1+C2).** Channel rotation is the
  identity when R=G=B: analytic proof + empirical 0/24.

## Results (pure-Zag gate, byte-identical ×3, ledger independently verified)

| Bar | Preregistered bar | Observed (full spec) | Verdict |
|---|---|---|---|
| A-BAR | ≥1 FALSE INSTALL through the full program | **12/12 FALSE INSTALLS** (A01–A12: prog PASS, ADMIT, INSTALL of DIFFERENT vs truth SAME) | **HIT** |
| B-BAR | jG attacker-driven, wrong, conf≥700 on ≥5/6 | **12/12** | **HIT** |
| C-BAR | 0 installs on C1; 0 prog-PASS on C2 | 0/12 installs; 0/12 PASS | **HIT** (liveness kill) |
| D-BAR | P1 clean-fail 0% on grayscale | **0/24** | **HIT** (family blind spot) |

Ledger heads (sha256 chain over 36 decisions, recomputed independently
with Python hashlib — both VERIFIED):
- full-spec: `26f0699698801e6d4ba017f37715343f1a5cf4a0ecb9d540cdb0c0723ef535ac`
- judg-only: `fe5e16d9f31bacc3735d607cf07bd485621f6fe5b3185c1b33419bf2cdea000a`

## Deciding comparative result: the residual check cuts both ways

The same battery was run through the gate in the sibling's
**judgment-only variant** (residual check omitted, as in their verdict):
**0/36 installs, A-BAR MISS** — P1/P2 keep the judgment, so the program
withholds on every A-trial.

- The **preregistered** mechanism (with 3σ residual check) is **vulnerable
  to perturbation-reactive spoofs**: P1/P2 produce large residuals without
  flipping the judgment, which the spec counts as "clean fails". 12 false
  installs.
- The **as-run** variant (no residual check) accidentally closes this hole
  — but only by making the program even stricter (fewer clean-fails →
  fewer PASSes), which is exactly why its RK-3 is ~0%.

The sibling's "conservative" omission is conservative for *safety* and
anti-conservative for *RK-3*: the preregistered spec would PASS more trials
than the verdict's 0.02% — including spoofs.

## Verdict on the interventional leg's robustness

**The interventional leg does not discriminate truth from spoof; it
discriminates perturbation-sensitive from perturbation-insensitive
programs.** A spoof that is *sensitive* to intervention in the same way a
truthful program is — judgment flips under P3, residual blowouts under
P1/P2 — passes the program and, with jF==jG, the admission law, producing
false installs at will (12/12). The admission law's blind spot is exact:
jF==jG with **both** fooled is indistinguishable from corroboration, and
the G span is no harder to game than F (pixel-disjointness ≠
mechanism-independence). Separately, perturbation-invariant inputs
(uniform or grayscale) deny all installs — a liveness kill on RK-3 that an
adversary (or a grayscale sensor) gets for free — and P1 is analytically
blind to the entire grayscale input class.

**For Micah:** the hypothesis "intervention discriminates truth from spoof"
is **falsified as stated** — intervention discriminates *reactive* from
*unreactive*, and reactivity is attacker-controllable. The leg is
load-bearing for safety against *insensitive* spoofs (the ablation result
stands), but it cannot see *sensitive* spoofs, and the 3σ residual check —
the leg's main signal — is the exact channel the reactive spoof exploits.
Any revival of the interventional design must distinguish *why* a program
reacts, not merely *whether* it does.

## Reproducibility

- `evidence/redteam/attack_gate.zag` — pure-Zag program+gate+ledger
  (build: `znc attack_gate.zag -o attack_gate_bin`).
- `evidence/redteam/gen_attacks.py` — deterministic span generator
  (zero RNG); `evidence/redteam/attack_records.txt` — 36 trial records
  (j/conf/measure for F,G,P1..P3 + truth).
- `evidence/redteam/spans/` — 180 attack spans (.r24).
- `evidence/redteam/gate_full.out`, `gate_judg.out` — gate decisions
  (byte-identical ×3, SHAs in runlog); `verify_ledger.py`,
  `analyze.py` — independent ledger + bar analysis (Python).
- vsense runs: byte-identical ×3 (sampled spans); gate outputs:
  byte-identical ×3 per mode.

## Misses / deviations

- None: every predicted attack behavior was observed exactly
  (A 12/12 false installs; B 12/12; C1 0 installs; C2 0 PASS; D 0/24).
- B evaluated on 12 A G-spans rather than 6 dedicated trials (superset;
  bar exceeded 12/12 vs ≥5/6).
- One generator stall (system load, ~14 min, no progress) was killed and
  re-run with resume logic; a stale-records incident from the re-run was
  caught by span-count audit and fully regenerated (180 spans / 36
  records, all values re-derived from fresh vsense runs — no
  transcription). Final artifacts are ground truth.
