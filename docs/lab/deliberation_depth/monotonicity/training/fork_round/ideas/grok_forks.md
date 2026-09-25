# H5 Fork Designs — Grok-4.7 Pass (highest reasoning)

Source: grok-4.7 via UnoRouter streaming wrapper, 2026-09-24 ~18:35–19:20 PDT.
Note on collection: attempt 1 streamed 0 chars (known grok-4.7 flaky-backend
signature: empty content, no choices); retry once per protocol — attempt 2
succeeded, 42,018 chars streamed. Raw response preserved at
`~/workspace/h5_fork_round/tmp_grok_raw2.md`.

Grok's forks are all built around one binding constraint: an incompatibility
between structural theater-safety and strict calibration under selection.
None is a reweighting of {f1..f8}, and none is an NEC iteration ("NEC with a
ledger tweak", "per-item min against a pooled ledger", and any bare
"target G=0" scheme were explicitly refused by grok as un-runnable).

## Shared analysis (grok's, applies to all forks)

**Release geometry.** M4 releases item i at depth d iff the leader never
changed, so released sets are nested: U_d ⊆ U_{d'} for d > d'. Correctness
of a released answer equals correctness of L_1 — constant on i's released
path. Leader changes (the only way an answer goes correct→wrong) are exactly
the paths that leave U_d. Hence G(d) = E[C|U_d] − Acc(U_d) never sees flipped
items; V1 lives on the flip event; V2 includes the dangerous residual:
released, stable, wrong, features improving.

**Selection identity** (failure mode 6 formalized). With U_{d−1} = U_d ∪ Drop
and E_d the confidence enrichment of stayers,
E_d = E[C(d−1)|U_d] − E[C(d−1)|U_{d−1}].
If every stayer is shifted by the same integer δ_d (thousandths),
G(d) − G(d−1) = E_d + δ_d − ΔA_d, ΔA_d = Acc(U_d) − Acc(U_{d−1}).
Flat per-item paths (δ=0) still have ΔG = E − ΔA: dropout of low-confidence
items (E>0) raises family G even when NO item's confidence rose. An identity,
not an estimation accident. A per-item ceiling does not touch E.

**Incompatibility lemma.** Decision-time C cannot depend on the current
label. Suppose some released trajectory τ is shared by honest items whose
survivor accuracy rises by >0.10 and by at least one wrong item. Then:
structural V2=0 forces C nonincreasing on τ; along that trajectory
ΔA > 100 thousandths with δ ≤ 0 gives ΔG ≤ −ΔA < −0.10, a B13 breach on any
cell with n_rel ≥ 8; tracking ΔA (δ ≈ ΔA − E) keeps G flat but raises C on
the wrong rider → V2=1, death at B2. So no label-free head passes structural
B2 and B13 simultaneously on a family whose released accuracy rises by
>~0.10 while a wrong item occupies the same index-level trajectory. Forks
claiming both must separate those trajectories in feature space, or switch
regime on a measured accuracy gain.

**Interior-ratio invariant** (used wherever a probability is stored). For
counts k≤n, ρ(k,n) = (k+1)·1000/(n+2). Since k ≤ n, ρ ≤ 998 and ρ ≥ 1:
0 and 1000 are NOT representable, so clamp attractors are outside the
codomain and cannot be fixed points. Cold start ρ(0,0) = 500.

**Tiny-n impossibility.** For an n=1 released cell, G = C−y with y∈{0,1}
unknown at decision time; no single C keeps G on the correct side of a
1e-12 monotone boundary for both labels. Strict B3 on redteam (n=1–3) is
probabilistic for every fork. Predictions below assume coarse bins and a
stream of at least a few thousand released outcomes; no item-id memory.

Notation: d_idx = log2(d) ∈ {0..6} for d ∈ {1,2,4,8,16,32,64}. All updates
integer, deterministic, run only after the outcome is observed. Current-item
labels never enter current-item C. Release rule (M4) untouched by all forks.

---

## Fork 1 — RSW (Regime-Switch Calibrator) — grok rank #1

### (a) Mechanism

Two ledgers over the same key r = (m, yld), plus a one-bit regime per key.

- m = min(4, f1/200) (5 margin bins). f7 is NOT a key.
- Marginal yield (thousandths, clamped [0,1000]): at depth 1, my = f5;
  later, my = min(1000, max(0, f5 − f5_prev)·1000 / max(Δf2, 1)),
  with Δf2 = (d − d_prev)·1000/64.
- yld = min(2, my/400) (3 bins). Key count 5·3 = 15, crossed with 7
  depths → 105 cells. Per cell, store n,k of RELEASED outcomes only.
  Historical transition statistics per key per depth (previous items only):
  sums needed for E_d and ΔA_d from the identity (stay vs all-released-at-
  previous-depth).
- Regime bit z_r ∈ {LATCH, TRACK}, default LATCH. After the cell has n ≥ 32
  released outcomes pooled over depth, γ_r = ρ_deep − ρ_shallow (deep =
  d_idx ≥ 4, shallow = d_idx ≤ 1, pooled). Switch LATCH→TRACK only if
  γ_r ≥ 100 AND three successive pooled steps are each nonnegative. Switch
  TRACK→LATCH if γ_r ≤ 60. The hysteresis gap IS the B13 budget, not a
  family constant.
- Depth-1 commitment (not a running min over a ledger): C* = ρ(k_{r,0}, n_{r,0}),
  stored on the item. Never raised by later feature movement inside LATCH.
- Closed-form shift from the selection identity, previous-item estimates only:
  δ_d(r) = ΔA_d(r) − E_d(r) − β_r, with β_r = 2 thousandths in LATCH and 4
  in TRACK (buffer; dominated by measured E,ΔA once n is large). Cumulative
  S_d = Σ_{j≤d} δ_j.
- Emit. LATCH: δ replaced by min(δ,0) before summing, so S_d nonincreasing
  ≤ 0: C = clamp(C* + S_d, 1, 999). On a leader-change OR an increase in f8
  this step: C ← min(C, C_prev − 1). TRACK: use unrestricted δ (can be
  positive, so honest accuracy gains are followed):
  C = clamp(ρ(k_{r,d}, n_{r,d}) + min(S_d, 0), 1, 999). Flip/trauma rule
  identical: C ← min(C, C_prev − 1).
- Update order: emit C → observe release and label → increment cell and
  stay/drop transition sums → recompute δ and possibly z_r. Byte-identical
  given the same trace order.

### (b) Failure modes targeted

- FM6: δ = ΔA − E − β is the exact rearrangement setting E[ΔG] = −β < 0
  when stay/drop moments are right. Selection is SUBTRACTED, not hoped away
  by monotonicity. The −β slope is what strict 1e-12 monotonicity needs; a
  target of G=0 exactly is a random walk that crosses upward.
- FM1: codomain is ρ plus a bounded sum of measured deltas, clamped
  [1,999]. Learning only adds nonnegative counts. C≡0 and C≡1000 unreachable.
- FM2: f7 not in the key; the sole-survivor pin cannot be absorbed into a
  bias (there is no bias term keyed on it).
- FM3: within a depth, C still varies across 15 keys; a flat head would
  require all keys to share ρ, which the update does not impose.
- FM4: no free spread parameter; spread equals empirical ρ gaps.
- FM5: the quantities that set G are computed on released items only, so
  the release mask is the conditioning event, not a hidden confounder.
- FM8: keys are margin × yield — the observable axis along which
  low-evidence ceiling items and high-trauma traps differ. They do not share
  (n,k).
- The lemma: LATCH is the structural-B2 corner, used ONLY where measured
  accuracy gain ≤ 0.10, so nonincreasing C cannot fall through the B13 floor
  by accuracy drift alone. TRACK is the B13 corner, used only where the gain
  exceeds the floor and a flat latch would be illegal. The SWITCH is the
  mechanism; the latch is not a global ratchet.

### (c) Predicted outcome per bar

B1 Pass (floor 1; ρ never 0). B2: Pass in LATCH regions; risk in TRACK —
LATCH stable paths are nonincreasing and flips force −1, so V1=V2=0 there;
predicted theater count = number of wrong released items sitting in TRACK
keys (target 0 if keys separate; a handful if not). B3: likely residual on
redteam only — on keys with n≳30, E[ΔG]=−β; predicted strict violations
1–4, concentrated at n<8 (vs NEC's 6). B4/B4b: pass after burn-in, ~0.62–0.80
(honest keys that gain accuracy are moved to TRACK, so deep correct items
are not stuck at the depth-1 rate). B5: borderline pass ~0.20–0.32; comes
only from margin/yield separation — if margin is weakly informative inside a
battery, this is the bar that fails. B6, B7: pass (M4 untouched). B8: pass on
large cells, |G| ~ β to 0.04. B13: pass IF the switch fires (LATCH regions
have acc gain ≤ 0.10 by the entry test; TRACK follows ρ(d)); floor risk is
the delay before n ≥ 32.

### (d) Falsifier

On a frozen split with n ≥ 32 per key, after regime bits stop flipping:
either (i) a LATCH key still shows survivor accuracy gain > 100 thousandths
(the gain estimator is wrong), or (ii) a TRACK key with γ_r > 100 still shows
G < −0.10 on a cell with n_rel ≥ 8 (following ρ does not track realized
accuracy — bin bias, not variance). Tiny-n B3 misses do NOT falsify RSW.

### (e) P(survives) = 0.26

Best shot at respecting the lemma instead of sitting in one corner of it;
dies if TRACK keys contain stable wrong items or if the stream is too short
for n ≥ 32 before scoring. Most likely death: a trap trajectory with rising
margin and rising consumed-evidence lands in the same (m,yld) key as an
honest family, γ_r crosses 100, regime flips to TRACK, and one stable wrong
item's confidence rises. B2 is zero-tolerance, so one such item kills the fork.

---

## Fork 2 — SRS (Selection-Residual Subtraction) — grok rank #2

### (a) Mechanism

RSW's shift, WITHOUT a regime bit and WITHOUT a depth-keyed probability
table as the emitted value. Discrimination and level are separated cleanly.

- Base score at depth 1 only, from a margin×survivor ledger (survivor uses
  f6, not f7): m = min(4, f1/200), s = min(3, f6/250),
  C* = ρ(k_{m,s}, n_{m,s}). C* is stored and is the ONLY place features enter
  the level.
- Residual tables, global within each (m,s) key, updated from released items
  only. For each depth arrival d: n^stay, ΣC^stay (C at d_prev of items
  released again at d); n^all, ΣC^all, k^all (everyone released at d_prev);
  k^stay (correct counts among stayers at d).
  E_d = ΣC^stay/n^stay − ΣC^all/n^all;
  ΔA_d = k^stay·1000/n^stay − k^all·1000/n^all;
  δ_d = ΔA_d − E_d − 3.
  Empty denominators contribute 0 and the depth is skipped. Identity solved
  for δ, integers, truncating toward 0.
- Emit at depth d, using δ frozen from previous items:
  C = clamp(C* + Σ_{j≤d_idx} δ_j − π, 1, 999),
  theater penalty π = 0 on a clean path, else
  π = min(400, 1_{f3>0}·50 + max(0, f8 − f8^(1))/8).
  π>0 only if a flip or trauma happened, implying the item is NOT in U_d,
  so π does not move released-set G. It forces C < C_prev on a correct→wrong
  transition provided the drop exceeds any positive δ that step; the
  50-thousandth flip term dominates δ (a difference of means, typically
  tens). Cap |δ_d| ≤ 40 as a numerical guardrail; if it binds often the fork
  is already false (see falsifier).
- No per-item running minimum. On a stable released path,
  C(d)−C(d−1) = δ_d, negative precisely when enrichment exceeds accuracy gain.

### (b) Failure modes targeted

Naive chain: a linear head puts positive weight on f2 or f1, both growing
with depth on stable items; released mean confidence rises; part of that is
real enrichment E, part is the weight; accuracy of stayers rises by
ΔA ≤ E on trap-like streams; G increases; B3 fires. SRS blocks the chain at
the ACCOUNTING step, not the feature step: whatever C* was, the depth
derivative of every released item in the key is the same measured δ, and δ
was solved so that E + δ − ΔA = −3 thousandths in expectation.
Feature-driven depth inflation never enters, because depth and
margin-velocity are not inputs to C after depth 1. Margin only chooses the
depth-1 bin. FM1: ρ plus a capped sum, clamped [1,999]. FM3: 20 depth-1 bins.
FM4: no spread knob. FM5: transition statistics are defined on the release
mask, so the mask is observed rather than marginalized out. FM2: no f7.
FM7 only partially handled — keys pool across families, which is the likely flaw.

### (c) Predicted outcome per bar

B1 Pass (floor 1). B2 Conditional: V1 pass (flip adds π≥50, |δ|≤40, so net
drop); V2 pass IFF δ_d ≤ 0 on keys containing stable wrong items — predicted
V2=0 on trap-like keys (E>ΔA), possibly >0 on honest keys (identity wants
δ>0). B3: best large-cell behavior of the set — algebra gives E[ΔG]=−3
thousandths when moments match; predicted violations 2–5, almost all n<8.
B4: ~0.60–0.75 if depth-1 margin bins are informative (deep tax can pull a
weak key down; cap of 40/step limits damage across 6 steps to 240
thousandths). B5: ~0.22–0.35 — inherited from depth-1 bins and shifted
uniformly inside a key, so within-key gaps are preserved. B6, B7 pass. B8:
pass on large cells; target band a few thousandths below 0. B13: risk exactly
where ΔA is large and δ is capped at +40 — uncapped identity would track;
the guardrail re-opens an underconfidence gap of ΔA − E − 40 per step.
Honest ceiling families are the exposure.

### (d) Falsifier

After ≥200 released transitions per depth, compare applied δ_d to δ
recomputed from the same window's stay/drop moments: if they differ by more
than truncation plus the cap on >1/4 of key-depth cells, the residual is not
the selection identity (bookkeeping bug or non-stationarity). Separately: if
E_d estimated inside one battery differs in SIGN from E_d of the pooled key
on ≥3 depths, cross-family pooling is false and SRS's global-within-key
assumption is dead — even if overall G looks acceptable.

### (e) P(survives) = 0.22

The only fork whose G-update is a solved identity rather than a controller,
so it cannot oscillate; it pays with a shared δ across every family landing
in the same margin bin. Most likely death: ceiling family O (correct, low
evidence, moderate margin) shares (m,s) with trap items; pooled E > ΔA of
honest items, so δ<0 and honest deep accuracy runs away from a falling C.
B13 fails on O at d∈{16,32,64} with n_rel ≥ 8. FM8 eats the closed form.

---

## Fork 3 — LST-WBA (Latched State Tax, Worst-Boundary Adversary) — grok rank #3

### (a) Mechanism

A feedback controller on G, region by region, with the adversary chosen
deterministically as the worst depth boundary. No closed form; the
measurement is G itself.

- Region r = (m, yld) as in RSW (15 regions). Latch: at depth 1 store
  C* = ρ(k_r, n_r) from that region's depth-1 released ledger. Features after
  depth 1 do not rewrite C*.
- Tax table T[d_idx][r] ≥ 0, initially 0. Invariant after every write:
  T[d][r] ≥ T[d−1][r].
- Emit (released or not): C = clamp(C* − T[d_idx][r] − π, 1, 999), π as in
  SRS (0 unless flip/trauma; irrelevant to released G). Then if f3 just
  latched or f8 increased, C ← min(C, C_prev−1). Because T is monotone in
  depth and C* is fixed, a clean path is nonincreasing even before the flip
  rule. This is a DEPTH TAX ON A FROZEN BASE, not a min() against a changing
  ledger value: the base does not move when margin grows, and two items in
  the same region share the tax schedule but keep their own C*.
- Worst-boundary update (the adversary). Maintain per region and depth
  released running sums ΣC, Σ(y·1000), n. Let
  g[d] = ΣC/n − Σy·1000/n once n ≥ 8, else carry forward g[d−1].
  d* = argmax_{d≥1}(g[d] − g[d−1]), ties to the larger depth (deeper
  selection compounds). If g[d*]−g[d*−1] > 0:
  T[d*][r] ← T[d*][r]+1, then repair monotonicity upward:
  for j ≥ d*: T[j] ← max(T[j], T[j−1]). If worst boundary ≤ 0 and some
  g[d] < −80: decrement T at the MOST NEGATIVE g subject to monotonicity and
  T ≥ 0. One unit per released outcome. No gain coefficient: step is 1
  thousandth, sign is the violation.
- B4 guard, region level not item level: track mean C of released CORRECT
  outcomes in the region. If that mean falls below 520, freeze further tax
  increments in that region. This does not lift wrong items (no per-item
  floor at 500); it only stops taxing a region whose correct members are
  already at the B4 line. Separation remains the gap between regions.

### (b) Failure modes targeted

Naive: confidence monotone in depth and margin → as U_d sheds low-margin
items, mean released confidence rises (the E term), G rises; a global bias
cannot subtract E in a trap region without subtracting it in an honest
region. LST-WBA blocks at two points. First the latch: post-depth-1 margin
growth is not an input, so within-item ΔG contribution ≤ 0. Second the
adversary: residual enrichment appears as g[d]−g[d−1] > 0 INSIDE the region
that produced it, and the next unit of tax lands exactly at d* and every
deeper depth. Dropped items are gone, so the tax falls only on stayers —
the enriched set. Regions without a rising G never get taxed, so an honest
region whose ΔA offsets E is left alone. That is the PER-FAMILY CEILING
WITHOUT A FAMILY LABEL: the family is discovered as the region whose
empirical G path misbehaves. FM1: tax moves C only inside (1, C*] ⊂
(0,1000); the correct-mean freeze stops the controller walking a region to
the floor to buy B3; the fixed point is the interior band [−0.08, 0], not a
clamp. FM5: the error signal is g on released cells, so abstentions do not
hide the schedule. FM3/FM4: C* still differs across margin bins; tax is a
level, not a variance; no spread parameter to anti-learn.

### (c) Predicted outcome per bar

B1 Pass (floor 1; freeze prevents a march to 0). B2: pass structurally on
clean and flipped paths — clean: T monotone ⇒ C nonincreasing; flip: extra
−1. Predicted V1=V2=0. This is the fork that should match NEC's theater
result without NEC's ledger ceiling. B3: improved, not guaranteed — each
violation is a one-thousandth tax on the offending boundary; convergence is
O(|G|·1000) released items per region; early in the stream violations
persist. Predicted remaining violations after a long stream: 1–4, redteam.
B4: ~0.55–0.75 (freeze at 520 on correct mean; weak families whose TRUE
accuracy <0.50 still fail B4b — the guard cannot invent signal). B5:
~0.20–0.30 (depth-1 ρ gaps unchanged by a uniform tax; borderline if margin
bins are tight). B6, B7 pass. B8: pass once the adversary quiets,
|G| ≲ 0.05 (setpoint band [−0.08, 0]). B13: controller tries; lag can
overshoot — decrement path exists but monotonicity forbids lowering a deep
tax without lowering shallow ones still needed. Predicted one or two cells
in [−0.12, −0.10] during lag.

### (d) Falsifier

Instrument per-region E_d (analysis-only, as in SRS). If, after taxes stop
changing for 500 released items, a region still has g[d]−g[d−1] > 0 on a
cell with n ≥ 30, the tax is not reaching the enriched items — the region
definition does not align with the selection event, and "state-conditional
ceiling" is false. Sharper kill: taxes still moving (no fixed point) after
10^4 released items — the unit-step adversary is chasing noise and the
setpoint is not an equilibrium.

### (e) P(survives) = 0.19

Structural theater plus a controller whose setpoint is exactly the B3/B13
band; the controller is slow, order-dependent, and can overshoot. Most
likely death: monotone repair. A violation at depth 16 increments T at 16,
32, 64. Depth 64's accuracy gain then drives g[64] < −0.10 before the
decrement branch may unwind T[16], which it refuses while g[16] is still
slightly positive. B13 fails at the ceiling of an honest region. The
adversary is greedily B3-safe and only lazily B13-safe.

---

## Fork 4 — MEY (Marginal-Yield Ledger) — grok rank #5

### (a) Mechanism

No depth feature, no tax, no latch. The claim: "overconfidence with depth"
is specifically confidence that increases in ELAPSED depth, and elapsed depth
should enter only as the denominator of yield.

- Key q = (m, y): m = min(4, f1/200); marginal yield my as in RSW;
  y = min(3, my/250) — 4 bins; the bottom bin is exactly "budget burned, no
  new evidence".
- Per depth index, per key, released counts n,k only. Emit C = ρ(k_{q,d}, n_{q,d}).
  Depth is a STRATUM, not an additive input. Two states with the same margin
  and same evidence gained per budget burned look up the same stratum cell
  only if also at the same depth; the cell's value is the historical accuracy
  of that situation, free to be lower at depth 64 than depth 8. Nothing in the
  formula can add points for a larger d_idx.
- Path rule, yield-gated, not a ceiling. Let q be the current key,
  q_prev the previous step's key. If f3 latched this step or f8 increased:
  C ← min(C, C_prev−1). Else if y < y_prev: C ← min(C, C_prev) — wasted
  budget cannot raise confidence. Else (y nondecreasing, clean path): emit ρ
  even if higher than C_prev. Confidence may rise only when this step's
  evidence rate beat the previous step's, and only up to the historical
  accuracy of that new situation. A pure depth increase with f5 flat moves the
  item into a weakly lower y bin and the middle rule blocks a rise.
- No learned weights. The ledger is the parameter. Update after the label,
  released items only.

### (b) Failure modes targeted

Naive: f2 = d·1000/64 gets a positive weight because, in aggregate, deeper
released items are somewhat more accurate (selection); the weight then fires
on EVERY deep item, including those that got there by sitting still; accuracy
did not rise for those; G rises with d. MEY removes f2 from the function
class: the only depth effect available is which stratum's accuracy you look
up, and zero-marginal-yield strata are populated by exactly the sit-still
trajectories. If those are less accurate — the empirical content of
"deliberation without evidence is not information" — their ρ is lower, and
the path rule forbids using any other feature to climb back out. FM6 is
attacked only on the part of enrichment that coincides with falling yield;
enrichment INSIDE a fixed key (high-margin items survive more, same yield)
is NOT removed — the honest weak point. FM1: pure ρ. FM2: f7 absent;
sole-survivor items influence C only via a distinctive yield, empirically.
FM3: 20 keys. FM4: none. FM5: each depth has its own counts, fit only on
items the mask released at that depth. FM8: low-evidence O items fall into
y=0 or y=1 and do not share counts with high-yield traps.

### (c) Predicted outcome per bar

B1 Pass (ρ≥1). B2 Partial: flips get structural −1; stable wrong items whose
YIELD BIN INCREASES may see C rise with ρ — predicted V2 low single digits
if traps consume evidence, 0 if traps are pure sit-still. B3 Mixed:
sit-still selection deflated; within-bin selection remains and can lift G;
predicted violations 3–6, i.e. not clearly better than NEC on B3 alone.
B4: ~0.65–0.80 on keys that keep receiving evidence. B4b FAIL RISK on honest
families that saturate f5 early: after f5 hits 1000, later steps have my=0,
so a correct item is scored as a no-new-evidence item; if that cell's
accuracy < 0.50, B4b fails. B5: ~0.18–0.30 — borderline; yield must separate
correct from wrong, not just depths. B6, B7 pass. B8: |G| ~ 0.03–0.08 where
the stratum is well populated. B13: the saturation case — correct,
evidence-saturated, deep cells scored at the zero-yield accuracy; if the gap
exceeds 0.10, B13 fires. Predicted failure on ceiling families.

### (d) Falsifier

Restrict to items with nondecreasing f5 at every recorded step (evidence
kept pace with budget). If those items still show a positive slope of mean C
against d_idx larger than the slope of their accuracy, on cells with n ≥ 30,
then yield-keying did not remove depth inflation — some other feature inside
the key (margin mix) is carrying it, and MEY's causal claim is wrong.

### (e) P(survives) = 0.15

Right attack on the elapsed-depth channel, incomplete attack on within-key
selection, and a concrete saturation failure on long ceilings. Most likely
death: f5 saturates by depth 8 on honest ceiling items; depths 16–64 all map
to y=0, whose ledger is dominated by genuinely stuck trap items with
accuracy ~0.4; honest deep G ≈ 0.4 − 0.85 < −0.10. B13 (and possibly B4b) on
family O or P.

---

## Fork 5 — CDC (Cluster-Discovered Ceilings) — grok rank #4

### (a) Mechanism

Per-family ceilings with no family input: maintain an explicit partition of
index-level state; each block gets its own selection residual.

- State vector (integers, thousandths), deliberately EXCLUDING f2 and f7:
  x = (f1, f5, f6, min(f8,1000), my) ∈ Z^5.
- Prototypes: up to K=8 vectors p_c. Assignment:
  c = argmin_j ‖x − p_j‖_1, ties to smaller j.
- Birth/merge, deterministic, no hand-tuned thresholds. After the first 32
  released items, set scale τ to the 75th percentile of those items'
  nearest-prototype distances (order statistic on a fixed prefix; recompute
  τ every 256 released items as median assignment distance × 2, integer).
  If ‖x − p_c‖_1 > τ and fewer than 8 prototypes exist, append x as a new
  prototype. If ‖p_i − p_j‖_1 < τ/3, merge the higher index into the lower:
  counts add, prototype becomes the count-weighted mean (integer division).
  Running-mean update of the assigned prototype: p_c ← p_c + (x − p_c)/n_c,
  division truncating toward 0. Order fully determined by the deliberation
  stream, so reruns match.
- Per cluster, the SRS residual: each cluster keeps its own stay/drop sums
  and its own δ_d(c), same formula as Fork 2 (including the −3 thousandth
  buffer and |δ| ≤ 40 guard). Depth-1 base C* = ρ(k_c, n_c) at d_idx=0.
  Emit C = clamp(C* + Σ_{j≤d} δ_j(c) − π, 1, 999), π as in SRS.
- Clusters are recomputed from x at every depth, so an item can change
  cluster if its evidence state moves. Constraint on transition: if the new
  cluster's emitted value exceeds C_prev and my did not increase, keep
  C_prev. If my increased, allow the new value. Flip/trauma always applies
  the −1 rule after that. This is a yield gate on cluster transitions, not a
  stored confidence ceiling.
- What is learned: prototypes, τ, per-cluster counts, per-cluster residuals.
  No family bit, no constant of the form "cluster 3 is redteam".

### (b) Failure modes targeted

FM8 is the target. A single margin bin pools low-evidence correct O items
with traps because both can have mid margins; their E and ΔA have opposite
structures, so one δ cannot serve both (this is SRS's death). CDC's claim:
those populations are far apart in (f5, f6, f8, my) even when f1 matches, so
L1 prototypes split them BEFORE residuals are estimated. Each cluster then
runs an identity valid INSIDE a homogeneous selection regime. FM6 handled
inside each cluster by the same identity as SRS. The discovery mechanism is
the prototype split, not a hand partition: birth happens when an item is far
from every existing center relative to the stream's own median distance, so
the number of regimes is data-determined up to the hard cap of 8 (the cap is
a memory bound; if it binds, the falsifier fires). FM1: ρ again. FM2: f7
excluded so a binary pin cannot become its own cluster center by
construction; f6 can, and if sole-survivor is real it shows up as low f6
with accuracy LEARNED, not stipulated. FM3: at most 8 bases. FM5: residuals
on released stay/drop, per cluster. FM4: none.

### (c) Predicted outcome per bar

B1 Pass. B2: same conditional as SRS, hopefully on fewer bad pairs — V2 iff
some cluster has δ_d>0 and a stable wrong member; traps separated into their
own cluster makes δ ≤ 0 there. Predicted theater: 0–2. B3: better than SRS
if clusters are pure, worse if fragmented — pure clusters: E[ΔG]=−3
thousandths; fragmented: tiny-n residuals with the wrong sign. Predicted
violations: 2–5. B4: ~0.60–0.78. B5: ~0.24–0.38 if clusters correlate with
correctness, else fail — an 8-way partition can separate more than 5 margin
bins, or can separate noise. B6, B7 pass. B8: conditional on cluster purity.
B13: better than SRS on O — O should be its own cluster with its own ΔA, so
it is not taxed at the trap rate; fails if O and traps stay inside one
prototype.

### (d) Falsifier

Post-hoc, labels used only as measurement: mutual information between
assigned cluster and battery id, on released items after prototypes
stabilize. If I(cluster; battery) ≈ 0 (clusters ignore the battery axis and
track only margin), discovery failed. Mechanical kill needing no labels: if
the merge/birth loop does not reach a fixed partition within the first 2000
released items (prototypes still moving by > τ/10 per 256 items), the
partition is not a parameter, it is a moving target, and residuals computed
inside it are meaningless.

### (e) P(survives) = 0.16

Right response to FM8, but online clustering on a short stream is a good way
to manufacture FM7 inside each cluster. Most likely death: birth order —
the first batteries encountered occupy the 8 prototype slots with fine
margin distinctions; a later ceiling family is forced into the nearest
trap-adjacent prototype because the cap binds; residuals there are trap
residuals; B13 fails on that family, and the merge rule never fires because
the prototype sits at a compromise center whose distance to both populations
is just above τ/3.

---

## Fork 6 — IFP (Interior Fixed-Point Head) — grok rank #6

### (a) Mechanism

Exists to kill clamp attractors and the uniform manifold DIRECTLY, and to
show why that is not enough for B3. A contracting map with a unique interior
fixed point per depth stratum. Grok bills it as a control as much as a
candidate.

- Fast score, features excluding f2 and f7: f1, f5, f6, max(f4,0), my, each
  in thousandths. Integer weights w_i, bias b, initialized 0. Linear score
  s = b + ⌊Σ w_i·f_i / 1000⌋.
- Codomain map, permanent pseudocounts: maintain global (A,B)=(1,2) and
  per-depth (A_d, B_d), invariant 1 ≤ A ≤ B−1 always. Emit
  C = (A_d + max(s,0))·1000 / (B_d + |s| + max(−s,0) + 1),
  same shape as ρ: numerator ≥ 1, denominator ≥ numerator+1, so
  C ∈ [1,998] for every finite s, A_d, B_d. Increasing s moves C up but with
  derivative ~1/B_d → 0 as data accumulate. Weights cannot shove mass onto a
  clamp; the best they can do is saturate the INFLUENCE of s, at which point
  C collapses to the depth base rate A_d·1000/B_d, an interior point. That
  collapse is detectable (see falsifier) and is exactly FM3, so the update
  penalizes it.
- Update, deterministic, released items only. (1) Counts: B_d ← B_d+1; if
  y=1 then A_d ← A_d+1. Invariant holds. (2) Weight step with mandatory
  decay, learning rate 1/(1000+t) in integer arithmetic:
  w_i ← w_i − ⌊w_i/(1000+t)⌋ + ⌊(1000y − C)·f_i / (1000·(1000+t))⌋,
  same for b with f=1000. Decay runs every step, including when the error
  term is 0, so w=0 is the unique origin and nonzero weights exist only
  while they keep paying for themselves in squared error. (3) Outward-clamp
  freeze: if C≥980 and y=1, or C≤20 and y=0, skip the error term (decay
  only) — the gradient pushing further out is dropped. (4) Monotone depth
  coupling of the base rate: let μ_d = A_d·1000/B_d. If μ_d > μ_{d−1} + 20
  and the extra is not supported by an increase in mean my at that depth
  (mean my tracked alongside), subtract the excess by incrementing B_d
  without A_d (one unit), i.e. structural drag on depth-only base-rate
  inflation. Fires at most until μ_d ≤ μ_{d−1}+20.
- Theater: same flip rule as MEY — leader-change or trauma increase forces
  C ← min(C, C_prev−1). No general ratchet (a ratchet plus this head would
  just be NEC with different features).

### (b) Failure modes targeted

FM1, mechanistically: a clamped linear head has zero gradient at 0 and 1000,
so SGD treats the clamp as a solution; the optimizer dumps a large positive
bias there and B5/B13 die. IFP's emit has nonzero derivative for every finite
s, the count invariant excludes {0,1000}, decay makes unbounded weights a
non-equilibrium, and the outward freeze removes the gradient at the
boundary. The only equilibrium of the fast weights at fixed counts is the
normal equation of the decayed least-squares problem, whose predictions sit
near the conditional mean — interior whenever both labels occur. FM3: the
uniform manifold is the large-B_d limit where s does not move C; decay plus
a live error term fights that, but if features are uninformative the
equilibrium IS the base rate and B5 fails honestly — IFP does not fake
separation. FM4: no spread parameter. FM2: f7 absent; a weight recreating it
from f6 near 0 is subject to decay and the ledger, not wired to a pin.
FM5: depth coupling uses per-depth released base rates, so the mask defines
the strata. FM6 only weakly addressed: a positive weight on f1 still lets
stayer mix raise mean C inside a depth; the +20 coupling limits only the
BASE RATE, not the feature-conditional mean. Deliberate: this fork isolates
"fix the dynamics" from "fix selection" — read as a control.

### (c) Predicted outcome per bar

B1 Pass (invariant). B2 FAIL RISK, same as any non-latched head: stable wrong
item with rising f1 → s rises → C rises → V2. Predicted V2 > 0; grok does not
expect this fork to be the theater survivor. B3 Weak: base-rate coupling
stops the crudest depth inflation; feature-mix enrichment remains; predicted
violations 4–8, not better than NEC. B4: ~0.58–0.75 once t is large. B5:
~0.15–0.28 — the bar most likely to miss, because decay shrinks weak signals
toward the base rate. B6, B7 pass. B8: |G| maybe 0.04–0.10; no servo pulling
G into a band. B13: moderate risk — coupling allows μ_d to exceed μ_{d−1} by
20 thousandths per step (six steps = 120), overshoot both ways open.

### (d) Falsifier

The core claim is about dynamics, so the kill is a FIXED POINT, not a bar:
log max_i|w_i| and the fraction of emits with C ∈ [1,20] ∪ [980,999]. If
after 10^4 released updates either the max weight is still growing linearly
with t (decay is not contracting) or >5% of emits sit in those edge bands,
the interior-fixed-point claim is false. A pure bar failure with weights
converged and edge-mass ≈ 0 does NOT falsify IFP; it falsifies the hope that
good dynamics imply monotone G.

### (e) P(survives) = 0.10

The correct anti-clamp machine and a weak selection machine. Included
because a fork set that only stacks selection corrections will rediscover
clamp attractors the moment a linear score is added back, and because its
falsifier is independent of B3. Most likely death: B2, via margin. Second
most likely: B5, via decay winning against a real but small feature signal
and flattening the head (FM3 at equilibrium, legitimately).

---

## Grok's ranking (best first)

1. RSW — the only design that treats the V2/B13 lemma as a measured regime
   split rather than picking one illegal corner globally. P=0.26.
2. SRS — same correction as a solved identity, so no controller lag and no
   oscillation; loses to RSW only because one δ is shared across families
   inside a margin bin. P=0.22.
3. LST-WBA — structural theater without a ledger-min ratchet, and the tax is
   applied where G actually rose; monotone repair makes it B13-fragile at
   large depths. P=0.19.
4. CDC — the right FM8 fix (discover the partition, then run SRS inside it),
   but online prototypes on a short, ordered battery list will often fail to
   discover it. P=0.16.
5. MEY — cleanly deletes elapsed depth from the function class; does not
   price within-key selection, and evidence saturation on long ceilings maps
   honest items onto the trap bin. P=0.15.
6. IFP — dynamics worth having (unique interior fixed point, decay, outward
   gradient dropped) but it does not subtract enrichment; should not be
   expected to beat NEC on B3. P=0.10.

## What grok would NOT run

Any linear reweighting of {f1..f8}; any scheme whose only monotone element
is a per-item min against a pooled ledger (i.e. NEC); any target of G=0 with
no negative buffer. The first cannot see E_d. The second is NEC. The third
is a random walk on the wrong side of a 1e-12 test.
