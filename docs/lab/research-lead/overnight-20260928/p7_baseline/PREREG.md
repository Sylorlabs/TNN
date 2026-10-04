# PREREG: P7-BASELINE — does the P7B belief learner beat the best simple baseline?

Worker: **P7-BASELINE**, 2026-10-04. Non-ledger lane.
Lane: `docs/lab/research-lead/overnight-20260928/p7_baseline/`
Branch: `lane/p7baseline`, base `8d35e2ce4` (the P7B lane HEAD).
Target under attack: `lane/p7belief` verdict **P7B-PASS 41/42**, claim **C503**
("a measurement channel's usefulness is learned from history, not declared; the
learner beats random and is not the fixed-query policy"), which the P7B lane
itself marked **Falsified: FP-M9** because the learner *tied* the fixed
non-adaptive query (both 15 information, both +100 payoff).

**Charter 79 governs:** if the simple baseline is not beaten, no intelligence
claim is made. This prereg exists to settle that, and to produce an honest
DOWNGRADE if the tie survives a stronger adversarial baseline family.

Frozen BEFORE any implementation. Nothing below moves after a run. Where a
prediction is wrong it is reported as a FAIL, not re-derived.

---

## 0. What is reused and what is new

REUSED VERBATIM (sha256 attested at run time, must match):
- `xf_block.zag` — the frozen TNN-2 block, 2668 lines, sha256 prefix
  `172a2e7dbbaa4e60d662` (copied from `p7_belief_inquiry/p7b_full.zag` lines
  1..2668; must equal the P7B REPORT's stated
  `172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a`).
- `p7b_learner_ref.zag` — the P7B learner's 1012 lines, **byte-identical**.
  It is never edited. The learner under attack is the artefact under test; a
  modified learner would not be the P7B result.

NEW: `p7x_driver.zag` only. It adds (a) 10 baseline selectors, (b) a
parameterised world generator, (c) the new arms NR/TR/DP/PD, (d) the
toolchain probes are separate small files. It adds **no** new learner
function and changes **no** line of `p7b_learner_ref.zag`.

The learner is therefore evaluated *exactly as P7B shipped it*, which is the
only way the P7B verdict can be adjudicated.

---

## 1. Structural invariants (checked in-driver, binary)

| id | invariant | kill condition |
|---|---|---|
| **SX-1** | learner file byte-identical to P7B's | sha256 differs → all bars VOID |
| **SX-2** | frozen block byte-identical to P7B's | sha256 differs → all bars VOID |
| **SX-3** | no inquiry mode label introduced by this lane | grep for `(if\|while)\(.*(uncert\|inquire\|mode\|need_info\|do_ask\|probe_mode)` over both lane files returns 0 |
| **SX-4** | no `_zag_raw_syscall` in this lane | grep returns 0 |
| **SX-5** | output non-empty | total bars emitted ≥ 60 and total bytes ≥ 1500 |
| **SX-6** | 3 of 3 byte-identical | `zbuild.sh --rep 3` |
| **SX-7** | pure Zag | `tnn_pure_zag_report` → `PURE-ZAG-CLEAN` |
| **SX-8** | every run behind the watchdog | `$W reg <name> <secs> ./bin`; no bare `./bin` |

---

## 2. THE BASELINE FAMILY (frozen, 10 members)

A baseline is a **selector**: a function from the current structural state to an
action code. It uses the same observable state the learner uses — the probe
candidate list in node-id order (`p7b_probe(i)`), each probe's channel
(`p7b_ch`), its declared cost (node field 28) and declared accuracy prior (node
field 32), the current mass vector, the learner's contingency table `C`, and the
run log. A baseline never calls `p7b_val`, never recurses on option value, and
never reads a state label. Each is one `if`-chain returning one action code.

Index `i` ranges over the `NP` candidate probes in scan order. A probe is
*unlicensed* iff `p7b_usedat(S,i)==0`. `nrun` = `get32(S,84)`.

| id | name | rule | tag |
|---|---|---|---|
| **B0** | WAIT | `SAFE` always | NONADAPT |
| **B1** | FIXED_FIRST | smallest unlicensed index (this is P7B's `p7b_sel_fixed`) | NONADAPT |
| **B2** | ROUNDROBIN | the `(nrun mod NP)`-th unlicensed probe in scan order | NONADAPT |
| **B3** | CHEAPEST | argmin declared cost, tie → smallest index | NONADAPT |
| **B4** | PRIOR_ACC | argmax declared accuracy prior, tie → smallest index. *This is the mission's "always probe the channel with the highest PRIOR".* | NONADAPT |
| **B5** | LAST_SUCCESS | channel of the most recent run in the run log whose contingency row was non-flat; the first unlicensed probe on that channel; if no such run, index 0 | ADAPT |
| **B6** | WIDEST_INTERVAL | argmax of (top1 − top2) of the posterior branch under that probe's channel using `C`; tie → smallest index. *Mission's "widest prior interval".* | ADAPT |
| **B7** | FIXED_ORDER_STOP | fixed index order; if some already-run probe produced a strict rise in top share, stop probing and `COMMIT` the argmax; else index 0. *Mission's "stop at first positive signal".* | ADAPT |
| **B8** | EIG1 | argmax one-step expected Gini reduction Σ L_o (gini(cur) − gini(branch_o)) / Σ L_o under `C`; tie → smallest index. **Myopic: no recursion, no payoff, no option value.** | ADAPT |
| **B9** | LAST_SPEAKER | `COMMIT(h)` for the last ledger claim's hypothesis (charter-79 stupid) | ADAPT |
| **B10** | RANDOM30 | uniform over {0,1} ∪ unlicensed probes, LCG seeded `1000+37j`, `j=0..29`, mean over the 30 seeds | ADAPT |

Plus **LEARN** = `p7b_sel_learn` (P7B's `p7b_val`), unchanged.

**Reported quantities**
- `BASEMAX` = max over the 10 baselines of the number of worlds in which that
  baseline realises payoff `== C_RIGHT`. Also reported per stratum.
- `BASEMAX_NONA` = same over {B0,B1,B2,B3,B4}.
- `BASEMAX_ADA` = same over {B5,B6,B7,B8,B9,B10}.
- Per world, the identity of the argmax baseline and the full 11-way payoff
  vector are printed, so no aggregate hides a world.

**Decision rule, frozen:** LEARN is declared to *beat the simple baseline* iff
(a) `win(LEARN) > BASEMAX`, AND (b) the one-sided exact Clopper–Pearson 95%
lower confidence bound on the paired win-rate `win(LEARN) − BASEMAX` over the
frozen world set exceeds 0, AND (c) `win(LEARN) > BASEMAX` in **every** stratum.
A tie in any stratum forces the DOWNGRADE verdict.

---

## 3. THE FROZEN WORLD SCHEDULE

A world `w` is `(q, NP, D, PA, PERM, C_RIGHT, C_WRONG, C_PROBE, CAL)`:
- `NP` candidate probes, node-id order = position 0..NP-1.
- Position `D` is the **discriminative** probe. Its channel `kD` is trained
  sharp (outcome `o` ⇒ hypothesis `o`). All other channels are trained flat.
- `worldout(k)`: `k==kD` → outcome 1; else outcome 0. Deterministic.
- `PA=1`: declared accuracy prior `acc(D)=200`, `acc(others)=60`
  (discoverable from priors alone). `PA=0`: all `acc=128` (not discoverable).
- declared cost: `cost(D)=200`, `cost(others)=20` unless the stratum overrides.
- `PERM` assigns channel codes `0..NP-1` to positions (identity by default).
- `CAL=1`: channels trained in-session on 3 revealed-truth questions first
  (P7B's CAL protocol, generalised to `NP` channels). `CAL=0`: no history.

**Grid A — luck quantification (35 worlds, full enumeration).**
`NP ∈ {2,3,4,5,6,7,8}`, `D ∈ {0..NP-1}`, `PA=0`, `PERM=id`, `CAL=1`,
`(C_RIGHT,C_WRONG,C_PROBE)=(100,100,6)`. Total 35.
*Frozen prediction P-A1:* B1 (FIXED_FIRST) is lucky on exactly the `D=0` worlds,
i.e. **7 of 35**, rate 20.0%; and its rate within stratum `NP` is exactly
`1/NP`. Any other value falsifies P-A1.
*Frozen prediction P-A2:* LEARN's channel equals `kD` in **35 of 35**.

**Grid B — prior-discoverable (24 worlds).**
`NP ∈ {4,8}`, `D ∈ {0..NP-1}`, `PA ∈ {0,1}`, `PERM=id`, `CAL=1`. Total 24.
*Frozen prediction P-B1:* in the `PA=1` stratum B4 (PRIOR_ACC) reaches the
maximum possible and ties LEARN on payoff in **12 of 12** worlds.
*Frozen prediction P-B2:* in the `PA=0` stratum B4 is at chance and LEARN
reaches `kD` in **12 of 12**.

**Grid C — position vs channel (8 worlds).**
`NP=8`, `D=0`, `PA=0`, `CAL=1`, channel codes assigned to positions by the 8
frozen permutations:

| perm | codes at positions 0..7 |
|---|---|
| P0 | 0 1 2 3 4 5 6 7 (identity) |
| P1 | 7 6 5 4 3 2 1 0 (reverse) |
| P2 | 0 2 4 6 1 3 5 7 (stride 2 from 0) |
| P3 | 1 3 5 7 0 2 4 6 (stride 2 from 1) |
| P4 | 3 5 7 1 4 0 2 6 (stride 2 from 3) |
| P5 | 0 4 1 5 2 6 3 7 (stride 4 from 0) |
| P6 | 6 4 2 0 7 5 3 1 (stride 2 from 6) |
| P7 | 2 6 3 7 0 4 1 5 (stride 4 from 2) |

The discriminative CHANNEL is `kD=3` in every Grid C world.
*Frozen prediction P-C1:* LEARN probes channel 3 in **8 of 8** worlds, i.e. it
keys on the learned channel, not on position.
*Frozen prediction P-C2:* B1 is lucky in **1 of 8** (only P0, where position 0
carries channel 3).

**Total main-comparison worlds: 67.**

---

## 4. THE VARIANCE QUESTION, frozen

- LEARN is deterministic; the only seed is B10's LCG. So "variance across
  seeds" is reported three ways, all integer:
  1. **Across worlds**: mean, min, max, and the 5th/95th percentile (by
     integer order statistic) of `INF(LEARN,w)` and of
     `INF(LEARN,w) − max_p INF(p,w)`.
  2. **Across seeds for B10**: mean and min/max of `INF(B10,·,j)` over the 30
     frozen seeds, pooled over the 67 worlds.
  3. **Paired margin**: per world `d_w = INF(LEARN,w) − max_p INF(p,w)`.
     `d̄`, `min d_w`, `max d_w`, and the count `#{w : d_w>0}`, `#{d_w=0}`,
     `#{d_w<0}`.
- **Exact interval.** With `n` worlds and `k` paired wins and 0 losses, the
  one-sided exact 95% Clopper–Pearson lower bound is the largest rational
  `A/D` (D = 1000) with `20·A^n ≥ (n+1)·D^n`, computed by the exact integer
  chain `r←20; repeat n times: r ← (r·A)/D` (each step floors, so the test
  `r ≥ n+1` is conservative and exact). Reported in per-mille.
- **Number of worlds needed.** For a pre-registered fixed baseline with
  per-world luck probability `q`, the number of worlds on which it must be
  observed to lose, every time, for that to be a 95% result, is the smallest
  `k` with `(1−q)^k ≥ 0.05`, i.e. `k ≥ ln 0.05 / ln(1−q)`. Computed by exact
  integer search on the same rational grid. Reported for `q = 1/2 … 1/8`.

---

## 5. ARM NR — the never-run channel (the lane's own unrun next experiment)

| id | construction | frozen prediction |
|---|---|---|
| **NR-A** | discriminative channel is **never run** (fresh row), the flat channel IS calibrated flat, contested posterior | action ≠ `COMMIT`; status = `REP-INS`(5); `maxgain < mbrk`. **Calibration is learned, not optimism.** |
| **NR-B** | NR-A then run the never-run channel 6× with uninformative outcomes, each followed by `p7b_resolve(truth)` | `p7b_rowflat==1`; status still `REP-INS`(5); action ≠ `COMMIT` |
| **NR-C** | a never-run channel that IS discriminative: run it once, reveal truth, then re-decide | LEARN's chosen channel == the newly calibrated channel (one-shot calibration works) |
| **NR-D** | zero claims, 3 hypotheses, no probes, payoffs 100/100 | action ≠ `COMMIT`. Pure prior never commits. |

**Kill bar NR-K:** if NR-A or NR-D commits on the prior, the `+1` smoothing
prior is a hardcoded optimism bias and **C503 is DOWNGRADED to a non-adaptive
result regardless of what section 2 measures.**

---

## 6. ARM TR — transfer to a new world with a different payoff structure

- Train `C` on questions 700+g, g=0..2, channels 0..2 sharp, 3..7 flat,
  truth revealed (P7B's CAL protocol, 8 channels).
- **TR-A** transfer world: new q, new claim set, discriminative channel 3
  (never trained during calibration), payoffs `(250,10,6)`.
  *Prediction P-TR1:* LEARN probes channel 3 and realises `+250`.
  *Prediction P-TR2:* the contingency is not re-initialised by the world
  switch (`p7b_ledger_reset` preserves it) — attested by non-zero `C[3][·][1]`.
- **TR-B** same but payoffs `(10,250,6)`. *Prediction P-TR3:* `mbrk` rises from
  31 to 245, so LEARN's status/commit decision changes even though `C` and the
  evidence are byte-identical to TR-A.
- **TR-C** trained in world X, evaluated in world Y with a *permuted* channel
  assignment, to separate "transferred calibration" from "memorised index".

---

## 7. ARM DP — provenance depth 3, 4, 5 (charter 133)

Self-generated inference chains: root observation `A`, then `k` links of
`kind=2` (self-inference) each with parent = previous link and a declared
dependency fraction `f`. Depth `k ∈ {1,2,3,4,5}`.

| id | `f` | frozen prediction | charter reading |
|---|---|---|---|
| **DP-0** | 255 | residual 0 at depth ≥ 1, `P` unchanged, all records live | 133 HOLDS |
| **DP-128** | 128 | residual strictly decreasing in depth; chain total ≤ 255 (no amplification) | 133 HOLDS |
| **DP-0dep** | 0 | **UNRESOLVED — no prereg prediction.** The declared dependence is zero, so the learner's residual rule gives full mass at every depth. Whether `P` inflates linearly with depth is the measurement. | if it inflates, **133 is VIOLATED whenever a writer declares `f=0` on a self-inference** |

Kill bars:
- **DP-K1** `f=0`: `P(depth 5) == P(depth 1)`. Prediction **FAIL** (P inflates).
- **DP-K2** `f=128`: chain total mass at depth 5 ≤ mass at depth 1.
- **DP-K3** `f=255`: chain total mass == 0 and `P` unchanged at every depth.
- **DP-K4** no record is ever deleted at any depth and any `f` (`p7b_live`
  constant), i.e. the inflation is arithmetic, not a deletion artefact.
- **DP-K5** the depth at which the inflated top share first crosses the commit
  bar `mbrk` is reported, and the same world re-run under `f=128` and `f=255`.

Also recorded: **the kind field (ledger field 8) is read by nothing in
`p7b_mass` or `p7b_resid`.** Grep attestation for `(kind)` in the mass path
returns 0 uses. So the only thing preventing self-inference from counting as
corroboration is the *declared* dependence fraction. That is the charter-133
exposure and DP measures it.

---

## 8. ARM PD — partial dependence (charter 131)

Construction: root claim `A` read by source 1. Sources 2 and 3 each file a
**distinct** claim (own ledger record, own store node, own content) that has `A`
as parent — shared ancestor, **not** identical content. Dependency fraction `d`
swept over `{0,64,128,192,255}`.

| id | frozen prediction |
|---|---|
| **PD-K1** | total mass `T(d) = m(A)+m(B2)+m(B3)` is strictly increasing in `d` |
| **PD-K2** | `T(255) == m(A)` |
| **PD-K3** | `T(d) < 3·m(A)` for every `d ≥ 64` |
| **PD-K4** | `T(0) == 3·m(A)`: with dependence declared zero the two shared-ancestor claims are counted as fully independent |
| **PD-K5** | the store *does* contain the ancestry (both claims have a type-2 edge to `A`) while `T(0) == 3·m(A)` — the learner holds the evidence of shared ancestry and does not use it. **This is the charter-131 hole.** |
| **PD-K6** | a claim with **two** parents takes `min` residual over them (the conservative rule), and `m < min(m(A),m(B))` |
| **PD-K7** | `T(d) ≤ 3·m(A)` for all `d` — no amplification anywhere |

---

## 9. ARM TC — the toolchain claim, adjudicated

The P7B lane reported the compiler "silently miscompiles forward function
references into a hang". Two analogous claims were refuted elsewhere. Frozen
probes, each a separate small file, each behind the watchdog:

| id | probe | expected |
|---|---|---|
| **TC-A** | `main` → `fwd_a` → `fwd_b`, `fwd_b` defined **after** `fwd_a`, plus mutual recursion `fwd_b` self-recursing with a base case | compiles and runs; `fwd_a(15)=611` |
| **TC-B** | the `get32`/`set32` **byte**-offset trap: same logical cell read at the wrong byte offset | `good=222`, `bad=0`, **no error of any kind** — the silent-wrong-answer mechanism |
| **TC-C** | mutual recursion with **no** base case (the only real hang in Zag) | `SIGSEGV` rc=139 **after** printing its entry marker — a program stack overflow, not a compiler hang |
| **TC-D** | forward reference into a flat arena with byte offsets, the exact P7B idiom, checked at all 16 cell offsets | exact, and 3/3 byte-identical |

Kill bar **TC-K:** if TC-A and TC-D are exact and TC-B reproduces a silent
wrong answer, the "forward reference miscompilation" claim is **REFUTED** and
TC-B is the mechanism that produced such reports. Note explicitly that a
reporter who built `true at position k` as `1==2` would produce the same
symptom class as TC-B and neither is a compiler defect.

---

## 10. Frozen predictions, collected

| id | prediction | consequence if wrong |
|---|---|---|
| P-A1 | B1 lucky on 7/35 Grid-A worlds, rate 1/NP per stratum | the luck model is wrong; section 4's world count is wrong |
| P-A2 | LEARN hits `kD` in 35/35 | the learner's discrimination is partial; **DOWNGRADE** |
| P-B1 | B4 ties LEARN in 12/12 `PA=1` worlds | adaptivity is *not* needed where priors suffice |
| P-B2 | LEARN hits `kD` in 12/12 `PA=0` worlds | as P-A2 |
| P-C1 | LEARN probes channel 3 in 8/8 permuted worlds | the learner keys on POSITION, not channel — that is a lookup, not calibration; **DOWNGRADE** |
| P-C2 | B1 lucky in 1/8 | — |
| P-TR1 | LEARN transfers, probes channel 3, `+250` | no transfer claim |
| P-TR3 | status flips between TR-A and TR-B | consequence scalars are not actually used |
| P-NR-A/D | no commit on a pure prior | **hardcoded optimism; DOWNGRADE (NR-K)** |
| P-DP-K1 | **expected FAIL**: `f=0` self-inference inflates `P` with depth | if it passes, `kind` is load-bearing after all |
| P-PD-K5 | **expected FAIL**: `T(0)==3m(A)` with ancestry present in the store | if it passes, ancestry is used |

---

## 11. Kill bars (any one voids the affected conclusion)

- **SX-1/SX-2** any hash mismatch → every bar VOID, run reported as PROCESS-FAIL.
- **SX-6** < 3/3 byte-identical → PROCESS-FAIL.
- **SX-5** empty output → PROCESS-FAIL, not a result.
- **SX-3/SX-4** any mode-label or raw-syscall hit → PROCESS-FAIL.
- Any run exceeding its watchdog limit → recorded **TIMEOUT**, counted as FAIL,
  **never** re-run with a larger limit.
- Stale binary: build with `tools/zbuild.sh`, which removes the old binary first.
- Load average above 30 at launch → still run, but report the load, and never
  launch more than one binary at a time.

## 12. Watchdog schedule (frozen limits, not extended after a miss)

| run | contents | limit |
|---|---|---|
| `p7x_tc` | TC-A..TC-D | 120 s each |
| `p7x_gridA` | Grid A, 35 worlds × 11 policies | 600 s |
| `p7x_gridB` | Grid B, 24 worlds × 11 policies | 600 s |
| `p7x_gridC` | Grid C, 8 worlds × 11 policies | 600 s |
| `p7x_arms` | NR, TR, DP, PD | 600 s |

If a grid run TIMEOUTs, it is split into the next run's budget by `NP` strata,
each with its own 600 s limit, and the split is recorded. It is not given more
time in one process.

## 13. Claim IDs

C7xx block only. Candidate claims, minted **only if the bars support them**:
- **C700** the P7B belief learner's inquiry decision does NOT beat the best
  member of the frozen 10-member non-adaptive/semi-adaptive baseline family
  across the frozen 67-world schedule.
- **C701** a single world cannot establish adaptivity: a pre-registered fixed
  order is lucky with probability 1/NP, and the number of worlds required for a
  95% result is as computed.
- **C702** where the discriminative channel is discoverable from the declared
  prior alone, a non-adaptive prior-follower ties the learner, so the measured
  advantage lives entirely in the not-discoverable stratum.
- **C703** self-generated inference with a declared dependence fraction of 0
  is counted as independent corroboration, scaling the belief with provenance
  depth; the charter-133 prohibition holds only as long as some writer declares
  a non-zero fraction.
- **C704** partial dependence between sources that share an ancestor is
  discounted only to the extent the writer declares; undeclared shared ancestry
  is visible in the store and unused.
- **C705** the "forward function reference miscompilation" is REFUTED; the
  `get32`/`set32` byte-offset trap reproduces the same silent-wrong-answer
  symptom with no compiler defect.
- **C706** (conditional) the learner's channel calibration transfers to a new
  world with a different payoff structure.

**Not claimed:** L3, open-form invention, anything about C377–C466, or any
intelligence claim if the DOWNGRADE verdict fires.