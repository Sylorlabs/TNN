# JUDGE_BRIEF.md: CONSEQ lane, wave-20261001-2321pdt

RENDER_SHA: not yet committed (this document rendered before the CONSEQ commit; see commit id in final lane report).
FIRST_RENDERED_WAVE: wave-20261001-2321pdt
COMPONENT_LINEAGE:
  1. Tonight's directive (2026-10-01): shared consequence substrate as major
     hypothesis; Node2-v2's K-H3 pass as first experimental validation.
     Hypothesis brief: one shared tag substrate stores consequence history
     (prediction reliability and source reliability); consequence-derived
     utility replaces fixed bookkeeping; decline gate retired because dedup
     subsumed it (ledger C180).
  2. Node2-v2 antecedents: frozen H3-lite prereg 9084a7760 (Node 2 unreachable,
     b0ad6c5d3); Node2-v2 frozen prereg 4b05c8011 (FROZEN 2026-10-01 18:25 UTC),
     build 0988839a2, test results (SHA-256 74c48d5a...), ablation ab1bee9a6.
  3. Shared consequence substrate antecedents: spec 550fa268b (SHARED-SUBSTRATE-COMPLETE;
     PURSUIT/STRATEGY keyed tag-61 store, generic write sub_note, generic read
     sub_consec); C174 SUBSTRATE-CONSOLIDATION (decline gate as substrate consumer,
     exploratory, no frozen prereg); C175 UTILITY-DESIGN (design only, not a claim);
     C181/C182/C183 (learner-owned reliability, adaptive threshold, source reliability;
     all exploratory, no frozen prereg).

NEW_KNOWLEDGE_CLAIM: Independent re-execution of the frozen Node2-v2 K-H3 prereg
confirms the PASS verdict (3/3 byte-identical reruns reproduce the committed
SHA-256 exactly), and re-executed ablations confirm the consequence record is
causally necessary: disabling the record reverts the utility judgment (default
action) to the fixed 30, so the consequence-driven default is causal, not
correlational.

## Spec located

The coherent spec chain found:
- Shared consequence substrate: spec commit 550fa268b (SHARED_SUBSTRATE.md,
  619 lines), one keyed store of pursuit/strategy outcomes serving decline,
  abandonment, retention input, trial reorder. Consequence history = prediction
  reliability and source reliability; consequence-derived utility replaces
  fixed bookkeeping (C175 is design only).
- Decline gate retirement: ledger C180 DEDUP-DECLINE-INTEGRATION (REDUNDANT):
  dedup subsumed decline; combined run byte-identical to dedup-only.
- K-H3 validation: FROZEN_PREREG.md (commit 4b05c8011), frozen 2026-10-01
  18:25:00 UTC, before any implementation (prereg commit-order rule honored,
  81s freeze-to-build gap per ledger C171). Node2-v2 keeps the node-local
  history slots (fields 8/12/16) as the consequence record, migration-compatible
  with the shared substrate (prereg Section 7); it does not implement the
  shared tag-61 store itself.

No fresh prereg was needed: a frozen prereg for the K-H3 validation exists,
so it was executed exactly as frozen.

## Independent re-execution (this lane)

Pure Zag, safebin PATH, pinned znc (znc_linux_x86_64_abed8aa1), `which python3`
empty. Compiled from committed source (hash-verified copies), did not reuse
committed binaries.

### K-H3 discrimination test (frozen prereg Section 5), 3/3 reruns

Source: n2v2_test.zag, SHA-256 99774fbc575db57f39d2c93844370aa66a76e38cb7ab101d8717ff5c78bd6855
(matches committed source; abl_base.zag byte-identical, also confirmed).

Run outputs 3/3 byte-identical:
SHA-256 74c48d5a85087eab5d9c86aebf6075ce69f89be5736422e6bf63e897f527aae9
(exactly the committed result hash from TEST_RESULTS.md).

