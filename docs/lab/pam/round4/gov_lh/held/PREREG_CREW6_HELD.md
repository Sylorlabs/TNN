# PREREG — PAM GOV-LH CREW 6: the three HELD items (V4 two-tier, O2 live machinery, F5 tightened-window)

**Status: FROZEN 2026-09-24. To be committed ALONE before any build output exists.**
**Parent task:** PAM GOV-LH — long-horizon testing of items awaiting Micah's word.
**Authorization:** Micah's 2026-09-24 order ("for the PAMs that need my word, do
more long-horizon testing") authorizes the TEST legs below. ADOPTION of any item
still needs his word: this crew does NOT resolve; it produces decision-grade evidence.
**Branch:** `tnn-native-lab`, repo `sylorlabs/TNN`.
**Work dir:** `docs/lab/pam/round4/gov_lh/held/` (prereg, then sources, evidence, verdict).

This prereg covers three HELD items in two test legs:

- **Leg A — V4/O2:** build the two-tier corroborated-revision machinery per the
  HELD draft (`PREREG_V4_TWOTIER_DRAFT_HELD.md`) and run it at 10x/100x scale.
  Testing V4's machinery IS the O2 test (per the task brief: "cover both with one
  build, adjudicate both bar sets").
- **Leg B — F5 tightened-window:** a window-size SWEEP between the two tested
  points at 10x/100x, to confirm or overturn the NO-GO with scale evidence.

---

## LEG A — V4/O2: two-tier corroborated-revision live machinery

### A.1 Question under test

The HELD draft asks: does the two-tier rule (revision only on ≥2 agreeing
high-conf PASS challengers + CC1 margin guard + F5-exemplar-distance
preconditions) recover the R2-4 withheld truths (621 conflict-withheld, offline
replay 621/621 at 0 false installs) at 0 false installs on frozen adversarial
streams, and does it move RK-3 toward the 85% bar?

O2 (DEBATES_R3.md §3, ranked offense hypothesis O2) is the same machinery in its
LIVE form: "a gate that revises only on two agreeing high-conf PASSes WITH the
margin guard AND the F5 bank as preconditions… explicitly marked as UNBUILT."
One build, both bar sets adjudicated.

### A.2 Frozen machinery spec (exact)

**Base (frozen, carried verbatim from `c3.zag`, Crew 3, verdict PASS):**
the O1 Delivery Adjudicator (admit iff `prog==PASS` OR
`progF==PASS AND agree==1 AND conf>=700`; repaired records get prog=PASS,
pred=1) + revised gate R1/R3/R4:

- R1: per-task challenger slot (jcode, measure, seq). Conflicting PASS
  (`jc != perm_jcode`) with `conf>=700`, `pred==1`, `mrgF>=thr_of(tc)`, no
  armed-negative match: stored challenger with same jcode and
  `|meas − meas_c| <= tol_of(tc)` → revision point; else store challenger →
  `CHALLENGER_PROV`. Weak challengers → `CONFLICT_WITHHELD` (frozen).
- R3: `mrgF >= thr_of(tc)` challenger margin bar (task-natural T3 bars).
- R4: negative entry arms only after TWO FAILs (same jcode, within tol);
  suppression checks the ARMED table only.
- `thr_of`/`tol_of` frozen as in c3.zag. Disposition codes 0..9 as in c3.zag.
- `truth`/`correct` (field 11) scoring-only, never in any gate rule.

**V4 addition 1 — CC1 margin guard (MG6, the survivor).** At the R1 revision
point (stored challenger + incoming same-jcode PASS within tol, both conf ≥ 700,
both `mrgF >= thr_of`), consult MG6 exactly as frozen in
VERDICT_CC1_GUARD.md:

allow `REVISED_INSTALL` iff ALL THREE hold, else veto → `CHALLENGER_PROV`:

1. `min(mrgF_stored, mrgF_incoming) >= 400` (MG1_FLOOR, frozen);
2. spans disjoint: NOT (`sa_stored < sb_incoming` AND `sa_incoming < sb_stored`)
   (touching counts as disjoint);
3. `|seq_stored − seq_incoming| >= 20` (MG4_SEQ_GAP, frozen).

**Veto semantics (faithful to guard_main.zag):** on veto, the trial is
dispositioned `CHALLENGER_PROV` (disp 8, counts as install), the challenger slot
is RETAINED (the previously stored challenger stays; the incoming does NOT
overwrite it; the slot is NOT cleared). Guards never authorize a revision.

