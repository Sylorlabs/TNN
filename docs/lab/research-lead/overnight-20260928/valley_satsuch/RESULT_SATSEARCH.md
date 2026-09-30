# RESULT: Valley Satisfiability Search

Date: 2026-09-30. Authority: PREREG_SATSEARCH.md (committed 7912fe11b,
strictly before implementation) plus ADDENDUM (sharded execution after
pilot OOM, committed before sharded runs).

## Build provenance

- Oracle: v2gen.zag extracted via
  `git show ea920137b:docs/lab/research-lead/overnight-20260928/valley_redesign2/v2gen.zag`,
  sha256 a93f9cd624294b7e1e2c475b392024e300f1a8be05173438979b8c6fc37604a9
  verified before every shard compile; the v2gen section of each
  concatenated build input diffs byte-identical against the blob.
- Helpers: v2_get32, v2_set32, v2_alloc, v2_emit, v2_e64, v2_nl,
  v2_mod_nonneg, v2_vm_run, v2_score, v2_s0, v2_slot copied verbatim
  from frozen v2inst.zag (sha256
  2b9b8bca05ffb88bd39fad1cff2dd1fed922833573e9d516c7486bf09b54e5a4),
  confirmed by diff per shard.
- New code: table_shard.zag (instance table only, SHARD_BASE
  remapping). No validation logic altered in any byte.
- Compiler: pinned src/tools/toolchain/znc_linux_x86_64_abed8aa1.
- Shards: 6 (s1: oids 1-12, s2: 13-24, s3: 25-33, s4: 34-45,
  s5: 46-57, s6: 58-71). Each shard: CAL-0 as id 0 (harness sanity)
  plus a contiguous run of original candidates. Each shard run 3x;
  all 18 logs byte-identical within shards (sha256 below).

## Run hashes (run 1 of each shard; runs 2,3 identical)

s1: 6de58d5ac3250d59896b19d951dbb9e2c8df30f3be92a462105939beac80f51e
s2: d82c2fccf9a61efdac81820e528abbf2cd4382722f63a45d4ccd129ac681d172
s3: 66d6414fa16443e484ce35427c0e826e5321cebb1ae10e4852c09ec7825ea8c1
s4: 83d5eaecc58e65b359174f169c05f9a351ed1ee9d007897739562f96d36deeb8
s5: e7c126c1649bf60e2929a12cdda01969a017a9eca49ae35415fdbfcbe84cac29
s6: 5588a942a6089f62bf36ffc711277f35c3b14b8d19cb7ea33f8220d80ea2edb6

(Full per-run hashes in SHARDS.log; all cmp-clean 3/3.)

## Per-candidate verdicts

CAL-0 (id 0 in every shard): PASS (CAL0-OK, harness sanity).

FOUND candidates (V1 and V2 and V3 all PASS): NONE. 0/71.

Failure breakdown (71 candidates):
- V1-FAIL s0>=n (constant target, no hits): 15.
  (F1 m=5 k=2,3; F1 m=7 k=3,5,6; all prologues.)
- V1-FAIL ties=2 (prologue B [PUSH 0,DROP] prefix ties s0): 4.
  (F1 pro B k=1,4 for m=5; F2 all three point-pairs.)
- V2-FAIL: 0. (All V1 survivors halt greedy as predicted.)
- V3-FAIL with concrete 2-edit solver: 52.

## V3 solver mechanisms (52 failures)

1. Negative-modulus MOD as lookup table (5): e.g. F1 m=5 k=1,
   append [PUSH -4, MOD] to the MOD prefix; (r mod -4) maps
   residues {0,1,4} to {0,1,0}, coinciding with (r==1).
2. GT/LT comparison exploiting residue extremum (14): e.g. F1 m=5
   k=4, append [PUSH 1, GT]; (r>1) on {0,1,4} equals (r==4).
3. DIV-by-zero indicator (14): e.g. F3 m=5 k=1, 2-edit replace to
   [PUSH 1, IN0, PUSH 1, ADD, PUSH 5, MOD, DIV]; 1/((x+1) mod 5)
   with DIV-by-zero gives 1 iff residue==1.
4. Repurposed prologue constant (33 replace solvers): e.g. F1 m=7
   k=2, 2-edit replaces [PUSH 0] with [PUSH 2] and drops [PUSH k],
   computing ((x^2 mod 7)==2) directly from the prologue slot.

## Verdict

VALLEY-SATSEARCH-UNSATISFIABLE. Zero of 71 candidates pass V1-V3.
Coverage: F1 (m in {5,7}, k in 1..m-1, pro A/B/C) 30 ids;
F2 (3 point-pairs, pro B) 3 ids; F3 (a=1, m in {5,7},
k in 1..m-1, pro A/B/C) 30 ids; F4 (m=5, k in 1..4, pro A/B)
8 ids. All L<=11. No claim about targets outside the table.

## Failure-mode analysis: the general obstruction

The 52 V3 failures instantiate Lemma 3 (MOD/DIV universality) as a
general obstruction for residue families: for any target of the
form ((poly(x) mod m)==k), the residue takes values in a small set
S; the 2-edit neighborhood of any canonical path contains a
MOD/DIV/comparison that encodes the indicator of {k} on S.
Negative MOD divisors give lookup tables; DIV-by-zero gives
1/r indicators; GT/LT exploit extremal residues; and any prologue
constant is 2 edits from becoming the comparison operand. The
4 V1 prologue-B failures show [PUSH 0,DROP] is not an inert prefix
(it ties s0). The 15 V1 constant-target failures are the k values
with empty residue classes, correctly filtered.

## Kill-bar results

K1: PASS. Prereg 7912fe11b strictly precedes implementation
(merge-base verified below). Addendum committed before sharded runs.
K2: PASS. VALLEY-SATSEARCH-UNSATISFIABLE with per-candidate frozen
gate outputs and 18/18 byte-identical logs (6 shards x 3 runs).
K3: PASS. Pure Zag, zero Python; dash-clean per shell-only snippet;
frozen V3 oracle byte-identical (sha256 + diff per shard).

## Recommended next step for the valley lane

The bounded search is exhausted: 0/71, with a general obstruction
identified (Lemma-3 universality kills all residue families at
L<=11; prologue tricks fail V1). Do NOT run a larger table of the
same families. The recommended next step is to either (a) abandon
the residue-target approach and search a qualitatively different
target class outside Lemma 3 (e.g. targets whose value set is not
small, or where the canonical path does not expose a bare residue),
requiring a new prereg; or (b) keep the valley battery VOID and
redirect the lane to the higher-priority frontier (generic
executable representation substrate). The valley lane should not
consume further waves on MOD-family variants.
