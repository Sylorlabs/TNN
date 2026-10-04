# PREREG: P7-BELIEF-INQUIRY (competing hypotheses, dependent evidence, one distinguishing experiment)

Worker: P7-BELIEF-INQUIRY, 2026-10-03. Non-ledger lane; claims minted
under the C5xx block (see Section 9).
Lane: `docs/lab/research-lead/overnight-20260928/p7_belief_inquiry/`
Status: **FROZEN.** Committed before any implementation `.zag` file
exists in this lane. Section 5 (amendment log) is empty at commit.

Charter anchors: 26 (9 required cases, score vs available evidence not
hidden truth), 27 (competing beliefs, both represented, unresolved
flag, history preserved, deletion is not revision), 28 / 108 (NO
INQUIRY MODE LABEL), 46 / 74 (derived epistemic status), 79 (stupid
baseline), 129 (rational ignorance), 131 (partial dependence), 133
(self-inference is not corroboration).

## 0. The question this lane asks

Can TNN, given only its own evidence record, (a) keep two competing
hypotheses alive without collapsing either, (b) refuse to count three
echoes of one copied report as three observations, (c) choose the
experiment that actually separates the hypotheses over random inquiry,
passive waiting, or a fixed researcher-chosen query, and (d) update
belief on the outcome, all **without any hardcoded inquiry branch**?

## 1. THE STRUCTURAL INVARIANT (the hard rule, charter 28 / 108)

**SI-1. One decision rule, one candidate set, one argmax.**
The learner contains exactly ONE selector. It builds a candidate set
by enumerating *what the frozen store structurally offers*, scores
every candidate with the SAME utility function, and takes the strict
argmax. The candidate kinds are:

- `COMMIT(h)`: present only if the **frozen** `bp2_select` over the MAP
  belief nodes licensing the question's hypothesis facts returns a node
  (it returns `-3` on an exact top tie or when `eff < bar`, so the
  frozen layer, not this lane, decides whether commitment is available).
- `RUN(p)`: one per **structurally discovered** probe, where a probe is
  a live tag-1 node whose `field20 == Q` and whose `field24` lies in the
  channel range `[900,990)` (the range TNN-2 already uses for its
  policy/query nodes), and which no MAP belief licenses yet.
- `SAFE`: always present while steps remain.
- `WITHHOLD`: always present, value `-C_DEADLINE`.

Inquiry is not a member of this list. `RUN` competes on utility with
the other three and wins only when its computed value is highest.

**SI-2. Uncertainty is DERIVED, never stored.** No array slot, node
field, or edge field in the learner ever holds a boolean named for
inquiry, uncertainty, contest, or mode. Every `if` in
`p7b_learner.zag` tests a structural integer (liveness, a count, a
mass, a field equality, an argmax comparison). The frozen layer's own
`-3` refusal is a *numeric return value* of a frozen function, not a
mode.

**SI-3. Epistemic status is a function of (mass record, probe
availability, consequence scalars).** The six status strings in
Section 3.6 are produced by a pure derivation over computed
quantities. Disclosed honestly: the TAXONOMY (six names, fixed
priority order) is researcher-authored, as in every lane that reports a
status; the ASSIGNMENT of a status to a state is not, and the
consequence-sensitivity bar K-B33 tests that.

**SI-4. One evidence path.** A probe result is appended to the claim
ledger by exactly the same call that appends a witness report. There is
no `if (this is an experiment) then ...` anywhere.

**SI-5. Grep-verifiable.** `grep -c -E 'uncert|inquire|inquiry_mode|
do_ask|need_info' p7b_learner.zag` returns 0 matches in any `if`
condition. Recorded as part of K-HYG.

## 2. Machinery (frozen in this prereg)

### 2.1 Substrate, reused verbatim
- `xhier_countmap_fix/xf_block.zag`, SHA-256
  `172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a`
  (re-verified before and after the build, K-HYG). Provides
  `tnn2_init`, `alloc_node`, `link_edge`, `ev_teach`, `ev_teach_in`,
  `ev_observe`, `ev_query`, `ev_act`, `miss_inquire`, `promote_graph`,
  `pol_get`, `pol_set`, `log_ev`, `ctx_push`, `ctx_get`, `ng/ns/eg/es`.