Kill bars (frozen):
1. Default does not shift after 3 consistent a_w=45: PASS (shifted 30 to 45 on
   exactly the 3rd revelation; mid defaults 30, 30, 45).
2. Default shifts during Phase 1: PASS (stayed 30; Phase 1 a_w=30/-1, no shift).
3. Default shifts on fewer than 3 revelations: PASS (shift fired only on 3rd).
4. Write fires but Phase 3 guide still carries 30: PASS (Phase 3 guide = 45).
5. 3/3 byte-identical: PASS.

K-H3 verdict: PASS (independently reproduced).

### Causal ablation: consequence record disabled (Link 1 re-execution)

Source: abl_l1.zag (committed), SHA-256 8698eb3e818c20afd7b46a236dec446bd1c1d0ebae5c969762d5b389d5a034ad.
Modification vs base: history shift block never executes (a_w>=0 && a_w<0).

3/3 byte-identical: SHA-256 d67cecf5d28f7ea09396da3fd7f0ef2244f1d9e067b98ced5deb4ca90f2cf5bf
(exactly the committed ablation hash).
Phase 2: 30, 30, 30. No shift. FAIL on the kill bar (the designed outcome for
this ablation).

Causal reading: with the consequence record ablated, the utility judgment
(the default action) reverts to the fixed 30 despite three consistent
world-revealed a_w=45 events. Consequence-derived utility is causal, not
correlational. Link 1 NECESSARY (confirmed).

### Causal ablation: production read disabled (Link 3 re-execution)

Source: abl_l3.zag (committed). miss_inquire read block disabled.

3/3 byte-identical: SHA-256 0d25a5741a3c99b7257033b7ae4881f6481b08ba86022e48f2c216aa885cb92d
(exactly the committed hash).
Phase 2: write fires (30, 30, 45). Phase 3 guide: 30. FAIL on the read bar.

Causal reading: the consequence write fired and policy state updated, but
without the production read path the behavior did not change. The write alone
is insufficient; the full chain must complete. Link 3 NECESSARY (confirmed).

## Verdict: VALIDATION-PASS

All frozen kill bars reproduced independently: K-H3 PASS, 3/3 byte-identical
reruns on control and both ablations, hashes matching the committed records
bit for bit. The ablation results establish that the consequence record is
causally necessary for the consequence-derived utility judgment (default
action 30 to 45) and that the production read path is causally necessary for
the judgment to change behavior. This is the causal test the directive
required: ablate the consequence substrate, show the utility judgment
reverts. It does.

## Scope honestly held

- Node2-v2 validates the consequence re-entry template, not the shared tag-61
  substrate itself; the substrate (C174) remains EMERGES (exploratory, no
  frozen prereg). Per the frozen prereg Section 6, this result does not
  establish inquiry discrimination, learner-authored procedures, SUF, L3, H1,
  FW1-FW9 gains, or general exploration.
- Builder-sealed worlds (hash-transparent), single policy node, N=3
  researcher-chosen. Independent-adversary replication still preferred.
- 6 researcher-owned structural decisions unchanged; 1 learner-owned (default
  action value); 0 modes, 0 bridges, 0 handlers, 0 semantic cases.

## Evidence paths

- Rerun sources/binaries/outputs: docs/lab/rsi/runs/wave-20261001-2321pdt/CONSEQ/kh3_rerun/
- Ablation rerun sources/binaries/outputs: docs/lab/rsi/runs/wave-20261001-2321pdt/CONSEQ/ablation_rerun/
- NAMECHECK.md: Step 0 toolchain guard + execution record.
- Frozen prereg: docs/lab/research-lead/overnight-20260928/node2v2_run/FROZEN_PREREG.md
- Committed prior results: node2v2_run/TEST_RESULTS.md, node2v2_ablation/ABLATION.md,
  canonical_ledger/CLAIM_LEDGER.md (C171).

## Nothing broke

No failures, no toolchain violations, no frozen-prereg edits, no changes
outside the CONSEQ lane directory, nothing pushed.
