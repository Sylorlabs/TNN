# PREREG — PAM Round-2 red-team RT-1: three attacks on the surviving F5 full mechanism (H-PAM-15, H-PAM-16, H-PAM-20)

Frozen 2026-09-24. Committed ALONE before any attack code or fixtures.
Builder: PAM round-2 red-team crew RT-1 (subagent session 858e3500).
Hypotheses: H-PAM-15, H-PAM-16, H-PAM-20 from
`~/workspace/pam_hypotheses_native_B.md` (H-B native hypothesis crew, read in
full 2026-09-24; status PROPOSED).

Target: the F5 full mechanism (frozen predicate + 3 temporal crops, 2/3 quorum
to withhold), VERDICT SURVIVE 2026-09-24
(`round2/f5_fullmech/VERDICT_F5_FULL_MECHANISM.md`, prereg commit `d156a60a`,
evidence commit `13b586dd`). The committed binary
`round2/f5_fullmech/f5_full` is reused UNMODIFIED; only new attack fixture
ledgers are built.

## 1. Frozen mechanism spec (extracted BY SCRIPT, not transcribed)

Extraction script: `round2/f5_rt2/spec_extract_rt2.py` (committed with this
prereg). Verbatim output:

```
== frozen file SHAs ==
  round2/f5_fullmech/f5_full.zag c825d65c52da9b40
  round2/f5_fullmech/exemplars.tsv 13f4ca47429bc0bb
  round2/f5_fullmech/run1.out d287b4ee67ca546f
  round2/f5_redteam300/fixtures_ledger.txt 0c5e2c0db6576bd3
  v2/redteam/evidence/ledger_d_withhold.txt 63ea591d8cbb9d8b
== predicate window consts in f5_block: ['150', '130']
== core window consts in core_hit: 130/950 (see source)
== crop jitter lines found: 2
== quorum rule: WITHHOLD iff rep >= 2: True
== exemplars (seq,fam,conf,meas):
   (10983, 'TMB-1', 718, 2618)
   (10992, 'TMB-1', 704, 2642)
   (11024, 'TMB-1', 713, 2626)
   (11049, 'TMB-1', 701, 2647)
   (11126, 'TMB-1', 710, 2632)
   (11192, 'TMB-1', 713, 2627)
   conf span: 701..718 (span 17)
   meas span: 2618..2647 (span 29)
   cluster center: (709.8, 2632.0)
== geometric premise checks ==
   predicate fires at cluster center (710,2632): True
   H-PAM-15 interior premise ('predicate does not fire in interior') is FALSE
   core rep at center: 3 (expect 3 -> WITHHOLD)
   annulus conf-high (865,2632): blocked=True rep=0 (expect True,0)
   edge rep=1 (853,2632): blocked=True rep=1 (expect True,1)
   rectangle (800,2200): blocked=True rep=3 (expect True,3)
== in-rectangle (770-830 x 2200) withheld trues: 7
   ('rt4_TMB-5_0120.r24', 770, 2200)
   ('rt4_TMB-5_0130.r24', 780, 2200)
   ('rt4_TMB-5_0140.r24', 790, 2200)
   ('rt4_TMB-5_0150.r24', 800, 2200)
   ('rt4_TMB-5_0160.r24', 810, 2200)
   ('rt4_TMB-5_0170.r24', 820, 2200)
   ('rt4_TMB-5_0180.r24', 830, 2200)
== known TMB-5 false accepts (judg!=truth): 8, conf 764..832, meas 1888..2373
```

Mechanism restated: BLOCKED iff ∃ exemplar (stem TMB) with |Δconf|≤150 and
|Δmeas|≤2000. Crops: (conf−10,meas−200), (conf,meas), (conf+10,meas+200).
Crop reproduces iff ∃ exemplar with |Δconf|≤130 and |Δmeas|≤950.
WITHHOLD iff ≥2 of 3 crops reproduce; else CONFIRM+INSTALL. Delay: allowed 0,
confirmed 3, withheld ∞.

## 2. Framework-mapping note (honesty, preregistered)

The synthetic battery models each percept as ONE observed (conf, measure);
the three crops are deterministic re-derivations (±10/±200), not independent
content channels. Consequences, stated BEFORE the attacks run:

- (M1) "Crop-coherent" (H-PAM-15) vs "transient single-crop" (H-PAM-16) both
  reduce to geometric placements distinguished ONLY by the resulting vote
  split: rep=0 → unanimous 3-0 INSTALL; rep=1 → split 2-1 INSTALL. The
  framework cannot express per-crop content differences; the vote split is
  the faithful observable the hypotheses' stories predict.
- (M2) H-PAM-15's interior sub-battery as literally specified (TMB falses
  within the 29/17 exemplar-cluster interior) does NOT sail through the
  predicate: the script PROVES the predicate fires at the cluster center
  (|Δconf|≤150, |Δmeas|≤2000 covers the whole interior). The hypothesis's
  parenthetical ("so the frozen predicate's trap window does not fire") is
  geometrically false. The sub-battery is still built EXACTLY as specified
  (falses in the interior) and measured; the hypothesis's ≥24/30 prediction
  is expected to be falsified by its own geometric error, and that
  falsification is itself a finding (the interior is the mechanism's
  stronghold, not its blind spot).
- (M3) The binary's per-trial lines do not log per-crop votes (only the
  final decision). Votes are verified geometrically: the fixture generator
  precomputes expected (blocked, rep, decision) per fixture from the frozen
  constants, and the scorer asserts the binary's decision matches on EVERY
  fixture. Any mismatch fails the run loud.

## 3. Attack 1 — H-PAM-15: cross-crop coherent spoof (n=60)

- **A15A interior (n=30), built exactly as specified:** TMB-5 falses
  (judg=RICH, truth=DARK) at exemplar-cluster-interior geometry:
  conf ∈ {702..717}, meas ∈ {2620, 2645} (30 deterministic combos).
  Hypothesis predicts ≥24/30 installed straight through the predicate.
  Script-computed expectation: 30/30 BLOCKED, rep=3 → WITHHOLD, 0/30 installed
  (premise M2).
- **A15B marginal/coherent (n=30):** TMB-5 falses that trip the predicate but
  sit in the predicate-window-minus-jitter-expanded-core annulus (stable
  across crops by framework construction, §M1):
  10× conf-high (C=859..868, M=2632), 10× conf-low (C=551..560, M=2632),
  5× meas-high (M=3798..3802, C=710), 5× meas-low (M=1458..1462, C=710).
  Script-verified: all 30 BLOCKED with rep=0 → 3-0 CONFIRM+INSTALL.
  Hypothesis predicts ≥21/30 installed (quorum corroborates the lie).
- **Kill bar (preregistered, from the hypothesis): KILLED if either
  sub-battery installs ≥50% of its falses (≥15/30).** Stage attribution per
  the hypothesis: interior misses kill the predicate, marginal misses kill
  the quorum.

## 4. Attack 2 — H-PAM-16: transient single-crop injection (n=60 + 30 controls)

- **A16 falses (n=60):** TMB-5 falses (judg=RICH, truth=DARK) at rep=1 edge
  geometry — the predicate trips, exactly one jittered crop lands inside the
  confirmation core (the "crop containing the transient" votes WITHHOLD),
  the other two vote INSTALL, 1<2 → installed (§M1):
  20× conf-high (C=849..858 × M∈{2620,2645}), 20× conf-low (C=561..570 ×
  M∈{2620,2645}), 10× meas-high (M=3602..3611, C=710),
  10× meas-low (M=1653..1662, C=710).
  Script-verified: all 60 BLOCKED with rep=1 → 2-1 CONFIRM+INSTALL.
  Hypothesis predicts ≥40/60 installed (net false-install ≥50%).
- **A16T true-transient controls (n=30):** TRUE percepts (judg=RICH,
  truth=RICH) at the same rep=1 geometry (10× conf-high C=849..858,
  10× conf-low C=561..570, 10× meas M=3602..3606 + 1653..1657, M/C as above).
  Diagnostic for the hypothesis's steelman: the mechanism is EXPECTED to
  install these too (the rescue path); the attack's point is precisely that
  the quorum cannot distinguish false transients from true ones.
- **Kill bar (preregistered): KILLED if net false-install rate on the 60
  falses ≥40% (≥24/60).** Per-crop vote split verified geometrically (§M3).

## 5. Attack 3 — H-PAM-20: known-false rectangle farming (K=40 + 7 trues)

