# SEALED_EVAL.md - H5R3: revision chain through full revert cycles

Lane: HPI, wave-20261002-1121pdt. Branch: lane-hpi-20261002-1121pdt.
Frozen prereg: docs/lab/rsi/runs/wave-20261002-0521pdt/HPI/PREREG_H5R3.md
(prereg commits bfb01b47e, b675b1d5a; implementation commits strictly after:
5d7e6691d and follow-ons. PREREG-ORDER-OK, verified before any verdict.)

Hypothesis (prereg section 1): the H5R2 provenance gate sustains the
revision chain through FULL revert cycles: after a revert promotes a fresh
MAP anchored to the live reverted fact, a subsequent contradiction of that
reverted fact still supersedes the revert MAP via its DEP edges, and the
next MAP-key query re-derives through the trial loop and promotes a fresh
MAP anchored to the new live fact.

## Substrate compliance (KB-S1): PASS

- Extracted source: tnn3_h5r3_substrate.zag, SHA-256
  04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a (match).
- Diff vs verified H5R base (tnn3_h5r.zag at 830f95ab7): exactly the
  t2_prov_ok definition plus the gate at all four t2_trial promote sites
  (5 occurrences: 1 definition + 4 call sites). Activate tag-20 admission
  hunk present; promote_graph carries zero ev_teach_in calls.
- Zero added / zero removed cognition lines vs the frozen H5R2 source
  (byte-identical extraction).
- Rebuild with the pinned znc: 3/3 byte-identical, SHA-256
  19dcf2e4436079a4ab6f9cf48b2b6a556f743d0ed1d9d16102249cd5ac970287,
  equal to the committed frozen binary at 9db334bd4a.
- PREREG DEFECT (recorded, not a bar move): the prereg prints the binary
  reference as a 61-char malformed string; the operative KB-S1 gate
  (source hash + hunks + zero cognition delta) is intact and the rebuild
  reproduces the true frozen binary byte-for-byte.

## Battery record (frozen numbers)

Driver: CY_FRAG.zag, SHA-256
5a41b73028e3dfc5f11812baea4904433d66cc71eefde47d87f22b7fe24587ee
(recorded before any run). Smoke frag (9xxx keys only): 13dc04f27dca720d4757bf6ebd562b3793a7f158ec0d80fdfd81f58c474d1ad2.
Smoke: 1 cycle probe on unsealed keys, PASS, 3/3 byte-identical.

World files (assembled per prereg 4.7; substrate portion differs by exactly
one line, the main alias; hashes recorded before any run):
- world_y1.zag: de6e6279394945de66018650cbdfef75b1c4cc1e496a0967fea0467685b94f57
- world_y2.zag: 72ce78af5d3a8ceb0cbc66b1ba6653bd9698fcc9e2711a2f848a46ce35eddbd3

Runs: y1 3/3 stdout SHA-256 d7db929fdcca700b60f458a05db5450c5cf3d1e06421e5e7d3618526b3537df8;
y2 3/3 stdout SHA-256 74df43ce14d480a6300f2a75eb6521efd9672eff8a386d91cf5a7d64829cedb7.
Zero stderr bytes on all runs.

## Kill-bar scorecard

- KB-W0 (white-box, PRIMARY): 32/32 MAP-key probe snapshots show t1live=0
  and every returned value equals the f28 of the single live tag-20 MAP.
  PASS.
- KB-CY: 6/6 cycle probes show exactly 3 superseded tag-20 MAPs carrying
  CON self-edges, exactly 1 live MAP with f28=c2, and every DEP edge of
  the live MAP targets a live tag-1 non-superseded fact. PASS.
- KB-RR: 2/2 revert-after-revert probes show exactly 3 superseded MAPs
  with CON, exactly 1 live MAP with f28=c1, every DEP edge to a live
  tag-1 non-superseded fact; in particular the live MAP anchors to the
  re-reverted fact F5, not the dead lowest-node-id F1. PASS.
