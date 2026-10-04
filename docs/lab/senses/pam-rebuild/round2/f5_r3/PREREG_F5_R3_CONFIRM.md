# PREREG — PAM Round-3 crew 5: F5 confirmation-path rebuild (R3-3/D2), two non-quorum organs vs KB-D2 + the RT-1/RT-2 kill battery

Frozen 2026-09-24. Committed ALONE before any build, battery, or mapping
query. Builder: PAM round-3 crew 5 (subagent session 2287ce08).

Debate slate: R3-3/D2 (`~/workspace/tmp_commit/pam_r3/HYPOTHESES_R3.md`,
lines 88–130): build the unbuilt half of F5 — a genuine deliberate
re-inspection organ (three temporal crops were the killed design's
instrument; the frozen spec's own rationale is "a separate deliberate organ,
not re-scoring the same judgment").

Critical context (read before designing — all from committed evidence):
- Crew 4 built the crop-quorum version (prereg `d156a60a`, evidence
  `13b586dd`): it SURVIVED KB-D2-style bars, then its own RT-1 red team
  KILLED it (`9e643a95`, `d332249d`): H-15 marginal coherent spoof 30/30
  installed, H-16 transient injection 60/60 installed, H-20 rectangle
  dilemma (logical kill of the residual tolerance).
- RT-2 (`49c0c6b6` + evidence, `round2/f5_rt3/`): H-17 boundary mapping
  60/60 installed, H-18 delay flood 40.0% both directions, H-19 rescue
  hijack 60/60 installed.
- Finding to beat: "a quorum has NO safe operating point vs a crop-aware
  adversary — it was a coherence detector, not admission security."

This crew builds something DIFFERENT — not a crop-quorum, not a coherence
vote. Two candidate organs, both genuine deliberate re-inspections, both
facing KB-D2 plus the full RT-1/RT-2 battery. If neither survives, the
verdict is KILL the confirmation path (keep F5 block-only) — reported
honestly, no quorum resurrection.

H-PAM-25 (warrant + standing witness, `~/workspace/hypothesis_backlog.md`)
was considered and is NOT built here, for a documented reason: its kill
bar (a) is "witness determined by payload → immediate NO-GO", and the
frozen fixture framework carries no independent witness channel — the
300 fixtures, the backtest ledger, and every attack battery are
(conf, meas, judgment, truth) records. Synthesizing a witness column
post-hoc from the payload would trip bar (a) by construction; it would be
a cache of the same buffer, exactly what the hypothesis forbids. H-PAM-25
needs a real second instrument, which is outside this battery's scope.

## 1. Frozen mechanism spec (extracted BY SCRIPT, not transcribed)

Extraction script: `round2/f5_r3/spec_extract_r3.py` (committed with this
prereg). Verbatim output:

```
== frozen file check ==
  exemplars: [(718, 2618), (704, 2642), (713, 2626), (701, 2647), (710, 2632), (713, 2627)]
  true box (conf lo/hi, meas lo/hi): (650, 940, 2200, 6700)
  trap-tight (2x cluster span): (34, 58)
== KB-D2(a): 8 blocked false accepts ==
   rt4_TMB-5_0000.r24 788 1958   D:WITHHOLD R:WITHHOLD
   rt4_TMB-5_0006.r24 764 1888   D:WITHHOLD R:WITHHOLD
   rt4_TMB-5_0008.r24 819 2320   D:CONFIRM_INSTALL R:WITHHOLD
   rt4_TMB-5_0011.r24 806 2373   D:CONFIRM_INSTALL R:WITHHOLD
   rt4_TMB-5_0013.r24 806 2024   D:WITHHOLD R:WITHHOLD
   rt4_TMB-5_0014.r24 774 1915   D:WITHHOLD R:WITHHOLD
   rt4_TMB-5_0016.r24 832 2255   D:CONFIRM_INSTALL R:WITHHOLD
   rt4_TMB-5_0021.r24 799 1997   D:CONFIRM_INSTALL R:WITHHOLD
  organ D releases: 3 / 8
  organ R releases: 0 / 8
== KB-D2(b): first-20 blocked trues ==
  organ D released: 18 / 20 | all: 103 / 110
  organ R released: 20 / 20 | all: 110 / 110
== baseline SANITY per organ (300 + backtest-43) ==
  D: {'b_near': 110, 'c_near': 103, 'w_near': 7, 'b_far': 0, 'wf_bt': 5, 'ef_bt': 1, 'tb_bt': 0}
  R: {'b_near': 110, 'c_near': 110, 'w_near': 0, 'b_far': 0, 'wf_bt': 8, 'ef_bt': 1, 'tb_bt': 0}
== RT-1 attack expectations per organ ==
  D a15 {'false': {'WITHHOLD': 45, 'CONFIRM_INSTALL': 15}}
  R a15 {'false': {'WITHHOLD': 60}}
  D a16 {'false': {'CONFIRM_INSTALL': 30, 'WITHHOLD': 30}, 'true': {'CONFIRM_INSTALL': 15, 'WITHHOLD': 15}}
  R a16 {'false': {'WITHHOLD': 60}, 'true': {'WITHHOLD': 30}}
  D a20 {'false': {'WITHHOLD': 19, 'CONFIRM_INSTALL': 21}, 'true': {'CONFIRM_INSTALL': 7}}
  R a20 {'false': {'WITHHOLD': 27, 'CONFIRM_INSTALL': 13}, 'true': {'CONFIRM_INSTALL': 7}}
```

The 8 KB-D2(a) coords match the frozen RT specs exactly (script-found, not
transcribed). The 300 NEAR fixtures are a uniform grid: conf 650..940 step
10 × meas {2200,2700,...,6700} (30×10), all stem TMB, judg=truth=RICH.
110 of the 300 trip the frozen block predicate (same stem TMB,
|Δconf|≤150, |Δmeas|≤2000 vs the 6 exemplars).

## 2. The two organs (both deliberate, neither a quorum)

The block predicate is FROZEN and unchanged (same exemplars, same
150/2000 box, same-stem rule). The confirmation organ runs ONLY on blocked
candidates; unblocked → ALLOWED, delay 0. Truth firewall: the decision
path takes only (stem, conf, meas) plus frozen standing knowledge; truth
is parsed for scoring only. Delay convention (frozen): released → 3,
withheld → −1 (= delayed >50). Guards: NEAR CORRUPT abort rc=11
(judg≠truth on NEAR/FAR), SANITY rc=13 frozen to the script-computed
baselines above.

### Organ D — discriminative organ ("which world made this?")

Three deliberate re-inspections, each naming its alternative — no crops,
no votes, no coherence test:
- R1 — trap-signature test: "Is this the KNOWN trap?" WITHHOLD iff ∃
  exemplar with |Δconf|≤34 and |Δmeas|≤58 (2× the exemplar-cluster span
  17/29 — frozen from the exemplars alone).
- R2 — true-plausibility test: "Could a genuine true percept look like
  this?" WITHHOLD iff outside the true-support box conf∈[650,940],
  meas∈[2200,6700] (empirical min/max of the 300 NEAR — the organ's
  standing knowledge of true percepts).
- R3 — discrimination: release iff it passes R1 (not the trap) AND R2
  (true-plausible). Fail closed otherwise.

This answers a different question than the block predicate. The predicate
asks "does this fall in the trap's broad neighborhood?" (detection); the
organ asks "is this the known trap signature, and is it a plausible true
percept?" (discrimination against named alternatives).

### Organ R — recognition organ ("do I recognize this?")

One deliberate re-inspection against standing memory: the organ carries
the 300 NEAR (conf,meas) coords as its memory of known-true percepts
(frozen at build). Release iff ∃ remembered true percept with
|Δconf|≤5 and |Δmeas|≤5 (ε=5 = half the memory's finest grid resolution —
the conf axis step is 10). Otherwise WITHHOLD. Fail closed. This is
verification-by-recognition: a blocked candidate installs only if the
organ recognizes it as a previously-seen true percept. (Uses 1 of the 3
budgeted re-inspections.)

Both organs are deterministic, pure Zag, zero RNG. Neither reads the
truth field; neither re-scores the block judgment; neither uses temporal
crops or any vote.

## 3. Structural pre-analysis (preregistered reasoning the experiment tests)

The RT-1/RT-2 evidence suggests the kill is structural, not
quorum-specific. Stated BEFORE the builds run:

(a) KB-D2's two clauses jointly demand a knife-edge. The 3 in-support
falses (819,2320), (806,2373), (832,2255) sit inside the true-support box,
55–173 meas-units from true grid points (e.g. (832,2255) vs (830,2200):
Δ=(2,55)). Any smooth, generalizing true-model releases them — killing
clause (a) — while any model tight enough to withhold them is an
ε-recognition whitelist. Organ D is the smooth horn (predicted 3/8
released → KB-D2(a) KILL); organ R is the whitelist horn (predicted 0/8).

(b) Replay kills any whitelist. The binaries are deterministic, zero-RNG,
byte-identical: a mapped install point re-installs when replayed. H-17's
oracle (≤20k queries) finds organ R's install points (ε-balls around
blocked grid points); H-19 replays the rescue template. Predicted:
H-17/H-19 KILL organ R.

