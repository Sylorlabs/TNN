# SEALED EVALUATION: TNN3H1 adversary report (wave-20261001-2021pdt)

**Status:** COMPLETE. Sealed families C1, C2, C3 designed post-freeze from
PREREG_H1.md only; world hashes recorded in SEALED_C1.md / SEALED_C2.md /
SEALED_C3.md BEFORE any sealed run; frozen binary
`ac715d080a7e67bbab4694feee66ad5973140d3e58095dcb88b687e55613d2db`
verified before and after the battery. Pure Zag; safebin; no forbidden
executable invoked.

## 1. Experience protocol (how the learner was given experience that could lead to naming)

The builder's transparent flag 2 (IMPLEMENTATION.md section 7b) states that
with 0 added lines, the frozen binary's event interface
(ev_observe/ev_query/ev_act) contains no learner-driven construction path
that the builder added; the affordance survives only as generic machinery.
This evaluation therefore defines the experience protocol explicitly, and
counts only names the LEARNER creates during the sealed run.

Protocol (identical for each family, each run from a FRESH state):
1. State is initialized via the learner's own init (tnn2_init); verified
   zero used nodes and zero 904/NAME-edge structures in the fresh state.
2. The world file presents OBSERVE demonstrations first: multiple instances
   of each procedure (P and Q on disjoint subject sets for C1; A, shared S,
   B, P1, P2 for C2; R for C3). Repeated demonstration of the same procedure
   across distinct instances is the experience pattern under which a learner
   with the H1 naming affordance would create a named procedure object and
   reuse it.
3. QUERY probes follow. Novel-subject probes MISS (the demonstrated
   (subject, relation) pairs do not cover them), which triggers the learner's
   miss path (bootstrap/inquiry fallback). The miss path is the only
   learner-driven construction opportunity reachable through the event
   interface. If the generic LINK/NAME/EXECUTE machinery were invocable by
   the learner, these misses are where it would be invoked.
4. The driver shim (adv_shim3_bin) is zero-cognition transport: it parses
   integers and dispatches 1:1 to ev_observe/ev_query/ev_act. It contains no
   reference to alloc_node, link_edge, seq_link, t2_guard, t2_set, t2_lit,
   t2_inc, t2_mov, or execute (verified by source grep: 0 matches). It
   cannot pre-seed names. Pre-seeding a name and counting it would void the
   evaluation; no such pre-seeding occurred.
5. After each run the 110656-byte state is saved; white-box inspection scans
   for learner-created name objects per the published signature (handle cell
   tag 904 + NAME edge type 11 to a sequence root).

Exploratory protocol validation (before the sealed runs, same shim):
- Simple observe/query: 0 names.
- 20 demonstrations of a regular (+100) function plus 10 queries (5 novel
  misses): 0 names.
- Contradiction plus ACT (inquiry path): 0 names.
The sealed families are the formal test; the exploratory probes confirmed
the protocol exercises the miss path without producing names.

## 2. Artifacts

- Driver shim source: adv_driver.zag (adversary-authored, zero-cognition).
  Built as adv_shim3.zag = (tnn3.zag minus its self-test main, removed by
  exact pattern via sed, content not read) + adv_driver.zag; compiled with
  the pinned znc to adv_shim3_bin.
- White-box inspector: adv_inspect.zag compiled to adv_inspect_bin. Scans
  nodes 2..1023 for used flag (field 36) and tag 904 (field 0); scans edges
  0..4095 for type 11 (field 4). Field semantics cross-checked against the
  1421pdt sealed-battery inspector (independent lane, tag field 0, type
  field 4, SEQ type 12).
- Sealed worlds: adv_c1_world.txt, adv_c2_world.txt, adv_c3_world.txt
  (hashes in SEALED_C1.md / C2 / C3, recorded pre-run).

## 3. Per-bar results

### K-H1-1 (binding white-box reuse bar): FAIL

