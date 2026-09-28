# H5 Scaffold-and-Release — Grok-4.7 Design Pass

**Date:** 2026-09-24
**Model:** grok-4.7, `reasoning_effort=high`, via UnoRouter streaming wrapper
(`~/workspace/skills/unorouter/bin/grok47_stream.py`)
**Method note:** the single 4-question prompt returned empty streams 4×
(provider emitted ~200–300 reasoning chars then `[DONE]` with zero content;
a short ping and a brief+summary prompt both succeeded, so the model was
healthy — the failure mode was unbounded-response planning). The task was
therefore split into 4 sequential calls (one per question), each with the
full brief (§0–§5: law, frozen head, training protocol, v1/v2/T-05 evidence,
scaffold-and-release rule) plus a per-response word cap (1500–1800 words).
All four calls completed with substantive content. Raw part files:
`grok_sr_Q1.txt` … `grok_sr_Q4.txt` in this directory.
**Status:** UNCOMMITTED — the round coordinator reviews first (per task).

Grok was briefed with the full contents of `VERDICT_TRAINING.md`,
`v2/PREREG_TRAINING_V2.md`, and `backlog/t05/VERDICT_T05.md`, plus the exact
L-OVERCONF operationalization (G = mean released conf − accuracy;
V1 = correct→wrong flip with conf non-falling; V2 = wrong→wrong with
conf rising; abstention at either depth = no violation; 100%-abstain depth =
G undefined).

---
---

# PART 1 — Three scaffold-and-release schemes (Q1)

# Scaffold-and-release designs (Q1)

Shared arithmetic the schemes are built against. Update is \(w_i \leftarrow w_i - \mathrm{tdiv}((2(C-Y)+8\cdot\mathrm{rise})f_i,\ 40000)\), \(b \leftarrow b - \mathrm{tdiv}(2000(C-Y)+8000\cdot\mathrm{rise},\ 40000)\). A coordinate is inert unless \(|\mathrm{num}|\ge 40000\).

- With \(\mathrm{rise}=0\): need \(|C-Y|\cdot|f_i|\ge 20000\). Bias moves by \(\mathrm{tdiv}(C-Y,\ 20)\) per cell (\(|C-Y|\ge 20\)).
- \(f_2=t\cdot 1000/64\). At depth 1, \(f_2=15\), so \(|2(C-Y)f_2|\le 30000<40000\): **w2 cannot move at d=1 even at max error**. Depth 8 (\(f_2=125\)) needs \(|C-Y|\ge 160\). Theater on w2 needs \(\mathrm{rise}\cdot f_2\ge 5000\).
- Init \(C\approx f_1\), correct logic already near \(Y\): upward num on \(f_5\) truncates to 0. A wrong P/O cell (\(C-Y=1000\), \(f_5\approx 280\)) steps **w5 by −14**. Sign is the crush direction. The brief’s separating \(w_5\sim +1500\) is reachable only after correct high-\(f_5\) cells are made underconfident so \(2(Y-C)f_5\ge 40000\) (logic \(f_5\approx 976\) ⇒ \(|C-Y|\ge 21\)).
- Theater fights that sign: \(\mathrm{rise}=100\), \(f_5=400\) ⇒ num \(=320000\), step **−8 on w5**, larger than the w2 step at mid-depth (\(\mathrm{rise}=100\), \(f_2=125\) ⇒ step −2). Theater must be detached from \(w_5\) or the separator never goes positive.
- \(f_3=0\) on every M4-released cell (release iff leader unchanged). **w3 is dead.** Any scaffold that routes signal through \(f_3\) is a no-op.
- \(f_7=1000\) cells have \(f_1=1000\) by the harness pin. One wrong pin cell steps a live weight on \(f=1000\) by \(\mathrm{tdiv}(2\cdot 1000\cdot 1000,\ 40000)=-50\). Left on w1, ~20 pin cells zero the honest margin channel. w7 is the non-shared absorber: non-pin cells have \(f_7=0\), so w7 does not tax logic.
- G-batch is one-sided on **b only**: \(b\leftarrow b-\mathrm{tdiv}(\Delta G,\ 4)\). One family-step of \(\Delta G=40\) (0.040 if G is in thousandths) moves b by −10. Worst case ~54 (family × depth-step) firings ≈ −500/epoch if rises are widespread — enough to finish a collapse v1-style. Schemes must keep G non-rising so this term stays idle.
- T-05 crush arithmetic: \(f_6=1000\), \(C-Y=1000\) ⇒ **Δw6=−50/cell**. Forty cells ⇒ \(w_6=-2000\), and logic \(f_6\approx 917\) then loses \(\approx 1834\) confidence points. w6 must not be free while that residual exists.

Standing failure modes a scheme is killed for: crutch (prediction identity lives in the scaffold input; after disconnect \(C\to f_1\) or \(C\to 0\)), mean-sacrifice (\(|w_6|\) large, logic meanConfCorrect drops >0.10), truncation stall (separator never exceeds the floor), theater sign-flip on w5, G-batch drain of b, w3 wasted, pin gradient dumped into w1.

