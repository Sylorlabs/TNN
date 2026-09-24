# VERDICT_RT_H.md — RT-H Class-H battery verdict (2026-09-24)

PAM Round-2 swarm, red-team crew RT-H. Grok's objection (objector commit
`772d6954`, `OBJECTOR_GROK47.md`): "pairwise death does not locate the
conjunction" — the D1 battery measured pairwise behavior but never one
artifact occupying all four blind quadrants at once. This battery builds
Grok's Class-H conjunction and fires it at the committed D1 hybrid
(`81dcfaf1`), unmodified.

Frozen prereg: `PREREG_RT_H.md` (committed alone, `354186d4`). Pure Zag,
zero RNG, three byte-identical runs with SHA comparison.

## Measured result (three byte-identical runs, SHA in SHASUMS_RT_H.txt)

```
RTHBAT rth_n=240 b_n=120 ledger_final=732243896
RTH-P7 hon_install=0 atk_install=0 b_install=120
RTH-P10 hon_inv=0 atk_inv=0
RTH-HYB h_inst=0 h_prov=120 h_with=0 h_uncov=0 a_inst=0 a_prov=120 a_with=0 a_uncov=0
RTH-AUDIT n=240 agree=240 shared1=240 f8c_n=1 f8c_h=0 verdict=SHARED_SOURCE
RTH-PROBE-HANDOFF wire1_n=120 wire1_install=120 wire1_f8c3=1 wire2_n=120 wire2_admit=120
RTH-PROBE-SYNRES fire_atk=120 fire_hon=120 ref_indep_atk=120 ref_indep_hon=120
RTH-KILL admission_num=120 KILL_H=1 KILL_AUDIT=1
```

## Primary kill bar — FIRED (hybrid DIES)

- Class-H install rate (committed + provisional + uncovered, prereg §4):
  **ADMISSION_H = 120/120** (a_inst=0, a_prov=120, a_uncov=0). Kill bar
  (≥97/120) fires.
- Honest loss: h_with=0 → **0/120**, well under the 15% ceiling. The battery
  does not win by breaking honest traffic: honest controls are admitted as
  PROVISIONAL at 120/120, exactly as the prereg predicted.
- Solo rates on this class (frozen, §4): solo P7 admission 0/120
  (p7_atk_install=0), solo P10 admission 0/120 (p10_atk_inv=0 — P10 is never
  even invoked). The conjunction is what kills: P7 withholds on all 120
  (deviant gain arm, |obs−lawful|=997>tau on meas≥6000), P10 has no cover
  (COL-4/PTC-4), and the commit rule routes the abstention to PROVISIONAL —
  which the prereg counts as admission, so the carve-out cannot hide the miss.
- The prediction in the frozen prereg matched the measurement on every
  single counter (120/120 provisional on H and N, 0 installs, 0 withholds).

## Handoff-inversion probe (POLICY PROBE — committed D1's audit is
observational and routes nothing; this tests grok's assumed policy)

- Wire 1 (audit-detect → P7-only fallback, committed Class-B fixtures):
  P7 installs **120/120**; the committed audit's class-gated f8c_3 flag fires
  (wire1_f8c3=1). Grok's assumed handoff policy installs the attack on every
  trial it is handed.
- Wire 2 (audit-silent → trust fusion, Class H): the audit is silent on all
  120 (its detection flags are class-gated to 1/2 and never fire on H), so the
  trust-fusion policy admits **120/120**.
- This probe does not independently kill the committed hybrid (per the frozen
  prereg, it adjudicates grok's policy critique): on both wires the assumed
  policy admits the attack at 100%.

## Synthetic-residual audit probe

- Committed audit: verdict SHARED_SOURCE is a constant — it fires on
  **120/120 attacks AND 120/120 honest controls** (agree=240/240,
  shared1=240/240). Zero discrimination; honest false-fire 120/120 ≫ 15% →
  **KILL_AUDIT=1** (audit component dies its own preregistered bar).
- Root cause (structural, preregistered §6): the audit derives path B by
  `reproj_c/m` from the SAME (c,m) record and compares the reprojection with
  itself — `shared` is tautologically true. It has no input channel for an
  independent path-B record, so grok's synthetic-residual distinction is
  unimplementable in the committed audit.
- Reference two-record check (labeled; NOT the hybrid): given an independent
  path-B record carrying the documented deterministic synthetic noise, a
  structural reprojection check reports INDEPENDENT on **240/240** — attacks
  and honest alike. Even a "fixed" two-record audit cannot separate the
  synthetic-residual attack from honest noisy traffic on the reprojection
  feature: grok's bind confirmed at the feature level.

## Verdict on real vs assumed complementarity

The committed D1 hybrid's P7/P10 complementarity is **assumed, not real** —
on the Class-H conjunction it is zero on both halves simultaneously:

- P7 alone: 0/120 admission (withholds on the deviant gain arm — correct
  abstention, wrong routing: PROVISIONAL instead of DROP).
- P10 alone: 0/120 admission (never invoked — no TMB-5 cover, and its
  invocation rule requires d7==1, which the abstention never produces).
- Hybrid: 120/120 admission via the provisional carve-out. Each half's
  failure is invisible to the other: the abstention that should have been a
  catch becomes the admission path, and the audit that should have seen the
  conjunction is a constant function on the shared record.

Grok's objection is sustained on the primary claim: one artifact occupying
all four blind quadrants kills the hybrid at 120/120 with 0% honest loss,
where the D1 battery's pairwise legs measured 121 committed falses. The
provisional carve-out — designed as a safety valve for complexity-abstaining
honest traffic — is the exact channel the conjunction exploits.

## Reproducibility

- `gen_rth.py` (no `random` import; deterministic sweeps) →
  `rth_fixtures.txt` (240 records).
- `assemble_rth.py` extracts 17 hybrid functions byte-identically from the
  committed `d1battery.zag` (verified SHA) and concatenates `rth_new.zag` →
  `rth_battery.zag`. `verify_rth_diff.py` → `hybrid_src_diff.txt`
  (ALL 17 IDENTICAL).
- Pinned toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`;
  `R33_NATIVE_IO_V1.zag` (verified SHA) colocated for the `@import`.
- Runs: `./rth_bin rth_fixtures.txt <committed d1_adv_fixtures.txt>` ×3 →
  byte-identical stdout; SHAs in `SHASUMS_RT_H.txt`.
- Not committed: `rth_bin`, `.zagd*` / `.zag-cache/` (build artifacts).
