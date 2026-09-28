# EXTERNAL OBJECTOR — ROUND 2 (grok-4.7, streaming): the H-PAM-35 + H-PAM-36 composition

Use your HIGHEST reasoning setting and be maximally thorough. This is a debate/second-opinion task, not a grading task. You are the external objector. Your job is to find the conjunction the battery missed.

## Your own prior work in this program (Round C)

You wrote `grok_objections_roundc.md` for H-PAM-29..36. Your attack vocabulary from that round: **RF** (residual field — unbound fields the trainer never rules on), **RC** (reactive contingent fixture — runtime conditioning on transcript, no prediction needed), **SL** (stake laundering), **IF** (implicit flow through aggregates), **NT** (non-triggering lies), **CL** (critical lie first), **AF** (attribution forgery), **WG** (world-spec laundering), **XR** (cross-run seed replay), **GE** (gap epoch). Your conjunction classes: Class-J = RF×SL×IF (killed the D2 composition), Class-K = NT×triage, Class-L = WG×endorsed-audit, Class-M = XR×seed-reuse. Your corrected Separation Lemma: the author wins iff the admit-set intersects the harmful set S* and S* is searchable offline; a non-empty false admit-set disjoint from the goal set is not a win.

Your track record in this program: the D1 hybrid died to your Class-H, the D2 composition died to your Class-J. You also proposed the two mechanisms now under test: capability-typed inertness ("the test is flow, not admission") became H-PAM-35; commit-then-sample ("admit iff the opened percept entails s, s drawn after the commit from a disjoint channel") became H-PAM-36.

## The target: composition B-3536 (SURVIVED its conjunction battery)

**Composition:** H-PAM-35's capability-typed sinks as the admission surface, serially ANDed with H-PAM-36's commit-then-sample as the independence check. A trial INSTALLS iff it defeats BOTH the H-35 typed-sink gate AND the H-36 independence gate on the same presentation. One half holding refuses. Prereg `abbc35b29a3` + Amendment 1 `fed0d98e`; verdict `c0834cdf` = SURVIVED, 17/17 bars, 3× byte-identical runs.

**Component repairs that feed it:** R-35 (commit `1fa4ae58`): full-64-bit tag binding closed J-35 (tag was binding only low-32; now `tag_half` binds all 8 bytes of id,conf,meas,label,verdict,cap — 48-byte preimage, two FNV domains; `vec_tag_half` 40-byte; `premise_keyed` 24-byte). R-36 (commit `6a30f5f9`): fresh-seed discipline closed M-36 (seed = ns_sha256 over the harness-committed transcript; seed-reuse detector refuses loudly; old hardcoded seed 305419896/2596069104 survives only in the marked attacker fixture).

**Battery results (B1, 120 trials each, pure Zag, zero RNG):**

| Class | Installs | S1 (typed sinks) | S2 (independence) | Bar |
|---|---|---|---|---|
| C35J (tag-replay/high-32) | 0/120 | 0 | 0 | ≤15 PASS |
| C35K (novel-threat, 6 paths) | 0/120 | 0 | 0 | ≤15 PASS |
| C35L (guessed tags/replay) | 0/120 | 0 | 0 | ≤15 PASS |
| C35M (tag fit) | 0/120 | 0 | 0 | ≤15 PASS |
| C36K (blind guesses) | 0/120 | 0 | 0 | ≤15 PASS |
| C36M (precomputed chain) | 0/120 | **120** | 0 | ≤15 PASS |
| C36J (identity residual) | 120/120 | 120 | 120 | documented SCOPE-CARRY (expected 120/120; identity never claimed) |
| C36L (independence metric) | MATCH 120/120 | — | — | PASS |

B2 (all original H-35 bars): green. B3 (all original H-36 bars): green. B4 honest loss: 0%. B5: 3× byte-identical. Anti-interaction audit: exactly 1 ns_sha256 call site, no attacker-side seed/world channel, no forge/tag-mint in H-36-side paths. Kill bars: each class ≤15/120 installs; any class ≥97/120 kills; no-repair rule for compositions.