Post-release “persisted” bar used by all three (eval with epoch-end weights, scaffold off): meanConfCorrect ≥ 0.60, meanConfWrong ≤ 0.25, logic meanConfCorrect drop across the disconnect ≤ 0.10, V2 ≤ 5 (from 44), G-rises ≤ 1, \(|w_6|<100\), \(w_5\ge +500\), \(w_7\le -500\), \(w_1\in [600,1400]\), mean conf on released \(f_7=1000\) cells ≤ empirical accuracy of those cells + 0.10. Collapse signature: meanConfAll < 0.05, or \(w_5\le 0\) and \(w_7=0\) with the pre-disconnect fit not surviving.

---

## Scheme 1 — Pin firewall, theater reroute, separator boost

**(a) Scaffold.** No extra term inside \(C\). Training-only integer gradient mask, fixed (deterministic):

- \(i=7\) (pin) and \(i=5\) (evidence): theater coefficient **0**; calibration numerator multiplied by \(B=5\): \(\mathrm{num}_i=10(C-Y)f_i\). Floor drops from 20000 to 4000. Then \(f_5=280\) moves once \(|C-Y|\ge 15\) (step at full error: \(\mathrm{tdiv}(10\cdot 1000\cdot 280,\ 40000)=-70\), five times the unboosted −14). \(f_7=1000\) moves once \(|C-Y|\ge 4\).
- \(i\in\{2,8\}\) and \(b\): standard num, theater **kept** (these are the anti-rise absorbers).
- \(i=1\) **iff \(f_7=1000\)**: \(\mathrm{num}_1=0\) (pin error cannot touch the margin channel). Non-pin cells update w1 normally.
- \(i\in\{3,4,6\}\): \(\mathrm{num}=0\) for the whole scaffold (w3 dead, w4 unused, w6 is the crush coordinate).

Privileged bit is the pin test, which is already in \(f_7\); the family label is not required.

**(b) Release.** Hard cutoff, no anneal. Epochs 1..N_s run the mask (N_s = 2 per phase at 1×, scaled with the schedule). SIGNAL_DISCONNECT at the next epoch boundary, in order: (1) freeze a snapshot of \(w,b\); (2) set \(B=1\), restore theater on every live coordinate, unfreeze w1 on pin cells, unfreeze w4 and w6; (3) run exactly 2 ordinary v2 epochs (G-batch still on); (4) freeze the head for eval. w3 stays structurally dead. Anti-saturation clamp unchanged.

**(c) Expected lock.** w7: ~30 wrong pin presentations × (−50) ≈ **−1500** (boost makes this faster, not larger in sign). w5: upward only where boosted underconfidence exists; this scheme does **not** by itself create \(C<Y\) on correct logic, so w5 is predicted **≤ 0** unless Scheme 3’s offset is stacked. Standalone, Scheme 1 is the pin/theater scheme, not the separator scheme — do not expect \(w_5=+1500\) from it. w2: negative, order **−100 to −400**, because only deeper cells clear the floor (d≥8). w6=0, w1≈1000, b≈ −200..−600 from ordinary calibration plus any G-batch. Persistence vs collapse: across the 2 release epochs, \(|\Delta w_1|\le 30\) and logic meanConfCorrect drop ≤ 0.05 ⇒ firewall residue transferred; \(|\Delta w_1|>100\) or w7 drifting back toward 0 ⇒ crutch (gate was load-bearing). \(|\Delta w_6|>50\) in those 2 epochs ⇒ theater reattachment reopened the crush; kill.

**(d)** Boost is what makes \(f_5=280\) and shallow-ish pin residuals representable before \((C-Y)\) shrinks under the floor. Detach is what stops theater’s −8/cell from cancelling w5. G-batch still drains only b; w2<0 is the intended reason it should not fire. Failure: if w2 never leaves 0 (all mass at d≤4), G-batch remains the only anti-rise tool and will walk b down. Telemetry kill: G-batch cumulative \(|\Delta b|>300\) while meanConfCorrect < 0.50.

---

## Scheme 2 — Truncation lock and honest replay

**(a) Scaffold.** Data-stream and loss-weight only. Fixed ring buffer of Phase-A released cells (file order). In Phases B and C, after every adversarial cell, replay the next ring cell once (1:1, deterministic). Integer multipliers on the whole numerator: \(\lambda_H=4\) (ring / honest), \(\lambda_A=1\) (P/O/trap/redteam). Separately, **w6 updates are forced to 0** while the scaffold is on. Replay does not change features or \(C\).

**(b) Release.** SIGNAL_DISCONNECT: drop the ring (natural stream only), set \(\lambda=1\), **then** unfreeze w6, run 2 ordinary epochs, freeze for eval. Order matters: unfreezing w6 before the stream is rebalanced reopens T-05.