**V4 addition 2 — F5-exemplar-distance precondition.** At the same revision
point, BEFORE MG6 (order preregistered; either veto → `CHALLENGER_PROV` with
the same retained-slot semantics; vetoes counted by first-firing guard):
veto iff EITHER challenger (stored or incoming) is within F5 exemplar distance
of ANY negative-bank exemplar, where:

- negative bank = the 6 frozen F5 exemplars (`exemplars.tsv`, SHA
  `13f4ca47429bc0bb8788d60406593766e48f6f064cb7538adf28be16a289200e`):
  TMB-1, conf 701–718, measure 2618–2647;
- "within F5 exemplar distance" = the frozen F5 tightened predicate:
  same family stem AND `|Δconf| <= 9` AND `|Δmeasure| <= 15`;
- family stem for gate trials: `tcode==4` (timbredisc) → `"TMB"`, else `"OTH"`
  (no exemplar carries stem `"OTH"`, so the veto can only fire on timbredisc —
  faithful, since the F5 bank is timbredisc-specific).

**Span derivation (frozen modeling choice).** The RK-3 case format carries no
evidence spans; MG6 needs them. Frozen rule: `span_a = seq`, `span_b = seq + 2000`
(W=2000, the CC1 fixtures' window scale — the only frozen span scale in the
program). Deterministic, no RNG. The span conjunct's veto rate on the battery is
downstream of this choice; vetoes are reported broken down by conjunct
(margin-floor / span-overlap / seq-gap / f5-exemplar) so the cost is attributable.

**Challenger slot extension:** stores (jcode, measure, seq, mrgF). Spans derived
from seq at veto time. No other state changes vs c3.zag.

### A.3 Batteries (frozen)

1. **RK-3 battery:** `c3_cases.txt` (11,840 rows, SHA
   `ed1ad01fb65a37125b06163bd1243bd930435e655b7a446c5f16fa91333e3357`),
   derived from the frozen `sweep.jsonl`
   (`4163fffa65f18f552d48f7efec0e9800a7406547a27c6259d39a48ec7f0833f2`).
   Metrics exactly as c3.zag: k1, k2, rk3 (num/den), rk1 (false
   PERMANENT/REVISED installs), rk2 (wrong high-conf permanent installs),
   repaired, revised_installs, challenger_provs, d0..d9.
   Scale: 1x (11,840), 10x (118,400), 100x (1,184,000) by exact file
   concatenation. KB-V4-1 adjudicated on the 1x RK-3 rate; 10x/100x confirm
   rate stability (long-horizon state behavior: challenger slots, negative
   tables, and cross-boundary corroboration over 1.18M trials).
2. **CC1 wrong-pair trials (frozen):** the 9 scored CC1-family cells from
   PREREG_CC1_GUARD.md §3 (CC1 base + V1…V8) + V9 as the unscored ceiling probe
   (reported, not kill-barred — precedent: the CC1 prereg §4). Transcribed into
   a trial stream by script from the prereg's cell table (verified against
   EXPECT_GUARD_CELL.tsv). KB-V4-3: any `REVISED_INSTALL` on the 9 scored cells
   → KILL.
3. **Adversarial boundary variants (new, deterministic, zero RNG):** wrong-pair
   trials engineered to probe the MG6 boundary: mrgF ∈ {399,400,401} ×
   |Δseq| ∈ {19,20,21} × spans {overlap-by-1, touching, disjoint-by-1}, all
   wrong (truth ≠ challenger jcode), conf ≥ 700, within tol. Expectation
   (preregistered, not a bar): the guard allows exactly the cells where all
   three conjuncts pass and vetoes otherwise — the boundary behaves as frozen.
   The perfect-storm geometry (V9-like: mrgF 6600/6603, disjoint spans,
   Δseq=427, WRONG) at 100x repetition = the decoy stream: preregistered
   expectation is REVISED_INSTALL (V9 proved no evidence-side guard separates
   it); reported as the V9 residual, NOT kill-barred (same status as V9 in the
   CC1 prereg).
4. **Safety on the frozen sweep (KB-V4-2):** RK-1 = 0 AND RK-2 = 0/1,109 on the
   1x/10x/100x runs. NOTE (frozen scoping decision): the hardening battery's
   red-team streams (clean/withhold/install/decoy, 288+288+44+52) are in the
   rt4 sense-record format, which carries NO mrgF/agree/strong/progF — fields
   V4's rules require (R3 bar, MG6 floor, adjudicator). A faithful translation
   is impossible without inventing values, so V4 cannot run on those streams;
   KB-V4-2 is adjudicated on (i) the frozen 11,840-row sweep's wrong high-conf
   trials (1,109 wrong high-conf percepts — the frozen RK-2 battery), and (ii)
   the frozen CC1 wrong-pair family (KB-V4-3). The engineered decoy stream (3)
   is reported alongside as the adversarial probe.