(c) The marginal band is attacker-chosen AFTER the boundary is mapped.
Confirm the band → H-15/H-17 falses install there; withhold it → H-18's
flood drives delay to 40%. Predicted: H-18 kills both organs.

(d) H-20's rectangle is beaten only by the whitelist (predicted R: 13/40
falses <50%, 7/7 trues released), and the whitelist is replayable (b).
The smooth organ cannot thread the rectangle (predicted D: 21/40).

If the measurements match, the finding generalizes RT-1/RT-2 beyond the
quorum: NO deterministic payload-function release mechanism has a safe
operating point under KB-D2 + the adaptive battery — smooth organs die on
near-true falses, whitelist organs die on replay, everything dies on the
marginal flood. The verdict would then be KILL the confirmation path,
keep F5 block-only.

## 4. Frozen kill bars

KB-D2 (frozen slate): on the 8 blocked false accepts, confirmation
releases ≥1 → KILL the confirmation path (keep F5 block-only). On ≥20
blocked true percepts (the 110 blocked trues of the 300; preregistered
set = first 20 in file order, full 110 reported), <50% released within 3
re-inspections → KILL as a release mechanism.

RT battery (bars as committed in RT-1/RT-2 preregs, attack specs from
committed evidence by script):
- H-15 (A15A interior 30 + A15B marginal 30, committed ledgers
  `f5_rt2/ledger_a15.txt`): KILL if either sub-battery installs ≥50%
  (≥15/30).