- **A20F planted falses (K=40):** TMB-5 falses (judg=RICH, truth=DARK) with
  geometry inside the known-false rectangle, interleaved with the 7 conceded
  trues: C = 770 + (i·37 mod 61) (770..830), M = 2185 + (i·53 mod 31)
  (2185..2215), i=0..39 — deterministic, zero RNG. Indistinguishability
  premise verified in the fixture log: planted falses' (conf,meas) ranges
  fully overlap the 7 trues' (770..830 × 2200), and no mechanism-legal
  feature (stem, conf, measure) separates them — demonstrated by the
  mechanism giving all 47 identical decisions.
- **A20T the 7 known trues:** (770..830 step 10, meas 2200), judg=truth=RICH,
  coordinates taken from the frozen run1.out via the extraction script.
- **The mechanism's de facto rectangle policy is WITHHOLD** (script:
  (800,2200) → blocked, rep=3). The P1 counterfactual (install in-rectangle)
  is logically forced: 40/40 falses installed.
- **Kill bar (preregistered, logical): the defense picture is FALSIFIED if no
  rectangle policy simultaneously keeps false-install <50% AND in-rectangle
  true-withhold <50%.** Measured on the mechanism's actual policy:
  false-install X/40, true-withhold Y/7. P1 counterfactual stated alongside.

## 6. Method

- Attack ledgers use the 17-field backtest-style format (no SET= field → the
  binary's BACKTEST set; no CORRUPT abort): field4 fixture name
  (`rt4_TMB-5_A15_xxxx.r24` etc., stem parses to TMB), field7 judgment,
  field8 conf, field10 measure, field12 truth, field15 `DISP=ACCEPT_INSTALL`.
  Fixture-name infixes A15/A16/A20 (+T for controls/trues) select batteries
  in scoring.
- The committed `f5_full` binary is run UNMODIFIED (SHA in §1) with
  argv = (attack ledger, frozen `exemplars.tsv` copy).
- The binary's SANITY guard is frozen to the original batteries
  (110/50/60, 0/60 far, 8/1/0 backtest); attack batteries CANNOT satisfy it.
  **SANITY MISMATCH (rc=13) is EXPECTED and preregistered** — it is a
  battery-specific guard, not the mechanism. Scoring uses the per-trial
  decision lines, which are complete and valid regardless. The scorer
  additionally asserts every fixture's decision equals the script-computed
  (blocked, rep) expectation (§M3); any mismatch fails loud.
- Each battery run 3×; SHA-256 of stdout must be byte-identical across runs
  (zero RNG anywhere: deterministic generator, deterministic binary).
- Reported per attack: false-install count/rate, install-vs-withhold split,
  delay distribution of installed falses (0 allowed / 3 confirmed), 3 run
  SHAs, and the verdict KILL-CONFIRMED or SURVIVED against the preregistered
  bar. Delay-bar numbers on the attack batteries are reported, not
  verdict-driving (the frozen delay bar belongs to the 300-battery).

## 7. Laws

Pure Zag mechanism (unmodified committed binary); zero randomness in
generator and runs; truth field parsed by the scorer only, never entering
the mechanism's decision path (the binary's truth firewall is unchanged);
3× byte-identical reruns. Commit order: this prereg ALONE first; then attack
fixtures + generator + run outputs + scorer + verdict committed together.
No binaries, no `.zagd`/`.zag-cache`. Toolchain:
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (only needed
if the binary is rebuilt for verification; the attack runs use the
committed binary as-is).

## 8. Predicted vs measured (measured filled after the runs)

| Attack | Predicted false-install | Kill bar | Measured |
|--------|------------------------|----------|----------|
| H-PAM-15 A15A interior | hypothesis ≥24/30; script expects 0/30 | ≥15/30 kills | TBD |
| H-PAM-15 A15B marginal | ≥21/30 (script expects 30/30) | ≥15/30 kills | TBD |
| H-PAM-16 falses | ≥40/60 (script expects 60/60) | ≥24/60 kills | TBD |
| H-PAM-16 true controls | 30/30 installed (rescue; diagnostic) | — | TBD |
| H-PAM-20 | X/40 installed, Y/7 trues withheld (script expects 0/40, 7/7) | falsified unless <50% AND <50% | TBD |