### A.4 Kill bars (frozen from the HELD draft; applied mechanically)

- **KB-V4-1 (liveness):** RK-3 < 85% → KILL.
- **KB-V4-2 (safety):** any false install (RK-1 > 0 OR RK-2 > 0) on §A.3(1) at
  any scale → KILL.
- **KB-V4-3 (CC1 regression):** any `REVISED_INSTALL` on the 9 scored CC1
  wrong-pair cells → KILL.
- **KB-V4-4 (determinism):** 3 runs byte-identical (sha256 of all outputs) per
  battery/scale → else VOID, rebuild, re-run.
- **KB-O2:** RK-3 < 85% → KILL; any false install → KILL; any CC1
  `REVISED_INSTALL` → KILL — adjudicated on the same runs as KB-V4-1..3
  (testing V4's machinery IS the O2 test).

### A.5 Pre-registered expectations (not bars)

- V4's RK-3' ≈ C3's 71.78%: vetoes convert `REVISED_INSTALL` → `CHALLENGER_PROV`
  and both count as installs, so the install rate is preserved up to downstream
  state drift (stale permanent slot). **KB-V4-1 (≥85%) is therefore expected to
  KILL** — the bar was unreachable by the unguarded predecessor (C3: 791/1,102),
  and vetoes cannot add installs. The decision-grade questions are the safety
  bars and the veto-cost breakdown.
- `revised_installs` expected to fall vs C3's 92 (MG6 vetoes most revisions on
  the dense battery: with W=2000 spans, corroborating pairs with |Δseq| < 2000
  have overlapping spans → span-conjunct veto). The conjunct breakdown will show
  which conjunct does the work.