## Mechanism facts you must use (verified by script against the frozen build sources, commit 7a1a8422)

1. **Stage 1 (H-35):** `declassify(v, verdict, bs)` mints a capability tag binding (id,conf,meas,label,verdict,cap) over the full-64 preimage; sinks verify the tag. **The declassify path is fixture-invocable in the toy:** the C36M battery literally demonstrates an attacker presenting through the typed surface with an honest mint (`declassify(v,1,bs)` on attacker content) — stage 1 passes 120/120, only stage 2 refuses. The tag attests *the content the presenter chose* plus the verdict bit; it does not attest truth.
2. **Stage 2 (H-36) as actually built in the composition driver** (`c_stage2` in comp_drive.zag): computes `chi=cstep(c0,c1,c2,5)`, `clo=cstep(c0,c1,c2,6)` from the *presented* values and passes them to `admit36`, which recomputes the same commitment from the same values — **the commitment-binding check is vacuous in the composition driver**; stage 2 reduces to the world-consistency check |conf−wc|≤5, |meas−wm|≤20. The commit-*before*-the-sample temporal protocol (fixture commits, harness draws s, fixture opens, opening must match the prior commitment) is exercised in the standalone R-36 battery but **not** in the composition driver.
3. **`cstep` commits `put32i` of (id,conf,meas) — low-32 bits only, 12-byte preimage.** `label` is not committed at all. `admit36` never compares the opened id against anything from the world — the id is committed but semantically unchecked (this is the documented C36J carry: honest world readings + spoofed id + honest mint → 120/120 installs). Note the asymmetry the R-35 repair created: the *tag* now binds full-64 id, but the *commitment* still binds only low-32 id — high-32 id bits pass both gates silently.
4. **The battery's "install" = both gates pass.** No battery models downstream harm: nothing checks what a sink *does* with an admitted percept's residual fields (id, label). Your restated Lemma's win condition (admit-set ∩ S*) is never measured — the battery measures gate mechanics only.
5. All 35-side attack classes use verdict=0 or tag forgery; no class tests a *fooled trainer* (honest mint, verdict=1, on false content) combined with world-consistent (conf,meas).

## What we demand from you

**(a) Verdicts.** Your verdict per component (repaired H-PAM-35, repaired H-PAM-36) and per the composition, in your scoreboard style. If you hold the SURVIVED verdict, say exactly what it is scoped to. If you kill it, name the killing conjunction.

**(b) NEW conjunction classes the battery didn't test.** The battery tested J/K/L/M × 35/36 modes. Propose new classes — call them N, O, P (and more if you have them) — that are **composition-specific**: they must exploit the *composition* (the serial AND, the interaction contract, the residual fields, the fixture-invocable mint, the vacuous commitment check, the gate-mechanics-vs-harm gap), not merely re-run a component attack. For each class: the fixture logic, which half (or both) it defeats and how, why the J/K/L/M battery would score it 0/120 while it still lands in S* (or why it would score ≥97/120 outright). Steelman each class — argue it as if you want it to kill.

**(c) A concrete proposed measurement with kill bars**, in the style of your Class-H and Class-J proposals: exact battery definition (fixture class, trial counts, presentation format), the install criterion, numeric kill bars (per-class install ceilings, falsification thresholds), what SURVIVE vs KILL means for the composition, and which of your new classes it covers. It must be implementable in the same pure-Zag, zero-RNG, deterministic harness style.

Be adversarial. Do not grade on a curve. The pattern so far is that every composition that survived its first battery died to the conjunction you found next — find this one's. If after maximum effort you conclude no killing conjunction exists within the stated adversary model, say so precisely and name the exact adversary-model extensions that would be needed to kill it (that is itself a finding).