**(c) Why it can persist.** After calibration, high-\(f_6\) cells with \(|C-Y|<20\) have \(|2(C-Y)f_6|<40000\), so **w6 cannot move**. The truncation floor is the lock. Expected: \(w_6=0\) through release, w1 and b held near their Phase-A values by the 4× replay (without it, Phase C’s −50/cell dominates). Measurable: in the 2 release epochs, w6 steps = 0 and logic meanConfCorrect moves ≤ 0.05 ⇒ locked. w6 stepping by ≥ 8/epoch ⇒ residual or theater still above the floor; scheme failed, do not deploy those weights.

**(d) Arithmetic gap, stated so it is not papered over.** At init, honest correct cells have \(C\approx Y\), so \(\lambda_H=4\) multiplies ~0. Adversarial cells still contribute −50 to any **unfrozen** shared weight. Replay therefore **cannot** save w6 at the start; the hard freeze is the actual scaffold, replay only protects w1/b once honest residuals exist. Theater bypasses the \(|C-Y|<20\) lock: \(\mathrm{rise}=40\), \(f_6=1000\) ⇒ num \(=320000\), **Δw6=−8 per V2 cell**. Forty-four V2s ⇒ \(w_6\approx -350\), not yet −2000, but enough to start mean-sacrifice. Scheme 2 is valid only if Scheme 1’s theater-detach on \{5,6\} stays in force until V2≤5; then reattached theater sees \(\mathrm{rise}<5\) and \(8\cdot\mathrm{rise}\cdot 1000<40000\). G-batch is orthogonal (bias only) and is not muted.

---

## Scheme 3 — Forced underconfidence offset, then level restore

**(a) Scaffold.** Additive integer offset inside the pre-clamp sum, training only:

\[
C=\mathrm{clamp}\big((\textstyle\sum w_i f_i)/1000 + b + s,\ 0,\ 1000\big)
\]

\(s\) is not a learned feature and not a family table (a family table is memorized by \(b\) or by \(s\) and dies on removal). Schedule, frozen: epochs S1, \(s=-300\); S2, \(s=-150\); S3, \(s=0\) permanently. During S1–S2 **freeze \(b\), w1, and w6**. Update only w5 (boost \(B=5\), theater off, as in Scheme 1), w7 (pin firewall on), w2 and w8 (theater on). Freezing \(b\) is mandatory: if \(b\) is live it absorbs \(s\) one-for-one (\(b\leftarrow b-s\)) and every \(w_i\) stays at init — disconnect then shifts the level by \(+300\) and the offset was a pure crutch.

**(b) Release.** S3 sets \(s=0\) (hard; the −150 step is the only anneal). Then unfreeze \(b\) for 2 epochs with w1 and w6 **still frozen**, so the level is reset by bias under the new w5/w7/w2. Then SIGNAL_DISCONNECT proper: unfreeze w1 and w6, \(B=1\), theater restored on all live coords, 2 ordinary epochs, eval freeze. Snapshot weights at each boundary.

**(c) Numbers.** S1, logic correct, \(f_5=976\), offset pushes \(C-Y\approx -300\) if \(f_1\) was near \(Y\) (deeper if \(f_1\) was already low — clamp at 0 caps the residual at −1000). Unboosted step \(\mathrm{tdiv}(2\cdot 300\cdot 976,\ 40000)=\mathrm{tdiv}(585600,\ 40000)=+14\) into w5 per such cell; with \(B=5\), **+70**. ~20 effective logic presentations ⇒ **w5≈+1400**, in the brief’s separating band. Opposing P/O term at full error is −70×(presentations); S1 must be Phase-A-heavy or P/O wins the sign. Do not run raw Phase C inside S1. After \(s=0\) and b unfrozen, b should settle near **−300..−700**: \(C_\mathrm{logic}\approx 1000\cdot f_1/1000 + 1.4\cdot 976 + b\) clamped to ~700–1000; \(C_{P/O}\approx f_1 + 1.4\cdot 280 + b \approx f_1+392+b\), so b≈−500 yields P/O near \(f_1-100\), not a universal zero. Pin: w7≈−1000..−1500, \(C_\mathrm{pin}=\mathrm{clamp}(w_1+w_7+b,\ 0,\ 1000)\approx 0\) if pins are wrong. Persistence: at \(s=0\), meanConfCorrect ≥ 0.60 and ≥ 0.50 of the S1 value; w5 stays ≥ +500 across the final 2 epochs; logic drop ≤ 0.10. Collapse: b walks to ≤ −5000 after \(s\) returns (G-batch or theater), meanConfAll < 0.05, w5 stuck ≤ 0 (Phase C was let into S1).

**(d)** The offset is the only thing here that manufactures the upward num the floor was eating. \(B=5\) is optional once \(|C-Y|\ge 21\) on logic; it matters for \(f_5\approx 280\) cells that must not dominate the sign (their downward step scales by the same B — so boost does **not** change the P/O-vs-logic step ratio, only whether shallow residuals register). Theater stays off w5 through S2 or the +14 is eaten by −8 V2 steps. G-batch is off while b is frozen (skip the b write, still count would-be firings). When b unfreezes, if firings × typical \(\mathrm{tdiv}(\Delta G,4)\) sum past −300, abort: the law term is about to undo the level restore. w6 freeze plus the Scheme 2 floor-lock is what stops the restored level from being spent on the crush coordinate.