- `belief_provenance_9/bp9_learner.zag`, SHA-256
  `2de20f5a0ff87bc45140a161548b613b008e9c2adda6d6d46040c5e`, copied
  verbatim as `p7b_learner.zag`'s prefix section: the 8-u8 belief table,
  R1-R7, `eff()`, `bp2_retire`, `bp2_relicense`, `bp2_bar_after`.
  **Zero changes to any `bp2_*` function.**

### 2.2 Block facts probe-measured 2026-10-03 (pure Zag, this host)
Probe source `pr2.zag`, two binaries, one per probe round, run under
`. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh`.

- **PB1** `ev_teach(W,801,90,101)` returns node 2. A second
  `ev_observe(W,801,90,102)` returns **0** (it returns a match/
  contradiction flag, not a node id), creates a new tag-1 fact node 4
  carrying `field28==102`, writes one type-3 self-edge on node 2, and
  one type-4 edge `4 -> 2`. A third `ev_observe(W,801,90,103)` returns
  0, creates node 6, writes a second type-3 self-edge on node 4 and a
  type-4 edge `6 -> 4`. **The frozen store therefore already represents
  three competing hypotheses about one (s,r) as three facts chained by
  type-3 (contradict) and type-4 (ref) edges**, and the first fact
  becomes `is_superseded`.
- **PB2** `promote_graph` over `[fact]` per hypothesis, then `bp2_form`,
  gives each MAP belief `b_sup==100`, `b_ext==1`, `formed==1`.
  `bp2_select` over the three with bar 50 returns **`-3`** (exact top
  tie). After one `bp2_confirm(m2,indep=1)` the record is 120 vs 100,
  `eff` 120 vs 100, and `bp2_select` returns m2. **The frozen layer
  refuses to select under a tie and resolves under a margin.** This is
  the structural uncertainty signal this lane uses; it is not written
  by this lane.
- **PB3** Probe facts are discoverable by structure: tag-1 nodes with
  `field20==Q` and `field24==901` / `902` are each found by scan.
- **PB4** Licensing marks use: `promote_graph(W,-1,Q,901,0,[pA],1)`
  makes `bp2_lic_live(W,mA)==1`, so "probe already run" is read from the
  store's own licensing structure, with no extra flag. Caveat recorded:
  `promote_graph` internally calls `ev_teach_in`, so the raw count of
  tag-1 nodes with a given `(field20,field24)` grows by one per MAP
  formed; the used-test is therefore the licensing test, not a count.
- **PB5** A type-2 edge's `field12` is preserved verbatim: two type-2
  out-edges from one claim with `field12` 255 and 128 are both
  readable. **The dependency fraction rides on an existing edge field of
  an existing edge type (2 = ET_SUP).**
- **PB6** `bp2_revise` halves `b_sup`, zeroes conf/disc, increments
  `b_rev`.
- **PB7** `tnn2_init` zeroes all 110656 bytes and all 4096 edge slots,
  so a fresh scenario per case costs nothing and no case can see
  another's nodes.
- **PB8** Node budget: the probe worlds used 15 nodes and 35 edges,
  far inside `NN()==1024` / `NE()==4096`.

### 2.3 New machinery this lane (the honest accounting)
New LEARNER functions, all in `p7b_learner.zag`:

1. **Append-only claim ledger.** 16 i32 fields per claim:
   `q, src, val, parent, dep, residual, root, kind, mass, step, live`.
   `kind`: 0 testimony, 1 direct observation, 2 self-inference. This is
   a record schema, not a control mode; nothing branches on `kind` to
   change arithmetic (case 11 and case 9 use the same code path).
2. **Provenance resolution.** `residual(root claim) = 255`;
   `residual(c) = residual(parent) * (255 - dep(c)) / 255`. A claim
   with no parent is a root. `root(c) = root(parent)` when a parent
   exists. Multi-parent ancestry is expressible (several type-2
   out-edges); the residual of a multi-parent claim is the residual of
   its **lowest** parent, which is the conservative (smallest) choice.
3. **Source reliability.** Beta(1,1) posterior mean on the 255 scale:
   `rel(s) = (1 + hits_s) * 255 / (2 + hits_s + misses_s)`, so
   `rel = 128` with no record. Updated only when the world's truth for
   a resolved question becomes known, by scoring every live
   `kind in {0,1}` claim from `s` on that question. Reliability is
   symmetric in direction, so both lying and rehabilitation are
   reachable by the same update.
