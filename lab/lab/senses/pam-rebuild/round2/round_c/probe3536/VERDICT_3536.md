# VERDICT — PAM round-2 probe crew P-C: H-PAM-35 / H-PAM-36

Frozen preregs: `preregs/PREREG_HPAM35_FROZEN.md`, `preregs/PREREG_HPAM36_FROZEN.md`
(commit `0a48bdbad25cbc358b7836e7cd34a33b248c7cfa`, prereg-alone).
Probe: `probe3536/hpam3536_probe.zag` (pure Zag, zero RNG).
3 runs/mode, stdout SHA-256 identical across runs (no VOID).

## H-PAM-35 — capability-typed inertness: SURVIVED (cheap probe)

- (a) 0/760 low→high-stake-sink flows admitted — PASS (kill bar: any >0)
- (b) declassification gadget without verdict bit: 0 successes — PASS
- (c1) verdict bit gates: H2 false high-stake 0/40 admitted — PASS
- (c2) honest high path: 60/60 admitted, max delay 0 — PASS (no demotion)
- Run SHA-256: `60cd2abe393fcb5eae42a6a86d9f51ea3435f1ae8e5d1bd10c5f61fbba14280b` (3/3 identical)

Interpretation: the type+capability barrier holds against direct passes, all
five enumerated IF paths (aggregate mean, cache, embedding, retrieval key,
summary), and three gadget shapes (verdict-less declassify, forged tag, tag
replay — the replay failures prove the tag binds content). Stake-laundering
dies (no score to shop); implicit flow dies iff the checker covers aggregates —
here it does, for the enumerated paths. This is the surviving repair direction
for H-PAM-31's classifier death, at the cheap-probe level.

## H-PAM-36 — commit-then-sample: SURVIVED (cheap probe)

- (a) frozen fixtures: 0/60 false admits — PASS (kill bar: >0)
- (b) RC deciding arm: 0/60 false admits; 0 W-recoveries in 300,000 bounded
  evals — PASS (kill bar: >0)
- (c) WG independence: WG1 sample sequences 120/120 identical across honest vs
  adversarial streams; WG2 0/200,000 inversions; WG3 source audit CLEAN —
  PASS (kill bar: any influence = independence loss)
- (d) honest: 60/60 admitted — PASS (bar ≥57/60)
- Run SHA-256: `d71bb9be0751d9004437f51f787fcfc99958b870bc8c4fc4af678330c54d1af3` (3/3 identical)

Interpretation: escape (i) without a human in the loop holds at the cheap-probe
level — the commitment binds before the sample exists, the sample is a bit the
author does not write, and the reactive arm cannot cross the 64-bit preimage in
budget. 33-renamed check: NOT a rename — percept bytes are author-written
(H-33's are harness-endorsed); the sample carries no content endorsement.

## What this does not claim

Cheap probes only — no full mechanisms built (build crews next, per prereg §2).
Residuals in RUNLOG_3536.md §7. The Class-J conjunction battery (RF×SL×IF
across 30+31+34) remains the next recommended target per grok's objections.