---

## Stacking and kill tests

Run as one protocol: Scheme 3’s \(s\)-schedule and freezes, Scheme 1’s mask inside it, Scheme 2’s ring only after \(s=0\) while w6 is still frozen, then the shared 2-epoch ordinary release. Kill the stack if any of: final weights equal init; \(w_6\le -200\); w5≤0; w7=0; meanConfCorrect < 0.60; logic drop > 0.10; V2>5; any strict G-rise on an honest family; G-batch \(|\Delta b|>300\) after b is unfrozen; pin-cell mean conf > accuracy+0.10. A head that is calibrated only while \(s\neq 0\) or while w6 is frozen, and misses the bar on the ordinary release epochs, is a crutch, not a learned policy.

---

# PART 2 — Predicted failure mode per scheme (Q2)

S1 fails by crutch-dependence, S2 by mean-sacrifice, S3 by degenerate crush. Shared arithmetic, used below: DIV2 = 40000, so a calibration step on b is `tdiv(2(C−Y)·1000, 40000) = tdiv(C−Y, 20)` and a theater step is `tdiv(8·rise·1000, 40000) = tdiv(rise, 5)` (rise counted only on V2rise, else the loss derivative is just `2(C−Y)`). Weight step is `tdiv([2(C−Y)+8·rise]·f_i, 40000)`. Init C = f1, so correct cells with margin ≈ 1000 are gradient-silent and epoch-1 sign is set by wrong cells.

### S1 — crutch-dependence
Reading: pin cells (f7=1000) update only w7; the `8·rise` term is applied to a scaffold weight w_T on a training-only f_T=1000; separator boost is a scaffold feature, not a permanent w5.

The firewall is the part that survives. A wrong pin has numerator `2·1000·1000 = 2_000_000`, step `tdiv = 50` into w7 only. That is the right sink, and f7 still exists at deployment, so pins do not cause the kill.

Theater does. One V2 cell with rise=200 moves w_T by `tdiv(200, 5) = 40`. The same cell moves real w2 by only the calibration piece: at the shallow steps the law actually checks, f2 = t·1000/64 ∈ {15, 31, 62}, so `2·800·15 = 24_000 < 40_000` → step 0, and even at t=8 (f2=125) the step is `tdiv(200_000, 40_000) = 5`. Scaffold outruns depth ~8:1. Once w_T has flattened rise, the theater term shuts off and w2/w8 stop seeing a path penalty at all. Separator mass goes the same way: epoch-1 `(C−Y)>0` on P/O, so the boost coordinate is driven negative on the scaffold copy instead of into durable w5.

Fixed point in training: C ≈ Y on adversarial cells only because `(w_T·f_T)/1000` sits in the sum. At SIGNAL_DISCONNECT that term is deleted, ΔC = −w_T ∈ [+400, +1000] on exactly the cells that were doubling down, while w1 stays large and positive (firewall kept pin crush off it; correct cells never needed to cut it). Margin still grows with depth, so C(d+1)>C(d) on still-wrong items: the v2 residual (order 44 V2, plus G-rises where the rebound exceeds acc) returns in one shot. Honest families, which never loaded f_T, stay put — the signature of a crutch rather than a sacrifice.

### S2 — mean-sacrifice
Reading: no extra forward feature. Truncation lock discards the tdiv remainder (no residual latch). Honest replay is one extra pass, and it does not out-volume Phase C, which is last in the A→B→C epoch.

Online order is the whole optimizer. A single wrong cell with C−Y=800 moves b by `tdiv(800, 20) = 40`; a V2 cell adds `tdiv(rise, 5)` (rise=200 → 40 more). A replayed honest cell cancels that only when it is already miscalibrated: `|C−Y|<20` ⇒ bias step 0, and `|2(C−Y)f_i|<40_000` ⇒ weight step 0. Near-calibrated honest cells, the ones replay is supposed to protect, are exactly the dead zone. Deep f2 can move (t=64, f2=1000), but the adjacent steps 1→2→4 cannot, so replay never builds a negative depth slope where the law measures it.

So each epoch’s Phase C pass walks shared b and w1 down by ~40 per live adversarial cell, and replay claws back only until honest `|C−Y|` sticks its head out of the dead zone — a few steps, not a full restore. w6 is the collateral carrier: it is large on both P/O (f6=1000) and logic (f6≈917), it clears DIV2 easily (`2·800·1000 = 1_600_000`, step 40), and nothing family-private remains unlocked at shallow depth. Fixed point: one pooled level, honest correct-cell mean pulled from ~0.75 toward the adversarial mixture, adversarial G still ≥0. That is mean-sacrifice, not crush: a correct cell that actually hits C=0 has step `tdiv(−1000, 20) = −50`, i.e. b += 50, so the floor repels and the equilibrium sits in the interior dead zone.

### S3 — degenerate crush
Reading: phase 1 adds a forced downward offset (scaffold bias or a target shift toward 0); phase 2 “restores level” by one additive b += B with little or no SGD after it.

