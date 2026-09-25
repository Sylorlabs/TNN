The binding constraint is an incompatibility between structural theater-safety and strict calibration under selection. Every fork below is built around that, not around a new linear weighting of \(f_1..f_8\).

## Shared analysis (why “tune the head” cannot work)

**Release geometry.** M4 releases item \(i\) at depth \(d\) iff the leader has never changed, so the released sets are nested: \(U_d \subseteq U_{d'}\) for \(d > d'\). Correctness of a released answer is the correctness of \(L_1\), hence constant on \(i\)'s released path. Leader changes, which are the only way an answer goes correct→wrong, are exactly the paths that leave \(U_d\). So:

- \(G(d) = \mathbb{E}[C \mid U_d] - \mathrm{Acc}(U_d)\) never sees flipped items.
- V1 (correct→wrong, confidence non-decreasing) lives on the flip event.
- V2 (wrong→wrong, confidence rising) includes the dangerous residual: **released, stable, wrong, features improving**.

**Selection identity.** Let \(U_{d-1} = U_d \cup \mathrm{Drop}\), and write \(E_d\) for confidence enrichment of stayers:
\[
E_d = \mathbb{E}[C(d-1)\mid U_d] - \mathbb{E}[C(d-1)\mid U_{d-1}] = \frac{n_{\mathrm{drop}}}{n_{d-1}}\Big(\mathbb{E}[C\mid U_d] - \mathbb{E}[C\mid \mathrm{Drop}]\Big).
\]
If every stayer is shifted by the same integer \(\delta_d\) (thousandths),
\[
G(d)-G(d-1) = E_d + \delta_d - \Delta A_d, \qquad \Delta A_d = \mathrm{Acc}(U_d)-\mathrm{Acc}(U_{d-1}).
\]
Flat per-item paths (\(\delta=0\)) still have \(\Delta G = E - \Delta A\). Dropout of low-confidence items (\(E>0\)) raises family \(G\) even when no item’s confidence rose. That is failure mode 6, and it is an identity, not an estimation accident. A per-item ceiling does not touch \(E\).

**Incompatibility lemma.** Decision-time \(C\) cannot depend on the current label. Suppose some released trajectory \(\tau\) is shared by honest items whose survivor accuracy rises by more than \(0.10\) and by at least one wrong item. Then:

- structural V2 \(= 0\) forces \(C\) nonincreasing on \(\tau\);
- along that trajectory \(\Delta A > 100\) thousandths with \(\delta \le 0\) gives \(\Delta G \le -\Delta A < -0.10\), which is a B13 breach on any cell with \(n_{\mathrm{rel}}\ge 8\);
- tracking \(\Delta A\) (\(\delta \approx \Delta A - E\)) keeps \(G\) flat but raises \(C\) on the wrong rider, so V2 \(= 1\) and the fork dies at B2.

Therefore no label-free head passes **structural** B2 and B13 simultaneously on a family whose released accuracy rises by more than \(\sim 0.10\) while a wrong item occupies the same index-level trajectory. Forks that claim both must either separate those trajectories in feature space, or switch regime using a measured accuracy gain. NEC’s ratchet is the structural-B2 corner of this lemma; it is why B13 and residual B3 remain. None of the forks below is “ratchet plus a ledger tweak.”

**Interior-ratio invariant** (used wherever a probability is stored). For integer counts \(k\le n\),
\[
\rho(k,n) = \frac{(k+1)\cdot 1000}{n+2}.
\]
Since \(k \le n\), \(\rho \le 1000\cdot n/(n+2) \le 998\) and \(\rho \ge 1\). Values \(0\) and \(1000\) are not representable. Clamp attractors are not fixed points because they are outside the codomain. Cold start \(\rho(0,0)=500\).

**Tiny-n impossibility.** For an \(n=1\) released cell, \(G = C-y\) with \(y\in\{0,1\}\) unknown at decision time. No single \(C\) keeps \(G\) on the correct side of a \(1\mathrm{e}{-12}\) monotone boundary for both labels. Strict B3 on redteam (\(n=1..3\)) is probabilistic for every fork. Predictions below assume coarse bins and a stream of at least a few thousand released outcomes; they do not assume item-id memory.

Depth index: \(d_{\mathrm{idx}}=\log_2 d \in \{0..6\}\) for \(d\in\{1,2,4,8,16,32,64\}\). All updates are integer, deterministic, and run only after the outcome is observed. Current-item labels never enter current-item \(C\).

---

## Fork 1 — RSW (Regime-Switch Calibrator)

### (a) Mechanism

Two ledgers over the same key \(r = (m, yld)\), plus a one-bit regime per key.

- \(m = \min(4, f_1/200)\) (5 margin bins). \(f_7\) is not a key.
- Marginal yield, thousandths, clamped to \([0,1000]\):
  - depth 1: \(\mathrm{my} = f_5\);
  - later: \(\mathrm{my} = \min\big(1000,\; \max(0,f_5-f_5^{\mathrm{prev}})\cdot 1000 / \max(\Delta f_2, 1)\big)\), with \(\Delta f_2 = (d-d_{\mathrm{prev}})\cdot 1000/64\).
- \(yld = \min(2, \mathrm{my}/400)\) (3 bins). Key count \(= 5\cdot 3 = 15\), crossed with 7 depths \(\Rightarrow 105\) cells.

Per cell, store \(n,k\) of **released** outcomes only. Historical transition statistics per key, per depth (previous items only): sums needed for \(E_d\) and \(\Delta A_d\) as in the identity (stay vs all-released-at-previous-depth).

**Regime bit** \(z_r \in \{\mathrm{LATCH}, \mathrm{TRACK}\}\), default LATCH. After the cell has \(n\ge 32\) released outcomes pooled over depth, let
\[
\gamma_r = \rho_{\mathrm{deep}} - \rho_{\mathrm{shallow}}
\]
where deep \(= d_{\mathrm{idx}}\ge 4\) and shallow \(= d_{\mathrm{idx}}\le 1\), each pooled. Switch LATCH→TRACK only if \(\gamma_r \ge 100\) and the three successive pooled steps are each nonnegative. Switch TRACK→LATCH if \(\gamma_r \le 60\). Hysteresis gap is the B13 budget, not a family constant.

**Depth-1 commitment** (not a running min over a ledger):
\[
C^{\star} = \rho(k_{r,0}, n_{r,0}).
\]
Stored on the item. Never raised by later feature movement inside LATCH.

**Closed-form shift** from the selection identity, previous-item estimates only:
\[
\delta_d(r) = \Delta A_d(r) - E_d(r) - \beta_r,
\]
\(\beta_r = 2\) thousandths in LATCH and \(4\) in TRACK (buffer; both are dominated by measured \(E,\Delta A\) once \(n\) is large — they are not the calibration). Cumulative \(S_d = \sum_{j\le d}\delta_j\).

**Emit.**
- LATCH: \(\delta\) is replaced by \(\min(\delta, 0)\) before summing, so \(S_d\) is nonincreasing and \(\le 0\).
  \[
  C = \mathrm{clamp}(C^{\star} + S_{d},\, 1,\, 999).
  \]
  Stable path: \(C\) cannot rise. On a leader-change **or** an increase in \(f_8\) this step: \(C \leftarrow \min(C, C_{\mathrm{prev}}-1)\).
- TRACK: use unrestricted \(\delta\) (can be positive, so honest accuracy gains are followed):
  \[
  C = \mathrm{clamp}\big(\rho(k_{r,d}, n_{r,d}) + \min(S_d, 0),\, 1,\, 999\big).
  \]
  The \(\min(S_d,0)\) term still subtracts residual enrichment the bin mean has not already absorbed. Flip/trauma rule identical: \(C \leftarrow \min(C, C_{\mathrm{prev}}-1)\).

**Update order.** Emit \(C\) → observe release and label → increment the cell and the stay/drop transition sums → recompute \(\delta\) and possibly \(z_r\). Byte-identical given the same trace order.

### (b) Failure modes

- **FM6.** \(\delta = \Delta A - E - \beta\) is the exact rearrangement that sets \(\mathbb{E}[\Delta G] = -\beta < 0\) when stay/drop moments are right. Selection is subtracted, not hoped away by monotonicity. The \(-\beta\) slope is what strict \(1\mathrm{e}{-12}\) monotonicity needs; a target of \(G=0\) exactly is a random walk that crosses upward.
- **FM1.** Codomain is \(\rho\) plus a bounded sum of measured deltas, then clamped to \([1,999]\). The learning update only adds nonnegative counts. \(C\equiv 0\) and \(C\equiv 1000\) are unreachable.
- **FM2.** \(f_7\) is not in the key. A sole-survivor pin cannot be absorbed into a bias; there is no bias term keyed on it.
- **FM3.** Within a depth, \(C\) still varies across 15 keys. A flat head would require all keys to share \(\rho\), which the update does not impose.
- **FM4.** There is no free spread parameter. Spread equals empirical \(\rho\) gaps.
- **FM5.** The quantities that set \(G\) are computed on released items only, so the release mask is the conditioning event, not a hidden confounder. Theater drops are structural and do not need a gradient through abstentions.
- **FM8.** Keys are margin × yield, which is the observable axis along which low-evidence ceiling items and high-trauma traps differ. They do not share \((n,k)\).
- **The lemma.** LATCH is the structural-B2 corner, used only where measured accuracy gain is \(\le 0.10\), so a nonincreasing \(C\) cannot fall through the B13 floor by accuracy drift alone. TRACK is the B13 corner, used only where the gain exceeds the floor and a flat latch would be illegal. The switch is the mechanism; the latch is not a global ratchet.

### (c) Bars

| Bar | Call | Why |
|---|---|---|
| B1 | Pass | Floor at 1; \(\rho\) never 0 |
| B2 | Pass in LATCH regions; risk in TRACK | LATCH: stable \(C\) nonincreasing and flip forces \(-1\), so V1=V2=0. TRACK can raise \(C\). Predicted theater count = number of wrong released items sitting in TRACK keys. Target 0 if keys separate; a handful if not |
| B3 | Likely residual on redteam only | On keys with \(n\gtrsim 30\), \(\mathbb{E}[\Delta G]=-\beta\). Predicted strict violations: 1–4, concentrated at \(n<8\), versus NEC’s 6 |
| B4 / B4b | Pass after burn-in, \(\sim 0.62\)–\(0.80\) | Correct items must occupy keys with \(\rho\ge 500\). Honest keys that gain accuracy are exactly those moved to TRACK, so deep correct items are not stuck at the depth-1 rate |
| B5 | Borderline pass, \(\sim 0.20\)–\(0.32\) | Comes only from margin/yield separation. If margin is weakly informative inside a battery, this is the bar that fails |
| B6, B7 | Pass | M4 untouched |
| B8 | Pass on large cells, \(\lvert G\rvert \sim \beta\) to \(0.04\) | Buffer is a few thousandths plus estimation error |
| B13 | Pass if the switch fires | LATCH regions have acc gain \(\le 0.10\) by the entry test. TRACK regions follow \(\rho(d)\). Floor risk is the delay before \(n\ge 32\) |

### (d) Falsifier

On a frozen split with \(n\ge 32\) per key, after the regime bits have stopped flipping: either (i) a LATCH key still shows survivor accuracy gain \(> 100\) thousandths (the gain estimator is wrong), or (ii) a TRACK key with \(\gamma_r > 100\) still shows \(G < -0.10\) on a cell with \(n_{\mathrm{rel}}\ge 8\) (following \(\rho\) does not track realized accuracy — bin bias, not variance). Tiny-n B3 misses do not falsify RSW.

### (e) \(P(\mathrm{survives}) = 0.26\)

Best shot at respecting the lemma instead of sitting in one corner of it; dies if TRACK keys contain stable wrong items or if the stream is too short for \(n\ge 32\) before scoring.

**Most likely death.** A trap trajectory with rising margin and rising consumed-evidence lands in the same \((m,yld)\) key as an honest family, \(\gamma_r\) crosses 100, regime flips to TRACK, and one stable wrong item’s confidence rises. B2 is zero-tolerance, so one such item kills the fork.

---

## Fork 2 — SRS (Selection-Residual Subtraction)

### (a) Mechanism

RSW’s shift, without a regime bit and without a depth-keyed probability table as the emitted value. Discrimination and level are separated cleanly.

**Base score at depth 1 only**, from a margin×survivor ledger (survivor uses \(f_6\), not \(f_7\)):
\[
m=\min(4,f_1/200),\quad s=\min(3, f_6/250),\quad C^{\star}=\rho(k_{m,s}, n_{m,s}).
\]
\(C^{\star}\) is stored and is the only place features enter the level.

**Residual tables**, global within each \((m,s)\) key, updated from released items only. For each depth arrival \(d\):

- \(n^{\mathrm{stay}}, \sum C^{\mathrm{stay}}\): \(C\) at depth \(d_{\mathrm{prev}}\) of items released again at \(d\);
- \(n^{\mathrm{all}}, \sum C^{\mathrm{all}}, k^{\mathrm{all}}\): everyone released at \(d_{\mathrm{prev}}\);
- \(k^{\mathrm{stay}}\): correct counts among stayers at \(d\).

\[
\begin{aligned}
E_d &= \frac{\sum C^{\mathrm{stay}}}{n^{\mathrm{stay}}} - \frac{\sum C^{\mathrm{all}}}{n^{\mathrm{all}}},\\
\Delta A_d &= \frac{k^{\mathrm{stay}}\cdot 1000}{n^{\mathrm{stay}}} - \frac{k^{\mathrm{all}}\cdot 1000}{n^{\mathrm{all}}},\\
\delta_d &= \Delta A_d - E_d - 3.
\end{aligned}
\]
Empty denominators contribute 0 to that term and the depth is skipped (no update). This is the identity solved for \(\delta\), in integers, truncating toward 0.

**Emit** at depth \(d\), using \(\delta\) frozen from **previous** items:
\[
C = \mathrm{clamp}\!\left(C^{\star} + \sum_{j=1}^{d_{\mathrm{idx}}}\delta_j - \pi,\; 1,\; 999\right),
\]
where the theater penalty \(\pi\) is 0 on a clean path and otherwise
\[
\pi = \min\big(400,\; \mathbf{1}_{f_3>0}\cdot 50 + \max(0, f_8 - f_8^{(1)})/8\big).
\]
\(\pi>0\) only if a flip or trauma happened, which implies the item is **not** in \(U_d\). So \(\pi\) does not move released-set \(G\). It does force \(C < C_{\mathrm{prev}}\) on a correct→wrong transition provided the drop exceeds any positive \(\delta\) that step; the \(50\)-thousandth flip term dominates \(\delta\), which is a difference of means and is typically tens, not hundreds. Cap \(|\delta_d|\) at 40 as a numerical guardrail so one corrupted transition cannot swing the head; the cap is a safety bound on a measured residual, and if it binds often the fork is already false (see falsifier).

No per-item running minimum. On a stable released path, \(C(d)-C(d-1)=\delta_d\), which is negative precisely when enrichment exceeds accuracy gain.

### (b) Failure modes

Walk the naive causal chain. A linear head puts a positive weight on \(f_2\) or on \(f_1\), both of which tend to grow with depth on stable items. Released mean confidence rises. Part of that rise is real enrichment \(E\) (low-margin items flipped and left the pool), part is the weight. Accuracy of stayers rises by \(\Delta A \le E\) on trap-like streams. \(G\) increases. B3 fires.

SRS blocks that chain at the accounting step, not at the feature step. Whatever \(C^{\star}\) was, the **depth derivative of every released item in the key is the same measured \(\delta\)**, and \(\delta\) was solved so that \(E + \delta - \Delta A = -3\) thousandths in expectation. Feature-driven depth inflation never enters, because depth and margin-velocity are not inputs to \(C\) after depth 1. Margin only chooses the depth-1 bin.

FM1: \(\rho\) plus a capped sum, clamped to \([1,999]\). FM3: 20 depth-1 bins. FM4: no spread knob. FM5: transition statistics are defined on the release mask, so the mask is observed rather than marginalized out. FM2: no \(f_7\). FM7 is only partially handled — keys pool across families, which is the point of the next paragraph and the likely flaw.

### (c) Bars

| Bar | Call | Why |
|---|---|---|
| B1 | Pass | Floor 1 |
| B2 | Conditional | V1 pass: flip adds \(\pi\ge 50\) and \(\lvert\delta\rvert\le 40\), so net drop. V2 pass **iff** \(\delta_d\le 0\) on keys that contain stable wrong items. Predicted V2 \(= 0\) on trap-like keys (where \(E>\Delta A\)) and possibly \(>0\) on honest keys (where the identity wants \(\delta>0\)) |
| B3 | Best large-cell behavior of the set | Algebra gives \(\mathbb{E}[\Delta G]=-3\) thousandths when moments match. Predicted violations: 2–5, almost all \(n<8\) |
| B4 | \(\sim 0.60\)–\(0.75\) if depth-1 margin bins are informative | Deep tax can pull a weak key down; cap of 40 per step limits the damage across 6 steps to 240 thousandths |
| B5 | \(\sim 0.22\)–\(0.35\) | Inherited from depth-1 bins and then shifted uniformly inside a key, so **within-key** gaps are preserved |
| B6, B7 | Pass | |
| B8 | Pass on large cells | Target band is a few thousandths below 0 |
| B13 | Risk exactly where \(\Delta A\) is large and \(\delta\) is capped at \(+40\) | Uncapped identity would track; the guardrail re-opens an underconfidence gap of size \(\Delta A - E - 40\) per step. Honest ceiling families are the exposure |

### (d) Falsifier

After \(\ge 200\) released transitions per depth, compare the **applied** \(\delta_d\) to the \(\delta\) recomputed from the same window’s stay/drop moments. If they differ by more than the truncation plus the cap on more than a quarter of key-depth cells, the residual is not actually the selection identity (bookkeeping bug or non-stationarity). Separately: if \(E_d\) estimated inside one battery differs in sign from \(E_d\) of the pooled key on \(\ge 3\) depths, cross-family pooling is false and SRS’s global-within-key assumption is dead — even if overall \(G\) looks acceptable.

### (e) \(P(\mathrm{survives}) = 0.22\)

The only fork whose \(G\)-update is a solved identity rather than a controller, so it cannot oscillate; it pays for that with a shared \(\delta\) across every family that lands in the same margin bin.

**Most likely death.** Ceiling family O (correct, low evidence, moderate margin) shares \((m,s)\) with trap items. Pooled \(E > \Delta A_{\mathrm{honest}}\), so \(\delta<0\) and honest deep accuracy runs away from a falling \(C\). B13 fails on O at \(d\in\{16,32,64\}\) with \(n_{\mathrm{rel}}\ge 8\). That is FM8 eating the closed form.

---

## Fork 3 — LST-WBA (Latched State Tax, Worst-Boundary Adversary)

### (a) Mechanism

A feedback controller on \(G\), region by region, with the adversary chosen deterministically as the worst depth boundary. No closed form; the measurement is \(G\) itself.

**Region** \(r=(m, yld)\) as in RSW (15 regions). **Latch:** at depth 1 store \(C^{\star}=\rho(k_r, n_r)\) from that region’s depth-1 released ledger. Features after depth 1 do not rewrite \(C^{\star}\).

**Tax table** \(T[d_{\mathrm{idx}}][r]\ge 0\), initially 0. Invariant enforced after every write: \(T[d][r] \ge T[d-1][r]\).

**Emit** (released or not):
\[
C = \mathrm{clamp}(C^{\star} - T[d_{\mathrm{idx}}][r] - \pi,\; 1,\; 999)
\]
with \(\pi\) as in SRS (0 unless flip/trauma; irrelevant to released \(G\)). Then if \(f_3\) just latched or \(f_8\) increased, \(C \leftarrow \min(C, C_{\mathrm{prev}}-1)\). Because \(T\) is monotone in depth and \(C^{\star}\) is fixed, a clean path is nonincreasing even before the flip rule. This is a **depth tax on a frozen base**, not a min() against a changing ledger value: the base does not move when the item’s margin grows, and two items in the same region share the tax schedule but keep their own \(C^{\star}\).

**Worst-boundary update** (the adversary). Maintain per region and depth the released running sums \(\sum C\), \(\sum y\cdot 1000\), \(n\). Let \(g[d] = \sum C/n - \sum y\cdot 1000/n\) once \(n\ge 8\), else carry forward \(g[d-1]\). Let
\[
d^{\star} = \arg\max_{d\ge 1}\big(g[d] - g[d-1]\big),
\]
ties to the larger depth (deeper selection has had more time to compound). If \(g[d^{\star}]-g[d^{\star}-1] > 0\), set \(T[d^{\star}][r] \leftarrow T[d^{\star}][r]+1\), then repair monotonicity by pushing the increment upward: for \(j\ge d^{\star}\), \(T[j] \leftarrow \max(T[j], T[j-1])\). If the worst boundary is already \(\le 0\) and some \(g[d] < -80\), decrement \(T\) at the **most negative** \(g\) subject to monotonicity and \(T\ge 0\). One unit per released outcome. No gain coefficient to tune: the step is 1 thousandth, the sign is the violation.

**B4 guard, region level not item level.** Track mean \(C\) of released **correct** outcomes in the region. If that mean falls below 520, freeze further tax increments in that region. This does not lift wrong items (no per-item floor at 500); it only stops a region whose correct members are already at the B4 line from being taxed further. Separation remains the gap between regions.

### (b) Failure modes

Naive head: confidence is a monotone function of depth and margin, so as \(U_d\) sheds low-margin items, mean released confidence rises (the \(E\) term) and \(G\) rises. A global bias cannot subtract \(E\) in a trap region without subtracting it in an honest region.

LST-WBA blocks the chain in two places. First the latch: margin growth after depth 1 is not an input, so the within-item contribution to \(\Delta G\) is \(\le 0\). Second the adversary: whatever enrichment remains shows up as \(g[d]-g[d-1] > 0\) **inside the region that produced it**, and the next unit of tax is applied exactly at \(d^{\star}\) and every deeper depth. Because dropped items are already gone, the tax falls only on stayers — which is the set whose mean was enriched. Regions that do not exhibit a rising \(G\) never get taxed, so an honest region whose \(\Delta A\) already offsets \(E\) is left alone. That is the per-family ceiling without a family label: the family is discovered as the region whose empirical \(G\) path misbehaves.

FM1: tax only moves \(C\) inside \((1, C^{\star}]\subset (0,1000)\), and the correct-mean freeze stops the controller from walking a region to the floor to buy B3. The fixed point of the controller, when it exists, is “worst boundary \(\le 0\) and all \(g\ge -80\)”, an interior band, not a clamp. FM5: the error signal is \(g\) on released cells, so abstentions do not hide the schedule; they are the reason \(g\) moved, and the controller sees the movement. FM3/FM4: \(C^{\star}\) still differs across margin bins; tax is a level, not a variance. There is no spread parameter that can anti-learn.

### (c) Bars

| Bar | Call | Why |
|---|---|---|
| B1 | Pass | Floor 1, and the freeze prevents a march to 0 |
| B2 | Pass structurally on clean and flipped paths | Clean: \(T\) monotone \(\Rightarrow C\) nonincreasing. Flip: extra \(-1\). Predicted V1=V2=0. This is the fork that should match NEC’s theater result without using NEC’s ledger ceiling |
| B3 | Improved, not guaranteed | Each violation is a one-thousandth tax on the offending boundary. Convergence is \(O(|G|\cdot 1000)\) released items per region. Early in the stream, violations persist. Predicted remaining violations after a long stream: 1–4, redteam |
| B4 | \(\sim 0.55\)–\(0.75\) | Freeze at 520 on the correct mean. Weak families whose **true** accuracy is \(<0.50\) still fail B4b; the guard cannot invent signal |
| B5 | \(\sim 0.20\)–\(0.30\) | Depth-1 \(\rho\) gaps, unchanged by a uniform tax. Borderline if margin bins are tight |
| B6, B7 | Pass | |
| B8 | Pass once the adversary has quieted, \(\lvert G\rvert\le \sim 0.05\) | The controller’s setpoint is the band \([-0.08, 0]\) |
| B13 | Controller tries; lag can overshoot | Decrement path exists, but monotonicity means you cannot lower a deep tax without lowering the shallow ones that may still be needed. Predicted one or two cells in \([-0.12,-0.10]\) during lag |

### (d) Falsifier

Instrument per-region \(E_d\) (defined as in SRS, analysis-only). If, after taxes have stopped changing for 500 released items, a region still has \(g[d]-g[d-1] > 0\) on a cell with \(n\ge 30\), the tax is not reaching the enriched items — the region definition does not align with the selection event, and “state-conditional ceiling” is false. A second, sharper kill: taxes still moving (no fixed point) after \(10^4\) released items, which means the unit-step adversary is chasing noise and the setpoint is not an equilibrium.

### (e) \(P(\mathrm{survives}) = 0.19\)

Structural theater plus a controller whose setpoint is exactly the B3/B13 band; the controller is slow, order-dependent, and can overshoot.

**Most likely death.** Monotone repair. A violation at depth 16 increments \(T\) at 16, 32, and 64. Depth 64’s accuracy gain then drives \(g[64] < -0.10\) before the decrement branch is allowed to unwind \(T[16]\), which it will refuse to do while \(g[16]\) is still slightly positive. B13 fails at the ceiling of an honest region. The adversary is greedily B3-safe and only lazily B13-safe.

---

## Fork 4 — MEY (Marginal-Yield Ledger)

### (a) Mechanism

No depth feature, no tax, no latch. The claim is that “overconfidence with depth” is specifically confidence that increases in **elapsed** depth, and elapsed depth should enter only as the denominator of yield.

**Key** \(q = (m, y)\):
- \(m = \min(4, f_1/200)\);
- marginal yield \(\mathrm{my}\) as in RSW;
- \(y = \min(3, \mathrm{my}/250)\) — 4 bins, the bottom bin is exactly “budget burned, no new evidence”.

Per depth index, per key, released counts \(n,k\) only. Emit
\[
C = \rho(k_{q,d}, n_{q,d}).
\]
Depth is a **stratum**, not an additive input. Two states with the same margin and the same evidence gained per budget burned look up the same stratum cell only if they are also at the same depth; the cell’s value is the historical accuracy of that situation, which is free to be lower at depth 64 than at depth 8. Nothing in the formula can add points for a larger \(d_{\mathrm{idx}}\).

**Path rule, yield-gated, not a ceiling.** Let \(q\) be the current key and \(q_{\mathrm{prev}}\) the previous step’s key.
- If \(f_3\) latched this step or \(f_8\) increased: \(C \leftarrow \min(C, C_{\mathrm{prev}}-1)\).
- Else if \(y < y_{\mathrm{prev}}\): \(C \leftarrow \min(C, C_{\mathrm{prev}})\). Wasted budget cannot raise confidence.
- Else (\(y\) nondecreasing, clean path): emit \(\rho\) even if it is higher than \(C_{\mathrm{prev}}\).

So confidence may rise only when this step’s evidence rate beat the previous step’s, and only up to the historical accuracy of that new situation. A pure depth increase with \(f_5\) flat moves the item into a weakly lower \(y\) bin and the middle rule blocks a rise.

**No learned weights.** The ledger is the parameter. Update after the label, released items only.

### (b) Failure modes

Naive chain: \(f_2 = d\cdot 1000/64\) gets a positive weight because, in aggregate, deeper released items are somewhat more accurate (selection). The weight then fires on **every** deep item, including those that got there by sitting still. Accuracy did not rise for those items. \(G\) rises with \(d\).

MEY removes \(f_2\) from the function class. The only depth effect available is which stratum’s accuracy you look up, and strata with zero marginal yield are populated by exactly the sit-still trajectories. If those trajectories are less accurate — the empirical content of “deliberation without evidence is not information” — their \(\rho\) is lower, and the path rule forbids using any other feature to climb back out. FM6 is attacked only on the part of enrichment that coincides with falling yield. Enrichment that happens **inside** a fixed key (high-margin items survive more, same yield) is **not** removed. That residual is the honest weak point; MEY does not claim to solve all of FM6, only the elapsed-depth channel.

FM1: pure \(\rho\). FM2: \(f_7\) absent; sole-survivor items only influence \(C\) insofar as they have a distinctive yield, which is an empirical question the ledger can answer either way. FM3: 20 keys. FM4: none. FM5: each depth has its own counts, fit only on items the mask released at that depth, so a depth schedule cannot hide in the abstention mass. FM8: low-evidence O items fall into \(y=0\) or \(y=1\) and do not share counts with high-yield traps.

### (c) Bars

| Bar | Call | Why |
|---|---|---|
| B1 | Pass | \(\rho\ge 1\) |
| B2 | Partial | Flips: structural \(-1\). Stable wrong items whose **yield bin increases**: \(C\) may rise with \(\rho\). Predicted V2 in the low single digits if traps consume evidence; 0 if traps are pure sit-still |
| B3 | Mixed | Sit-still selection is deflated. Within-bin selection remains and can still lift \(G\). Predicted violations: 3–6, i.e. not clearly better than NEC on B3 alone |
| B4 | \(\sim 0.65\)–\(0.80\) on keys that keep receiving evidence | |
| B4b | Fail risk on honest families that saturate \(f_5\) early | After \(f_5\) hits 1000, later steps have \(\mathrm{my}=0\), so a correct item is scored as a no-new-evidence item. If that cell’s accuracy is \(<0.50\), B4b fails |
| B5 | \(\sim 0.18\)–\(0.30\) | Borderline; yield must actually separate correct from wrong, not just separate depths |
| B6, B7 | Pass | |
| B8 | \(\lvert G\rvert\sim 0.03\)–\(0.08\) where the stratum is well populated | The zero-yield stratum can sit near \(-0.05\) to \(+0.05\) depending on who else lands there |
| B13 | The saturation case | Correct, evidence-saturated, deep cells scored at the zero-yield accuracy. If that gap exceeds 0.10, B13 fires. This is the predicted failure on ceiling families |

### (d) Falsifier

Restrict to items with nondecreasing \(f_5\) at every recorded step (evidence kept pace with budget). If those items still show a positive slope of mean \(C\) against \(d_{\mathrm{idx}}\) larger than the slope of their accuracy, on cells with \(n\ge 30\), then yield-keying did not remove depth inflation — some other feature inside the key (margin mix) is carrying it, and MEY’s causal claim is wrong.

### (e) \(P(\mathrm{survives}) = 0.15\)

Right attack on the elapsed-depth channel, incomplete attack on within-key selection, and a concrete saturation failure on long ceilings.

**Most likely death.** \(f_5\) saturates by depth 8 on honest ceiling items. Depths 16–64 all map to \(y=0\), whose ledger is dominated by genuinely stuck trap items with accuracy \(\sim 0.4\). Honest deep \(G \approx 0.4 - 0.85 < -0.10\). B13, and possibly B4b, on family O or P.

---

## Fork 5 — CDC (Cluster-Discovered Ceilings)

### (a) Mechanism

Per-family ceilings with no family input, by maintaining an explicit partition of index-level state and giving each block its own selection residual.

**State vector** (integers, thousandths), deliberately not including \(f_2\) or \(f_7\):
\[
x = (f_1,\; f_5,\; f_6,\; \min(f_8, 1000),\; \mathrm{my}) \in \mathbb{Z}^5.
\]

**Prototypes.** Up to \(K=8\) vectors \(p_c\). Assignment: \(c = \arg\min_j \|x-p_j\|_1\), tie to smaller \(j\).

**Birth / merge, both deterministic and threshold-free in the hand-tuned sense.** After the first 32 released items, set scale \(\tau\) to the 75th percentile of those items’ nearest-prototype distances (order statistic on a fixed prefix; recompute \(\tau\) every 256 released items as the median assignment distance \(\times 2\), integer). If \(\|x-p_c\|_1 > \tau\) and fewer than 8 prototypes exist, append \(x\) as a new prototype. If \(\|p_i-p_j\|_1 < \tau/3\), merge the higher index into the lower: counts add, prototype becomes the count-weighted mean, integer division. Running-mean update of the assigned prototype:
\[
p_c \leftarrow p_c + \frac{x-p_c}{n_c}
\]
with the division truncating toward 0. Order is fully determined by the deliberation stream, so reruns match.

**Per cluster, the SRS residual.** Each cluster keeps its own stay/drop sums and its own \(\delta_d(c)\), same formula as Fork 2, including the \(-3\) thousandth buffer and the \(|\delta|\le 40\) guard. Depth-1 base:
\[
C^{\star} = \rho(k_c, n_c)\quad\text{at }d_{\mathrm{idx}}=0.
\]
Emit \(C = \mathrm{clamp}(C^{\star} + \sum_{j\le d}\delta_j(c) - \pi,\, 1,\, 999)\), \(\pi\) as in SRS.

Clusters are recomputed from \(x\) at every depth, so an item can change cluster if its evidence state moves. On a cluster change along a clean path, \(C\) may jump. **Constraint:** if the new cluster’s emitted value exceeds \(C_{\mathrm{prev}}\) and \(\mathrm{my}\) did not increase, keep \(C_{\mathrm{prev}}\). If \(\mathrm{my}\) increased, allow the new value. Flip/trauma always applies the \(-1\) rule after that. This is a yield gate on cluster transitions, not a stored confidence ceiling.

**What is learned:** prototypes, \(\tau\), per-cluster counts, per-cluster residuals. No family bit, no constant of the form “cluster 3 is redteam.”

### (b) Failure modes

FM8 is the target. A single margin bin pools low-evidence correct O items with traps because both can have mid margins. Their \(E\) and \(\Delta A\) have opposite structures, so one \(\delta\) cannot serve both (this is SRS’s death). CDC’s claim is that those populations are far apart in \((f_5, f_6, f_8, \mathrm{my})\) even when \(f_1\) matches, so L1 prototypes split them before residuals are estimated. Each cluster then runs an identity that is valid **inside** a homogeneous selection regime.

FM6 is handled inside the cluster by the same identity as SRS. The discovery mechanism is the prototype split, not a hand partition: birth happens when an item is far from every existing center relative to the stream’s own median distance, so the number of regimes is data-determined up to the hard cap of 8 (the cap is a memory bound; if it binds, the falsifier below fires).

FM1: \(\rho\) again. FM2: \(f_7\) excluded so a binary pin cannot become its own cluster center by construction; \(f_6\) can, and if sole-survivor is real it shows up as low \(f_6\), with accuracy learned rather than stipulated. FM3: at most 8 bases. FM5: residuals are on released stay/drop, per cluster. FM4: none.

### (c) Bars

| Bar | Call | Why |
|---|---|---|
| B1 | Pass | |
| B2 | Same conditional as SRS, hopefully on fewer bad pairs | V2 iff some cluster has \(\delta_d>0\) and a stable wrong member. Separation of traps into their own cluster makes \(\delta\le 0\) there. Predicted theater: 0–2 |
| B3 | Better than SRS if clusters are pure; worse if fragmented | Pure clusters: \(\mathbb{E}[\Delta G]=-3\) thousandths. Fragmented clusters: tiny-n residuals with the wrong sign. Predicted violations: 2–5 |
| B4 | \(\sim 0.60\)–\(0.78\) | |
| B5 | \(\sim 0.24\)–\(0.38\) if clusters correlate with correctness, else fail | Eight-way partition can separate more than 5 margin bins, or can separate noise |
| B6, B7 | Pass | |
| B8 | Conditional on cluster purity | |
| B13 | Better than SRS on O | O should be its own cluster with its own \(\Delta A\), so it is not taxed at the trap rate. Fails if O and traps stay inside one prototype |

### (d) Falsifier

Post-hoc, labels used only as measurement: mutual information between assigned cluster and battery id, on released items after prototypes stabilize. If \(I(\mathrm{cluster};\mathrm{battery}) \approx 0\) (clusters ignore the battery axis and track only margin), discovery failed. A mechanical kill that does not need labels: if the merge/birth loop does not reach a fixed partition within the first 2000 released items (prototypes still moving by \(> \tau/10\) per 256 items), the partition is not a parameter, it is a moving target, and residuals computed inside it are meaningless.

### (e) \(P(\mathrm{survives}) = 0.16\)

Right response to FM8, but online clustering on a short stream is a good way to manufacture FM7 inside each cluster.

**Most likely death.** Birth order. The first batteries encountered occupy the 8 prototype slots with fine margin distinctions; a later ceiling family is forced into the nearest trap-adjacent prototype because the cap bound. Residuals there are trap residuals. B13 fails on that family, and the merge rule never fires because the prototype was pulled toward a compromise center whose distance to both populations sits just above \(\tau/3\).

---

## Fork 6 — IFP (Interior Fixed-Point Head)

### (a) Mechanism

This one exists to kill clamp attractors and the uniform manifold directly, and to show why that is not enough for B3. It is a real fork, not a footnote: its emitted value is a contracting map with a unique interior fixed point per depth stratum.

**Fast score**, features excluding \(f_2\) and \(f_7\): \(f_1, f_5, f_6, \max(f_4,0), \mathrm{my}\), each in thousandths. Integer weights \(w_i\), bias \(b\), initialized at 0. Linear score
\[
s = b + \left\lfloor \frac{\sum_i w_i f_i}{1000} \right\rfloor.
\]

**Codomain map, permanent pseudocounts.** Maintain global \((A,B) = (1,2)\) and per-depth \((A_d, B_d)\), invariant \(1 \le A \le B-1\) always. Emit
\[
C = \frac{(A_d + \max(s,0))\cdot 1000}{B_d + |s| + \max(-s,0) + 1},
\]
which is the same shape as \(\rho\): numerator \(\ge 1\), denominator \(\ge\) numerator \(+1\), so \(C\in[1,998]\) for every finite \(s, A_d, B_d\). Increasing \(s\) moves \(C\) up but with derivative \(\sim 1/B_d \to 0\) as data accumulate. The weights cannot shove mass onto a clamp; the best they can do is saturate the **influence** of \(s\), at which point \(C\) collapses to the depth base rate \(A_d\cdot 1000/B_d\), an interior point. That collapse is detectable (see falsifier) and is exactly FM3, so the update penalizes it.

**Update, deterministic, released items only.**
1. Counts: \(B_d \leftarrow B_d+1\); if \(y=1\) then \(A_d \leftarrow A_d+1\). Invariant holds.
2. Weight step with mandatory decay, learning rate \(1/(1000+t)\) in integer arithmetic:
   \[
   w_i \leftarrow w_i - \left\lfloor\frac{w_i}{1000+t}\right\rfloor + \left\lfloor\frac{(1000y - C)\cdot f_i}{1000\cdot(1000+t)}\right\rfloor,
   \]
   and the same for \(b\) with \(f=1000\). Decay runs on every step, including when the error term is 0, so \(w=0\) is the unique origin and nonzero weights exist only while they keep paying for themselves in squared error.
3. **Outward-clamp freeze:** if \(C\ge 980\) and \(y=1\), or \(C\le 20\) and \(y=0\), skip the error term (decay only). The gradient that would push further out is dropped.
4. **Monotone depth coupling of the base rate.** Let \(\mu_d = A_d\cdot 1000/B_d\). If \(\mu_d > \mu_{d-1} + 20\) and the extra is not supported by an increase in mean \(\mathrm{my}\) at that depth (mean \(\mathrm{my}\) tracked alongside), subtract the excess by incrementing \(B_d\) without \(A_d\) (adding failures-worth of pseudocount mass, one unit). This is a structural drag on depth-only base-rate inflation. It can fire at most until \(\mu_d \le \mu_{d-1}+20\).

**Theater.** Same flip rule as MEY: leader-change or trauma increase forces \(C \leftarrow \min(C, C_{\mathrm{prev}}-1)\). No general ratchet, because a ratchet plus this head would just be NEC with different features.

### (b) Failure modes

FM1, mechanistically. A clamped linear head has zero gradient at 0 and at 1000, so SGD treats the clamp as a solution; the optimizer dumps a large positive bias there and B5/B13 die. IFP’s emit function has nonzero derivative for every finite \(s\), the count invariant excludes \(\{0,1000\}\), decay makes unbounded weights a non-equilibrium, and the outward freeze removes the gradient at the boundary. The only equilibrium of the fast weights at fixed counts is the normal equation of the decayed least-squares problem, whose predictions sit near the conditional mean, which is interior whenever both labels occur.

FM3. The uniform manifold is the large-\(B_d\) limit where \(s\) does not move \(C\). Decay plus a live error term fights that, but if features are uninformative the equilibrium **is** the base rate and B5 fails honestly. IFP does not fake separation.

FM4. No spread parameter. FM2. \(f_7\) absent, and a weight that tried to recreate it from \(f_6\) near 0 is subject to decay and to the ledger, not wired to a pin. FM5. Depth coupling uses per-depth released base rates, so the mask defines the strata. What IFP does **not** do is subtract \(E_d\). A positive weight on \(f_1\) still lets stayer mix raise mean \(C\) inside a depth. The \(+20\) coupling only limits the **base rate**, not the feature-conditional mean. So FM6 is only weakly addressed. That is deliberate: this fork isolates “fix the dynamics” from “fix selection,” and should be read as a control as much as a candidate.

### (c) Bars

| Bar | Call | Why |
|---|---|---|
| B1 | Pass | Invariant |
| B2 | Fail risk, same as any non-latched head | Stable wrong item with rising \(f_1\): \(s\) rises, \(C\) rises, V2. Predicted V2 \(> 0\). I do not expect this fork to be the theater survivor |
| B3 | Weak | Base-rate coupling stops the crudest depth inflation. Feature-mix enrichment remains. Predicted violations: 4–8, not better than NEC |
| B4 | \(\sim 0.58\)–\(0.75\) once \(t\) is large | |
| B5 | \(\sim 0.15\)–\(0.28\) | The bar most likely to miss, because decay shrinks weak signals toward the base rate |
| B6, B7 | Pass | |
| B8 | \(\lvert G\rvert\) maybe \(0.04\)–\(0.10\) | No servo pulling \(G\) into a band |
| B13 | Moderate risk | Coupling allows \(\mu_d\) to exceed \(\mu_{d-1}\) by 20 thousandths per step, six steps is 120, which can overshoot accuracy and also, in the other direction, the pseudocount drag can undershoot. Both tails are open |

### (d) Falsifier

The core claim is about dynamics, so the kill is a fixed point, not a bar. Log \(\max_i |w_i|\) and the fraction of emits with \(C\in[1,20]\cup[980,999]\). If after \(10^4\) released updates either the max weight is still growing linearly with \(t\) (decay is not contracting) or more than 5% of emits sit in those edge bands, the interior-fixed-point claim is false. A pure bar failure with weights converged and edge-mass \(\approx 0\) does **not** falsify IFP; it falsifies the hope that good dynamics imply monotone \(G\).

### (e) \(P(\mathrm{survives}) = 0.10\)

It is the correct anti-clamp machine and a weak selection machine. Included because a fork set that only stacks selection corrections will rediscover clamp attractors the moment a linear score is added back, and because its falsifier is independent of B3.

**Most likely death.** B2, via margin. Second most likely: B5, via decay winning against a real but small feature signal and flattening the head (FM3 at equilibrium, legitimately).

---

## Ranking

1. **RSW** — the only design that treats the V2/B13 lemma as a measured regime split rather than picking one illegal corner globally.
2. **SRS** — same correction as a solved identity, so no controller lag and no oscillation; loses to RSW only because one \(\delta\) is shared across families inside a margin bin.
3. **LST-WBA** — structural theater without a ledger-min ratchet, and the tax is applied where \(G\) actually rose; monotone repair makes it B13-fragile at large depths.
4. **CDC** — the right FM8 fix (discover the partition, then run SRS inside it) but online prototypes on a short, ordered battery list will often fail to discover it.
5. **MEY** — cleanly deletes elapsed depth from the function class; does not price within-key selection, and evidence saturation on long ceilings maps honest items onto the trap bin.
6. **IFP** — dynamics worth having (unique interior fixed point, decay, outward gradient dropped) but it does not subtract enrichment, so it should not be expected to beat NEC on B3.

**What I would not run.** Any linear reweighting of \(\{f_1..f_8\}\), any scheme whose only monotone element is a per-item min against a pooled ledger, and any target of \(G=0\) with no negative buffer. The first cannot see \(E_d\). The second is NEC. The third is a random walk on the wrong side of a \(1\mathrm{e}{-12}\) test.
