# JUDGE_BRIEF: H5R2-SKEPTIC2 (the stronger skeptic the decoy lane recommended)

## Provenance header

- RENDER_SHA: bbbc333d6 (sealed-eval commit: 10 assembled chained
  decoy world files, 10 compiled world binaries, EVAL_SKEPTIC2.md with
  the 3/3 byte-identical full-stdout hashes; this judge brief finalized
  in the immediate follow-up commit; implementation commit f461e812d
  strictly follows prereg freeze commit 709e1e82e)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: H5R2 BUILD-PASS + REPRO-PASS, H5R2-BASELINE
  BASELINE-MATCHES, H5R2-DECOY DECOY-DISCRIMINATES as the motivating
  results (the gate beat recency, no-gate, and chance on worlds where
  the newest fact is not the live one). This lane built the stronger
  skeptic the decoy lane recommended (NEWEST-LIVE-ON-KEY) and scaled
  the decoy family to chained decoys at both chain levels.
- NEW_KNOWLEDGE_CLAIM: The stronger skeptic NEWEST-LIVE-ON-KEY matches
  H5R2 8/8 with byte-identical stdout on chained decoy worlds, so the
  t2_prov_ok gate's necessity is still unproven against the
  per-key newest-live heuristic even though the gate beats recency,
  no-gate, and chance at every chain level.

## Verdict

SKEPTIC-SURVIVES. All five frozen kill bars hold, with SB-2 landing
on the pre-registered MATCH outcome: H5R2 8/8 "CD ok";
NEWEST-LIVE-ON-KEY 8/8 "CD ok" (byte-identical full stdout to H5R2 on
both worlds); REVERT-TO-LATEST 0/8 with CD-DECOY-FAIL on 8/8
(decoy-anchored at both chain levels, the pre-registered failure
signature); NO-GATE 0/8 via CD-DEP-FAIL to the superseded original
fact; RANDOM-ANCHOR 0/8 (chance level); 3/3 byte-identical runs on all
10 worlds; both decoy facts answer correctly on all arms at both
levels (no adversarial-by-brokenness).

## What this means

The decoy lane showed the gate is necessary against the recency
heuristic. This lane shows the gate is NOT yet shown necessary against
a strictly stronger skeptic: anchoring each chain link to the newest
live fact on its (subject, relation) key reproduces the gate's
behavior exactly on all 16 probes run across both lanes (8 simple
decoy + 8 chained decoy). The honest reading: t2_prov_ok's
first-all-live-candidate rule and per-key newest-live selection
coincide whenever each chain key holds at most one live fact, which
the frozen event semantics currently guarantee (contradiction always
supersedes). The next discriminating family must break that
coincidence: a world where the node-id-first all-live candidate
licenses a live-but-not-newest fact on some key while the key-newest
fact licenses a later candidate.

## Evidence

- EVAL_SKEPTIC2.md (per-arm per-bar numbers, hashes, white-box traces)
- sealed/ (10 world .zag + 10 .bin)
- bl_newest.zag (e5df3ddb28858b60efb01f3d8df524a98ce79686e199532e53713c24f367b649),
  CHAIN_FRAG.zag (6d3c767600bf06340d7d6eafd6a8b4317114df0feab4a70fed810f832552abd1)
- PREREG_SKEPTIC2.md (frozen bars SB-1..SB-5, decision rule, seeds)