- KB-BCY: 18/18 behavioral (post-contradiction c1, post-revert c0,
  post-re-revision c2), each via a fresh MAP with strictly increasing
  node ids on the key. PASS.
- KB-BRR: 6/6 behavioral (c1, c0, c1), each via a fresh MAP. PASS.
- KB-G3 (architecture accounting): substrate byte-identical to the frozen
  H5R2 record (0 added, 0 removed cognition lines); no new modes,
  bridges, routers, handlers; no core-ISA additions; none of the
  forbidden protected semantic operations; no time, clock, or random
  reads in any new code (grep-verified); the driver is evaluation
  scaffolding only. PASS.
- KB-D3 (determinism): 3/3 byte-identical full-stdout runs per sealed
  world. PASS.
- KB-P3 (process): zero forbidden-executable invocations; safebin PATH;
  `which python3` empty at lane startup (NAMECHECK.md Step 0). PASS.

Supplementary (logged): SELC con=3 on all 8 probes (exactly the three
superseded MAPs per probe carry CON; zero stray CON edges).

## Negative controls

- NC-0R3: absent (KB-S1 passed). NC-1R3: absent (24 MAP-CON transitions
  fired across the battery: 6x3 + 2x3). NC-2R3: absent (KB-W0 passed).
- NC-3R3: absent (every post-contradiction probe returned the exact new
  value via a fresh MAP; FRESH ok=1 on all 32 probes). NC-4R3: absent
  (no revert MAP survived the contradiction of its live licensing fact;
  the revert MAP carries CON in every final dump). NC-5R3: absent (zero
  cognition-line delta). NC-6R3: absent (KB-D3). NC-7R3: absent (KB-P3).
- NC-8R3: the two worlds use fresh seeds, fresh 95xxx-98xxx ranges, and a
  cycle family (contradict, revert, contradict-the-reverted,
  revert-after-revert) never tested in FW1-FW9, the 1421pdt battery, the
  killed H5/H5R batteries, or the H5R2 battery. Not trivial variants.

## Post-freeze adversarial red team (REDTEAM_SELF.md; informative, not bars)

Three post-freeze probes on fresh 99xxx keys (ADV_FRAG.zag, SHA-256
191e5a772eec70ae43b3630de97e6627d65208fb8390ef87d0b75dc1dea26fc8):
- ADV-A (snapshot attack): novel never-taught value 99399 derived via a
  FRESH MAP (id 151, strictly increasing) after the full cycle; then a
  historical non-predecessor value 99306 re-derived via fresh MAP id 208.
  Final: 5 superseded MAPs with CON, 1 live, DEP to live facts. SURVIVES.
- ADV-B (back-to-back contradictions, unqueried intermediate): c2 derived
  via fresh MAP; exactly 1 superseded MAP; intermediate dead fact licensed
  nothing and caused no confusion. SURVIVES.
- ADV-C (chain-fact contradiction): all 4 MAPs superseded via their chain
  DEP link; the next MAP anchored to the NEW chain fact (NEWCHAIN ok=1)
  after the gate declined the verifying dead-chain candidate. The chain is
  live in both DEP links, not a stored snapshot. SURVIVES.
All three 3/3 byte-identical. The prereg section 9 self-attacks are
answered in REDTEAM_SELF.md.

## VERDICT: H5R3 ADVANCES

All frozen bars in prereg section 5 pass, no killing negative control
fires, no void condition fires. The DEP based revision chain holds
through full revert cycles on the two tested worlds: the H5R2 provenance
gate repairs anchoring AND sustains revision through revert, including
the revert-after-revert discriminator where the dead lowest-node-id
candidate verifies first.

Scope (prereg section 10, unchanged): this verdict reports only that the
DEP based revision chain holds through full revert cycles on the two
tested worlds. No broad generality claim. No L3 claim (the four C0
clauses are not asserted here). The re-teach separator family remains an
explicit open gap in H5R2's scope. No tie-breaking rule is crowned.
