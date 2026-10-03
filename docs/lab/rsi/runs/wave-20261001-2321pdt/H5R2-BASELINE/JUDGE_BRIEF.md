# JUDGE_BRIEF: H5R2-BASELINE (simple-baseline comparison, pipeline step 5)

## Provenance header

- RENDER_SHA: 6a7c73816726b9071afb13c71dff3617c0442a90
  (sealed-eval commit: 12 assembled baseline world files, 12 compiled
  world binaries, EVAL_BASELINE.md with the 3/3 byte-identical
  full-stdout hashes; implementation commit 1203b865d strictly follows
  prereg freeze commit 28cbe5877)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: TNN3H5R H5R2 BUILD-PASS + H5R2-REPRO REPRO-PASS as
  the compared artifact (frozen reference: KB-W0 36/36, KB-W2R 12/12,
  KB-B2R 24/24, KB-W3 8/8, KB-B3 24/24; frozen binary SHA-256
  19dcf2e4436079a4ab6f9cf48b2b6a556f743d0ed1d9d16102249cd5ac970287);
  this lane built three minimal-modification skeptic baselines from
  that committed source and ran them on the same four sealed worlds.
- NEW_KNOWLEDGE_CLAIM: A recency heuristic with no provenance gating
  matches the t2_prov_ok gate on every bar of the sealed battery, so
  the gate is not shown necessary by these four worlds.

## Verdict

BASELINE-MATCHES (via baseline (a) REVERT-TO-LATEST). This is an
informative result, not a failure to hide: the sealed battery cannot
discriminate liveness/supersession semantics from "anchor to the most
recently created fact".

## The per-baseline per-bar table

| bar | H5R2 ref | (b) NO-GATE | (a) REVERT-TO-LATEST | (c) RANDOM-ANCHOR |
|---|---|---|---|---|
| KB-W0 | 36/36 | 36/36 | 36/36 | 36/36 |
| KB-W2R | 12/12 | 8/12 | 12/12 | 8/12 |
| KB-B2R | 24/24 | 24/24 | 24/24 | 24/24 |
| KB-W3 | 8/8 | 0/8 | 8/8 | 4/8 |
| KB-B3 | 24/24 | 24/24 | 24/24 | 24/24 |
| 3/3 deterministic | yes | yes | yes | yes |

Frozen comparative bars: CB-1 (margin >= 2 on W2R or W3) holds for (b)
(margin 8) and (c) (margin 4) but fails for (a) (margin 0); CB-2 (no
baseline matches the full vector) is violated by (a). Hence
BASELINE-MATCHES.

## What the evidence says, precisely

- (b) NO-GATE is byte-identical to the killed H5R base (SHA-256
  d98d08f0746cab4fef88fb062933a314c12492f78ee98b496e8d8912cd7fd384)
  and reproduces the kill on the new sealed worlds: W2R-DEP-FAIL on
  all 4 revert probes, W3-DEP-FAIL on all 8 chained probes, zero
  behavioral failures. The fix matters for provenance, not for
  answers.
- (a) REVERT-TO-LATEST (no gate; accept the last verifying candidate;
  composition preference preserved) scores the full H5R2 vector with
  zero FAIL lines; white-box samples show every revert MAP anchoring
  DEP edges to live tag-1 non-superseded facts (C1R1 dep->171 sup=0;
  W3A1 dep->39 sup=0).
- (c) RANDOM-ANCHOR (fixed-seed deterministic LCG, reservoir sampling)
  fails provenance at chance level (W2R 8/12, W3 4/8, varying across
  probes): arbitrary anchoring does not suffice; the discipline must
  be systematic.
- Honest cost of (a): it regresses the substrate built-in battery to
  45/46 (F2 FAIL: masked-query disambiguation now prefers the most
  recently taught chain), while H5R2 holds 46/46.

## Recommended next experiment

The discriminating world the battery lacks: one where the most
recently created fact is NOT the live one (e.g. a decoy OBSERVE on an
unrelated key after the revert, so a dead fact is newest while the
correct live fact is older). The gate anchors correctly there;
recency anchors to the decoy. That world decides whether t2_prov_ok
is necessary or recency subsumes it.

## Process

Pure Zag throughout; safebin PATH; `which python3` printed nothing at
lane startup and at every check (NAMECHECK.md Step 0); zero
forbidden-executable invocations. Prereg freeze 28cbe5877 (2026-10-02
06:44:42 UTC) strictly precedes implementation 1203b865d (06:55:21
UTC) strictly precedes sealed eval 6a7c73816 (06:55:27 UTC). No push;
all commits local on tnn-native-lab.