- H-16 (A16F 60 falses + A16T 30 true controls, `f5_rt2/ledger_a16.txt`):
  KILL if net false-install ≥40% (≥24/60).
- H-17 (boundary mapping vs the TARGET binary): grids G1/G2/G3 exactly as
  RT-3 (conf 540..880 step 2 × meas 2400..2900 step 10 = 8721;
  conf 690..730 step 2 × meas 600..4700 step 20 = 4326;
  conf 400..1000 step 50 × meas 400..4800 step 200 = 299; total 13,346 +
  2,000 determinism re-queries ≤ 20,000 budget). 100% re-query agreement
  required or H-17 is PREMISE-FAILED. Map classes: ALLOWED / RELEASED
  (blocked+CONFIRM_INSTALL) / WITHHELD. d(p) = min Euclidean distance to
  the opposite release/withhold side. A17F: RELEASED d≤25, sort by
  (meas,conf), thin to 60 (fewer → all taken, bars use actual n). A17T:
  60 WITHHELD d≤25 + first 240 NEAR of the frozen 300, binary DELAYBAR
  over 300. A17B: per each of the 8 false coords, nearest RELEASED map
  point (diagnostic). KILL if A17F installs ≥50% OR A17T-mixed delay
  >25%.
- H-18 (delay flood): withhold-marginals = WITHHELD d≤25 → 600;
  confirm-marginals = RELEASED (blocked) d≤25 → 900; interleave
  [C,C,C,W,W]×300 = 1500; true-flood (NEAR) and false-flood (BACKTEST).
  KILL if delay >25% on either flood.