- RK-1 = 0, RK-2 = 0/1,109 (C3's safety preserved — vetoes only remove revisions).
- 0 `REVISED_INSTALL` on the 9 scored CC1 cells (MG6 already proved 0/9; the F5
  veto independently catches the base CC1 pair, which sits inside the exemplar
  cluster: conf 718/704 vs 701–718, meas 2618/2642 vs 2618–2647).
- 10x/100x RK-3 rates stable within ±0.5pp of 1x (no long-horizon state rot).

### A.6 Honest limits (preregistered)

- The span derivation (W=2000) is a modeling choice, not frozen evidence; the
  span-conjunct veto rate is downstream of it. The conjunct breakdown is the
  honest accounting.
- The F5-exemplar veto reuses the tightened windows (|Δconf|≤9, |Δmeasure|≤15)
  that Leg B may confirm as NO-GO for the live gate; here they are a veto
  precondition, not a gate — the verdict reports the veto's measured cost
  (how many correct revisions it vetoes) separately.
- The hardening-stream format gap (§A.3(4) NOTE) bounds KB-V4-2's stream coverage.
- Single-task streams; cross-task interference untested (same as the CC1 guard).

---

## LEG B — F5 tightened-window: the sweep between the tested points

### B.1 Question under test

The F5 tightened fork (H-PAM-1, TESTED-KILLED) found: window tuning passed the
bars vacuously (delay 0/300, far 0/60) BUT backtest false-block retention 0/9
(was 8/9) — tightening deleted catch power; NO-GO for the live gate via window
tuning. The kill was at two tested points: tightened (|Δconf|≤9, |Δmeas|≤15)
and frozen (|Δconf|≤150, |Δmeas|≤2000). This leg probes whether ANY intermediate
window separates honest from false: a 2-D sweep of (conf-radius, meas-radius)
measuring catch power (retention) vs over-block cost at each point.

### B.2 Frozen sweep spec (exact)

**Predicate:** the F5 pre-confirmation block predicate, pure Zag, derived from
`f5_tight.zag` by parameterizing ONLY the two window constants (rc, rm) via
argv — no other logic change. Candidate BLOCKED iff EXISTS a bank exemplar with
ALL three: same family stem; `|conf_cand − conf_ex| ≤ rc`; `|measure_cand −
measure_ex| ≤ rm`.

**Window grid (frozen):** rc ∈ {9, 25, 46, 80, 150}, rm ∈ {15, 53, 100, 245, 500,
1000, 2000} — 35 windows. Bracketing rationale (frozen): the nearest backtest
false accept sits 245 measure units / 46 conf units from the cluster edge
(F5 prereg §3 — so retention can only rise at rm ≥ 245 AND rc ≥ 46); the nearest
NEAR-grid point sits 53 measure units from the cluster edge (2700 vs 2647 — so
over-block can only rise at rm ≥ 53, conf-dependent). The grid brackets both
thresholds on both axes. (9,15) = the killed tightened point; (150,2000) = the
frozen point — both reproduced as anchors.

**Batteries (frozen fixtures, SHA-verified before every run):**
- Block battery: `fixtures_ledger.txt` (300 NEAR + 60 FAR, SHA
  `0c5e2c0db6576bd37ff53513fb1361cdf7936d4826274bdcc9742be2261233a0`) —
  metrics per window: NEAR blocked / 300 (over-block), FAR blocked / 60
  (far-control).
- Retention replay: the 43 backtest candidates via `ledger_d_withhold.txt`
  (SHA `63ea591d8cbb9d8b3e1cd088364e96d8fdfa19d435e337dfac0ad17a0326c2b1`,
  read-only) through the parameterized replay predicate — metrics per window:
  false blocked / 9, true blocked / 34. (The replay binary is `f5_tight_replay.zag`
  with the same (rc, rm) parameterization; same parser, same 43 candidates.)
- Scale: full 35-window sweep at 1x; the Pareto-frontier windows plus the two
  anchor points re-run at 10x (3,600 trials) and 100x (36,000 trials) by exact
  fixture repetition, confirming rate stability.

**Adversarial boundary percepts (new, deterministic, zero RNG):** near-exemplar
CORRECT percepts engineered to sit at window boundaries: for each window on the
measured Pareto frontier, generate correct percepts at `|Δmeas| = rm ± 1` and
`|Δconf| = rc ± 1` from the nearest exemplar (both sides of each boundary, both
axes, stem-matched TMB). Run through the predicate at that window. Preregistered
expectation (not a bar): the boundary does not separate — for any window with
retention > 0, boundary-correct percepts on the inside are also blocked (the
false accepts and near-exemplar corrects occupy the same neighborhood, per the
F5 verdict's honest reading). Measured block/allow per boundary percept.

### B.3 Decision rule (frozen)

**OVERTURN the NO-GO** iff there EXISTS a swept window with ALL THREE:
retention ≥ 8/9 (matches the frozen trap's catch power), over-block ≤ 25%
(≤ 75/300, the red-team's bar), far-control 0/60.
Otherwise **CONFIRM the NO-GO**. The full Pareto frontier
(retention vs over-block for all 35 windows) is reported regardless, plus the
boundary-percept results — so a partial separator (e.g. 4/9 at 10% over-block)
is visible even if it does not overturn.

### B.4 Pre-registered expectations (not the decision rule)

- Retention stays 0/9 for all windows with rm < 245 or rc < 46 (nearest-false
  geometry); over-block stays 0/300 until the window reaches the first NEAR
  grid point.
- The F5 verdict's honest reading predicts the frontier shows retention and
  over-block rising together with no separating gap (the falses at 245/46 and
  the NEAR grid at 53 meas units interleave once the window opens). The sweep
  tests this prediction; if a gap exists, the decision rule catches it.

### B.5 Laws and method (both legs)

- Pure Zag for mechanisms and batteries; Python only for glue (fixture
  generation, sweep driver, scorers). Zero RNG in any decision path.
- Test-first: this prereg committed ALONE before any build. Gate built from the
  prereg, not the reverse.
- Determinism: ≥2 (here: 3) runs byte-identical (sha256) per binary per battery;
  else VOID.
- `truth`/`correct` never in any gate/predicate rule (static check: appear only
  in scoring code).
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Commit order: this prereg ALONE → then sources + evidence + verdict together.
  No binaries, no `.zagd` / `.zag-cache`. Via `~/workspace/commit_racefree.py`
  (or `commit_big_files.py` for large evidence), lab-relative paths,
  `TMPDIR=~/workspace/tmp_commit`.
- Repo paths: `docs/lab/pam/round4/gov_lh/held/` on branch `tnn-native-lab`.

## Deliverables

1. This prereg (alone).
2. Leg A: `src/v4.zag` (+ byte-identical `R33_NATIVE_IO_V1.zag`,
   `R33_NATIVE_SHA256_V2.zag` copies), `evidence/` (metrics 3× per
   battery/scale, digests, CC1 stream + boundary variants + veto breakdown),
   `VERDICT_V4_O2.md` with KB-V4-1..4 and KB-O2 adjudicated.
3. Leg B: `src/f5_sweep.zag` (+ parameterized replay), `evidence/` (35-window
   table, Pareto frontier, boundary percepts, 10x/100x confirmations),
   `VERDICT_F5_SWEEP.md` with the B.3 decision rule applied.
4. Final report to the parent: decision-grade evidence summary for Micah's word.
   ADOPTION of V4/O2/F5-window is NOT resolved by this crew under any outcome.