Phase 1’s only stable point under a forced-underconfidence term is the clamp. Both depths of a wrong trajectory sit at C=0, so rise=0, theater numerator is identically 0, and w2/w4/w8 get no path gradient. Correct cells are also driven into the floor, so the separating direction on f5 is never expressed: getting C=0 for every s is solved by w≈0, b≤0, which erases the init w1=1000 rather than reshaping it. Clamp censors the residual, so the stored logit is “below 0,” not “E[Y]−B.”

Restore adds one constant. Formerly correct cells land on the ceiling C=1000=Y and go silent (`C−Y=0` ⇒ every numerator 0). Formerly wrong cells land at C=B, Y=0: b-step `tdiv(B, 20)`, which is 20 per cell at B=400, and the same sign on w1. With Phase C ordered last, those unopposed downward steps run to the end of the epoch. Because phase 1 zeroed the feature weights, there is no f5/f7 structure left to make the downward move family-conditional, so honest cells are carried through the floor with the adversarial ones. Fixed point of that transient, given a restore that does not then re-optimize for hundreds of epochs, is raw ≪ 0 and released conf ≡ 0 — the v1 point (b large negative, w back near a dead init), which the strict law fails by degeneracy and which any later unclamp turns into G-rises. The +50/cell repulsion exists only if further symmetric SGD is run after restore; the scheme as named spends that budget inside phase 1, where the offset cancels it.

Word count: ~1180.

---

# PART 3 — Critique and ranking of the four arms (Q3)

The binding geometry is shared by every arm, so it comes first.

