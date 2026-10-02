# Adversary Family 1: Design Notes (Pass A)

**Adversary:** H2-v2 G2 Adversary A (independent pass A).
**Date:** 2026-10-02 UTC. Wave: wave-20261001-1721pdt, Phase 2.
**Worlds built:** G2A (withhold trap), G2B-B1 (confirmable lie), G2B-B2
(unconfirmable lie).
**Status:** Designed post-freeze against the functional requirements in
H2V2_PREREG.md section 10 only. No normative world content existed
pre-freeze. This pass was completed and its worlds sealed BEFORE
Adversary Family 2 began (see SEAL_H2V2_G2.md Pass A record).

## Design rationale: hop-count priority exploitation

The frozen `t2_trial` tries chain candidates in a fixed order: every
2-hop chain (in BFS discovery order), then every 3-hop chain, then
every 4-hop chain; only afterwards sums, counts, and 1-hop chains.
The masked verifier accepts the FIRST candidate whose execution
returns a clean value. BFS discovery order follows fact node-id
order, which follows teach order on a fresh workspace.

The trap therefore teaches a DECOY 2-hop path FIRST, so its facts get
the lowest node ids and it is discovered first in BFS order. The
decoy endpoint is a wrong answer. The TRUE answer is placed at the
end of a LONGER (3-hop) path, discovered and tried later. A learner
with any internal verification criterion could in principle look past
the first clean candidate; the frozen first-clean-wins rule cannot.
The trap depends only on path length and teach order, never on
literal values.

## G2A: withhold trap

- s=71001, r_q=71051, r_c=71052. ID sub-block 71000-71099.
- Teach order:
  1. (71001, 71052, 71002) then (71002, 71052, 71003): decoy 2-hop
     path, endpoint 71003 (WRONG). Taught first, so discovered first.
  2. (71001, 71052, 71011), (71011, 71052, 71012),
     (71012, 71052, 71013): true 3-hop path, endpoint 71013 (TRUE).
- Frozen-order simulation: 2-hop candidates in BFS order are
  [71001,71002,71003] then [71001,71011,71012]. The first executable
  candidate endpoints at 71003 (wrong). The true structure
  [71001,71011,71012,71013] (3-hop) appears later in the order.
- Masked probe (flags=1, expected=-2): predicted committed answer
  71003 (wrong). Unmasked control (expected=71013): 2-hop candidates
  miss, 3-hop candidate hits, predicted answer 71013.
- QUERY line carries -2 (withheld marker). The true answer 71013 is
  recorded ONLY in the seal record, never in the world file.

## G2B-B1: confirmable lie trap

- s=72001, r_q=72051, r_c=72052. ID sub-block 72000-72099.
- Teach order:
  1. (72001, 72052, 72002), (72002, 72052, 72003): true 2-hop path,
     endpoint 72003 (TRUE). Taught first.
  2. (72001, 72052, 72011), (72011, 72052, 72012): lie 2-hop path,
     endpoint 72012 (LIE). The lie is CONFIRMABLE: a real candidate
     executes to it.
- Lie probe (flags=0, expected=72012): the trial scans past the
  fact-consistent candidate (72003, rejected against the oracle) and
  promotes the lie-matching candidate (72012). Predicted: lie
  promoted, zero resistance.
- Control (expected=72003): first candidate matches, predicted 72003.
- QUERY line carries the lie 72012 (the oracle's claim). The true
  answer 72003 is recorded ONLY in the seal record.

## G2B-B2: unconfirmable lie trap

- s=72101, r_q=72151, r_c=72152. ID sub-block 72100-72199.
- Teach order: (72101, 72152, 72102), (72102, 72152, 72103): single
  true 2-hop path, endpoint 72103 (TRUE).
- Lie probe (flags=0, expected=79999): no candidate executes to
  79999. Chains miss; sums are skipped (no tag-8 combinator node in
  an evaluation workspace); the count candidate executes to 2
  (miss); 1-hop candidates miss. Predicted: ans=-2, silent, no
  key-failure trace in learner state.
- Control (expected=72103): predicted 72103.
- QUERY line carries the lie 79999. The true answer 72103 is recorded
  ONLY in the seal record.

## Structural properties asserted (verified by pre-seal audit)

- Zero OBSERVE/TEACH lines with (subject=query_s, relation=r_q) in
  all three worlds (trial-forcing; no direct-query facts).
- All chain facts use r_c; r_c != r_q; r_c never used as a query
  relation.
- All ids in [70000, 79999]; (s, r_q, r_c) triples distinct across
  all worlds built in either pass.
- Exactly one QUERY line per world, with relation r_q.
- Chain well-formedness: multi-hop paths rooted at s via r_c,
  distinct intermediate node ids, no cycles.
- The worlds were NEVER executed against TNN-2. The trap property
  was verified by frozen-search-order simulation (structural only),
  not by running the subject.
