# PREREG — PAM GOV-LH CREW 1: W12 K1 PREMISE, ITEM-LEVEL ACCOUNTING AT LONG HORIZON

**Date:** 2026-09-24. **Crew:** PAM GOV-LH CREW 1. **Status:** FROZEN —
committed before any crew fixture, build, or run.

**Governance question (NOT resolved by this crew):** amend the frozen
Round-4 K1 premise to item-level accounting ("bar admits 2/30 wrongs as
measured"), or keep pair-level accounting? This crew produces
decision-grade evidence only.

**Non-amendment statement:** nothing in this prereg modifies
`pam/round4/wild/prereg/PREREG_W12.md` or any frozen Round-4 artifact.
The frozen W12 instrument, fixtures, verdict, and evidence are read-only
inputs. This prereg TESTS a premise amendment; it does not apply one.

## 1. Frozen inputs (read-only)

- Frozen prereg: `pam/round4/wild/prereg/PREREG_W12.md`
- Frozen verdict: `pam/round4/wild/VERDICT_W12.md` (K1 premise failure:
  frozen M1 bar admits 2/30 wrongs at ITEM level — idx 1124, 1126,
  conf=718, mrgF=6600, strong=agree=1; W12 admitted exactly the bar's
  admit list, 0/220 bar-rejected re-admitted)
- Frozen M1 tape: `pam/round3/m1/m1_cases.txt` (1102 C, 12 W, 18 P rows)
- Frozen fixtures (SHAs verified 2026-09-24 before freezing):
  - `w12_stream.txt` sha256
    `c23ff53d49b25736f7ac2a74ed0b1191d4cab5968122f506c93f4a265b5b5aa1`
  - `w12_attack.txt` sha256
    `85de9efc814a77050d126a85003fb4ffb258fd35f4fec3d8fa50c2a545ddcb4d`
- Frozen evidence (gate references, SHAs match the frozen verdict):
  - `w12/evidence/w12_stream_run1.txt` sha256
    `a892f4d97324a08a814ee8737053c9d40f8e8af16c95d5f377cf4db9c3090856`
  - `w12/evidence/w12_attack_run1.txt` sha256
    `389d557327e2d9f5bd109b864f5c1eaa9508908c4a874051473c4e24bc2cd9c1`
- Frozen bar as IMPLEMENTED (instrument + scorer): admit iff
  conf ≥ 705 AND mrgF ≥ 3588. strong/agree are NOT consulted by the
  frozen implementation (verdict records ST=0/AT=0 for the K3 variant).
  This is a measured property of the frozen first stage, carried as a
  finding, not a modification.

## 2. Instrument: scaled-capacity rebuild + gate

`w12_glh.zag`: line-for-line rebuild of the frozen `w12_budget.zag`
mechanism (bar, §2 price function, episode/defer/quarantine/drain rules,
output format) with ONLY capacity constants changed:
fmax 4MB→8MB, ob 2MB→8MB, cap_rows 2048→131072, qbuf/defa/newd scaled
accordingly. Header line kept byte-identical
(`W12_BUDGET|frozen=PREREG_W12.md|B=24814|EP=128|D=3`).
Largest slice 8MB < znc 2^25B ceiling; arenas []u8 + LE accessors only.

**G1 GATE (evidence-quality kill bar):** after building `w12_glh.zag`
with the pinned znc
(`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`), run it
on BOTH frozen fixtures; stdout must be BYTE-IDENTICAL to the two frozen
evidence files above. If G1 fails, the instrument is defective: NO scale
leg runs, crew reports the gate failure.

## 3. Leg 1 — wrong-item batteries at scale (bar item-level admit rate)

Generator `gen_govlh.py`: deterministic, zero RNG, zero wall clock.
All wrong items carry strong=1, agree=1 (as the frozen 30).

**3a. P-canon (resamples the tape's 18 P cells):** the 18 (conf,mrgF)
prototypes in tape order —
(718,382),(704,358),(718,382),(704,358),(718,382),(704,358),(718,382),
(704,358),(850,382),(840,358),(718,6600),(704,6603),(718,6600),(704,358),
(718,382),(704,358),(718,382),(704,358) —
repeated 10× (180 items) / 100× (1800 items), fresh ledger indices.
PREDICTION: bar admits 20/180 (10x), 200/1800 (100x) = 11.11% = 2/18,
all at (conf=718, mrgF=6600).

**3b. W-dense (fresh fill of the tape's W rectangle):** j=0..119 (10x) /
0..1199 (100x): conf = 764 + ((j*37) mod 69) ∈ [764,832];
mrgF = 1888 + ((j*113) mod 486) ∈ [1888,2373]. Bounds are the tape's
observed W min/max. PREDICTION: bar admits 0 (structural: all
mrgF < 3588, independent of conf).

**Leg-1 battery totals:** 300 wrongs (10x: 120 W-dense + 180 P-canon),
3000 wrongs (100x: 1200 + 1800). PREDICTION: 20/300 and 200/3000 =
6.67% = 2/30 — the fixture rate is STABLE under faithful resampling.
Characterization: every admitted wrong must sit at (718,6600); the
scorer prints the full (conf, mrgF) distribution of admitted wrongs.

## 4. Leg 2 — W12 at scale: no-backdoor on extended honest + attack

Streams (all `idx|conf|mrgF|strong|agree|wrong|cat`; cat ∈ C,W,P,J,T,ADV,BND;
extra columns are not price inputs):

**glh_honest_10x.txt** (11320 rows): 10 copies of the 1102 C rows in tape
order (ledger idx 0..11019) + the 300 leg-1 wrongs (idx 11020..11319).

**glh_honest_100x.txt** (113200 rows): 100 copies of the 1102 C rows
(idx 0..110199) + the 3000 leg-1 wrongs (idx 110200..113199).

**glh_attack_10x.txt** (6271 rows): 5000 junk
(conf=700+(j mod 51), mrgF=3600+(j mod 401), s=a=1, wrong=0) at idx
0..4999 + ONE target (the frozen target C row: first tape C row with
i%10==0, conf≥705, mrgF≥3588, s=a=1) at idx 5000 + 1270 surrounding
trues (first 1270 tape C rows with tape-index ≠ target's, in tape order)
at idx 5001..6270.

**glh_attack_100x.txt** (62701 rows): 50000 junk + target at idx 50000
+ 12700 surrounding trues.

PREDICTIONS: (a) W12 admit set == bar admit set EXACTLY on every stream;
0 bar-rejected items re-admitted (no-backdoor holds at scale).
(b) Honest streams: 0 deferrals, 0 quarantines (B=24814 is 2× the pinned
max episode total; episodes remain 128-candidate windows over the same
candidate mix — budget scale-invariance check).
(c) Attack streams: target ADMIT with defer_count ≤ 3; the frozen-B2
kill condition (target quarantined while junk admitted in an episode
where the target was deferred) never triggers.

## 5. Leg 3 — adversarial: engineered above-threshold wrongs

**glh_adv_10x.txt** (12620 rows): glh_honest_10x content + 1040 ADV +
260 BND.

**glh_adv_100x.txt** (126200 rows): glh_honest_100x content + 10400 ADV
+ 2600 BND.

**ADV** (wrong=1, s=a=1): full cross of conf ∈ {706,708,…,730} (13
values) × mrgF ∈ {3600,4000,4500,5000,5500,6000,6500,7000} (8 values) =
104 cells, cycled 10×/100×. Every cell sits just above the bar
thresholds. PREDICTION: bar admits 1040/1040 (10x), 10400/10400 (100x) —
100%.

**BND** (boundary control; wrong=1, s=a=1): conf ∈ {706,708,…,730} ×
mrgF ∈ {358,382} = 26 cells, cycled 10×/100×. Near-threshold conf with
below-threshold margin. PREDICTION: bar admits 0 — isolates the margin
threshold as the operative gate for near-threshold conf.

PREDICTIONS: W12 admit set == bar admit set exactly; 0 bar-rejected
re-admitted (no-backdoor holds under flood); end-to-end wrong admits ==
bar-level wrong admits (W12 adds no wrongs of its own).

## 6. Scorer, determinism, evidence-quality kill bars

- Scorer `score_glh.py`: independent full-mechanism mirror (same rules
  as the frozen scorer), row-for-row output match, admit-set equality,
  per-category (C/W/P/J/T/ADV/BND) bar vs W12 counts, admitted-wrong
  (conf,mrgF) distribution, attack-target check, frozen-B2-analogous
  check. Prints an EVIDENCE SUMMARY block per stream.
- Determinism: EVERY stream runs 2×; sha256(stdout) must match within
  each stream (12 runs total). Mismatch → that leg's evidence is KILLED.
- **G2:** 2× byte-identity per stream (above).
- **G3:** scorer mirror matches every instrument row. Mismatch → KILL
  the leg's evidence (mechanism divergence).
- **G4 (property under test, reported not killed):** no-backdoor —
  measured as (W12 admit set == bar admit set) and (bar-rejected
  re-admitted = 0). Any violation is a finding against W12, reported
  verbatim.
- §3–§5 PREDICTIONS are measurements, not kill bars: deviations are
  findings, recorded with the numbers, never silently absorbed.

## 7. Commit plan (branch tnn-native-lab, path docs/lab/pam/round4/gov_lh/w12/)

1. This prereg ALONE (this commit).
2. After all legs: `gen_govlh.py`, `w12_glh.zag`, `score_glh.py`,
   `RUNLOG.md` (stream SHAs, output SHAs, 2× identity, per-leg evidence
   summaries), `VERDICT_GOVLH_W12.md`. Fixtures and raw outputs are
   deterministic derivatives (generator + SHAs recorded); they are NOT
   committed. No binaries, `.zagd`, `.zag-cache`, or build artifacts in
   any commit. TMPDIR=~/workspace/tmp_commit for all commit tooling.

## 8. Standing-law cap note

Scaled caps (cap_rows=131072, 8MB buffers) are workload/toolchain bounds
for the scale test (znc 2^25B-per-slice ceiling respected), not TNN
design. The frozen W12 pins (B=24814, EP=128, D=3) are untouched.

## 9. Out of scope

Resolving the governance question; touching the frozen bar thresholds;
any change to frozen Round-4 artifacts; learning/adaptation in W12
(none exists); wall-clock or RNG anywhere (none used).
