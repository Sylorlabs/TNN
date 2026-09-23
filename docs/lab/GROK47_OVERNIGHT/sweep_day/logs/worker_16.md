# worker_16 sweep log — chunk_16 (50 rows), 2026-09-22

Method: SHA sweep for duplicates; mechanical pattern scan of all 28 .zag
files (RNG tokens comment-stripped; ZNC-007 consecutive same-size casts;
ZNC-004 annotated slice-let; `slice as *u8`; chained s.field.subfield);
spot znc compiles + runs of red_trial.zag (RT_FAILURES,0) and sr_trial.zag
(SR_FAILURES,0); md claims verified vs known outcomes; calibrate.py executed
(2000-block self-check); diff integ.zag vs integ_stretch.zag (58 changed
lines — matches STRETCH_NOTES). No grok calls used (native review primary;
no ambiguous judgment required). No commits, no cron, no external sends.

## Verdict summary

- PASS: 44
- dup: 4 (trial/ copies byte-identical to EVIDENCE_RT1_20260920T014020Z/ copies)
- review: 3 (calibrate.py mirror staleness; world.zag dormant LCG; integ_stretch.zag stale comment)
- not evaluable: 0

## Findings (all non-kill)

**F1 — calibrate.py header claim stale.** `wave5/deliberative-refusal/design/calibrate.py`
calls itself "exact integer mirror of dr.zag's deliberation". Ran the 2000-block
self-check: all first-take predictions match the final battery (myopic T2@b=5,
T4@b=47, T1@b=500; pressure T1@b=500; sens140 T1@b=1501). But variant take counts
diverge from TRIAL_RESULTS §1/§3: myopic T2 200/200 (mirror) vs 76/200 (trial);
pressure T1 1484 (mirror) vs 1405 (trial). TRIAL_RESULTS §4's post-battery fix
("take counter moves on every take in every variant") is not reflected in the
mirror, and the mirror's catch model never attenuates. The mirror is a pre-run
design tool; the trial's byte-identical evidence is authoritative. Recommended:
qualify the header or re-mirror the fixed variant logic. Not a verdict threat
(main-leg and first-take claims verified).

**F2 — dormant world LCG.** `wave4/trainer-console/trial/substrate/cl/world.zag`
contains a Park-Miller LCG (`(cl_u32(w,12)*48271)%2147483647`, seeded via
`cw_init(w,seed)`). Status: (a) module header says NEVER imported by the
learner; (b) nothing in the trial imports it (no @import of world.zag anywhere
in trial/); (c) the LCG state is updated each `cw_step` but never READ by any
decision logic — inert; (d) deterministic given seed. Not a violation of
"no randomness in decision paths" (TC PREREG §I's no-RNG gate covers the
runner-grepped trial files, all clean). Caveat: the runner's grep
(`rand|srand|random`) would NOT match the token "rng" — if this module is ever
wired in, the static gate needs widening. Flagged for coordinator awareness.

**F3 — stale comment in integ_stretch.zag.** Line 46:
`const IG_BIG_CAP:i32=20480; // biglog entries (480*4=1920 max)` — comment
copied from integ.zag unscaled; correct value per STRETCH_NOTES.md item #7 is
4800×4=19200 max ≤ 20480 cap. Behavioral non-issue; notes are authoritative.