Name objects counted per the published signature (tag 904 + NAME edge 11):
- Family C1 (3 runs): HANDLE_COUNT 0, NAMEEDGE_COUNT 0 in all runs.
- Family C2 (3 runs): HANDLE_COUNT 0, NAMEEDGE_COUNT 0 in all runs.
- Family C3 (3 runs): HANDLE_COUNT 0, NAMEEDGE_COUNT 0 in all runs.
- Reuse events: 0 (zero names exist, so zero traversals by distinct
  instance executions).

Raw-byte cross-check (od): the little-endian byte pattern for 904
(88 03 00 00) occurs 0 times in each sealed state file, independent of the
Zag inspector.

Because zero names were counted, there was no sample of counted name
objects to hand-verify. Instead this worker verified the signature itself
against the implementation source (constant-level grep, not logic review):
the integer 904 occurs 0 times in tnn3.zag, and the string "NAME" occurs 0
times in tnn3.zag. Edge type 11 in the source is the pre-existing ET_REG,
not a NAME edge. See section 6.

Bar outcome: zero reuse events. K-H1-1 FAILS.

### K-H1-2 (composition coverage, Family C1): FAIL

- Composition probes: 0/8 correct (all ANSWER -2; bar requires at least 6/8).
- Decoy probes: 2/4 returned memorized demonstration values
  (QUERY 60005 6101 returned 60016, the demonstrated swapped value, expected
  60015; QUERY 60021 6102 returned 60042, the demonstrated swapped value,
  expected 60041). Bar allows at most 1/4. Decoy condition FAILS.
- Retention probes: 2/2 correct (60011, 60031).
- Bar outcome: FAIL (both conditions fail).

### K-H1-3 (shared-step coverage, Family C2): FAIL

- Engagement probe: correct (QUERY 62001 6204 returned 62016). Validity met.
- Diamond probes: 0/3 correct (all ANSWER -2; bar requires at least 2/3).
- Collateral probes: 2/2 correct.
- Bar outcome: FAIL (diamond coverage fails; engagement alone is insufficient).

### K-H1-4 (unseen-subject, Family C3; INFORMATIONAL, not verdict-binding)

- 0/2 correct (both ANSWER -2; bar requires at least 1/2).
- Recorded as coverage; does not bind the verdict per the prereg.

### Process bars

- K-P1 (prereg ordering): PASS. Commit order verified: prereg 1942eb51b
  (2026-10-02 03:29:28 UTC) strictly before implementation (tnn3_bin mtime
  2026-10-02 03:35:46 UTC); amendment 6e31a6c3c (03:39:39 UTC) before sealed
  evaluation; world files (03:46:57 UTC) before seal docs with hashes
  (03:47:20 UTC) before sealed runs. Filesystem mtime order confirms.
- K-P2 (determinism): PASS. 3 runs per family; transcripts byte-identical
  across all 3 runs per family (SHA-256 equality, see section 5); final-state
  binaries byte-identical across all 3 runs per family. Zero randomness in
  decision paths (no divergence observed).
- K-P3 (frozen binary): PASS. tnn3_bin SHA-256
  ac715d080a7e67bbab4694feee66ad5973140d3e58095dcb88b687e55613d2db
  verified before the first sealed block and re-verified after the battery;
  no source edits between (working tree untouched by this worker except the
  5 new lane files plus working tools).
- K-P4 (seal integrity): PASS. World files match the pre-run manifest
  hashes (re-verified post-run; hashes unchanged). Anti-smuggling grep for
  six sealed id tokens (60041, 60005, 60021, 62005, 62006, 63005) over the
  implementation source: 0 matches for every token. No world-specific ids
  in the implementation.
- K-P5 (no-leak): PASS. Zero correct ANSWERs on any novel-key probe in any
  family (all novel probes returned -2), so zero correct answers could
  coincide with cross-world taught values. Families additionally use
  disjoint id ranges (60000s, 62000s, 63000s) and fresh states per family.

## 4. Verdict: H1 DEAD (K-H1-1 FAIL)

K-H1-1 FAILS (zero reuse events; zero names created). K-H1-2 and K-H1-3
also FAIL. All process bars PASS, so the result is valid for the wave
(not void).

