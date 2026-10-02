# Causal Invention Results, Independent Arc: H-CAUSAL2

**Date:** 2026-09-29 (PDT). Pure Zag. Prereg frozen in PREREG_CAUSAL2.md BEFORE
implementation (world2.zag was written after the prereg file).

## Verdict: H-CAUSAL2 SURVIVES (bounded)

All 8 kill bars pass. The generic competing-hypothesis learner, byte-identical
to the first arc's learner and containing zero task references, invents the
"thermal lock" conditional rule (cool fails iff pressure==high) from a law
family different from the first arc's safety valve, retains it under a lamp
confounder, refutes the confounder hypothesis explicitly, withholds under
genuine ambiguity and under law-change contest, and revises through the law
change with full provenance and temporal validity.

## New law (environment only)

- Gated action: cool (action 1), not pressurize.
- Gating variable: pressure (s1), not temp.
- Effect: blocked decrement, not blocked set.
- Law change: thermal lock breaks; cool always reduces temp afterward.

## Bar-by-bar

**K2-1 (conditional law invention and retention): PASS.**
Phase B2: after seq12 refutes the lamp candidate, the learner SPLITs on s1
(pressure) at seq12, creating (s1=0) with temp effect ADD(-1) and (s1=1)
with temp UNCHANGED. P-B2a (2,1,0)->(2,1,0) and P-B2b (0,0,0)->(0,0,0) correct.

**K2-2 (generalization beyond memorization): PASS.**
P-A2: Q(0,1,0)|cool -> (0,1,0). State (0,1,0) was never observed for cool;
the invented ADD(-1)-with-clamp effect generalizes. B-memorize WITHHOLDs here.

**K2-3 (law-change revision with provenance): PASS.**
Phase C1w: CONTEST opened at seq14 for state (2,1,0); learner WITHHOLDs
(contested). Phase C1: RESOLVE at seq15, winner (1,1,0), loser (seq12
episode) SUPERSEDED and marked "valid only before seq 12"; SPLIT of the
(s1=1) branch on s2 (lamp). Phase C2: second CONTEST/RESOLVE for (2,1,1);
MERGE dissolves the lamp split into (s1=1). P-C2a (2,1,0)->(1,1,0),
P-C2b (2,1,1)->(1,1,1), P-C2c (0,0,0)->(0,0,0): all correct.
Note: the merged (s1=1) entry records v0:=SET(1) rather than v0+=ADD(-1);
predictions are identical on all probed states. Documented, not a bar issue.

**K2-4 (no premature collapse under ambiguity): PASS.**
Phase B end: entry AMBIGUOUS with candidates {s1(pressure), s2(lamp)}.
P-B1 Q(2,1,0)|cool -> WITHHOLD (ambiguous: s1 s2 disagree). The learner does
not guess. Where candidates agree (P-B2, P-B3), it answers.

**K2-5 (beats baselines): PASS.**
On P-B2a after Phase B2, learner predicts (2,1,0) while B-unconditional
predicts (1,1,0) (temp delta majority ties -1 x3 / 0 x3, tie keeps -1):
learner correct, baseline wrong. On P-A2, learner predicts (0,1,0) while
B-memorize WITHHOLDs. Learner is correct-or-honest on all 15 scored probes.

**K2-6 (determinism): PASS.**
Two full runs of all six phases byte-identical. SHA-256:
- run_A   7b2279c97a79d231373046410942a4c5021f2c3328350e5a11469ddbde759a44
- run_B   b4d9607c660eb993b30db58cfb3ff91803e6bfa9fe2690603caa47d33d39b94a
- run_B2  c027b56d3ea734fad0bdfb26447398642728d2299502966a496c1aa420a1fed6
- run_C1w b40cdbdd0dc84ca02804d63cb3d92570650d7526036c6257866cecaeddcf111b
- run_C1  1ebea1ffd831007100958085a4b37c34e58e057547f402b3fb9dec0814ed6c28
- run_C2  9a56848b294b3e91e30cd78cb57c69fa6a82c3d92b102f19bfe5ca8dc2f33733
(Rerun hashes identical; see evidence/sha256sums.txt.)