**F4 (minor, ledger-gating counting convention).** PREREG.md says "6 probes"
Leg B and P6 expects "7 expected adversarial disagreements"; TRIAL_RESULTS.md
adjudicates "exactly the 8 expected" blocked events (B1,B2,B3a,B3b,B4,B5,B6,
C2-stale). Same 8 events, counted as 6 probes (B3a/B3b as one probe) vs 8
claims. All 8 blocked with exact codes, so falsifier F1 ("any escaped cheat =
NEGATIVE") is satisfied at the finer granularity too. Presentation-level only.

## Kill bars — applied mechanically

All falsification criteria were checked against their results docs; none
tripped, so all POSITIVE verdicts stand:

- scaffold-release F1–F6 (P1–P7 all hold incl. amended control sequence) → no kill
- trainer-console F1–F8 (117/117, byte-identical, zero RNG) → no kill
- deliberative-refusal F1–F6 + stop-run criteria (2,595/2,595 refused; NC-DR1–4 detected) → no kill
- differentiation-robustness G/X/D/P falsifiers (G2 hard constraint holds; G3 corrected baseline fires as designed) → no kill
- integ-1 F1–F7 (137/137; F2 non-vacuity: all families bite on synthetics/arm C; F7 calibration fires) → no kill
- ledger-gating F1–F7 (0/60 false-block, 8/8 blocked exact codes, 433/433 checks) → no kill

## Claims vs known outcomes

- scaffold-release POSITIVE 40/40 ↔ program law (RL demoted to red-team;
  scaffold-and-release with learner-initiated SIGNAL_DISCONNECT; learned =
  persists after disconnect). LH-contamination note in PREREG.md §(contamination
  note) transparently quarantines LH-5 quantitative claims. ✓
- trainer-console 117/117 ↔ "overseer authority ... in (117/117)". ✓
- deliberative-refusal 100% over 2,595 temptations 10x+100x ↔ memory. ✓
- integ-1 "truthful (not untested, not hiding)", 8 families, sensor-hole
  finding ↔ memory. sr.zag sha 24a61ed672dd… matches TRIAL_RESULTS's
  24a61ed6… cross-reference. (il_core.zag hash 4b723b65… anchored in
  PREREG_INTEG1.md §1/§3 — file lives in wave4/integrity-ledger/, out of this
  chunk; not verifiable here.)
- differentiation-robustness: wave-5 investigation 10; impostor trap UNKNOWN,
  graded refutation; differentiation unparked/experimental. ✓
- ledger-gating: il_check(24/24 wave-4) gating HSS (wave-3) claim path. ✓
- rl-redteam: deterministic adversary ladder, header-stated "never RNG". ✓
- dr.zag sha 11a972cc99… == TRIAL_RESULTS §7 evidence claim. ✓

## zag scan summary (all 28 files)

- RNG tokens: ZERO anywhere in TNN decision/harness paths (only hit: dormant
  world.zag LCG, F2 above).
- ZNC-007 (consecutive same-size `as []i32/u32/u16` casts): ZERO — no such
  casts anywhere; all indexed tables use []u8 arenas (sanctioned workaround).
- ZNC-004 (annotated slice-let off local struct value): ZERO hits.
- `slice as *u8` (ZNC-002 shape): ZERO — only `_zag_malloc(n) as *u8` and
  `null as *u8` comparisons (both sanctioned).
- Chained `s.field.subfield` through pointer-in-struct-field: ZERO.
- `};` hits are all struct literals in `return X{...};` statements (correct
  syntax; clean compiles confirm).
- Spot compiles: red_trial.zag → RT_FAILURES,0; sr_trial.zag → SR_FAILURES,0
  (incl. amended P6 control checks: UNCOMMIT@29, re-commit A→1@31). Analyzer
  emitted only string-ownership hints (non-fatal) on sr_trial.

## Duplicates

trial/ vs EVIDENCE_RT1_20260920T014020Z/: red_common, red_judge, red_sut,
red_trial are byte-identical (4 pairs). Canonical = evidence path (frozen
timestamped EVIDENCE dir, P2 tier); trial copies marked dup. red_adv.zag is
trial/-only (no evidence twin).

## Not evaluable

None. Every row was read/checked. il_core.zag (cross-referenced by integ-1
docs) is outside this chunk — flagged as unverifiable here, not as a gap in
the chunk itself.

## Follow-ups recommended (for coordinator, not user)

1. Update or qualify calibrate.py's "exact mirror" header (F1).
2. Widen TC runner's RNG grep to include `rng`/`lcg` tokens (F2).
3. Fix integ_stretch.zag line-46 comment (F3).
4. Unify probe/event counting language in ledger-gating PREREG vs RESULTS (F4).