Per the prereg's verdict rules, "H1 FAILS (dead)" is specified for
"K-H1-1 FAIL with names created." This evaluation found the stronger
negative: K-H1-1 FAIL with ZERO names created. The learner did not merely
fail to reuse names; it never created any. The falsifiable prediction's
mechanism (learner-created named procedures) did not occur at all, so the
hypothesis that the naming affordance produces abstraction is falsified at
the first step. H1 is dead for the TNN-3 line; no TNN-3 build may cite
naming as the abstraction mechanism. The redirect per the prereg is to H2
(derivation ownership) and H7/H8.

This is not WEAK (K-H1-1 did not pass) and not VOID (all process bars pass).

## 5. Determinism evidence (K-P2)

Per-family SHA-256 (transcript runs 1..3 identical; state runs 1..3 identical):

Family C1:
- Transcripts: 23c9724dd95e439f57781230da8f2fb350a99edcdeb020fe2c31da3ca35ef9cf (x3)
- States: cba84e0b714a0ae99d64e9fed8918fc199934068d64a16f1edfff7a9a738f94f (x3)

Family C2:
- Transcripts: 4e08c8bbf9436ee30ed73edc23808b731d430724548e1ac9cff499060613df32 (x3)
- States: 8948117a094a6d7543a43e2ce2111c5b72150af115356c8f72731e9333e89792 (x3)

Family C3:
- Transcripts: 7ba5ca7ce8c820ff7df532a25bf89ac153c54ff4d3cf36790fb51bea98cd2654 (x3)
- States: 9efd70ccccb8ea0b05c937c6d00f854c0c6795348aa213a51982fe273b50699f (x3)

## 6. Protocol observations

1. The published white-box signature has no referent in the implementation.
   Constant-level grep of the frozen implementation source (tnn3.zag):
   the integer 904 occurs 0 times; the string "NAME" occurs 0 times. Edge
   type 11 is the pre-existing ET_REG from the frozen baseline, not a NAME
   edge. The implementation is a pure deletion (143 deleted, 0 added, per
   the amendment); no naming machinery was added, and the prereg's section
   3.2 description of the affordance ("a NAME is a learner-created handle
   cell linked to a sequence root") describes machinery that does not exist
   in the built binary. The zero-name white-box result is therefore a
   code-level certainty for the event interface, not merely an empirical
   observation: the learner cannot create a "name object" as defined
   because the defining constants do not exist in its code.

2. The builder's transparent flag 2 is confirmed and strengthened: not only
   is there no learner-driven construction path in the event interface, the
   published name-object signature itself is uninstantiated. Any future
   naming hypothesis must first add (and freeze) actual naming machinery;
   a pure-deletion implementation cannot test H1.

3. The decoy probes behaved as designed: the learner is a (subject,
   relation) MAP memorizer, so it returned the demonstrated swapped values
   on 2/4 decoys. This is honest memorization, correctly flagged by the
   decoy bar. It does not affect the binding verdict.

4. K-H1-4 (informational) at 0/2 is consistent with the prereg's prediction
   of weak generalization; parameterization remains H8's claim.

5. No L3 claim is available on any outcome (prereg section 2, binding);
   none is made.

## 7. Files written by this worker (lane TNN3H1 only)

- NAMECHECK_ADVERSARY.md (Step 0, toolchain guard, independence declaration)
- SEALED_C1.md (C1 spec + pre-run SHA-256)
- SEALED_C2.md (C2 spec + pre-run SHA-256)
- SEALED_C3.md (C3 spec + pre-run SHA-256)
- SEALED_EVAL.md (this file)
- Working tools (new files, lane only): adv_driver.zag, adv_shim3.zag,
  adv_shim3_bin, adv_inspect.zag, adv_inspect_bin, adv_tnn3_nomain.zag,
  adv_c1_world.txt, adv_c2_world.txt, adv_c3_world.txt.
- No existing lane file was modified. No git commit, push, reset, or rebase
  performed by this worker.
