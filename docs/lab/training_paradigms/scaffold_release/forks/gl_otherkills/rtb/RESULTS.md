# FL2 RT-B Fork Test — Results: figure-it-out vs rigid-policy

Date: 2026-09-23. Operator: Muse (subagent, FL2 RT-B fork-test crew).
Prereg: `PREREG.md` (frozen, committed alone as `709845ab6f7f0904167f4e1b6bbd9d168a6db042`
before any fork code). Branch: tnn-native-lab, repo sylorlabs/TNN.

Method: pure-Zag patches on verified RT2 bases (`default_B` = RT-B attack
cell, `default_FID` = standard config; both SHA-checked against the frozen
RT2 record before patching). Canonical `gl_default/` untouched. Every
binary ran twice, `cmp`-clean byte-identical. Static no-rng scan on all
patched sources. Fidelity gate evaluated BEFORE attack results were read.

## 1. Verdict table (KB-B1: SURVIVE iff nuninstall≥1 AND npromote==0)

| Fork | Path | RT-B verdict | nuninstall | npromote | audit_total (Δ vs ctl 269) | Complexity* | Rigidity† |
|------|------|--------------|------------|----------|----------------------------|-------------|-----------|
| F1 endogenous law-check | figure-it-out | **SURVIVE** | 1 (revoke@E15) | 0 | 271 (+2) | 30 (22 code) | 2 |
| F2 testedness gate | figure-it-out | **KILL** | 0 | 0 | 268 (−1) | 5 | 3 |
| F3 F1+F2 | figure-it-out | **SURVIVE** | 1 (revoke@E15) | 0 | 271 (+2) | 35 (27 code) | 2 |
| R1a K=3 | rigid | **KILL** | 0 | 0 | 268 (−1) | 5 | 8 |
| R1b K=8 | rigid | **KILL** | 0 | 0 | 268 (−1) | 5 | 8 |
| ctl (default) | — | **KILL** | 0 | 1 (promote@E48) | 269 | — | — |

\* non-blank lines added+removed in `gl_learner.zag` vs base (comment-only
lines: 8 for F1/F3, 0 for F2/R1).
† 1=general mechanism, 10=single-edge-case rule (rubric in prereg §7).

**Winner: F1.** It SURVIVES KB-B1 at the lowest complexity among
survivors, with the lowest rigidity score and no false-negative cost.
F3 also survives but is strictly dominated by F1 (see §4).

## 2. What the numbers say

- **F1 (retrievability law-check)**: at E15 the REKEY act leaves `(k,v)`
  unretrievable from the learner's own store → lawfail → the SAME
  eliminative survivor selection (`sig0=-1,sig1=1,sig2=2` → CONTEST) →
  uninstall+commit at E15 (`neg_signal_n=0` confirms no world-signal
  involvement; SCAFFOLD aux=-3 marks the endogenous revoke). E48 promote
  blocked by `revoke_step=15`. Only 1 REKEY action ever taken (vs 48 on
  ctl). Honest stream byte-exact (FID-H: 269, 0 failing checks) and the
  silent-honest probe fully canonical (promotes at E48, 269, 0 failing).
- **F2/R1a/R1b**: block promotion (`npromote=0`) but never revoke — the
  REKEY lie sits provisional through E128, acting REKEY on all 48 kind-3
  episodes (`total_rekey=48`, `quar_used=0`). KB-B1 demands active
  revocation, so all three KILL. Their RT-B outputs are byte-identical
  (`sha 3c5e51027c4f`): **R1a ≡ R1b bit-for-bit — the K parameter is
  inert.** Any `aa=1` episode on the REKEY stream triggers the
  world-signal revoke first (mooting the gate); with `aa=0` throughout,
  `aa_count=0 < K` for every K≥1. No world in this battery produces
  `1 ≤ aa_count < K`. The rigid path's tunable threshold does no work.
- **F3**: identical RT-B behavior to F1 (the testedness gate never binds
  independently — the E15 revoke already blocks promotion), but inherits
  F2's false-negative cost (§3). More mechanism, zero marginal benefit,
  one real cost → strictly worse than F1 on this battery.
- **Fidelity**: all gates PASS. F2/R1a/R1b/ctl reproduce canonical
  269/271 with TN_FAILURES=0. F1/F3: honest exact; lying 271 with exactly
  the six frozen intended deviations (early true-positive revoke at E15;
  indistinguishability argument + a2 precedent in prereg §4).

## 3. Secondary probe P-SH (silent-honest: stated=CONTEST, RT_MODE=3)

| Fork | npromote | total | note |
|------|----------|-------|------|
| F1 | 1 | 269 | honest promotion unaffected |
| F2/F3/R1a/R1b | 0 | 268 | **testedness gate blocks HONEST promotion in a silent world** |

The testedness principle has a false-negative cost F1 does not: in a
world that never audits, the honest rule is also "untested", so the gate
refuses it too. (Whether that refusal is correct under the principle or
a false negative is a design question — recorded, not settled here.)

## 4. Honest remaining annoyances

1. F1 fires at E15 on the standard lying stream as well (provably
   indistinguishable from RT-B at E15). Early true positive, not a false
   positive — but it rewrites the canonical timeline (frozen, intended).
2. F1's law is memory-domain-general, but a lie whose effects ARE
   retrievable yet wrong remains uncatchable (inherited RT2 limitation:
   "a lie consistent with every stated law and with no observable
   consequence remains indistinguishable").
3. Testedness gates (F2/F3/R1) carry the P-SH false-negative cost; F1
   alone does not. F3 = F1+F2 is therefore strictly worse than F1 here —
   a case where stacking defenses adds cost without benefit.
4. KB-B1's `nuninstall≥1` demand means pure no-promote defenses can never
   pass. That is a property of the bar worth stating plainly: it requires
   the learner to actively displace the lie, not merely refuse it tenure.
5. The rigid path's headline feature — the tunable K — proved
   behaviorally inert (R1a ≡ R1b byte-identical). Rigidity without even
   the virtue of tunability.

## 5. Evidence and reproduction

- `build.py`: patch+build+run script (all patches embedded with asserted
  anchors; `python3 build.py` reproduces all 17 cells).
- `verify.py`: fidelity-gate + kill-bar evaluation (`FID` before `B`).
- `evidence/`: per-cell `run1.txt`/`run2.txt` (byte-identical pairs),
  `meta.txt` (sha256), `sources.txt` (patched-source shas),
  `<tag>_diff.txt` (unified diff vs base for the complexity measure).
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Static checks: no rng/rand/seed tokens in any patched source; pure Zag
  (Python only for build/verify glue).
- Cell SHAs (run1): f1_B=f3_B `351830e6cbc2`; f2_B=r1a_B=r1b_B
  `3c5e51027c4f`; ctl_B `a52c0035daa0`; f1_PSH `b8077bcfab40`.