4. **Mass recomputation.** For every live claim,
   `mass(c) = 255 * residual(c) * rel(src(c)) / 65025`.
   `w[h] = prior(h) + sum of mass(c) over live claims with `val(c)==h`.
   `prior(h) = 32 + RESOLVED_H[h]*255/(1 + RESOLVED_TOTAL)`, i.e. a
   flat 32 floor plus the learned base rate, 32 when nothing is
   resolved. `W = sum_h w[h]`; `P[h] = w[h]*255/W`.
   **Masses are recomputed from the ledger on every change; they are
   never decremented in place. Belief revision is recomputation over a
   preserved history, so no record is ever deleted to revise.**
5. **Claim-to-store sync.** After each recompute the MAP belief for
   hypothesis `h` gets `b_sup = P[h]` (so `eff()` returns `P[h]` when
   `b_ext=1, b_self=0`), one `bp2_confirm(m_h, indep)` per live claim
   with `residual>0` asserting `h`, one `bp2_disconfirm(m_h)` per such
   claim asserting a different `h`, and one `bp2_revise(m_h')` plus a
   `bp2_retire`-style kind-3 self-edge with `field12 = 1` (REVISION
   reason, novel `field12` VALUE on the pre-existing kind-3 edge type
   already written by `bp2_retire`) whenever the question's argmax
   hypothesis changes. `b_sup` is written last, so the frozen rules'
   counters survive while the support value stays ledger-derived.
   **The frozen R2/R3/R5 rules are themselves dependence-gated**,
   because a copied claim has `residual==0` and therefore applies no
   frozen rule at all.
6. **Probe-channel contingency.** `C[k][h][o]`, up to 8 channels x 6
   hypotheses x 6 outcomes, counts of "channel k reported outcome o on
   an occasion whose truth was h". Trained only when truth is known.
   `num[k][h][o] = C[k][h][o] + 1`; `den[k][h] = sum_o num[k][h][o]`;
   `P(o|h,k) = num[k][h][o]/den[k][h]`. The `+1` is uniform smoothing,
   so an **unseen channel is exactly uninformative** and an
   `argmax_h num[k][h][o]` over a flat row is a tie, which the outcome
   mapper records as an uninformative claim. A channel's usefulness is
   therefore learned, never declared.
7. **Branch update and utility.** For probe channel `k`, outcome `o`:
   `q[h] = P[h] * num[k][h][o]`, `w2[h] = q[h]*255/sum q`, branch
   weight `L_o = sum_h P[h]*num[k][h][o]`, `P_o = L_o*255/sum_o L_o`.
   Posterior is scale-invariant, so `w2` needs no renormalisation
   beyond the above. Utility of a commit to `h`: `U = 160*P[h] -
   30600` in payoff units with `CR=40, CW=120`, i.e.
   `U = P*(CR+CW) - 255*CW`. Utility of `RUN(k)`:
   `U = (sum_o P_o * U_o)/255 - C_PROBE`. `SAFE`: `-C_SAFE + V(next)`.
   `WITHHOLD`: `-C_DEADLINE`. All integer, all exact rational
   comparisons by cross-multiplication where needed; `P` lives in
   0..255 so all magnitudes stay under 8e6, far inside i32.
8. **Depth-2 option value.** `p7b_val(d, step, off)` recurses to depth 2
   (at most two probes then decide), with the base case `step >= HZN`
   forcing `WITHHOLD`. Disclosed: this is a bounded-horizon
   approximation, not a full policy; the disclosure matters because the
   probe-vs-commit margin depends on `HZN`.
9. **Selectors** `p7b_sel_learn`, `p7b_sel_rand` (LCG, fixed seed,
   `seed = seed*1103515245 + 12345`), `p7b_sel_wait`, `p7b_sel_fixed`
   (smallest node id among candidates), `p7b_sel_stupid` (commit to the
   most recently appended claim's asserted hypothesis, never probes).
   All five call the same `p7b_val`; they differ only in which candidate
   they return, which is the comparison the mission asks for.
10. **Ablation switches**, default ON, each a single predicate inside
    `residual` / `rel` / mass:
    - `ABL_NODEP=1`: `residual(c) = 255` for every claim, whatever the
      provenance edges say. Expects copied reports to be counted as
      independent observations.
    - `ABL_NOREL=1`: `rel(s) = 128` for every source. Expects a lying
      source to be trusted exactly as much as a reliable one.
    - `ABL_PLAIN=1`: both of the above **and** `rel = 255`, i.e. every
      claim is one independent unit vote. This is the stupid-baseline
      belief updater and the ablation control in one.

## 3. Worlds, fixtures, and predictions

Consequence scalars for the MAIN world (given to the learner as a
payoff description, never as a mode): `C_RIGHT=40`, `C_WRONG=120`,
`C_PROBE=6`, `C_SAFE=8`, `C_DEADLINE=30`, `HZN=2`.
Derived thresholds: `MBREAK = C_WRONG*255/(C_RIGHT+C_WRONG) = 191`
(a share of 192 or more makes commitment pay); a commit to `h` pays iff
`P[h] >= 192`.

### 3.0 CALIBRATION (runs once, builds `C`; truth revealed each time)
Three questions with known truth, hypothesis values 0,1,2.
- `CL1` truth 0: run channel 0, outcome 0. Run channel 1, outcome 0.
- `CL2` truth 1: run channel 0, outcome 1. Run channel 1, outcome 1.
- `CL3` truth 2: run channel 0, outcome 2. Run channel 1, outcome 2.
Result: `C[0][h][h]=1` for `h=0,1,2` and `C[0][h][o]=0` for `o != h`
(rows `2,1,1`); `C[1][h][o]=1` for all `h,o` (rows `2,2,2`, flat).
Plus **7 further channel-0 runs** on truth 0 (repeats), giving
`C[0][0][0]=8`. Final rows: `h=0 -> (9,1,1)`, `h=1 -> (1,2,1)`,
`h=2 -> (1,1,2)`.
Prediction **FP-CAL**: `C[0]` rows are `(9,1,1) (1,2,1) (1,1,2)`;
`C[1]` rows are all `(2,2,2)`.

### 3.1 MAIN world M (`Q=801, QQ=90`; hypotheses 0,1,2 as facts 2/4/6)
Passive evidence only, then a decision.
- `M1` source 1 (S1) reports H0. **ROOT** (`parent=-1`, `dep=0`).
- `M2` source 2 (S2) reports H0. Claims to have copied S1:
  `parent = claim(M1)`, `dep = 255`.
- `M3` source 3 (S3) reports H0, copy of S1: `dep = 255`.
- `M4` source 4 (S4) reports H1. **ROOT.**
- `M5` source 5 (S5) reports H1, copy of S4: `dep = 255`.
- `M6` the learner infers H0 from S1 (self-inference): `parent =
  claim(M1)`, `dep = 255`, `kind = 2`.
- Probes present in the store and unlicensed: `PA` (`field24=900`,
  channel 0) and `PB` (`field24=901`, channel 1).

All sources start with no record, so `rel = 128` everywhere and
`mass(root) = 255*255*128/65025 = 128`.
Derived masses: `w = (32+128, 32+128, 32) = (160,160,32)`, `W = 352`,
`P = (115,115,23)`.

**FP-M1 (K-B01):** `bp2_select` over the three MAP beliefs at bar 50
returns **`-3`**.
**FP-M2 (K-B02):** no MAP belief has a kind-3 self-edge
(`bp2_has_k3(m_h)==0` for all h); all three hypothesis facts are live;
the ledger holds 6 live claims (H0: 4, H1: 2) and no claim was deleted.
**FP-M3 (K-B03):** derived status for the state is `CONTESTED`.
**FP-M4 (K-B04):** `p7b_sel_learn` returns `RUN(channel 0)`.
**FP-M5 (K-B05):** `p7b_sel_rand` over 30 seeds returns `RUN(channel 0)`
at most 30% of the time (there are exactly 3 candidates: `RUN(c0)`,
`RUN(c1)`, `WITHHOLD`, since no `COMMIT` exists and `SAFE` exists;
random draws uniformly among 4). **FP-M5 is a bar, not a prediction.**
**FP-M6 (K-B06):** `p7b_sel_learn` returns `RUN(channel 0)` and
`p7b_sel_wait` returns `SAFE`, and `p7b_sel_fixed` returns `RUN(channel
0)` **only because channel 0 happens to have the smaller node id**: the
bar K-B06 is that the learner's choice is `channel 0` while
`p7b_sel_fixed` over the *reversed* store ordering returns
`RUN(channel 1)`. So the learner is not a fixed-query learner.
**FP-M7 (K-B07):** after `RUN(channel 0)` returns outcome 1 (world
truth for M is H1), the ledger has 7 live claims, the newest asserting
H1 with `kind=1`, `parent=-1`, `residual=255`;
`P[H1] > 192`; the frozen `bp2_select` returns `m_H1`;
`p7b_sel_learn` returns `COMMIT(H1)`. Terminal realised payoff `+40`.
**FP-M8 (K-B08):** information gained by the learner's chosen action
(`G(before) - G(after)`, `G = 255 - 255*sum_h P[h]^2/255^2`, so 0 at
uniform and 255 at a point mass) exceeds that of random, waiting, and
fixed, on the same world with the same seed.
**FP-M9 (K-B13):** with `ABL_PLAIN=1` the same world yields
`P = (148,100,5)`: argmax H0, `bp2_select` returns `m_H0`,
`p7b_sel_learn` returns `COMMIT(H0)`, realised payoff **`-120`**,
i.e. the ablation makes a confident wrong commitment on evidence whose
provenance is one copied chain.

### 3.2 CASE 1 (only evidence supports H0; hidden truth is H1)
Two INDEPENDENT roots for H0 from S1 and S4, no other evidence.
`w = (32+128+128, 32, 32) = (288,32,32)`, `W = 352`, `P = (208,23,23)`.
**FP-1a (K-B10):** `bp2_select` returns `m_H0` (not -3).
**FP-1b (K-B11):** `P[H0] = 208`, i.e. the learner reports a
provisional share of 208/255 and does NOT report certainty; the derived
status is `CONTRADICTED` (share above `MBREAK`, challenger mass 0 is
required for `KNOWN`, and here challenger mass is 0 too, so the frozen
rule yields `KNOWN`). Corrected: challenger mass is 0, share >= MBREAK
=> status **`KNOWN`** (K-B11 asserts `KNOWN` and `P[H0]==208`).
**FP-1c (K-B12):** the realised payoff is `+40` **or** `-120`; the bar
is on the reported share, not on the hidden truth. Explicitly: hidden
truth for case 1 is **H1**, so if the learner commits to H0 the
realised payoff is `-120` and **this is not scored as a failure**.

### 3.3 CASE 5 (three sources repeating ONE COPIED claim)
Sweep `n = 1..5` copies of one root report for H0, versus a sweep of
`n = 1..5` INDEPENDENT roots for H0. The learner runs in both.
**FP-5a (K-B14):** `max - min` of `P[H0]` over the copied sweep is
`<= 2` (of 255).
**FP-5b (K-B15):** over the independent sweep `P[H0]` is strictly
increasing in `n` and rises by `>= 30` from `n=1` to `n=5`.
**FP-5c (K-B16):** with `ABL_PLAIN=1`, `P[H0]` rises by `>= 40` from
`n=1` to `n=5` on the COPIED sweep: double-counting returns.

### 3.4 CASE 6 / CASE 7 (reliability adapts both ways)
Source S1 track record, resolved one truth at a time:
`0/0 -> rel=128`; `+4 correct -> rel=(1+4)*255/(2+4)=212`;
`+5 wrong -> rel=(1+4)*255/(2+9)=106`; `+8 correct ->
rel=(1+12)*255/(2+20)=165`.
**FP-6 (K-B17):** the four values are 128, 212, 106, 165; `rel` strictly
decreases when S1 starts lying and strictly increases when S1 improves.
**FP-7 (K-B18):** the mass of a claim from S1 is strictly decreasing
across the lying segment and strictly increasing across the
rehabilitation segment; rehabilitation is not blocked by the prior.
**FP-7b (K-B19):** with `ABL_NOREL=1`, `rel` is 128 at all four
stations and the mass curve is flat: the adaptation disappears.

### 3.5 CASE 8 (direct observation vs testimony; two arms, opposite answers)
Arm 8a: one direct observation by the learner (source 0) with a learned
`rel(0)=200`, versus one testimony root from a source with `rel=128`.
`mass(obs)=200`, `mass(test)=128`; two hypotheses:
`w = (232,160)`, `W=392`, `P = (150,104)` -> argmax **observation**.
Arm 8b: identical events, but `rel(0)=40` and `rel(testifier)=255`.
`mass(obs)=40`, `mass(test)=255`; `w = (72,287)`, `W=359`,
`P = (51,203)` -> argmax **testimony**.
**FP-8 (K-B20):** the argmax hypothesis **flips** between the two arms.
This is the bar that refutes a hardcoded "observation always wins".
**FP-8b (K-B21):** the frozen `bp2_select` agrees with the ledger
argmax in both arms.

### 3.6 CASES 2, 3, 4, 9 (contest, revision, reversion, experiment)
- **K-B22 (case 2, contest not overwrite):** from world M,
  `bp2_select==-3`; both `m_H0` and `m_H1` live with
  `bp2_has_k3==0`; all 6 ledger claims live; derived status
  `CONTESTED`; the driver's own `nlive` count never decreases across the
  whole battery.
- **K-B23 (case 3, revision toward H1):** from a one-sided H0 state
  (`w=(288,32,32)`, select -> `m_H0`), add two INDEPENDENT roots for H1:
  `w=(288,288,32)`, `P` tied, `bp2_select==-3`, argmax ledger value
  recorded as a revision, `b_rev` of the H1 belief incremented, and a
  kind-3 self-edge with `field12==1` present on the H1 belief while
  `bp2_has_k3(m_H0)==0`: **revision without deleting or retiring the
  old belief or any ledger record.**
- **K-B24 (case 4, rational reversion):** continuing case 3, add two
  independent roots for H0: `w=(544,288,32)`, `P[H0]=159` >= `MBREAK`,
  `bp2_select` returns `m_H0`, a SECOND revision edge appears, both
  beliefs still live, ledger holds 8 live claims.
- **K-B25 (case 9, experiment resolves):** world M, learner's action is
  `RUN(channel 0)`, outcome 1 arrives as a direct observation, and the
  same bar set as FP-M7 holds; realised payoff `+40`.
- **K-B26 (case 9b, a second experiment is not chosen):** with world M
  already resolved after step 0, `p7b_sel_learn` at step 1 returns
  `COMMIT(H1)`, not `RUN`. No channel-0 probe remains unlicensed and
  the informative one was consumed.

### 3.7 CASES 10 / 11 (partial dependence, self-inference)
- **K-B27 (partial dependence):** root R from S1 (`residual 255`), then
  S2 with `dep=128` (`residual 128`), then S3 with `dep=0`
  (`residual 255`, no parent edge: a genuinely independent root).
  Masses are `128 : 64 : 128` exactly (with `rel=128` and
  `mass = 255*residual*rel/65025 = residual/2`... hand-derived:
  `255*255*128/65025 = 128` for residual 255; `255*128*128/65025 = 64`
  for residual 128; `128` for residual 255). Then a second world with
  two `dep=128` siblings: total mass 128+64+64 = 256, i.e. 2 units,
  **not** 3 units: partial dependence is counted, not discarded.
- **K-B28 (charter 133):** chain R -> I1 -> I2 -> I3, each `dep=255`.
  Mass of H0 is unchanged from the single-root value, and `P[H0]` is
  identical to the 4-claim world M value: three inferences corroborate
  nothing. Bar: `P[H0]` with the chain equals `P[H0]` with only R, to
  within 2.

### 3.8 Rational ignorance and representation insufficiency (charter 129, 46/74)
- **K-B29 (rational ignorance is not failure):** world M with
  `C_PROBE=200`. The informative probe's value cannot exceed its cost, so
  `p7b_sel_learn` returns `SAFE` then `WITHHOLD` and **never** `COMMIT`.
  The bar asserts `COMMIT` was never selected and that the run is
  reported as `WITHHELD`, not as an error. No penalty.
- **K-B30 (representation insufficient):** world M with **only**
  channel-1 probes available (channel 0 absent from the store). Channel
  1 is flat, so every branch leaves the posterior unchanged:
  `p7b_sel_learn` returns `SAFE`/`WITHHOLD`, and the derived status is
  `INSOLVABLE`, distinct from `WITHHELD`. The two are distinguished by
  the computed quantity `maxprobe_gain` (0 when no available probe can
  lift the leader above `MBREAK`).
- **K-B31 (consequence sensitivity of the status):** the same world M
  scored under `(C_RIGHT=120, C_WRONG=40)` instead of `(40,120)` flips
  `MBREAK` from 191 to 85, so the derived status changes. The bar
  asserts `status(M; 40/120) != status(M; 120/40)`. Calibration is
  sensitive to consequences, so it cannot be a stored label.

### 3.9 Baselines and information-gain comparison
On world M, `HZN=2`, one decision, then the outcome is delivered:
- **K-B32:** `info(learn) >= info(rand_mean over 30 seeds)` and
  `>= info(wait)` and `>= info(fixed)`, where
  `info = G(prior P) - G(P after the chosen action's outcome)`.
- **K-B33:** `utility(learn) >= utility(rand_mean)` and
  `>= utility(wait)` and `>= utility(fixed)`.
- **K-B34 (stupid baseline, charter 79):** `p7b_sel_stupid` commits to
  the most recent claim, which on world M is H0 (a self-inference from
  S1), realised payoff `-120`, and `info(stupid) == 0`: the stupid
  baseline is measurably worse than the learner on both metrics.
- **K-B35:** `info(rand_mean) < info(learn)` strictly, i.e. the learner
  beats random, not merely ties it.

In-driver total: 35 bars. Expected all-PASS is NOT assumed; the report
states which bars failed.

## 4. Determinism and hygiene bars
- **K-DET:** 3/3 runs of `p7b_full` byte-identical (SHA-256 recorded in
  REPORT.md).
- **K-NONEMPTY:** every run emits `P7B-START`, at least one
  `P7B-BAR` line, `P7B-SUMMARY p/t`, and `P7B-END`, and the byte count
  is greater than 200. Asserted in-driver as `K-NONEMPTY` and again
  outside by `wc -c`.
- **K-HYG:** pure Zag under the restricted PATH
  (`. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh`; `which
  python3` / `which python` empty at build and at run, recorded in
  REPORT.md); zero em/en dash bytes in any authored file or run output;
  zero `_zag_raw_syscall` occurrences in this lane's sources; output via
  `_zag_print` / `_zag_println` only; frozen block SHA-256 unchanged;
  `p7b_learner.zag`'s `bp2_*` section byte-identical to
  `bp9_learner.zag` (SHA-256 recorded); 0 new edge types (types 1, 2, 3,
  7, 14 all pre-exist in the block or in BP-2..9; type 2 = `ET_SUP` is
  a pre-existing unused-on-facts type); 0 new node types (tags 1, 3, 20
  pre-exist); 0 modes, 0 bridges, 0 handlers; opaque identifiers.
- **K-SI:** SI-5 grep returns 0 matches for
  `uncert|inquire|inquiry|do_ask|need_info|mode` inside `if`/`while`
  conditions of `p7b_learner.zag`; the words may appear only in comments.

## 5. Amendment log
Pre-implementation: none. Frozen as committed.

## 6. Falsifiable predictions, sealed
FP-CAL, FP-M1..FP-M9, FP-1a..FP-1c, FP-5a..FP-5c, FP-6, FP-7, FP-7b,
FP-8, FP-8b. All numbers above were hand-derived from the frozen forms
in Section 2 before any implementation existed. Where truncation makes a
prediction unsafe the BAR is a comparison (argmax identity, ordering,
monotonicity) and the number is reported without being a bar; that is
stated at each such place.

## 7. What would falsify the lane's thesis
If `p7b_sel_learn` returns `RUN(channel 1)` on world M, or if
`ABL_PLAIN` produces the same posterior as the real learner on world M,
the claim that TNN discounts dependent evidence is false and must be
reported as such.

## 8. Boundaries declared in advance
The world is a constructed fixture with two hypotheses and a small probe
set; the contingency table is trained on three calibration questions in
the same session, so this measures **within-session** calibration, not
transfer. The ledger and contingency tables are learner-side structures
that do not exist in the frozen store; they are new machinery, counted
in Section 2.3, and their construction is the main design decision of
this lane. The ledger is append-only and unbounded only up to
`NC=96` claims per scenario; a scenario needing more claims is out of
scope. No claim is made about L3, about open-form strategy invention, or
about the ledger claims C377-C466 (contested).

## 9. Claim IDs
Non-ledger lane. Candidate claims, minted only if the bars support
them, in the C5xx block as instructed:
- **C500** competing hypotheses are retained simultaneously with no
  overwrite and no deletion; the frozen `-3` refusal is the mechanism.
- **C501** three reports of one copied claim are counted as one
  observation; ablation restores the double count.
- **C502** self-generated inference is not corroboration for itself.
- **C503** probe-channel usefulness is learned, not declared; the
  learner chooses the separating experiment over random, waiting, and a
  fixed query.
- **C504** source reliability adapts downward and upward under a
  symmetric Beta update.
- **C505** direct-observation-over-testimony arbitration is reversible:
  the answer flips with the reliability record, so it is not hardcoded.
- **C506** epistemic status is a derived function of evidence and
  consequence scalars, including rational ignorance and
  representation-insufficient.