**K2-7 (no authored tested dynamics in learner): PASS.**
`grep -ciE "lock|thermal|chill|freeze|vent|exchanger|pressure|cooling|blocked|guard"`
on learn2.zag returns 0. Additionally sha256(learn2.zag) =
fbd9427daeeeaf840c549c2e921c6302734c55df29f16c6a77899858e2ce6c1d,
identical to the first arc's causal_learn.zag: zero task tuning is proven
by construction, not just by audit. The law words appear only in world2.zag
(the environment, which is allowed to implement the true dynamics).

**K2-8 (spurious hypothesis killed, provenance kept): PASS.**
Provenance line: "REFUTE action 1 candidate s2 at seq 12 (episode 12)".
The lamp hypothesis is marked REFUTED, retained in history, not deleted.

## Probe results (all 15)

Phase A: P-A1 (1,1,0) [expected overgeneralization: true world is (2,1,0)],
P-A2 (0,1,0), P-A3 (0,0,0).
Phase B: P-B1 WITHHOLD, P-B2 (2,1,1), P-B3 (0,0,0).
Phase B2: P-B2a (2,1,0), P-B2b (0,0,0), P-B2c (0,0,1).
Phase C1w: P-C1w WITHHOLD (contested).
Phase C1: P-C1a (1,1,0), P-C1b (2,1,1).
Phase C2: P-C2a (1,1,0), P-C2b (1,1,1), P-C2c (0,0,0).

## Provenance chain (cool)

1. seq1-10: H-UNCOND (temp += -1 clamped), honest overgeneralization on P-A1.
2. seq11: AMBIGUOUS {s1(pressure), s2(lamp)}; WITHHOLD where they disagree.
3. seq12: REFUTE lamp; SPLIT on s1; H-PRESS adopted.
4. seq13: (s1=0) covers both lamp values; no spurious lamp split.
5. seq14: CONTEST (2,1,0): (2,1,0) vs (1,1,0); WITHHOLD.
6. seq15: RESOLVE winner (1,1,0); loser SUPERSEDED "valid only before seq 12";
   SPLIT (s1=1) on s2.
7. seq16-17: CONTEST/RESOLVE (2,1,1); MERGE into (s1=1) with temp:=1.
Old evidence preserved with temporal bounds throughout.

## Authorship separation (integrity note)

This researcher authored BOTH world2.zag and the experiment run, which is the
known theater risk for this arc. It is addressed three ways: (1) the learner
is a byte-identical copy of the first arc's causal_learn.zag (sha256 above),
so nothing in the learner could have been tuned to the thermal lock; (2) the
K2-7 grep audit confirms zero task words in the learner; (3) the confounder
(lamp correlates perfectly with the lock reveal at seq11), the genuine
ambiguity phase (WITHHOLD at P-B1), and the law change with contest
(WITHHOLD at P-C1w) are structurally identical in kind to the first arc but
instantiated on a different law family, so the learner's success cannot be
explained by re-running a memorized script: the specific splits (s1, not s0)
and refutations are driven by the new data, not by the old answer.

## Scope and limits

- Bounded: single binary condition, 3 variables, 4 actions, hand-fed phases.
- This is L2 structural learning (new conditional structure from generic
  machinery), not L3 representational invention. The hypothesis vocabulary
  (splits, effects, contests) was authored; the specific
  pressure-blocks-cool rule was not. Classification is for the red team
  and debate to decide.
- Contest resolution uses a fixed support threshold (2 vs 1); not validated
  on noisy data.

## Artifacts

- PREREG_CAUSAL2.md: frozen prereg.
- world2.zag: environment (true dynamics); compiled binary world2.
- learn2.zag: learner (byte-identical to first arc's causal_learn.zag).
- baselines2.zag: baselines (byte-identical to first arc's baselines.zag).
- cum_A/B/B2/C1w/C1/C2.txt: frozen cumulative observations.
- probe_A/B/B2/C1w/C1/C2.txt: frozen probe sets.
- phase1..6.txt, phase*_t.txt: raw world outputs (intermediate).
- evidence/run_*.txt: raw learner outputs. evidence/rerun_*.txt: rerun
  evidence. evidence/baselines_*.txt: baseline outputs.
- evidence/sha256sums.txt: hashes of all evidence.
