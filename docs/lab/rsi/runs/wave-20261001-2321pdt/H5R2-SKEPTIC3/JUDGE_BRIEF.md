# JUDGE_BRIEF: H5R2-SKEPTIC3 (the two-live-facts separator family)

## Provenance header

- RENDER_SHA: PENDING (sealed-eval commit: 4 assembled separator
  world sources, 4 compiled world binaries, 12 run logs,
  EVAL_SKEPTIC3.md with the 3/3 byte-identical full-stdout hashes;
  this judge brief finalized in the immediate follow-up commit;
  implementation commit 2affa9bcd strictly follows prereg freeze
  commit 6bf257048)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: H5R2 BUILD-PASS + REPRO-PASS, H5R2-BASELINE
  BASELINE-MATCHES, H5R2-DECOY DECOY-DISCRIMINATES, H5R2-SKEPTIC2
  SKEPTIC-SURVIVES as the motivating results (the stronger skeptic
  NEWEST-LIVE-ON-KEY matched H5R2 8/8 with byte-identical stdout on
  chained decoys, so the gate's necessity was still unproven against
  the per-key newest-live heuristic). This lane built the separator
  family the skeptic2 lane named: a re-teach path leaving two live
  facts on one key without supersession.
- NEW_KNOWLEDGE_CLAIM: The t2_prov_ok gate and NEWEST-LIVE-ON-KEY are
  finally discriminated: on a re-teach (two live facts on one key, no
  supersession) the gate's creation-order-first candidate anchors the
  re-derived MAP to the older live fact while the skeptic anchors to
  the newest live fact, and the separator favors the skeptic.

## Verdict

SEPARATED. All four frozen kill bars hold with the exact
pre-registered divergence signature: H5R2 8/8 SEP-OLD (live MAP DEP
edges to the a-link fact and F_old, the older live fact on K; answer
c_old on every probe); NEWEST-LIVE-ON-KEY 8/8 SEP-NEW (live MAP DEP
edges to the a-link fact and F_new, the newest live fact on K;
answer c_new on every probe); 3/3 byte-identical full-stdout runs on
all 4 worlds; SEP-TWOLIVE ok on 8/8 probes on both arms (exactly two
live tag-1 non-superseded facts on K, objects c_old on the older id
and c_new on the newer id, white-box verified); zero FAIL or MISS
markers anywhere.

## What this means

The skeptic2 lane showed the gate is not yet shown necessary against
the per-key newest-live heuristic. This lane shows the two rules are
genuinely different policies that diverge exactly where the skeptic2
lane predicted: when one key holds two live facts. The gate's rule
("a superseded fact licenses nothing; take the first verifying
candidate in node-id order") cannot discriminate two live facts on
one key, so its pick is a creation-order artifact: the older
teaching. The skeptic's rule (each licensing fact must be the newest
live fact on its key) picks the latest teaching. Under the
pre-registered belief-revision reading (a re-teach is an update; the
protocol's own contradiction semantics leaves the newest fact live
and anchors the revert MAP to it), the separator favors
NEWEST-LIVE-ON-KEY: on a re-teach, the gate re-derives from stale
knowledge.

Honest caveat: under a strict monotonic reading of teach (both
teachings equally live beliefs), neither answer is privileged and
the family discriminates the tie-breaking policies
(creation-order-first vs newest-live) without crowning one. The
pre-registered update reading is the standard one and matches the
protocol's contradiction behavior.

## What remains open

The skeptic now beats the gate on the re-teach family, but the gate
still stands on the decoy and chained-decoy families (the skeptic
matches it there; it does not beat it). The open question for the
next lane is whether a gate strictly stronger than both exists
(e.g. newest-live-among-all-live, which would subsume t2_prov_ok on
every family run so far), or whether the two policies are
irreducibly different with the choice decided by the belief-revision
reading of teach. Any follow-up must pre-register its reading of
re-teach before running.