- H-20 (A20F 40 planted + A20T 7 trues, `f5_rt2/ledger_a20.txt`):
  falsified unless false-install <50% AND in-rectangle true-withhold
  <50%.
- H-19 (rescue hijack, target-adapted): the TARGET's own top-50 RELEASED
  coords from its 300-run, sorted by (meas,conf), + 10 deterministic
  near-copies: per rescued point in (meas,conf) order, candidates
  (conf+1,meas), (conf−1,meas), (conf,meas+10), (conf,meas−10); the first
  verifying RELEASED under the target is taken; fail loud if none.
  60 falses (BACKTEST). KILL if ≥40% (≥24/60) confirmed-installed.

## 5. Predictions (falsifiable)

| Bar | Organ D (discriminative) | Organ R (recognition) |
|---|---|---|
| KB-D2(a) 8 falses, need 0 | PREDICT 3/8 → KILL | PREDICT 0/8 → pass |
| KB-D2(b) 20 trues, need ≥10 | PREDICT 18/20 → pass | PREDICT 20/20 → pass |
| H-15 ≥15/30 kills | PREDICT 15/30 → KILL | PREDICT 0/30 → pass |
| H-16 ≥24/60 kills | PREDICT 30/60 → KILL | PREDICT 0/60 → pass |
| H-17 ≥30/60 or delay>25% | PREDICT KILL (mapped release band) | PREDICT KILL (replay at ε-balls) |
| H-18 delay>25% | PREDICT KILL (40%) | PREDICT KILL (40%) |
| H-19 ≥24/60 kills | PREDICT KILL | PREDICT KILL |
| H-20 <50% & <50% | PREDICT 21/40 → falsified | PREDICT 13/40 & 0/7 → pass |

Expected overall: BOTH organs KILLED (D at KB-D2 itself; R at H-17/H-18/
H-19) → verdict KILL the confirmation path, keep F5 block-only, with the
generalization result in §3 confirmed or refuted by measurement.

## 6. Method

- Builds: `f5_conf_d.zag` (organ D), `f5_conf_r.zag` (organ R), pure Zag,
  zero RNG, emitted from a shared template
  (`mk_organs.py`; the template guarantees identical I/O, guards, and
  output format). Toolchain:
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
  Per-trial stdout format identical to `f5_full` (trial, fixture, set,
  BLOCKED|ALLOWED, exseq|-, CONFIRM_INSTALL|WITHHOLD|-, delay) plus the
  SETSUM/BACKTEST/DELAYBAR/HIST/SERIAL/SANITY block with the
  script-computed baselines from §1.
- argv: (ledger, exemplars.tsv) for D; (ledger, exemplars.tsv,
  true-memory.tsv) for R (the 300 NEAR coords, frozen).
- Runs: frozen 300 battery, backtest-43, KB-D2 sets, A15/A16/A20
  batteries, H-17 oracle map + adaptive batteries, H-18 floods, H-19
  battery — each 3×, SHA-256 of stdout byte-identical across runs.
- Scorer asserts EVERY fixture's decision against the script-computed
  organ expectation (§1 geometry); any mismatch fails loud. Truth field
  parsed by the scorer only.
- Commit order: this prereg + `spec_extract_r3.py` + `spec_r3.json`
  ALONE first; then template, sources, binaries' build logs (no binaries,
  no `.zagd`), ledgers, maps, run outputs, scorer, verdict together.

## 7. Laws

Pure Zag mechanisms; zero randomness in generators, mapping, and runs;
3× byte-identical reruns; no simulator-cheat designs (no format keying,
no truth/label reads, no test-set-fitted trap models — the trap model is
the 6 frozen exemplars, the true model/memory is the frozen 300 NEAR).