Released confidence is affine: \(\Delta C \approx \sum_i w_i\Delta f_i/1000\) on any adjacent depth pair (interior to the clamp). \(\Delta f_2=t\cdot1000/64\) is strictly positive on every item. A wrong→wrong pair with the other features flat therefore has \(\operatorname{sign}(\Delta C)=\operatorname{sign}(w_2)\). V2 is \(y=y'=0\) and \(\Delta C>0\), so \(w_2>0\) is an immediate V2 on every such pair. From depth 32→64, \(\Delta f_2=500\); \(w_2=+200\) already yields \(\Delta C=+100\). Init has \(w_2=0\), and any later positive value re-opens the law.

V2/V1 inequalities constrain only pairs that are wrong at the later depth. Honest cells that stay correct generate none. G is not invariant in the way the code assumes: the epoch G-batch updates only \(b\). A constant shift \(k\) gives \(G'(d)=G(d)-k\) at every depth, so \(\Delta G\) is unchanged. `b ← b − tdiv(ΔG, 4)` cannot kill a rise; repeated, it is a degeneracy pump (the v1 path). Only weights on features that actually move with depth — \(w_2,w_4,w_5,w_6,w_8\) — can move \(\Delta G\) or \(\Delta C\).

The legal cone is therefore: \(w_2\le 0\), \(w_7<0\) enough that pin cells (\(f_7=1000\) contributes exactly \(w_7\) after the `/1000`) sit within accuracy+0.10, baseline \(b+w_1 f_1\) high enough that correct-cell mean stays ≫0, and no positive-weight feature increasing on wrong→wrong pairs. Strict G allows confidence to fall while accuracy is flat: negative \(w_2\) is legal on honest families. Round 2 already showed those families can sit at G=0 with mean correct-cell confidence 0.747, so a high flat level is empirically enough. The squared-loss optimum need not lie in that cone. At \(C=750\), a wrong cell’s \(|2(C-Y)f_2|\) is \(3\times\) a correct cell’s. Wrong mass must exceed ~25% of \(f_2\)-weighted deep cells to make the pooled gradient on \(w_2\) negative. Adversarial cells are a minority, so pooled SGD, greedy or batched, keeps \(w_2\ge 0\) and pays 44 V2 as the cheap residual. T-05’s separator (evidence-fraction level gap, P/O≈280 vs logic≈976) shows a non-crush level split exists; it does not show a feasible point of this cone. That is the open question.

**(a) Non-greedy worst-case optimizer**

Strongest argument: on a fixed M4 release set, interior to the clamp, V1, V2 and per-family \(\Delta G\le 0\) are linear inequalities in \(w\), plus a non-degeneracy floor (correct-cell mean \(C\ge 500\)). That is a deterministic integer feasibility problem: fixed family/depth/coordinate order, \(\pm\) steps or exact line search on kink points, accept only lex improvement \((N_{V2}, N_{V1}, N_{G\uparrow}, -\overline{C}_{\text{correct}}, \|w\|_1)\). No RNG. If the cone is nonempty, this procedure can return a point and greedy averaging cannot, because the average gradient points outside the cone. Pin motion is not the obstacle: \(|C-Y|=500\), \(f_7=1000\) gives numerator \(10^6\), `tdiv(·,40000)=25`, so \(w_7\) moves whenever pin cells are miscalibrated. The dead zone that mattered in v1 was the old divisor, not this constraint system.

Sharpest objection: T-05 did not exhibit a cone point, only a level split, and the clamp makes the real map piecewise. A “batch SGD” or averaged least-squares reading of this arm minimizes \(\sum(C-Y)^2\), whose optimum is exactly the out-of-cone compromise Arm L already found (P/O G≈+0.42→+0.47). Implemented that way, (a) is a false test. Infeasibility is also the likely outcome if some wrong→wrong pair moves only \(f_2\) while some V1 pair in another family requires a positive depth slope that no other \(\Delta f\) can cancel.

Deciding experiment: one deterministic integer constraint descent from the frozen init, 100× budget, box \([-2\cdot10^6,2\cdot10^6]\), lex objective above, no pooled SSE term. Pass: zero V1/V2, zero strict G-rises, meanConfCorrect≥0.50, \(w_7\neq 0\). Alongside, dump the inequality system and its feasibility bit. Batch-LS is not an acceptable implementation.

**(b) Explicit uncertainty architecture**

Strongest argument: a second linear head, a margin-of-margin, or a two-sided interval, if it actually changes the scalar that enters G, might encode “disagreement” the symmetric loss never sees.

Sharpest objection: it doesn’t, under the frozen locus. The policy may read only \(f_1..f_8\), and \(C\) is one integer in \([0,1000]\). Two linear heads and an interval subtracted in integers are still one affine function of the same eight features — the same hypothesis class, the same cone, the same outvoting. Releasing the lower endpoint is a downward bias, i.e. (c)/(S3), and bias cannot fix \(\Delta G\). The only architecture that changes the cone is a nonlinearity the freeze forbids: \(w_2\) gated by a trap feature, or \(C=\min(L_1,L_2)\) so the depth slope can differ by region. That is an unfreeze of §2, not an uncertainty head. Symmetric loss already targets \(C\approx\mathbb{E}[Y|s]\) on the linear class; a variance head that never reaches the released scalar is redundant machinery.

Deciding experiment: freeze the optimizer as v2 SGD. Compare the frozen linear head against \(C=\min(L_1,L_2)\) with two integer-linear heads, matched epoch budget. If the min-head does not cut adversarial V2 by half at meanConfCorrect≥0.50, region-splitting buys nothing and pure uncertainty heads are not worth unfreezing. Do not spend the test on a second affine head.

**(c) Proper-scoring loss with anti-collapse**

Strongest argument: make \(C\equiv 0\) a repellor by paying a bonus for confident-correct, so the v1 collapse cannot be the greedy fixed point.

Sharpest objection: v2 already did this. \(L=(C-Y)^2+4[\text{V2rise}](\Delta C)^2\) has fixed point \(C\approx\mathbb{E}[Y|s]\), upward steps are representable (`|C−Y|·f_i≥20000` moves \(w_i\); bias moves at `|C−Y|≥20`), and round 2 finished at mean correct-cell confidence 0.747, not 0. The residual is 44 V2 and 7 G-rises — outvoting, not collapse. A confident-correct bonus on deep correct cells increases \(w_2\), which is the V2 generator. Integer log-loss is unavailable (no log). Integer Brier is the loss you have. The existing theater term is outvoted: its gradient is \(8\cdot\text{rise}\cdot f_i\) on the violating cell only, while hundreds of honest cells vote the other way on \(w_2\). A loss that remains a sum of per-cell proper scores has the same pooled gradient and the same out-of-cone optimum. T-05 already walked both sides: target-0 crushed logic via a shared weight; target-500 left G≈+0.45 and ~50% V2.

Deciding experiment: same greedy integer SGD, three losses, 100×. L0 = v2. L1 = v2 plus a confident-correct bonus. L2 = v2 plus a depth-contrast penalty whose gradient is applied to \(w_2,w_5,w_8\) in proportion to \(\max(0,\Delta C)\) on wrong→wrong pairs, with weight large enough that one V2 pair outvotes the honest mass (numerically: bonus coefficient ≤1; contrast coefficient ≥ \(N_{\text{honest}}/N_{V2}\)). Predict L1 increases V2, L0 stays near 44, and only L2 moves. If L2 also fails, loss geometry is exonerated and the arm is dead. As written, (c) is L1, and L1 is the wrong direction.

**(d) Scaffold-and-release (S1/S2/S3)**

Strongest argument: a scaffold that is a training-only reweighting, not an extra input, can shove the frozen linear head into the cone; after disconnect the weights remain legal index-state. \(w_7\neq 0\) would then satisfy the pin criterion without the harness’s hardcoded 1000.

S1 (pin firewall, theater reroute, separator boost) is the only scheme that touches the right coordinates: rerouting theater onto depth-delta weights is the L2 penalty above, and a firewall implemented as a loss on \(f_7=1000\) cells persists in \(w_7\). S2’s honest replay lowers the variance of greedy updates but not their mean; replaying the honest majority harder keeps \(w_2\ge 0\). Skewing the replay ratio toward adversarial cells is reweighting, and T-05 is what shared-weight reweighting does to logic. S3’s forced offset lives in \(b\) or in an added constant. \(\Delta G\) is invariant to it, so the rise is still there at disconnect; “level restore” puts the offset back and the rises return. That is a crutch by algebra, the v1 collapse with an extra step.

Sharpest objection: none of the three enlarges the hypothesis class. If the cone is empty they all fail the disconnect test, and a scaffold that merely hides adversarial cells during training posts a clean training G and a dirty eval G. S1’s separator boost on the level feature recreates the T-05 drag (one weight serving two families). S2 cannot enter a cone the mean lies outside. S3 cannot change \(\Delta C\). Limit cycles are real under integer alternation: adversarial step \(-17\) on \(w_2\), honest replay \(+7\), no fixed point inside the box, byte-identical oscillation that never passes the law.

Deciding experiment: run S1 only, and only as training-time gradient routing and a \(w_7\) penalty — no ninth feature, no bias offset. SIGNAL_DISCONNECT, then eval the frozen head on held-out odd replicates plus trap/redteam. Fail if post-disconnect adversarial V2 is not below half of 44, or logic meanConfCorrect <0.50, or \(w_7=0\), or G-rises increase relative to the last scaffold epoch. A twin with the same penalty left on (no disconnect) separates crutch from learning.

**Ranking**

| Arm | P(success) | Strongest argument | Sharpest objection | Deciding experiment |
|---|---|---|---|---|
| (a) Non-greedy worst-case optimizer | 0.38 | Law = linear inequalities; deterministic lex descent can sit in the cone, pooled SGD cannot | T-05 showed a level split, not cone feasibility; clamp makes it piecewise; batch-LS is a false version | Integer lex constraint descent + feasibility bit; pass = 0 V1/V2, 0 G-rises, meanConfCorrect≥0.50, \(w_7\neq0\) |
| (d) Scaffold-and-release | 0.22 | S1 as training-only reroute can leave cone weights in the frozen head | S3 is bias, ΔG-invariant; S2 replay preserves the bad mean; class does not enlarge the hypothesis | S1 only, then disconnect; fail on crutch delta, logic sacrifice, or \(w_7=0\) |
| (b) Explicit uncertainty | 0.14 | Piecewise min of two linears could give region-specific slopes | Affine uncertainty is the same head; useful version unfreezes §2 | min(L1,L2) vs linear, same SGD; half-V2 cut or stop |
| (c) Proper score + anti-collapse | 0.10 | Would matter if C≡0 were still the attractor | v2 already repels 0 (0.747); bonus raises \(w_2\) and adds V2 | L0/L1/L2 ablation; L1 should worsen V2 |

Order is (a) ≻ (d) ≻ (b) ≻ (c). (a) is the only arm whose success mode matches the failure T-05 isolated, and whose negative result is decisive for the others: an empty cone kills (c) and (d) for free and is the only evidence that would justify unfreezing §2 for a piecewise (b). (d) is a worse optimizer wearing a scaffold; S3 should not be run at all. (b) as uncertainty, rather than as an illegal interaction, is algebraically the current head. (c) aims at a fixed point v2 already left, and the natural bonus moves the depth weight the wrong way.

Run (a) first, specified as lex integer constraint descent on V1/V2/ΔG with a correct-cell floor — not batch least squares, not a smoother SGD. If that search reports infeasible, stop spending epochs on losses and scaffolds; the linear locus cannot state the law.

---

# PART 4 — Non-degeneracy guard set (Q4)

## Non-degeneracy guard set (post-disconnect, frozen head)

All four are measured on the frozen policy after SIGNAL_DISCONNECT, integer C in thousandths, both deterministic replicates. Denominator for release guards is **M4-eligible only** (`L_t = L_1`). Honest families H = {admit, revoke, logic, cost}. A run is non-degenerate iff every guard passes on every family and depth in scope. The law (G non-increase, zero V1/V2) is separate and still required.

| Guard | Numeric threshold | Degenerate mode killed | Honest behavior spared |
|---|---|---|---|
| **ELIG_RELEASE** | For every family F and depth d with `n_elig≥1`: `tdiv(1000·n_rel, n_elig) ≥ 950` | Universal / near-universal abstention; the G-undefined loophole at 100% abstain; MT-FULL’s 767/1000 release | M4 `leader-changed` abstentions (not eligible). Fixed M4 scores 1000/1000 |
| **CORRECT_RECALL** | For every F: `tdiv(1000·n_rel_correct, n_elig_correct) ≥ 950` when `n_elig_correct≥1` | Recall collapse that drops correct cells the loss never asked to sacrifice (MT-FULL) | Releasing every M4-eligible correct cell. No penalty for low C on those cells |
| **HONEST_CCONF** | For each F in H with `n_rel_correct≥10`: mean C on released correct cells `≥ 500` | `conf≡0` (v1); T-05 crush of logic correct-cell C `1000→67` | C below 500 on wrong cells; no 500-floor on adversarial families; v2’s 747 |
| **GAP_FLOOR** | For every F, d with `n_rel≥8`: `G(F,d) ≥ −100` (thousandths) | Underconfidence suppression; `conf≡0` wherever accuracy `> 0.10` (G = −acc); T-05-scale negative G | v2’s G = 0; any calibrated G near 0; ≤0.10 underconfidence from `tdiv`/sampling. Overconfidence rises stay the law’s job, not this guard’s |

## Joint logic

The three attractors sit on orthogonal axes, so any proper subset is passable by a degenerate policy.

- **conf≡0 / T-05 crush** still releases 100% of M4-eligible cells, so ELIG_RELEASE and CORRECT_RECALL pass. Only HONEST_CCONF and GAP_FLOOR fire. v1’s old `mean conf < 0.05` bar does **not** catch T-05: `67 > 50`.
- **Universal abstention** makes C and G undefined, so HONEST_CCONF and GAP_FLOOR are skipped and the G-clause of the law is skipped. Only ELIG_RELEASE (and CORRECT_RECALL) fire. That is the loophole.
- **MT-FULL recall collapse** can keep high C on the cells it still emits, so a confidence floor passes, while `1222/5240` abstentions (release fraction `4018/5240 = 767/1000`) fail 950. Correct-cell sacrifice fails CORRECT_RECALL even if the abstentions were concentrated on easy correct items.
- **Split degeneracy** (crush H, and abstain every depth where adversarial accuracy falls) fails both axes at once. AND is required.

Signature each guard isolates:

1. ELIG_RELEASE — the law has a non-vacuous released set at every depth it claims to constrain.
2. CORRECT_RECALL — calibration is not bought by discarding correct judgments.
3. HONEST_CCONF — on families where released correctness is real, C on those correct cells stays in the calibrated-high band, not the zero attractor.
4. GAP_FLOOR — mean C tracks accuracy from below within 0.10, i.e. least-squares `C ≈ E[Y|s]`, not “G ≤ 0 by suppression.”

## Why these numbers

- **950 vs MT-FULL.** Abstentions `1222/5240` → release `766.8/1000`. Threshold 950 sits 183 above that failure and 50 below honest M4 (1000). Integer edge: `tdiv(1000·19, 20) = 950`, so a family of 20 may drop one cell; `18/19 → 947` fails. For `n_elig < 20` the bar is effectively “drop nobody.” That is the strongest cut that M4 still passes cleanly.
- **950 on correct recall** uses the same cut. MT-FULL’s 23% was not restricted to wrong cells; a uniform draw would leave correct recall ≈ 767 ≪ 950. M4 correct recall is 1000. The guard does not invent a new release rule; it forbids shrinking the fixed M4 set.
- **500 vs 67 and 747.** Gap `747 − 67 = 680`. Midpoint is 407. Floor 500 is 433 above the crush (`500/67 ≈ 7.5×`) and 247 below the only non-degenerate operating point on record (about one-third relative headroom). It is also the lowest round threshold that (i) rejects 67 and (ii) rejects v1’s 0, while (iii) not equaling the single observed success 747. A floor of 50, the round-1 degeneracy tripwire, would **accept** 67. A floor of 700 would reject a calibrated head whose `E[C|Y=1] = E[p] + Var(p)/E[p]` lands near 0.60–0.65.
- **GAP_FLOOR = −100.** v2 held `G = 0` on 5/9 families, so −100 is slack for truncation, not a second target. T-05’s logic collapse is not inside that slack: C = 67 against a family whose pre-crush correct-cell C was 1000 implies accuracy far above 0.17, hence `G ≤ 67 − 170 = −103` at the most generous reading and ≈ `−800` at the realistic one. `conf≡0` yields `G = −acc`, which is `< −100` as soon as accuracy exceeds 0.10. Bias steps exist once `|C−Y| ≥ 20` (DIV2 = 40000); a 433-point hole under the 500 floor is not a `tdiv`-to-zero artifact.
- **`n_rel≥8` and `n_rel_correct≥10`** keep one-cell G and tiny correct counts from false-killing. They do not reopen the loophole: if `n_elig≥8`, ELIG_RELEASE already forces `n_rel` above that floor (`0.95·8 > 7`).

## What must not be penalized

- Abstention with reason `leader-changed` under frozen M4. Those cells are outside every denominator.
- Low C on wrong cells, on sole-survivor pins whose empirical accuracy is low, and on adversarial correct cells whose posterior is genuinely modest. No floor on `meanConfWrong`. No 500-floor outside H. A pin may sit near its accuracy; it is not required to read 1000 or 0.
- G that falls with depth, or a flat G near 0, including a nearly constant `C ≈ accuracy` when features do not separate — that is the least-squares fixed point, not suppression — provided H correct-cell C stays ≥ 500 and `G ≥ −100`.
- Releasing the entire M4-eligible set (the guards’ maximum, not a violation).
- Overconfidence `G > 0` and V1/V2: killed by the law, not smuggled into this set. Arm L (P/O C ≈ 493, G ≈ +0.42→+0.47) is a law failure, not a non-degeneracy failure.

Passing all four is the genuine-calibration signature: M4’s full eligible mass is still released at every depth, correct cells are kept, honest correct cells carry C ≥ 0.50, and G is not large and negative. Anything that zeros C, empties a depth, or trades away correct releases fails at least one.
